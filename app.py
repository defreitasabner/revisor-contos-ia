import os

from docx import Document
from flask import Flask, render_template, request
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


@app.route("/leitura-critica", methods=["GET", "POST"])
def leitura_critica():
    if request.method == "GET":
        return render_template("leitura-critica.html")

    context = request.form.get("context", "").strip()
    upload = request.files.get("file")

    def fail(error):
        return render_template("leitura-critica.html", error=error, context=context), 400

    if not upload or not upload.filename:
        return fail("Envie o conto como arquivo (.docx, .pdf, .txt ou .md).")
    try:
        text = extract_text(upload)
    except ValueError as e:
        return fail(str(e))
    except Exception:
        return fail("Não foi possível ler o arquivo.")

    prompt = PROMPT_TEMPLATE.format(
        contexto=context or "(nenhum contexto informado)", conto=text
    )
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )
    except Exception as e:
        return fail(f"Erro ao chamar o Gemini: {e}")

    return render_template(
        "resultado-leitura-critica.html", result=response.text, filename=upload.filename
    )


def extract_text(upload):
    ext = os.path.splitext(upload.filename)[1].lower()
    if ext == ".docx":
        return "\n".join(p.text for p in Document(upload).paragraphs)
    if ext == ".pdf":
        return "\n".join(p.extract_text() for p in PdfReader(upload).pages)
    if ext in (".txt", ".md"):
        return upload.read().decode("utf-8")
    raise ValueError("Formato não suportado. Envie .docx, .pdf, .txt ou .md.")


if __name__ == "__main__":
    app.run(debug=True)
