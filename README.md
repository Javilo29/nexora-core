---
title: Nora Nexora
emoji: 🤖
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# 🤖 Nexora Visual — Nora Assistant

> Asistente Virtual de IA para automatización administrativa y comercial, desplegada 24/7 en Telegram.

---

## ¿Qué es Nexora Visual?

**Nexora Visual** es una empresa de soluciones de Inteligencia Artificial orientada a la automatización de procesos administrativos y comerciales para PyMEs y corporaciones.

**Nora** es su asistente virtual oficial: un bot de Telegram con capacidades multimodales que puede:

- 💬 Mantener conversaciones de soporte comercial con IA (Groq / LLaMA 3.3 70B)
- 📄 Procesar imágenes de facturas y tickets fiscales extrayendo CUIT, importe y fecha (LLaMA 4 Scout Vision)
- 🧠 Recordar el contexto de cada cliente durante la sesión (memoria multi-usuario en RAM)
- ⚡ Responder preguntas frecuentes al instante sin consumir tokens de API

---

## 🗂️ Estructura del Proyecto

```
NEXORA_CORE/
├── nora_bot.py          # Bot principal — handlers Telegram + polling
├── requirements.txt     # Dependencias Python
├── .env.example         # Plantilla de variables de entorno
├── .gitignore
├── README.md
├── NoraCore/
│   ├── __init__.py
│   ├── brain.py         # Prompt del sistema + lógica de conversación (Groq)
│   ├── vision.py        # Procesamiento de imágenes 100% en RAM
│   ├── memory.py        # Gestión de historial multi-cliente
│   └── faq.py           # Respuestas predefinidas (ahorro de tokens)
└── deploy/
    └── fps_ms_guide.md  # Guía de despliegue en FPS.ms
```

---

## 🚀 Instalación Local

### Requisitos previos
- Python 3.11+
- Una cuenta en [Groq Console](https://console.groq.com) con API Key activa
- Un bot de Telegram creado con [@BotFather](https://t.me/BotFather)

### Pasos

```bash
# 1. Clonar o descomprimir el proyecto
cd D:\NEXORA_CORE

# 2. Crear entorno virtual (recomendado)
python -m venv venv
venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
copy .env.example .env
# Editar .env con tus credenciales reales

# 5. Lanzar el bot
python nora_bot.py
```

---

## ☁️ Despliegue en Producción (FPS.ms)

Ver guía completa: [`deploy/fps_ms_guide.md`](deploy/fps_ms_guide.md)

Resumen rápido:
1. Subir los archivos al panel de FPS.ms
2. Configurar las 3 variables de entorno: `BOT_TOKEN`, `GROQ_API_KEY`, `ADMIN_CHAT_ID`
3. Establecer comando de inicio: `python nora_bot.py`
4. El bot quedará activo 24/7 en modo polling

---

## 🔑 Variables de Entorno

| Variable | Descripción |
|---|---|
| `BOT_TOKEN` | Token del bot (obtenido en @BotFather) |
| `GROQ_API_KEY` | API Key de Groq ([console.groq.com](https://console.groq.com/keys)) |
| `ADMIN_CHAT_ID` | Tu ID personal de Telegram (para notificaciones admin) |

---

## 🧩 Arquitectura Técnica

| Capa | Tecnología |
|---|---|
| Bot Framework | python-telegram-bot 20.8 (async) |
| IA Conversacional | Groq API — LLaMA 3.3 70B Versatile |
| IA Visual | Groq API — LLaMA 4 Scout 17B Vision |
| Procesamiento imagen | Pillow (100% RAM, sin escritura a disco) |
| Memoria de sesión | Dict en RAM con ventana deslizante (6 mensajes) |
| Configuración | python-dotenv + variables de entorno del servidor |

---

## 📞 Contacto Comercial

**Nexora Visual**  
📧 contacto@nexoravisual.com  
🌐 nexoravisual.com  

Para consultas sobre licenciamiento, personalización o integración empresarial del sistema Nora, contáctenos por los canales oficiales.

---

*Nexora Visual © 2025 — Todos los derechos reservados.*
