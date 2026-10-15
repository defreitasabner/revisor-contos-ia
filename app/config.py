import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

class Config:
    DEBUG = os.environ.get('FLASK_DEBUG', 'False') in ('True', '1')
    MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    API_KEY = os.environ.get("GEMINI_API_KEY")