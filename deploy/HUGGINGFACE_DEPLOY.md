# 🚀 Despliegue en Hugging Face Spaces — NEXORA_CORE

> **Tiempo:** 3 minutos · **Costo:** $0 · **Sin tarjeta de crédito**  
> **Modo:** Docker + Polling + Health Server en puerto 7860

---

## Paso 1 — Crear el Space

1. Ir a [huggingface.co/new-space](https://huggingface.co/new-space)
2. Configurar:

| Campo | Valor |
|-------|-------|
| **Space name** | `nora-nexora` |
| **License** | MIT (o la que prefieras) |
| **SDK** | **Docker** |
| **Visibility** | Public *(requerido en plan gratuito)* |

3. Click en **"Create Space"**

---

## Paso 2 — Configurar Secrets

1. En tu Space, ir a **Settings** (icono de engranaje arriba a la derecha)
2. Bajar hasta la sección **"Repository secrets"**
3. Agregar estas **2 variables** (click en "New secret" para cada una):

| Name | Value |
|------|-------|
| `BOT_TOKEN` | *Tu token de @BotFather* |
| `GROQ_API_KEY` | *Tu key de console.groq.com* |

> 💡 Opcionalmente podés agregar `ADMIN_CHAT_ID` con tu ID de Telegram.

---

## Paso 3 — Subir el código

### Opción A — Desde Git (recomendado)

```bash
# Clonar el Space vacío
git clone https://huggingface.co/spaces/TU_USUARIO/nora-nexora
cd nora-nexora

# Copiar los archivos del proyecto
cp -r /ruta/a/NEXORA_CORE/* .

# Push
git add .
git commit -m "Nora v13.0 - Deploy inicial"
git push
```

### Opción B — Desde la Web

1. En tu Space, click en **"Files"** → **"Upload files"**
2. Arrastrar **todos** los archivos del proyecto:
   - `nora_bot.py`
   - `requirements.txt`
   - `Dockerfile`
   - `README.md`
   - Carpeta `NoraCore/` (con brain.py, vision.py, memory.py, faq.py)

---

## Verificación

1. Ir a la pestaña **"App"** de tu Space
2. Esperar que el build termine (1-2 minutos)
3. Debe mostrar: **"Nora esta activa — Nora v13.0 NEXORA_CORE"**
4. Abrir Telegram y escribir `/start` a tu bot

### Si hay errores:
- Ir a pestaña **"Logs"** → revisar el build log y el container log
- Error común: `BOT_TOKEN not found` → verificar Secrets en Settings

---

## Cómo actualizar

Cada push a tu Space dispara un rebuild automático:

```bash
git add .
git commit -m "update: descripción"
git push
```

---

*Guía para NEXORA_CORE — Nora v13.0 🤖*
