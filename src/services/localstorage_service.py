import os
import uuid
import json
from pathlib import Path
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


class LocalStorage:
    """
    Industry-standard local storage service for storing uploaded files,
    intermediate results, OCR text, logs, etc.
    """

    def __init__(self, base_dir: str = "storage"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"LocalStorage initialized at: {self.base_dir}")

    # -------------------------------------------------
    # File Saving
    # -------------------------------------------------
    def save_file(self, file, subfolder: str = "uploads") -> Path:
        """Save an uploaded file to disk and return the saved path."""
        folder = self.base_dir / subfolder
        folder.mkdir(parents=True, exist_ok=True)

        ext = Path(file.name).suffix or ".bin"
        filename = f"{uuid.uuid4()}{ext}"
        file_path = folder / filename

        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        logger.debug(f"Saved file: {file_path}")

        return file_path

    # -------------------------------------------------
    # Save arbitrary text
    # -------------------------------------------------
    def save_text(self, text: str, subfolder: str = "texts") -> Path:
        folder = self.base_dir / subfolder
        folder.mkdir(parents=True, exist_ok=True)

        filename = f"{uuid.uuid4()}.txt"
        path = folder / filename

        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

        logger.debug(f"Saved text: {path}")
        return path

    # -------------------------------------------------
    # Save JSON
    # -------------------------------------------------
    def save_json(self, data: dict, subfolder: str = "json") -> Path:
        folder = self.base_dir / subfolder
        folder.mkdir(parents=True, exist_ok=True)

        filename = f"{uuid.uuid4()}.json"
        path = folder / filename

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        logger.debug(f"Saved JSON: {path}")
        return path

    # -------------------------------------------------
    # Load JSON by path
    # -------------------------------------------------
    def load_json(self, file_path: Path) -> dict:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"JSON file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # -------------------------------------------------
    # List files
    # -------------------------------------------------
    def list_files(self, subfolder: str) -> List[Path]:
        folder = self.base_dir / subfolder
        if not folder.exists():
            return []
        return list(folder.glob("*"))

    # -------------------------------------------------
    # Clear folder
    # -------------------------------------------------
    def clear(self, subfolder: Optional[str] = None):
        """Clear a subfolder or all folders."""
        target = self.base_dir if subfolder is None else self.base_dir / subfolder

        if not target.exists():
            return

        for f in target.glob("**/*"):
            if f.is_file():
                f.unlink()

        logger.info(f"Cleared storage: {target}")

    # -------------------------------------------------
    # Ensure directory exists
    # -------------------------------------------------
    def ensure_dir(self, subfolder: str):
        path = self.base_dir / subfolder
        path.mkdir(parents=True, exist_ok=True)
        return path
