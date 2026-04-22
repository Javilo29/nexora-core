"""
wsgi.py — NEXORA_CORE
=====================
Punto de entrada WSGI para PythonAnywhere (modo Webhook).

BLINDAJE TOTAL: Auto-detecta la ruta del proyecto sin depender de
rutas hardcodeadas. Funciona aunque el nombre de la carpeta cambie.
"""

import sys
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wsgi")

# ---------------------------------------------------------------------------
# AUTO-DETECCIÓN DE RUTA DEL PROYECTO (Blindaje anti-traducción)
# ---------------------------------------------------------------------------
# Primero intentamos resolver la ruta relativa al propio archivo wsgi.py,
# ya que este archivo siempre está en la raíz del proyecto.
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# Verificar que estamos en la carpeta correcta buscando nora_bot.py
if os.path.exists(os.path.join(_THIS_DIR, 'nora_bot.py')):
    PROJECT_PATH = _THIS_DIR
    logger.info(f"Proyecto encontrado via __file__: {PROJECT_PATH}")
else:
    # Fallback: buscar en ubicaciones conocidas
    _CANDIDATES = [
        '/home/javilo2/nexora-core',
        '/home/javilo2/NEXORA_CORE',
        '/home/javilo2/nexora-nucleo',
        '/home/javilo2/Nexora-Core',
    ]
    PROJECT_PATH = None
    for _p in _CANDIDATES:
        if os.path.exists(os.path.join(_p, 'nora_bot.py')):
            PROJECT_PATH = _p
            logger.info(f"Proyecto encontrado via fallback: {PROJECT_PATH}")
            break

    if PROJECT_PATH is None:
        # Último recurso: escanear /home/javilo2/ buscando nora_bot.py
        _home = '/home/javilo2'
        if os.path.isdir(_home):
            for _entry in os.listdir(_home):
                _candidate = os.path.join(_home, _entry)
                if os.path.isdir(_candidate) and os.path.exists(
                    os.path.join(_candidate, 'nora_bot.py')
                ):
                    PROJECT_PATH = _candidate
                    logger.info(f"Proyecto encontrado via escaneo: {PROJECT_PATH}")
                    break

    if PROJECT_PATH is None:
        raise RuntimeError(
            "FATAL: No se encontró la carpeta del proyecto. "
            "Ejecute en Bash: ls -la /home/javilo2/"
        )

# Agregar al path de Python
if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

_nora_core = os.path.join(PROJECT_PATH, 'NoraCore')
if os.path.isdir(_nora_core) and _nora_core not in sys.path:
    sys.path.insert(0, _nora_core)

# Cargar .env (buscar dentro del proyecto primero, luego en home)
try:
    from dotenv import load_dotenv
    _env_candidates = [
        os.path.join(PROJECT_PATH, '.env'),
        '/home/javilo2/.env',
    ]
    for _env in _env_candidates:
        if os.path.exists(_env):
            load_dotenv(_env)
            logger.info(f".env cargado desde: {_env}")
            break
except ImportError:
    logger.warning("python-dotenv no instalado, usando variables de entorno del sistema")

# ---------------------------------------------------------------------------
# APLICACIÓN FLASK + WEBHOOK
# ---------------------------------------------------------------------------
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN no definida. Verificar .env o variables de entorno.")

# Importar handlers de nora_bot
from nora_bot import start, handle_text, handle_photo, groq_client

# Construir la aplicación de Telegram
ptb_app = Application.builder().token(BOT_TOKEN).build()
ptb_app.add_handler(CommandHandler("start", start))
ptb_app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
ptb_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

# Flask app para recibir los updates del webhook
flask_app = Flask(__name__)


@flask_app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook_token():
    """Endpoint que recibe los updates de Telegram vía Webhook (ruta con token)."""
    return _process_update()


@flask_app.route("/", methods=["POST"])
def webhook_root():
    """Endpoint que recibe los updates de Telegram vía Webhook (ruta raíz)."""
    return _process_update()


def _process_update():
    """Procesa un update de Telegram entrante."""
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, ptb_app.bot)
    asyncio.run(ptb_app.process_update(update))
    return "ok", 200


@flask_app.route("/", methods=["GET"])
def health():
    """Health check — PythonAnywhere lo usa para mantener la app activa."""
    return "Nora esta activa.", 200


# Variable requerida por el servidor WSGI de PythonAnywhere
application = flask_app
