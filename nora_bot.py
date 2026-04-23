"""
NEXORA_CORE — nora_bot.py
=========================
Bot principal de Nora v13.0 — Polling 24/7
Plataforma objetivo: Hugging Face Spaces / Render / cualquier servidor con Python 3.11+

Responsabilidades:
- Inicializar cliente Groq con credenciales de entorno.
- Registrar handlers de Telegram.
- Lanzar servidor de health check (puerto 7860 para HF Spaces).
- Lanzar polling infinito.
"""

import logging
import os
import sys

import requests
from io import BytesIO
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

# Cargar .env para desarrollo local (ignorado si no está instalado)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- Módulos de NoraCore ---
from NoraCore.brain import conversar_con_nora, es_cortesia
from NoraCore.vision import procesar_imagen_con_groq

# ---------------------------------------------------------------------------
# Configuración de logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("nora_bot")

# ---------------------------------------------------------------------------
# Variables de entorno (obligatorias en producción)
# ---------------------------------------------------------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not BOT_TOKEN:
    logger.critical("❌ BOT_TOKEN no definida. Configurar en variables de entorno.")
    sys.exit(1)

if not GROQ_API_KEY:
    logger.critical("❌ GROQ_API_KEY no definida. Configurar en variables de entorno.")
    sys.exit(1)

groq_client = Groq(api_key=GROQ_API_KEY)
logger.info("✅ Cliente Groq inicializado correctamente.")

# ---------------------------------------------------------------------------
# Handlers de Telegram
# ---------------------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /start — Presentación de Nora."""
    await update.message.reply_text(
        "👋 Bienvenido. Soy *Nora*, asistente virtual de Nexora Visual.\n"
        "Puedo ayudarle con facturas, recordatorios y consultas administrativas.\n"
        "¿En qué puedo asistirle hoy?",
        parse_mode="Markdown",
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja mensajes de texto del usuario."""
    chat_id = update.effective_chat.id
    texto = update.message.text

    # Cortesías: respuesta directa sin llamar a la IA
    if es_cortesia(texto):
        await update.message.reply_text("Es un placer asistirle. Estamos a un mensaje de distancia. 🤝")
        return

    respuesta = conversar_con_nora(texto, chat_id, groq_client)
    await update.message.reply_text(respuesta)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja imágenes: descarga en RAM y procesa con Groq Vision."""
    await update.message.reply_text("📸 Procesando documento fiscal... un momento.")

    try:
        file = await update.message.photo[-1].get_file()
        response = requests.get(file.file_path, timeout=15)
        response.raise_for_status()

        img_bytesio = BytesIO(response.content)
        datos = procesar_imagen_con_groq(img_bytesio, groq_client)

        if datos.get("error"):
            await update.message.reply_text(
                "❌ No se pudo leer el documento. "
                "Por favor, asegúrese de que la imagen sea clara y bien iluminada."
            )
        else:
            cuit = datos.get("cuit") or "No detectado"
            importe = datos.get("importe") or "No detectado"
            fecha = datos.get("fecha") or "No detectada"
            respuesta = (
                f"📋 *Documento Procesado:*\n"
                f"• CUIT: `{cuit}`\n"
                f"• Importe: `${importe}`\n"
                f"• Fecha: `{fecha}`"
            )
            await update.message.reply_text(respuesta, parse_mode="Markdown")

    except requests.RequestException as e:
        logger.error(f"Error descargando imagen: {e}")
        await update.message.reply_text("❌ No se pudo descargar la imagen. Por favor, inténtelo de nuevo.")
    except Exception as e:
        logger.error(f"Error inesperado procesando imagen: {e}")
        await update.message.reply_text("❌ Error interno al procesar la imagen.")


# ---------------------------------------------------------------------------
# Servidor de Health Check (para Hugging Face Spaces / Render)
# ---------------------------------------------------------------------------
from flask import Flask
import threading

health_app = Flask(__name__)


@health_app.route("/", methods=["GET"])
def health():
    """Health check — HF Spaces necesita un endpoint activo en puerto 7860."""
    return "Nora esta activa — Nora v13.0 NEXORA_CORE", 200


def run_health_server():
    """Lanza el servidor Flask en un hilo separado."""
    port = int(os.getenv("PORT", 7860))
    logger.info(f"🌐 Health server iniciado en puerto {port}")
    health_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)


def check_network():
    """Realiza un diagnóstico simple de conexión a Internet."""
    logger.info("🔍 Iniciando diagnóstico de red...")
    targets = [
        ("Google", "https://www.google.com"),
        ("Telegram API", "https://api.telegram.org")
    ]
    for name, url in targets:
        try:
            response = requests.get(url, timeout=10)
            logger.info(f"✅ Conexión exitosa con {name} (Status: {response.status_code})")
        except Exception as e:
            logger.error(f"❌ Fallo de conexión con {name}: {e}")

# ---------------------------------------------------------------------------
# Main — Polling 24/7
# ---------------------------------------------------------------------------

def main() -> None:
    """Punto de entrada principal. Lanza health server + bot en modo polling."""
    logger.info("🚀 Nora v13.0 | NEXORA_CORE | Iniciando...")

    # Diagnóstico de red inicial
    check_network()

    # Lanzar health server en hilo de fondo
    health_thread = threading.Thread(target=run_health_server, daemon=True)
    health_thread.start()

    # Lanzar bot de Telegram con Timeouts aumentados
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .read_timeout(60)
        .connect_timeout(60)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("✅ Nora está VIVA y escuchando mensajes.")
    
    # run_polling maneja los reintentos internamente
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()

