import json
import os
import base64
import asyncio
import logging

from openai import OpenAI
from google import genai
from google.genai import types
from dotenv import dotenv_values
import sys

import streamlit as st

logger = logging.getLogger(__name__)


class LLMImageParser:
    """
    Automatically detects provider from model name.
    Example inputs:
        - "gpt-4o-mini"
        - "gpt-4.1"
        - "gemini-2.0-flash"
        - "gemini-1.5-flash"
    """

    # Mapping prefixes → provider
    PROVIDER_MAP = {
        "gpt": "openai",
        "o1": "openai",
        "o3": "openai",
        "gemini": "gemini",
    }

    ENV_KEYS = {
        "openai": "OPENAI_API_KEY",
        "gemini": "GEMINIAI_API_KEY",
    }

    MODEL_OPTIONS = [
        "gemini-2.0-flash",
        "gpt-3.5-turbo",
        "gpt-4o-mini",
        "gpt-4o",
        "groq-0"
    ]

    def __init__(self, model: str):
        self.model = model

        # detect provider
        self.provider = self._detect_provider(model)
        env_vars = dotenv_values()

        # load API key
        env_key = self.ENV_KEYS[self.provider]
        api_key = env_vars.get(env_key)
        if not api_key:
            raise ValueError(f"{env_key} not found in environment variables")

        # init correct client
        if self.provider == "openai":
            self.client = OpenAI(api_key=api_key)
        elif self.provider == "gemini":
            self.client = genai.Client(api_key=api_key)

    # --------------------------------------------------------
    def _detect_provider(self, model: str) -> str:
        prefix = model.split("-")[0].lower()
        for key in self.PROVIDER_MAP:
            if prefix.startswith(key):
                return self.PROVIDER_MAP[key]
        raise ValueError(f"Unknown model provider for: {model}")

    # --------------------------------------------------------
    def _safe_json_load(self, text: str):
        """Clean text from code fences and parse JSON."""
        try:
            text = text.strip()
            for fence in ["```json", "```"]:
                text = text.replace(fence, "")
            return json.loads(text)
        except Exception as e:
            logger.warning(f"Failed to parse JSON: {e}")
            return {}

    # --------------------------------------------------------
    def _read_image_bytes(self, image_file):
        """Read bytes and detect MIME type from path or Streamlit UploadedFile."""
        if hasattr(image_file, "read"):  # Streamlit UploadedFile
            data = image_file.read()
            image_file.seek(0)
            mime_type = getattr(image_file, "type", "image/jpeg")
        else:  # Local file path
            with open(image_file, "rb") as f:
                data = f.read()
            ext = str(image_file).lower()
            mime_type = "image/jpeg"
            if ext.endswith(".png"):
                mime_type = "image/png"
            elif ext.endswith(".webp"):
                mime_type = "image/webp"
        return data, mime_type

    # --------------------------------------------------------
    # Public method
    # --------------------------------------------------------
    def parse_image(self, image_path: str, schema_description: str):
        if self.provider == "openai":
            return self._parse_openai(image_path, schema_description)
        return self._parse_gemini(image_path, schema_description)

    # --------------------------------------------------------
    async def parse_image_async(self, image_path: str, schema_description: str):
        """Async wrapper for non-blocking Streamlit calls."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.parse_image, image_path, schema_description)

    # --------------------------------------------------------
    def _parse_openai(self, image_path, prompt: str):
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{b64}",
                        },
                    ],
                }
            ],
        )
        return self._safe_json_load(response.choices[0].message["content"])

    # --------------------------------------------------------
    @st.cache_resource
    def _parse_gemini(_self, image_file, prompt: str):
        """Parse an image using Google Gemini Vision and return structured JSON."""
        try:
            # Read image bytes and MIME type
            image_data, mime_type = _self._read_image_bytes(image_file)

            # Prepare prompt


            response = _self.client.models.generate_content(
                model=_self.model,
                contents=[
                    prompt,
                    types.Part.from_bytes(data=image_data, mime_type=mime_type)
                ],
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )

            return _self._safe_json_load(response.text)

        except Exception as e:
            logger.error(f"Gemini parse failed: {e}")
            raise RuntimeError(f"[Gemini ERROR] {e}")
