"""
NoraCore.vision
===============
Procesamiento de imágenes fiscales 100% en RAM (sin escritura a disco).
Extrae datos estructurados (CUIT, importe, fecha) de facturas y tickets.
"""

import base64
import json
import logging
from io import BytesIO

from PIL import Image
from groq import Groq

logger = logging.getLogger(__name__)

# Modelo de visión actual — actualizar aquí si Groq lo depreca
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
MAX_IMAGE_SIZE = 1024  # px en el lado más largo


def encode_image_from_bytesio(img_bytesio: BytesIO) -> str:
    """
    Codifica un BytesIO de imagen a base64.

    Args:
        img_bytesio: Stream de imagen en memoria.

    Returns:
        String base64 de la imagen.
    """
    img_bytesio.seek(0)
    return base64.b64encode(img_bytesio.read()).decode("utf-8")


def optimizar_imagen_en_ram(img_bytesio: BytesIO, max_size: int = MAX_IMAGE_SIZE) -> BytesIO:
    """
    Redimensiona y comprime la imagen en RAM sin escribir a disco.

    Args:
        img_bytesio: Stream de imagen original.
        max_size: Tamaño máximo en píxeles del lado más largo.

    Returns:
        Nuevo BytesIO con la imagen optimizada en formato JPEG.
    """
    img_bytesio.seek(0)
    img = Image.open(img_bytesio)

    if max(img.size) > max_size:
        ratio = max_size / max(img.size)
        new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

    output = BytesIO()
    img.save(output, format="JPEG", quality=85)
    output.seek(0)
    return output


def procesar_imagen_con_groq(img_bytesio: BytesIO, groq_client: Groq) -> dict:
    """
    Envía una imagen a Groq Vision y extrae datos fiscales estructurados.

    Args:
        img_bytesio: Stream de imagen en memoria.
        groq_client: Instancia autenticada del cliente Groq.

    Returns:
        Dict con claves: 'cuit', 'importe', 'fecha' (o 'error' si falla).
    """
    try:
        img_optimizada = optimizar_imagen_en_ram(img_bytesio)
        img_base64 = encode_image_from_bytesio(img_optimizada)

        prompt = (
            "Analizá esta imagen de factura o ticket.\n"
            "Devolvé UNICAMENTE un JSON válido con este formato:\n"
            '{"cuit": "xx-xxxxxxxx-x", "importe": numero, "fecha": "dd/mm/aaaa"}\n'
            "Si no podés leer algún dato, usá null."
        )

        completion = groq_client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
                        },
                    ],
                }
            ],
            temperature=0.1,
            max_tokens=200,
        )

        raw = completion.choices[0].message.content.strip()
        return json.loads(raw)

    except json.JSONDecodeError as e:
        logger.error(f"Vision JSON parse error: {e}")
        return {"cuit": None, "importe": None, "fecha": None, "error": "JSON inválido"}
    except Exception as e:
        logger.error(f"Vision error: {e}")
        return {"cuit": None, "importe": None, "fecha": None, "error": str(e)}
