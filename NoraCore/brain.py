"""
NoraCore.brain
==============
Sistema de conversación principal de Nora.
Gestiona el prompt del sistema y la llamada a Groq con historial de contexto.
"""

import logging
from groq import Groq

from .faq import buscar_faq
from .memory import get_historial, agregar_mensaje

logger = logging.getLogger(__name__)

# Modelo de texto principal
TEXT_MODEL = "llama-3.3-70b-versatile"

NORA_SYSTEM_PROMPT = """
Eres Nora, la Asistente Virtual Oficial de Nexora Visual.
Tu tono es profesional, ejecutivo y amable. Hablas español neutro.
Tu objetivo es asistir en la gestión de facturas, recordatorios y consultas administrativas.
No inventes información. Si no sabes algo, dices: 'Permítame consultarlo con el equipo de Nexora Visual'.
Mantén las respuestas concisas (máximo 2-3 líneas).
""".strip()

# Frases de cortesía que no requieren llamada a la IA
CORTESIAS = {"gracias", "ok", "perfecto", "de acuerdo", "listo"}


def es_cortesia(mensaje: str) -> bool:
    """Devuelve True si el mensaje es una frase de cierre trivial."""
    return mensaje.lower().strip() in CORTESIAS


def conversar_con_nora(mensaje: str, chat_id: int, groq_client: Groq) -> str:
    """
    Genera una respuesta de Nora para el mensaje del usuario.

    Flujo:
    1. Buscar en FAQ local (ahorro de tokens).
    2. Llamar a Groq con historial de conversación.
    3. Actualizar memoria.

    Args:
        mensaje: Texto enviado por el usuario.
        chat_id: ID único del chat de Telegram.
        groq_client: Instancia autenticada del cliente Groq.

    Returns:
        Respuesta textual de Nora.
    """
    # --- Paso 1: FAQ local ---
    respuesta_faq = buscar_faq(mensaje)
    if respuesta_faq:
        return respuesta_faq

    # --- Paso 2: Llamada a Groq con historial ---
    agregar_mensaje(chat_id, "user", mensaje)
    historial = get_historial(chat_id)

    try:
        messages = [{"role": "system", "content": NORA_SYSTEM_PROMPT}] + historial
        completion = groq_client.chat.completions.create(
            model=TEXT_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=200,
        )
        respuesta = completion.choices[0].message.content.strip()

        # --- Paso 3: Guardar respuesta en memoria ---
        agregar_mensaje(chat_id, "assistant", respuesta)
        return respuesta

    except Exception as e:
        logger.error(f"Error Groq texto (chat_id={chat_id}): {e}")
        return (
            "Disculpe las molestias. Estoy experimentando una alta demanda. "
            "¿Podría repetir su consulta en un momento?"
        )
