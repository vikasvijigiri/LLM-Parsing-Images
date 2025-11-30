from paddleocr import PaddleOCR
from PIL import Image
import io
import numpy as np

class OCRProcessor:
    def __init__(self, use_doc_orientation_classify=False,
                       use_doc_unwarping=False,
                       use_textline_orientation=False):
        self.ocr = PaddleOCR(
            use_doc_orientation_classify=use_doc_orientation_classify,
            use_doc_unwarping=use_doc_unwarping,
            use_textline_orientation=use_textline_orientation
        )

    def run(self, input_bytes):
        """
        Run OCR on image bytes.

        Args:
            input_bytes (bytes): Image in bytes format.
        """
        try:
            # Convert bytes → PIL → NumPy array
            img = Image.open(io.BytesIO(input_bytes)).convert("RGB")
            img_array = np.array(img)

            # PaddleOCR can process NumPy arrays
            result = self.ocr.predict(img_array)

            # # Process results
            # for line in result:
            #     print(line)
            ocr_text = "\n".join(result[0]["rec_texts"])
            return ocr_text

        except Exception as e:
            print(f"[OCR ERROR]: {e}")
            return None