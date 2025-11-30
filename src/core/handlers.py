# core/handlers.py

import logging
from src.core.pipeline import PipelineError

logger = logging.getLogger(__name__)


class RequestHandler:
    """
    Unified handler layer between UI/API and pipeline.
    Converts raw files/inputs → pipeline calls → UI-safe responses.
    """

    def __init__(self):
        pass


    # -----------------------------
    # New: Custom error handler
    # -----------------------------
    def handle(self, func, *args, **kwargs):
        """
        Wrap any function call with consistent error handling.
        Returns: (result, error) tuple
        """
        try:
            result = func(*args, **kwargs)
            return result, None
        except PipelineError as pe:
            logger.warning(f"Pipeline error: {pe}")
            return None, str(pe)
        except Exception as e:
            logger.exception("Unexpected failure in custom handler")
            return None, "Unexpected error occurred."