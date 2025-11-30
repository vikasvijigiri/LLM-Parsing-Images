# core/pipeline.py

import time
import logging
import tempfile
import os
import json
import streamlit as st



logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PipelineError(Exception):
    """Raised when the document pipeline fails."""
    pass


class Pipeline:
    """
    End-to-end document processing pipeline:
    1. Validate input files
    2. Generate schema from ground-truth JSON
    3. Run LLM parsing
    4. Evaluate predictions
    5. Save results
    6. Update metrics
    """

    def __init__(self, llm_service, evaluator, storage, metrics, ocr):
        self.llm = llm_service
        self.evaluator = evaluator
        self.storage = storage
        self.metrics = metrics
        self.ocr = ocr


    # -----------------------------
    # Validate a single uploaded file
    # -----------------------------
    def validate_input(self, file):
        if file is None:
            raise PipelineError("No file uploaded.")

        filename = file["name"].lower()
        if not (filename.endswith(".jpg") or filename.endswith(".jpeg")):
            raise PipelineError(f"{file["name"]} is not a JPG/JPEG file.")

        return True

    # -----------------------------
    # Generate schema from ground-truth JSON
    # -----------------------------
    @staticmethod
    def extract_schema_from_gt(ground_truth):
        """
        Recursively convert ground-truth JSON to JSON schema (values → empty 'string')
        """
        def _extract(obj):
            if isinstance(obj, dict):
                return {k: _extract(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [_extract(obj[0])] if obj else []
            else:
                return "string"

        return _extract(ground_truth)


    #@st.cache_resource
    def process_document(_self, file, ground_truth, ocr_use):
        """
        Process a single JPG document with its corresponding ground-truth JSON.

        Args:
            file: uploaded JPG file object
            ground_truth: corresponding ground-truth JSON (dict)

        Returns:
            dict: structured result for UI/metrics
        """
        schema_description = json.dumps(_self.extract_schema_from_gt(ground_truth))
        start_time = time.time()

        try:
            # Validate file
            _self.validate_input(file)

            # # Save temporarily
            # temp_dir = tempfile.gettempdir()
            # file_path = os.path.join(temp_dir, file["name"])
            # with open(file_path, "wb") as f:
            #     f.write(file.getbuffer())

            # Save temporarily
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, file["name"])

            with open(file_path, "wb") as f:
                f.write(file["bytes"])                

            ocr = ""
            if ocr_use:
                ocr = _self.ocr.run(file["bytes"])


            prompt = (
                f"You are an exert Image extractor.\n"
                f"Analyze the image and extract data according to this schema.\n"
                f"From the options shown below also classify the document_type and fill it in the JSON field appropriately.\n"
                f"The options are: INVOICE, RECEIPT, GAS BILL, ELECTRICITY BILL, WATER BILL, BANK STATEMENT, SALARY SLIP, PAYSLIP, ITR FORM 16, CHECK, other (use your judgement).\n"
                f"I have also tried providing a OCR extract for cross checking or for more help, OCR Extracted Text (ignore if empty): {ocr}."
                f"Return ONLY valid JSON.\n\nSchema Description:\n{schema_description}\n"
            )

            # LLM parsing
            logger.info(f"Running LLM parser for {file["name"]}...")
            prediction = _self.llm.parse_image(file_path, prompt)


            # st.write(ground_truth)


            # Evaluation
            result = _self.evaluator.evaluate(ground_truth, prediction)

            # st.write(print("DEBUG: Type of metrics inside pipeline:", type(_self.metrics)))

            # Update metrics
            _self.metrics.update_metrics(prediction, result)
            elapsed = time.time() - start_time
            _self.metrics.record_processing(elapsed)
            
            # # Save results
            # _self.storage.save(
            #     file_name=file["name"],
            #     evaluation=result,
            # )


            # self.metrics.update(processing_time=elapsed)

            # Structured result
            return {
                "file_name": file["name"],
                "result": result,
                "processing_time": round(elapsed, 2),
            }

        except Exception as e:
            logger.exception(f"Pipeline failed for {file["name"]}")
            raise PipelineError(f"{file["name"]} → Pipeline error → {e}")