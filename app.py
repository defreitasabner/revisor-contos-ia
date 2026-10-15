import json
import os

from docx import Document
from flask import Flask, jsonify, render_template, request
from google import genai
from google.genai import types
from pypdf import PdfReader



def load_env(path=".env"):
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


load_env(os.path.join(os.path.dirname(__file__), ".env"))

MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")

with open(os.path.join(PROMPTS_DIR, "default_system_prompt.txt"), encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

with open(os.path.join(PROMPTS_DIR, "default_prompt_template.txt"), encoding="utf-8") as f:
    PROMPT_TEMPLATE = f.read()

app = Flask(__name__)
client = genai.Client()


@app.get("/")
def index():
    return render_template("index.html")


def extract_text(upload):
    ext = os.path.splitext(upload.filename)[1].lower()
    if ext == ".docx":
        return "\n".join(p.text for p in Document(upload).paragraphs)
    if ext == ".pdf":
        return "\n".join(p.extract_text() for p in PdfReader(upload).pages)
    if ext in (".txt", ".md"):
        return upload.read().decode("utf-8")
    raise ValueError("Formato não suportado. Envie .docx, .pdf, .txt ou .md.")


@app.post("/chat")
def chat():
    message = request.form.get("message", "").strip()
    history = json.loads(request.form.get("history", "[]"))

    upload = request.files.get("file")
    if upload and upload.filename:
        try:
            text = extract_text(upload)
        except ValueError as e:
            return jsonify(error=str(e)), 400
        except Exception:
            return jsonify(error="Não foi possível ler o arquivo."), 400
        context = message or "(nenhum contexto informado)"
        message = PROMPT_TEMPLATE.format(context=context, conto=text)
    elif not history:
        return jsonify(error="Envie o conto como arquivo (.docx, .pdf, .txt ou .md)."), 400
    elif not message:
        return jsonify(error="Escreva uma mensagem ou envie um arquivo."), 400

    contents = [
        types.Content(role=m["role"], parts=[types.Part(text=m["text"])])
        for m in history
    ]
    contents.append(types.Content(role="user", parts=[types.Part(text=message)]))

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )
    except Exception as e:
        return jsonify(error=f"Erro ao chamar o Gemini: {e}"), 502

    # Devolve a mensagem final (com o conteúdo do arquivo) para compor o histórico.
    return jsonify(reply=response.text, sent=message)


if __name__ == "__main__":
    app.run(debug=True)
