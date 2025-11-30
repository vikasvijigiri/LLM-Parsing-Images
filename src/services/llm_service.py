import json
import os
import base64

from openai import OpenAI
from google import genai
from google.genai import types
from dotenv import dotenv_values
#import streamlit as st
import sys              # ← ADD THIS


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
        env_vars = dotenv_values()

        # Access keys
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
        """
        Detects provider based on model prefix.
        """

        # model examples:
        # gpt-4o-mini → gpt → openai
        # gemini-2.0-flash → gemini → gemini
        prefix = model.split("-")[0].lower()

        for key in self.PROVIDER_MAP:
            if prefix.startswith(key):
                return self.PROVIDER_MAP[key]

        raise ValueError(f"Unknown model provider for: {model}")

    # --------------------------------------------------------
    # Safe JSON
    # --------------------------------------------------------
    def _safe_json_load(self, text: str):
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)

    # --------------------------------------------------------
    # Public method
    # --------------------------------------------------------
    def parse_image(self, image_path: str, schema_description: str):
        if self.provider == "openai":
            return self._parse_openai(image_path, schema_description)
        return self._parse_gemini(image_path, schema_description)

    # --------------------------------------------------------
    def _parse_openai(self, image_path, schema_description):
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
                            "text": (
                                "Return ONLY JSON following this structure:\n"
                                f"{schema_description}"
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{b64}",
                        },
                    ],
                }
            ],
        )

        return self._safe_json(response.choices[0].message["content"])

    # --------------------------------------------------------

    def _parse_gemini(self, image_file, schema_description: str):
        """
        Parse an image using Google Gemini Vision and return structured JSON.
        Supports local file path or Streamlit UploadedFile.
        """
        try:
            # -----------------------------
            # 1. Read image bytes and detect MIME type
            # -----------------------------
            mime_type = "image/jpeg"  # Default fallback

            if hasattr(image_file, "read"):  # Streamlit UploadedFile
                image_data = image_file.read()
                if hasattr(image_file, "type") and image_file.type:
                    mime_type = image_file.type
                # Reset pointer in case the file is reused
                image_file.seek(0)
            else:  # Local file path
                with open(image_file, "rb") as f:
                    image_data = f.read()
                ext = str(image_file).lower()
                if ext.endswith(".png"):
                    mime_type = "image/png"
                elif ext.endswith(".webp"):
                    mime_type = "image/webp"

            # -----------------------------
            # 2. Prepare prompt
            # -----------------------------
            prompt = (
                f"From the options shown below also classify the document_type and fill it in the JSON field appropriately.\n"
                f"The options are: INVOICE, RECEIPT, GAS BILL, ELECTRICITY BILL, WATER BILL, BANK STATEMENT, PAYSLIP, PURCHASE ORDER, CREDIT NOTE, DEBIT NOTE, OTHERS.\n"
                f"Analyze the image and extract data according to this schema.\n"
                f"Return ONLY valid JSON.\n\nSchema Description:\n{schema_description}"
            )

            # -----------------------------
            # 3. Call Gemini
            # -----------------------------
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    prompt,
                    types.Part.from_bytes(data=image_data, mime_type=mime_type)
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )

            # -----------------------------
            # 4. Parse JSON response
            # -----------------------------
            return self._safe_json_load(response.text)

        except Exception as e:
            raise RuntimeError(f"[Gemini ERROR] {e}")
