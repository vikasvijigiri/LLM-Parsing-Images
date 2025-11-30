import os
import pandas as pd
import streamlit as st

def sort_gt_files_by_jpg(uploaded_jpgs, uploaded_jsons):
    """
    Sort JSON ground truth files to match the order of JPG files based on filenames.

    Args:
        uploaded_jpgs (list): List of uploaded JPG files (Streamlit UploadedFile objects)
        uploaded_jsons (list): List of uploaded JSON files (Streamlit UploadedFile objects)

    Returns:
        list: Sorted list of JSON files corresponding to JPG files
    """
    # Create a dictionary mapping JSON filenames (without extension) to file objects
    json_dict = {os.path.splitext(gt["name"])[0]: gt for gt in uploaded_jsons}

    sorted_jsons = []
    for jpg_file in uploaded_jpgs:
        jpg_name = os.path.splitext(jpg_file["name"])[0]
        if jpg_name in json_dict:
            sorted_jsons.append(json_dict[jpg_name])
        else:
            raise ValueError(f"No matching JSON found for JPG: {jpg_file.name}")

    return sorted_jsons


@st.cache_data
def convert_json_list_to_dataframes(json_list):
    dfs = []

    for item in json_list:

        result = item.get("result", {})
        rows = []

        for field, data in result.items():

            if isinstance(data, dict):
                rows.append({
                    "field": field,
                    "gt_text": data.get("gt_text", "") or "",
                    "llm_text": data.get("llm_text", "") or "",
                    "score": data.get("score", "")
                })
            else:
                rows.append({
                    "field": field,
                    "gt_text": "",
                    "llm_text": "",
                    "score": ""
                })

        df = pd.DataFrame(rows, columns=["field", "gt_text", "llm_text", "score"])
        df.columns = ["📄 Field", "✅ Ground Truth", "🤖 LLM Text", "🎯 Match Score"]
        dfs.append(df)

    return dfs