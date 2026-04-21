"""
NoraCore.faq
============
Respuestas predefinidas para preguntas frecuentes.
Ahorra tokens de Groq en consultas comunes.
"""

FAQ_RESPUESTAS = {
    "servicios": (
        "En Nexora Visual ofrecemos soluciones de IA para automatización administrativa "
        "y comercial. ¿Le gustaría agendar una demo con nuestro equipo?"
    ),
    "contacto": (
        "Puede comunicarse con nuestro equipo comercial al email contacto@nexoravisual.com "
        "o visitar nuestra web en nexoravisual.com."
    ),
    "precio": (
        "Nuestros planes se adaptan al tamaño de su negocio. "
        "¿Le gustaría que un asesor le comparta los planes vigentes?"
    ),
    "ayuda": (
        "Soy Nora, su asistente virtual. Puedo ayudarle a procesar facturas, "
        "recordarle tareas o responder consultas sobre Nexora Visual."
    ),
}


def buscar_faq(mensaje: str) -> str | None:
    """
    Busca una coincidencia de palabra clave en el mensaje.

    Args:
        mensaje: Texto del usuario (se normaliza a minúsculas).

    Returns:
        La respuesta predefinida si hay coincidencia, None en caso contrario.
    """
    mensaje_lower = mensaje.lower()
    for clave, respuesta in FAQ_RESPUESTAS.items():
        if clave in mensaje_lower:
            return respuesta
    return None
