# src/pages/upload_page1.py

import streamlit as st
import json
import io

# from src.ui.streamlitUI import StreamlitUI
from src.core.handlers import RequestHandler
from src.ui.widgets import FileUploadWidget
from src.core.state import AppState
from src.core.pipeline import Pipeline
from src.services.llm_service import LLMImageParser
from src.services.evaluation_service import Evaluator as GroundTruthEvaluator
from src.services.localstorage_service import LocalStorage
from src.services.metrics_service import Metrics
from src.services.highlight_service import render_boxes_component
from src.utils.file_utils import *
from st_aggrid import AgGrid, GridOptionsBuilder


def run(ui):
    """
    Main page logic for Upload & Process workflow.
    Handles:
    - JPG & JSON uploads
    - Persistent image viewer like a book
    - Persistent model selection
    - Persistent 'Process All Files' button
    - LLM pipeline processing
    """
    #st.session_state.clear()
    ui.title("🖼️ JPG Image Processor")
    ui.subtitle("A Rag app based on LLMs for Image extractions along with dashboard.")
    ui.divider()


    # -----------------------------
    # Initialize AppState
    # -----------------------------
    AppState.init()
    handle = RequestHandler()

    # Ensure upload_counter exists
    upload_counter = AppState.get("upload_counter") or 0

    # -----------------------------
    # Columns for Uploads
    # -----------------------------
    col1, col2 = st.columns([1, 1])

    # -----------------------------
    # JPG Uploads
    # -----------------------------
    with col1:
        ui.subheader("Upload JPG Image Files*")
        uploader_key = f"uploader_JPG_{upload_counter}"

        uploader = FileUploadWidget(
            label="JPG Upload Section*",
            key=uploader_key,
            type=["jpg", "jpeg", "png"]
        )
        uploader.render()

        # Persist uploaded files safely
        existing_jpgs = AppState.get("uploaded_files") or []
        if uploader.files:
            for f in uploader.files:
                if f is not None and f not in existing_jpgs:
                    AppState.add_uploaded_file(f)

        uploaded_files = AppState.get("uploaded_files") or []
        st.write(f"No. of JPGs uploaded: {len(uploaded_files)}")

        if ui.button("Clear All JPG Uploads", key="clear_jpg_uploads"):
            AppState.reset()
            AppState.set("upload_counter", upload_counter + 1)
            

    # -----------------------------
    # JSON Uploads
    # -----------------------------
    with col2:
        ui.subheader("Upload Ground Truth JSON Files*")
        uploader_json_key = f"uploader_JSON_{upload_counter}"

        uploader_json = FileUploadWidget(
            label="JSON Upload Section*",
            key=uploader_json_key,
            type=["json"]
        )
        uploader_json.render()

        existing_jsons = AppState.get("groundtruth_json") or []
        if uploader_json.files:
            for f in uploader_json.files:
                if f is not None and f not in existing_jsons:
                    existing_jsons.append(f)
        AppState.set("groundtruth_json", existing_jsons)

        uploaded_jsons = AppState.get("groundtruth_json") or []
        st.write(f"No. of JSONs uploaded: {len(uploaded_jsons)}")

        if ui.button("Clear All JSON Uploads", key="clear_json_uploads"):
            AppState.reset()
            AppState.set("upload_counter", upload_counter + 1)
            

    ui.divider()

    # -----------------------------
    # Load Model & Files
    # -----------------------------
    saved_model = AppState.get("selected_model", "gemini-2.0-flash")
    uploaded_jpg_files = AppState.get("uploaded_files") or []
    uploaded_gt_files = AppState.get("groundtruth_json") or []

    if uploaded_jpg_files and uploaded_gt_files:

        # Sort GT JSONs according to uploaded JPGs
        sorted_gt_files, _ = handle.handle(sort_gt_files_by_jpg, uploaded_jpg_files, uploaded_gt_files)
        AppState.set("groundtruth_jsons", sorted_gt_files)

        # -----------------------------
        # MODEL SELECTION (Persistent)
        # -----------------------------
        ui.header("Model")
        _, col, _ = st.columns([1, 1, 1])
        with col:
            model_options = [
                "— Select Model —",
                "gpt-3.5-turbo",
                "gpt-4o-mini",
                "gpt-4o",
                "gemini-2.0-flash",
                "groq-0"
            ]
            current_index = model_options.index(saved_model) if saved_model in model_options else 0
            st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
            model_choice = st.selectbox("Select LLM Model", model_options, index=current_index)

            if model_choice != saved_model:
                AppState.set("selected_model", model_choice)

        # -----------------------------
        # LOAD GROUND TRUTH JSONS
        # -----------------------------
        ground_truth_map = {}
        if model_choice != "— Select Model —":
            for jpg_file, gt_file in zip(uploaded_jpg_files, sorted_gt_files):
                try:
                    gt_data = json.loads(gt_file["bytes"].decode("utf-8"))
                    ground_truth_map[jpg_file["name"]] = gt_data
                except Exception as e:
                    ui.error(f"Failed to load JSON {gt_file['name']}: {e}")
                    continue

        llm_service = LLMImageParser(saved_model)
        evaluator = GroundTruthEvaluator()
        storage = LocalStorage()
        # Load persistent metrics
        metrics = Metrics()
        pipeline = Pipeline(llm_service, evaluator, storage, metrics)

        _, col, _ = st.columns([1, 1, 1])
        with col:
            if AppState.get("process_all_clicked") is None:
                AppState.set("process_all_clicked", False)

            if ui.button("🚀 Process All Files", key="processor") and not AppState.get("process_all_clicked"):

                results = []
                for file in uploaded_jpg_files:
                    gt_data = ground_truth_map[file["name"]]
                    res = ui.run_with_stopwatch(pipeline.process_document, file=file, ground_truth=gt_data)
                    results.append(res)
                    #st.write(metrics.to_dict())    
                    AppState.set("metrics", metrics.to_dict())
                    AppState.update_metrics(metrics.to_dict())

                AppState.set("pipeline_results", results)
                AppState.set("process_all_clicked", True)

    # -----------------------------
    # Persistent Image Viewer
    # -----------------------------
    ui.header("Output")
    c1, c2 = st.columns([1, 1])
    with c1:
        uploaded_images = AppState.get("uploaded_images") or []

        current = AppState.get_current_image()
        if current:
            st.image(current["img"], caption=current["name"])
            col_prev, _, col_next = st.columns([1, 2, 1])
            with col_prev:
                if ui.button("⬅ Previous", key="prev_image"):
                    AppState.prev_image()
            with col_next:
                if ui.button("Next ➡", key="next_image"):
                    AppState.next_image()
        else:
            st.info("Upload JPG images to view them like a book.")

    with c2:
        results = AppState.get("pipeline_results") or []
        for res in results:
            render_boxes_component(res.get("result", {}))

    # -----------------------------
    # Results Table
    # -----------------------------
    results = AppState.get("pipeline_results") or []
    dfs = convert_json_list_to_dataframes(results)

    if dfs:
        idx = AppState.get("dict_page") or 0
        idx = min(idx, len(dfs) - 1)  # Clamp index
        AppState.set("dict_page", idx)

        ui.header("Results")
        gb = GridOptionsBuilder.from_dataframe(dfs[idx])
        gb.configure_grid_options(domLayout='normal', headerHeight=40)
        gb.configure_columns(dfs[idx].columns.tolist(), headerClass='custom-header')
        grid_options = gb.build()
        AgGrid(dfs[idx], gridOptions=grid_options, enable_enterprise_modules=False, fit_columns_on_grid_load=True)

        container = st.container()
        with container:
            col1_btn, col2_btn, col3_btn = st.columns([1, 1, 1])
            with col1_btn:
                if st.button("⬅ Previous", disabled=(idx == 0)):
                    AppState.set("dict_page", max(idx - 1, 0))
                    
            with col3_btn:
                if st.button("Next ➡", disabled=(idx == len(dfs) - 1)):
                    AppState.set("dict_page", min(idx + 1, len(dfs) - 1))
                    
            with col2_btn:
                csv_buffer = io.StringIO()
                dfs[idx].to_csv(csv_buffer, index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv_buffer.getvalue(),
                    file_name=f"results_page_{idx+1}.csv",
                    mime="text/csv"
                )
    else:
        st.info("No results to display yet.")
