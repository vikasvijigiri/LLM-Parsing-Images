

# JPG Image Processor
![Diagram](images/diagram.png)

A Streamlit-based application for automated document parsing and evaluation. Upload JPG images along with ground-truth JSON files, extract structured data using LLMs (optionally with OCR), track metrics, and generate results in CSV format.

---

## Features

- Upload JPG, JPEG, and PNG images.
- Upload corresponding ground-truth JSON files.
- Parse images using LLMs such as GPT-based or Gemini models.
- Optional OCR integration for text extraction.
- Persistent metrics tracking:
  - Total documents processed
  - Correct vs incorrect predictions
  - Correct vs incorrect classifications
  - LLM failures
  - Field-level accuracy
  - Processing times
- Book-like image viewer for easy navigation through uploaded images.
- Download processed results as CSV.

---

## Installation

1. Clone the repository  
`git clone https://github.com/your-username/jpg-image-processor.git`  
`cd jpg-image-processor`

2. Create a virtual environment  
`python -m venv venv`  
Activate the environment:  
On Windows: `venv\Scripts\activate`  
On macOS/Linux: `source venv/bin/activate`

3. Upgrade pip  
`pip install --upgrade pip`

4. Install dependencies  
`pip install -r requirements.txt`

---

## Running the Application

1. Start the Streamlit server  
`streamlit run app.py`

2. Open the URL provided in the terminal (usually `http://localhost:8501`) in your browser.

---

## Usage

1. **Upload JPG Images**  
   Click on the left column upload section and select JPG, JPEG, or PNG files.

2. **Upload Ground-Truth JSON Files**  
   Upload corresponding JSON files in the right column.

3. **Select Model & OCR Option**  
   Choose your LLM model from the dropdown. Optionally enable or disable OCR for text extraction.

4. **Process All Files**  
   Click `🚀 Process All Files` to run the processing pipeline. Metrics will update in real-time and persist across the session.

5. **View Results**  
   Use the book-like image viewer to navigate images. View processed results in the interactive AgGrid table. Download CSV results page-wise using the download button.

---

## Metrics

The app tracks and displays metrics for performance evaluation:

- Total documents processed
- Correct vs incorrect predictions
- Correct vs incorrect classification
- LLM failures
- Field-level accuracy percentages
- Processing times per document

Metrics persist across the session and are updated with each new processing run.

---

## Project Structure

src/  
 ├─ core/  
 │   ├─ pipeline.py           # Main processing pipeline  
 │   ├─ state.py              # Session state management  
 │   └─ handlers.py           # Request handlers and utilities  
 ├─ pages/  
 │   └─ upload_page1.py       # Main Streamlit page  
 ├─ services/  
 │   ├─ llm_service.py        # LLM parsing service  
 │   ├─ evaluation_service.py # Ground truth evaluation  
 │   ├─ localstorage_service.py  
 │   ├─ metrics_service.py    # Metrics tracking  
 │   └─ highlight_service.py  # Highlight visualization  
 └─ ui/  
     └─ widgets.py            # Custom UI widgets

---

## Dependencies

- Python 3.12+  
- Streamlit  
- Pillow  
- st-aggrid  
- Other dependencies listed in `requirements.txt`

---

## Contribution

- Fork the repository  
- Create a feature branch  
- Submit a pull request

---

## License

MIT License
