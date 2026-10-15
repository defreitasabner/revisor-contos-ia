import os
from pathlib import Path

from flask import current_app
from google import genai
from google.genai import types


def leitura_critica(context, text):

    client = genai.Client(
        api_key = current_app.config["API_KEY"],
    )

    PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

    with open(PROMPTS_DIR / "default_system_prompt.txt", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()

    with open(PROMPTS_DIR / "default_prompt_template.txt", encoding="utf-8") as f:
        PROMPT_TEMPLATE = f.read()

    prompt = PROMPT_TEMPLATE.format(
        contexto = context or "(nenhum contexto informado)", conto = text
    )
    response = client.models.generate_content(
        model = current_app.config["MODEL"],
        contents = prompt,
        config = types.GenerateContentConfig(system_instruction = SYSTEM_PROMPT),
    )
    return response.text