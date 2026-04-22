# 🚀 Despliegue en Render — NEXORA_CORE

> **Tiempo estimado:** 5 minutos  
> **Modo:** Polling (24/7 automático)  
> **Costo:** Gratis (tier Free)

---

## Paso 1 — Conectar GitHub con Render

1. Ir a [https://render.com](https://render.com) y crear cuenta (o iniciar sesión)
2. Click en **"New +"** → **"Web Service"**
3. Conectar tu cuenta de **GitHub** si no lo hiciste antes
4. Buscar y seleccionar el repositorio **`nexora-core`**

---

## Paso 2 — Configurar el servicio

Render detectará automáticamente el `render.yaml`, pero verificá estos valores:

| Campo | Valor |
|-------|-------|
| **Name** | `nora-nexora` |
| **Region** | Oregon (US West) |
| **Branch** | `master` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python nora_bot.py` |
| **Plan** | Free |

---

## Paso 3 — Variables de entorno

En la sección **"Environment"**, agregar estas 3 variables **manualmente**:

| Key | Value |
|-----|-------|
| `BOT_TOKEN` | *(tu token de @BotFather)* |
| `GROQ_API_KEY` | *(tu key de console.groq.com)* |
| `ADMIN_CHAT_ID` | *(tu chat ID de Telegram)* |

> ⚠️ **No subas el archivo `.env` a GitHub.** Las variables se configuran directamente en Render.

---

## Paso 4 — Deploy

1. Click en **"Create Web Service"**
2. Esperar a que termine el build (2-3 minutos)
3. Verificar que los logs muestren:
   ```
   ✅ Cliente Groq inicializado correctamente.
   ✅ Nora está VIVA y escuchando mensajes.
   ```

---

## Paso 5 — Mantener vivo el servicio (Anti-Sleep)

El plan gratuito de Render suspende el servicio tras 15 minutos de inactividad.  
Para evitarlo, configurar un **ping automático**:

1. Ir a [https://cron-job.org](https://cron-job.org) y crear cuenta gratuita
2. Crear un nuevo cron job:

| Campo | Valor |
|-------|-------|
| **Title** | `Nora Keep Alive` |
| **URL** | `https://nora-nexora.onrender.com/` |
| **Schedule** | Cada **5 minutos** |
| **Method** | `GET` |

3. Activar y guardar

> 💡 La URL exacta de tu servicio la encontrás en el dashboard de Render, arriba a la izquierda.

---

## Actualizar el bot

Cada vez que hagas `git push`, Render hace deploy automáticamente:

```bash
git add .
git commit -m "update: descripción del cambio"
git push origin master
```

---

## Troubleshooting

| Síntoma | Solución |
|---------|----------|
| Bot no responde | Verificar logs en Render → buscar errores |
| `ModuleNotFoundError` | Verificar que el módulo esté en `requirements.txt` |
| Build falla | Revisar que `requirements.txt` no tenga errores de tipeo |
| Se suspende el servicio | Configurar cron-job.org (Paso 5) |
| `BOT_TOKEN not found` | Verificar variables de entorno en Render Dashboard |

---

*Guía generada para NEXORA_CORE — Nora de Nexora 🤖*
