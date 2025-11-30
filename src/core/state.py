# core/state.py

import streamlit as st
from PIL import Image
import io

class AppState:
    """
    Centralized session state management layer.

    Industry standard pattern:
    - No direct st.session_state access outside this class
    - Ensures keys exist before usage
    - Provides clean getters / setters
    """

    DEFAULTS = {
        "uploaded_jpg_files": [],        # raw uploaded files
        "uploaded_json_files": [],       # PIL images
        "current_image_index": 0,    # current image shown in book view
        "groundtruth_json": None,
        "llm_results": [],
        "metrics": {},
        "processing_times": [],
        "current_page": "Upload & Process",
    }

    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------
    @classmethod
    def init(cls):
        """Initialize all default session keys."""
        for key, value in cls.DEFAULTS.items():
            if key not in st.session_state:
                st.session_state[key] = value

    # ---------------------------------------------------------
    # Generic helpers
    # ---------------------------------------------------------
    @staticmethod
    def get(key, default=None):
        return st.session_state.get(key, default)

    @staticmethod
    def set(key, value):
        st.session_state[key] = value

    @staticmethod
    def append(key, value):
        if key not in st.session_state:
            st.session_state[key] = []
        st.session_state[key].append(value)

    @staticmethod
    def clear(key):
        if key in st.session_state:
            del st.session_state[key]


    @classmethod
    def reset(cls):
        """
        Delete all session state variables except metrics.
        """
        current_metrics = cls.get("metrics") or {}  # store metrics safely

        # Delete all keys except metrics
        keys_to_delete = [key for key in st.session_state.keys() if key != "metrics"]
        for key in keys_to_delete:
            del st.session_state[key]

        # Restore metrics just in case
        st.session_state["metrics"] = current_metrics


    # ---------------------------------------------------------
    # File & Image helpers
    # ---------------------------------------------------------
    @classmethod
    def add_uploaded_file(cls, file):
        cls.append("uploaded_files", file)
        # convert to PIL and store
        img = Image.open(io.BytesIO(file["bytes"]))
        cls.append("uploaded_images", {"img": img, "name": file["name"]})

    @classmethod
    def get_current_image(cls):
        images = cls.get("uploaded_images", [])
        idx = cls.get("current_image_index", 0)
        if images:
            return images[idx]
        return None

    @classmethod
    def next_image(cls):
        images = cls.get("uploaded_images", [])
        if images:
            st.session_state["current_image_index"] = (st.session_state["current_image_index"] + 1) % len(images)

    @classmethod
    def prev_image(cls):
        images = cls.get("uploaded_images", [])
        if images:
            st.session_state["current_image_index"] = (st.session_state["current_image_index"] - 1) % len(images)

    # ---------------------------------------------------------
    # Processing specific helpers
    # ---------------------------------------------------------
    @classmethod
    def add_processing_time(cls, t):
        cls.append("processing_times", t)

    @classmethod
    def set_metrics(cls, data: dict):
        st.session_state["metrics"] = data

    @classmethod
    def get_metrics_obj(cls):
        if st.session_state.get("metrics") is None:
            from src.services.metrics_service import Metrics
            st.session_state["metrics"] = Metrics()
        st.write(type(st.session_state["metrics"]))            
        return st.session_state["metrics"]



    @classmethod
    def set_metrics_obj(cls, metrics_obj):
        from src.services.metrics_service import Metrics
        if not isinstance(metrics_obj, Metrics):
            raise TypeError("set_metrics expects a Metrics object, not a dict.")
        st.session_state["metrics"] = metrics_obj


    @classmethod
    def update_metrics(cls, new_data: dict):
        """
        Update existing metrics dict in session_state with new_data.
        - Adds numerical values field-wise.
        - Appends lists if the existing value is a list.
        """
        if "metrics" not in st.session_state or st.session_state["metrics"] is None:
            st.session_state["metrics"] = {}

        metrics = st.session_state["metrics"]

        for key, value in new_data.items():
            if key in metrics:
                if isinstance(value, (int, float)) and isinstance(metrics[key], (int, float)):
                    metrics[key] += value  # add numbers
                elif isinstance(value, list) and isinstance(metrics[key], list):
                    metrics[key].extend(value)  # append lists
                else:
                    # fallback: overwrite if types mismatch
                    metrics[key] = value
            else:
                metrics[key] = value  # new key

        st.session_state["metrics"] = metrics

    # ---------------------------------------------------------
    # Page Navigation
    # ---------------------------------------------------------
    @classmethod
    def set_page(cls, name: str):
        st.session_state["current_page"] = name

    @classmethod
    def get_page(cls):
        return st.session_state.get("current_page", "Upload & Process")
