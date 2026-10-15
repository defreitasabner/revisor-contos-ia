from flask import Blueprint, render_template, request
from google.genai import types
from app import services
from app import utils

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route("/leitura-critica", methods=["GET", "POST"])
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
        text = utils.extract_text(upload)
    except ValueError as e:
        return fail(str(e))
    except Exception:
        return fail("Não foi possível ler o arquivo.")

    try:
        resultado = services.leitura_critica(context, text)
    except Exception as e:
        return fail(f"Erro ao chamar o Gemini: {e}")

    return render_template(
        "resultado-leitura-critica.html", result = resultado, filename = upload.filename
    )
