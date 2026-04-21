# 🚀 Guía de Despliegue en Koyeb — NEXORA_CORE

> **Para:** Javi  
> **Proyecto:** NEXORA_CORE / Nora Bot  
> **Plataforma:** [Koyeb](https://www.koyeb.com)  
> **Última actualización:** Abril 2026

---

## ¿Por qué Koyeb?

Koyeb ofrece un **Free Tier permanente** con contenedores que corren 24/7, sin los "sleep" de Render. Perfecto para un bot de Telegram que necesita estar siempre activo.

---

## Paso 1 — Crear cuenta en Koyeb

1. Ve a [https://app.koyeb.com/signup](https://app.koyeb.com/signup)
2. Regístrate con tu **cuenta de GitHub** (recomendado, simplifica el paso siguiente).
3. Verifica tu correo electrónico si te lo pide.
4. No necesitas tarjeta de crédito para el plan gratuito.

---

## Paso 2 — Conectar tu repositorio de GitHub

1. Una vez dentro del dashboard de Koyeb, haz clic en **"Create App"**.
2. Selecciona **"GitHub"** como fuente de despliegue.
3. Autoriza a Koyeb a acceder a tus repositorios.
4. Busca y selecciona el repositorio **`NEXORA_CORE`** (o como lo tengas nombrado en GitHub).
5. Selecciona la rama **`master`** (o `main` si la renombraste).

---

## Paso 3 — Configurar el servicio

En la pantalla de configuración del servicio:

| Campo | Valor |
|---|---|
| **Service type** | Worker *(NO Web Service — el bot no necesita puerto HTTP)* |
| **Builder** | Buildpack (detección automática de Python) |
| **Run command** | `python nora_bot.py` |
| **Instance type** | Free (eco) |

> **Importante:** Koyeb detectará el `Procfile` y el `requirements.txt` automáticamente. No necesitas configurar el build command manualmente.

---

## Paso 4 — Agregar Variables de Entorno

En la sección **"Environment Variables"**, agrega las siguientes variables:

| Variable | Descripción | Ejemplo |
|---|---|---|
| `TELEGRAM_TOKEN` | Token de tu bot de Telegram (obtenido de @BotFather) | `7123456789:AAF...` |
| `GROQ_API_KEY` | API Key de Groq Cloud | `gsk_...` |

### ¿Cómo obtener estos valores?

**TELEGRAM_TOKEN:**
1. Abre Telegram y busca `@BotFather`
2. Escribe `/mybots` → selecciona tu bot → "API Token"

**GROQ_API_KEY:**
1. Ve a [https://console.groq.com/keys](https://console.groq.com/keys)
2. Crea una nueva API Key si no tienes una

> ⚠️ **Nunca subas estos valores al repositorio.** El archivo `.env` ya está en `.gitignore`.

---

## Paso 5 — Hacer el Deploy

1. Revisa toda la configuración.
2. Haz clic en **"Deploy"**.
3. Koyeb comenzará a construir la imagen (tarda ~2-3 minutos la primera vez).
4. Cuando el estado cambie a **"Healthy"** 🟢, tu bot está activo.

---

## Verificar que funciona

1. Abre Telegram y busca tu bot.
2. Escribe `/start` — Nora debería responder.
3. En el dashboard de Koyeb, ve a **"Logs"** para ver la actividad en tiempo real.

---

## Actualizaciones futuras

Cada vez que hagas `git push origin master`, Koyeb **redesplegará automáticamente** el bot con los nuevos cambios. Sin pasos manuales adicionales.

---

## Troubleshooting rápido

| Síntoma | Posible causa | Solución |
|---|---|---|
| Bot no responde | Variable de entorno incorrecta | Revisa `TELEGRAM_TOKEN` en Koyeb |
| Error en logs `401 Unauthorized` | Token inválido o expirado | Regenera el token en @BotFather |
| Error `groq.AuthenticationError` | `GROQ_API_KEY` incorrecta | Verifica la key en console.groq.com |
| Build falla | Dependencia faltante | Asegúrate que `requirements.txt` está en la raíz |
| Status "Crashed" repetido | Error en `nora_bot.py` | Revisa los logs de Koyeb para el traceback |

---

## Estructura de archivos requeridos (ya en el repo ✅)

```
NEXORA_CORE/
├── Procfile              ← Le dice a Koyeb cómo arrancar el bot
├── requirements.txt      ← Dependencias Python
├── nora_bot.py           ← Punto de entrada principal
├── NoraCore/
│   ├── brain.py
│   ├── vision.py
│   ├── memory.py
│   └── faq.py
└── deploy/
    └── koyeb_deploy_guide.md   ← Esta guía
```

---

*Guía generada para el proyecto NEXORA_CORE — Nora de Nexora 🤖*
