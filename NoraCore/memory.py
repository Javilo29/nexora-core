"""
NoraCore.memory
===============
Gestión de historial de conversación multi-cliente en RAM.
Cada usuario tiene su propia ventana de historial de hasta 6 mensajes recientes.
"""

import logging

logger = logging.getLogger(__name__)

# Estado global: { chat_id (int) -> list[dict] }
_memoria_usuarios: dict[int, list[dict]] = {}

MAX_HISTORIAL = 6  # Cantidad máxima de mensajes a retener por usuario


def get_historial(chat_id: int) -> list[dict]:
    """
    Devuelve el historial de conversación del usuario.
    Si no existe, lo inicializa vacío.

    Args:
        chat_id: ID único del chat de Telegram.

    Returns:
        Lista de mensajes en formato {'role': str, 'content': str}.
    """
    if chat_id not in _memoria_usuarios:
        _memoria_usuarios[chat_id] = []
    return _memoria_usuarios[chat_id]


def agregar_mensaje(chat_id: int, role: str, content: str) -> None:
    """
    Agrega un mensaje al historial del usuario y aplica la ventana deslizante.

    Args:
        chat_id: ID único del chat de Telegram.
        role: 'user' o 'assistant'.
        content: Contenido del mensaje.
    """
    historial = get_historial(chat_id)
    historial.append({"role": role, "content": content})

    # Ventana deslizante: conservar solo los últimos MAX_HISTORIAL mensajes
    if len(historial) > MAX_HISTORIAL + 2:
        _memoria_usuarios[chat_id] = historial[-MAX_HISTORIAL:]
        logger.debug(f"Historial truncado para chat_id={chat_id}")


def limpiar_historial(chat_id: int) -> None:
    """
    Elimina el historial de un usuario (útil en tests o comando /reset).

    Args:
        chat_id: ID único del chat de Telegram.
    """
    _memoria_usuarios.pop(chat_id, None)
    logger.info(f"Historial eliminado para chat_id={chat_id}")
