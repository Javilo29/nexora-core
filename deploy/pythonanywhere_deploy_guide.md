# 🐍 Guía de Despliegue en PythonAnywhere — NEXORA_CORE

> **Para:** Javi  
> **Proyecto:** NEXORA_CORE / Nora Bot  
> **Plataforma:** [PythonAnywhere](https://www.pythonanywhere.com)  
> **Modo:** Webhook (Web App WSGI) — 24/7 gratuito  
> **Última actualización:** Abril 2026

---

## ¿Por qué PythonAnywhere?

PythonAnywhere ofrece hosting gratuito de Web Apps Python con:
- **Sin "sleep"** — tu bot siempre está activo
- **HTTPS incluido** — requerido por Telegram para webhooks
- **Bash console** — para instalar dependencias y gestionar archivos
- **Python 3.10+** disponible

---

## Paso 1 — Crear cuenta en PythonAnywhere

1. Ve a [https://www.pythonanywhere.com/registration/register/beginner/](https://www.pythonanywhere.com/registration/register/beginner/)
2. Elige un **username** (este será parte de tu URL, ej: `javilo29`)
3. Completa el registro — **no necesitas tarjeta de crédito**
4. Confirma tu correo electrónico

---

## Paso 2 — Abrir una consola Bash

1. Desde el Dashboard, haz clic en **"Consoles"** en el menú superior
2. Haz clic en **"Bash"** para abrir una nueva consola
3. Verás el prompt: `$ username@pythonanywhere:~$`

---

## Paso 3 — Clonar el repositorio de GitHub

En la consola Bash, ejecuta:

```bash
cd ~
git clone https://github.com/TU_USUARIO/NEXORA_CORE.git
```

> Reemplaza `TU_USUARIO` con tu usuario de GitHub.  
> El proyecto quedará en `/home/javilo29/NEXORA_CORE/`

---

## Paso 4 — Instalar dependencias

En la misma consola Bash:

```bash
cd ~/NEXORA_CORE
pip install --user -r requirements.txt
```

También necesitarás Flask para el webhook:

```bash
pip install --user flask
```

Verifica que todo instaló correctamente:

```bash
python -c "import telegram; import groq; import flask; print('✅ Todo OK')"
```

---

## Paso 5 — Subir el archivo `.env`

El archivo `.env` contiene tus tokens secretos y **NO está en GitHub** (está en `.gitignore`). Debes subirlo manualmente.

### Opción A — Desde el Editor de Archivos (recomendado)

1. En el Dashboard, ve a **"Files"**
2. Navega a tu directorio home: `/home/javilo29/`
3. Haz clic en **"Upload a file"**
4. Sube tu archivo `.env` con el siguiente contenido:

```
BOT_TOKEN=tu_token_real_aqui
GROQ_API_KEY=tu_groq_key_real_aqui
ADMIN_CHAT_ID=tu_chat_id_aqui
```

### Opción B — Desde Bash

```bash
cat > ~/.env << 'EOF'
BOT_TOKEN=tu_token_real_aqui
GROQ_API_KEY=tu_groq_key_real_aqui
ADMIN_CHAT_ID=tu_chat_id_aqui
EOF
```

### ¿Cómo obtener los valores?

| Variable | Dónde obtenerla |
|---|---|
| `BOT_TOKEN` | Telegram → @BotFather → `/mybots` → tu bot → API Token |
| `GROQ_API_KEY` | [https://console.groq.com/keys](https://console.groq.com/keys) |
| `ADMIN_CHAT_ID` | Telegram → @userinfobot → te muestra tu ID |

---

## Paso 6 — Configurar la Web App (WSGI)

1. En el Dashboard, ve a **"Web"**
2. Haz clic en **"Add a new web app"**
3. Selecciona **"Manual configuration"** (NO "Flask" — usamos nuestro propio wsgi.py)
4. Selecciona **Python 3.10**
5. En la configuración de la Web App:

### Source code
```
/home/javilo29/NEXORA_CORE
```

### WSGI configuration file
Haz clic en el enlace del archivo WSGI (algo como `/var/www/javilo29_pythonanywhere_com_wsgi.py`) y **reemplaza TODO su contenido** con:

```python
import sys
sys.path.insert(0, '/home/javilo29/NEXORA_CORE')

from wsgi import application
```

Guarda el archivo.

### Virtualenv (opcional pero recomendado)
Si quieres un entorno aislado:
```bash
mkvirtualenv nexora --python=python3.10
workon nexora
pip install -r ~/NEXORA_CORE/requirements.txt flask
```
Y en la sección "Virtualenv" de la Web App, pon:
```
/home/javilo29/.virtualenvs/nexora
```

---

## Paso 7 — Setear el Webhook de Telegram

El webhook le dice a Telegram que envíe los mensajes a tu URL de PythonAnywhere.

Tu URL será: `https://javilo29.pythonanywhere.com/<BOT_TOKEN>`

En la consola Bash, ejecuta (reemplaza los valores):

```bash
BOT_TOKEN="tu_token_aqui"
URL="https://javilo29.pythonanywhere.com/${BOT_TOKEN}"

curl -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook" \
     -d "url=${URL}"
```

Deberías ver:
```json
{"ok":true,"result":true,"description":"Webhook was set"}
```

Verifica que el webhook está activo:
```bash
curl "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo"
```

---

## Paso 8 — Reload y probar

1. En el Dashboard → **"Web"**
2. Haz clic en el botón verde **"Reload"** (o el botón con el nombre de tu app)
3. Espera que aparezca el indicador verde ✅
4. Abre Telegram y escribe `/start` a tu bot

### Si hay errores:

- En el Dashboard → **"Web"** → sección **"Log files"**
- Revisa **"Error log"** — te mostrará el traceback exacto
- Revisa **"Server log"** — para ver las requests entrantes

---

## Actualizar el bot en el futuro

Cada vez que hagas cambios y push a GitHub:

```bash
# En la consola Bash de PythonAnywhere:
cd ~/NEXORA_CORE
git pull origin master
```

Luego hacer **Reload** desde el Dashboard → Web.

---

## Troubleshooting rápido

| Síntoma | Posible causa | Solución |
|---|---|---|
| Bot no responde | Webhook no seteado | Ejecuta el comando `setWebhook` del Paso 7 |
| Error 500 en logs | Error en el código | Revisa Error log → busca el traceback |
| `ModuleNotFoundError` | Dependencia faltante | `pip install --user <modulo>` en Bash |
| `BOT_TOKEN not found` | `.env` no subido o ruta incorrecta | Verifica que `.env` está en `/home/javilo29/` |
| Webhook rejected | URL incorrecta o sin HTTPS | PythonAnywhere ya provee HTTPS, verifica la URL |
| `401 Unauthorized` | Token incorrecto | Regenera token en @BotFather |

---

## Estructura de archivos requeridos en PythonAnywhere

```
/home/javilo29/
├── .env                          ← Subir manualmente (NO en GitHub)
└── NEXORA_CORE/
    ├── wsgi.py                   ← Entry point WSGI ✅
    ├── nora_bot.py               ← Handlers del bot ✅
    ├── requirements.txt          ← Dependencias ✅
    ├── .env.template             ← Referencia de variables ✅
    ├── NoraCore/
    │   ├── brain.py
    │   ├── vision.py
    │   ├── memory.py
    │   └── faq.py
    └── deploy/
        └── pythonanywhere_deploy_guide.md   ← Esta guía ✅
```

---

*Guía generada para el proyecto NEXORA_CORE — Nora de Nexora 🤖*
