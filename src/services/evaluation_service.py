import json
from typing import Any, Dict
import re
from difflib import SequenceMatcher
import streamlit as st



class Evaluator:
    """
    Evaluates nested JSON structures (any depth).
    Returns flat scores:

    {
        "agency_details.agency_name": {
            "llm_text": "...",
            "score": 0.82
        }
    }
    """

    # ------------------------------------------------------
    def evaluate(self, ground_truth: Dict[str, Any], llm_output: Dict[str, Any]):
        results = {}


        
        try:
            self._compare_recursive(
                gt=ground_truth,
                pred=llm_output,
                prefix="",
                results=results
            )
            return results

        except Exception as e:
            return {"evaluate error": str(e)}

    # ------------------------------------------------------
    def _compare_recursive(self, gt, pred, prefix: str, results: dict):
        """
        Recursively compare ground-truth and prediction structures.
        Handles dict, list, tuple, set, and leaf values.
        """
        # ---- DICTIONARY ----
        if isinstance(gt, dict):
            for key, value in gt.items():
                new_prefix = f"{prefix}.{key}" if prefix else key
                pred_value = pred.get(key) if isinstance(pred, dict) else None
                self._compare_recursive(value, pred_value, new_prefix, results)

        # ---- LIST OR TUPLE ----
        elif isinstance(gt, (list, tuple)):
            for idx, item in enumerate(gt):
                new_prefix = f"{prefix}[{idx}]"
                pred_item = pred[idx] if isinstance(pred, (list, tuple)) and idx < len(pred) else None
                self._compare_recursive(item, pred_item, new_prefix, results)

        # ---- SET ----
        elif isinstance(gt, set):
            # Convert set to sorted list for deterministic comparison
            gt_list = sorted(gt)
            pred_list = sorted(pred) if isinstance(pred, set) else (list(pred) if pred else [])
            self._compare_recursive(gt_list, pred_list, prefix, results)

        # ---- LEAF NODE ----
        else:
            score = self._compute_score(gt, pred)
            results[prefix] = {
                "llm_text": pred,
                "gt_text": gt,
                "score": round(score, 4)
            }

    # ------------------------------------------------------


    def normalize_text(self, text: str) -> str:
        """Lowercase, remove punctuation, standardize spaces."""
        if not text:
            return ""
        text = text.lower()
        # Replace common separators with space
        text = re.sub(r"[\/,;|]", " ", text)
        # Remove any remaining non-alphanumeric chars except spaces
        text = re.sub(r"[^a-z0-9\s]", "", text)
        # Collapse multiple spaces
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _compute_score(self, gt: str, pred: str) -> float:
        """
        Robust similarity score between ground truth and predicted strings.
        Uses tokenization and SequenceMatcher to handle missing/extra words and separators.
        Returns score between 0.0 and 1.0.
        """
        if not pred:
            return 0.0

        gt_norm = self.normalize_text(gt)
        pred_norm = self.normalize_text(pred)

        # If exactly equal after normalization
        if gt_norm == pred_norm:
            return 1.0

        # Split into tokens
        gt_tokens = gt_norm.split()
        pred_tokens = pred_norm.split()

        # If empty GT
        if not gt_tokens:
            return 1.0 if not pred_tokens else 0.0

        # Use SequenceMatcher on tokens
        matcher = SequenceMatcher(None, gt_tokens, pred_tokens)
        return matcher.ratio()
