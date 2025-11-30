import streamlit as st
from typing import Dict, List
from src.utils.json_checker import is_json

class Metrics:
    """
    Industry-standard metrics tracker for monitoring:
    - document counts
    - prediction correctness
    - OCR/LLM failures
    - processing time
    """

    def __init__(self):
        self.reset()




    # -------------------------------------------------
    # Reset all metrics
    # -------------------------------------------------
    def reset(self):
        self.total_docs = 0
        self.correct_classification = 0
        self.incorrect_classification = 0
        self.correct_predictions = 0
        self.incorrect_predictions = 0
        self.llm_failures = 0
        self.accuracy_: List[float] = []
        self.processing_times: List[float] = []

    # -------------------------------------------------
    # Add one processing record
    # -------------------------------------------------
    def record_processing(self, elapsed_time: float):
        self.processing_times.append(elapsed_time)

    # -------------------------------------------------
    # Increment document count
    # -------------------------------------------------
    def add_document(self):
        self.total_docs += 1

    # -------------------------------------------------
    # Prediction tracking
    # -------------------------------------------------
    def mark_correct(self):
        self.correct_predictions += 1

    def mark_incorrect(self):
        self.incorrect_predictions += 1

    # -------------------------------------------------
    # Classification tracking
    # -------------------------------------------------
    def mark_classification_correct(self):
        self.correct_classification += 1

    def mark_classification_incorrect(self):
        self.incorrect_classification += 1

    # -------------------------------------------------
    # LLM failure tracking
    # -------------------------------------------------
    def mark_llm_failure(self):
        self.llm_failures += 1

    def record_accuracy(self, accuracy: float):
        self.accuracy_.append(accuracy)

    # -------------------------------------------------
    # Export as a dictionary (for Streamlit dashboard)
    # -------------------------------------------------
    def to_dict(self) -> Dict:
        return {
            "total_docs": self.total_docs,
            "correct_classification": self.correct_classification,
            "incorrect_classification": self.incorrect_classification,
            "correct_predictions": self.correct_predictions,
            "incorrect_predictions": self.incorrect_predictions,
            "llm_failures": self.llm_failures,
            "accuracy": self.accuracy_,
            "processing_times": self.processing_times

        }
    

    # def time_data(self, res) -> Dict:
    #     return {
    #         "file": res["name"],
    #         "avg_processing_time": res["processing_times"],
    #         "model": res["choosen_model"],
    #         "correct_prediction": res["prediction_percentage"],
    #         "correct_classification_percentage": res["classification_percentage"],
    #         "total_llm_failures": res["total_llm_failures"],   # ← missing value filled
    #     }


    
    @classmethod
    def get_metrics(cls):
        if st.session_state.get("metrics") is None:
            from src.services.metrics_service import Metrics
            st.session_state["metrics"] = Metrics()
        return st.session_state["metrics"]

    @classmethod
    def set_metrics(cls, metrics_obj):
        st.session_state["metrics"] = metrics_obj

    # @classmethod
    # def set_metrics_object(cls, metrics_obj):
    #     st.session_state["metrics"] = metrics_obj


    def mark_by_score(self, res):
        """
        Evaluate each field individually by its 'score'.
        score >= 0.9 → mark as correct
        score < 0.9  → mark as incorrect

        Marks overall correctness based on % of correct fields.
        """

        # if not isinstance(res, dict):
        #     self.mark_incorrect()
        #     return

        total = 0
        correct = 0

        for field, obj in res.items():
            if not isinstance(obj, dict):
                continue

            score = obj.get("score")
            if isinstance(score, (int, float)):
                total += 1
                if score >= 0.75:
                    correct += 1
                    self.mark_correct()
                else:
                    self.mark_incorrect()

        # # No scores found → incorrect
        # if total == 0:
        #     self.mark_correct()
        #     return

        accuracy = correct / total

        self.record_accuracy(accuracy)


        #st.write(f"Field accuracy: {accuracy:.2%}")




    def update_metrics(self, pred, res):
        #st.write(res)
        if res["document_type"]["score"] > 0.8:
            #st.write("Vikasss")
            self.mark_classification_correct()
        else:
            self.mark_classification_incorrect()


        #                         # ----- Persistent Metrics update -----
        self.add_document()
        if not is_json(pred):
            self.mark_llm_failure

        #st.write(res)
        self.mark_by_score(res)    
        #self.record_processing(res["processing_time"])



