import sys
from paddleocr import PaddleOCR

class OCRProcessor:
    def __init__(self, use_doc_orientation_classify=False,
                       use_doc_unwarping=False,
                       use_textline_orientation=False):
        """
        Initialize the PaddleOCR instance with configurable options.
        """
        self.ocr = PaddleOCR(
            use_doc_orientation_classify=use_doc_orientation_classify,
            use_doc_unwarping=use_doc_unwarping,
            use_textline_orientation=use_textline_orientation
        )

    def run(self, input_image):
        """
        Run OCR on the given input image path and save results.

        Args:
            input_image (str): Path to the input image.
        """
        try:
            # Run OCR inference
            results = self.ocr.predict(input=input_image)

            # Process each result
            for res in results:
                res.print()                   # Print detected text info
                #res.save_to_img("output")     # Save annotated image
                #res.save_to_json("../../output")    # Save JSON results

        except Exception as e:
            print(f"[OCR ERROR]: {e}")


# ----------------------
# Example usage
# ----------------------
if __name__ == "__main__":
    image_path = "../../data/Check/1.jpg"  # Replace with your image path
    ocr_processor = OCRProcessor()
    ocr_processor.run(image_path)
