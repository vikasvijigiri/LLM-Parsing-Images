

# JPG Image Processor
<img width="1920" height="729" alt="logo" src="https://github.com/user-attachments/assets/0fefe573-62d6-4228-9bd5-9bcec86b3e0d" />

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

5. Fill the .env file with your API keys (mandatory) 
`e.g. GEMINIAI_API_KEY = "A..."`
---

## Running the Application

1. Start the Streamlit server  
`streamlit run app.py`

2. Open the URL provided in the terminal (usually `http://localhost:8501`) in your browser.

---

## Usage

1. **Upload JPG Images**  
   Click on the left column upload section and select JPG, JPEG, or PNG files.
   <img width="500" height="474" alt="Screenshot (466)" src="https://github.com/user-attachments/assets/ed0fa7a2-6641-40e4-b1b4-6ab9961c96f0" />


2. **Upload Ground-Truth JSON Files**  
   Upload corresponding JSON files in the right column.
   <img width="500" height="479" alt="Screenshot (466)" src="https://github.com/user-attachments/assets/7c7353b2-380f-4f46-9ae8-f61f3af0aae2" />

4. **Select Model & OCR Option**  
   Choose your LLM model from the dropdown. Optionally enable or disable OCR for text extraction.
   <img width="500" height="367" alt="Screenshot (467)" src="https://github.com/user-attachments/assets/457b5024-2902-4111-9603-17208f77b630" />

5. **Parse**  
   Click `🚀 Parse` Button to run the processing pipeline. Metrics will update in real-time and persist across the session.

6. **View Results**  
   Use the book-like image viewer to navigate images. View processed results in the interactive AgGrid table. Download CSV results page-wise using the download button.
   <img width="500" height="749" alt="Screenshot (468)" src="https://github.com/user-attachments/assets/09312624-106a-46c8-96d6-d27879bea0b6" />
   <img width="1920" height="817" alt="Screenshot (463)" src="https://github.com/user-attachments/assets/fbc4d933-2b52-4845-9471-6883d584c1d4" />

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
