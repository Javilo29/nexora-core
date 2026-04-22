"""
wsgi.py — NEXORA_CORE
=====================
Punto de entrada WSGI para PythonAnywhere (modo Webhook).

IMPORTANTE: Este archivo asume que el bot está configurado para recibir
updates via Webhook (no polling). PythonAnywhere requiere una Web App
con WSGI para operar 24/7 de forma gratuita.

Rutas asumidas en PythonAnywhere:
  - Proyecto: /home/javilo2/nexora-core
  - .env:      /home/javilo2/nexora-core/.env
"""

import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el .env dentro del proyecto
dotenv_path = '/home/javilo2/nexora-core/.env'
load_dotenv(dotenv_path)

# Agregar el proyecto al path de Python
path = '/home/javilo2/nexora-core'
if path not in sys.path:
    sys.path.insert(0, path)

# --- Importar la app Flask que maneja el webhook ---
# nora_bot.py debe exportar una variable 'application' (Flask app)
# o se usa un adaptador simple a continuación.

from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wsgi")

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Importar handlers de nora_bot
from nora_bot import start, handle_text, handle_photo, groq_client

# Construir la aplicación de Telegram
ptb_app = Application.builder().token(BOT_TOKEN).build()
ptb_app.add_handler(CommandHandler("start", start))
ptb_app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
from telegram.ext import filters as tg_filters
ptb_app.add_handler(MessageHandler(tg_filters.TEXT & ~tg_filters.COMMAND, handle_text))

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
    return "✅ Nora está activa.", 200

# Variable requerida por el servidor WSGI de PythonAnywhere
application = flask_app
