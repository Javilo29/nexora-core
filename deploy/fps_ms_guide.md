# Guía de Despliegue en FPS.ms — Nora (NEXORA_CORE)

> Despliegue del bot Nora en modo Polling 24/7 usando FPS.ms como servidor de hosting Python.

---

## Requisitos Previos

- Cuenta activa en [FPS.ms](https://fps.ms)
- Archivo `NEXORA_CORE_READY.zip` listo para subir
- Bot de Telegram creado con el token de @BotFather
- API Key de Groq activa

---

## Paso 1 — Crear el Servicio Python en FPS.ms

1. Inicia sesión en tu panel de control de **FPS.ms**
2. Ve a **"Services"** → **"Create New Service"**
3. Selecciona el tipo: **Python App**
4. Asigna un nombre: `nexora-nora`
5. Selecciona la versión de Python: **3.11** o superior

---

## Paso 2 — Subir los Archivos

### Opción A — Subida por ZIP (recomendado)
1. En el panel del servicio, busca la sección **"File Manager"** o **"Upload Files"**
2. Sube el archivo `NEXORA_CORE_READY.zip`
3. Extrae el contenido en la raíz del servicio (`/home/user/nexora-nora/`)

### Opción B — Git Clone
```bash
git clone https://github.com/tu-usuario/nexora-core.git .
```

### Estructura esperada en el servidor:
```
/home/user/nexora-nora/
├── nora_bot.py
├── requirements.txt
├── .env.example
├── NoraCore/
│   ├── __init__.py
│   ├── brain.py
│   ├── vision.py
│   ├── memory.py
│   └── faq.py
└── deploy/
```

---

## Paso 3 — Configurar Variables de Entorno ⚙️

> [!IMPORTANT]
> Este es el paso más importante. **NUNCA** pongas las keys directamente en el código.

1. En el panel de FPS.ms, ve a tu servicio → **"Environment"** o **"Environment Variables"**
2. Agrega las siguientes variables:

| Variable | Valor |
|---|---|
| `BOT_TOKEN` | El token de tu bot (ej: `8638244059:AAGEk...`) |
| `GROQ_API_KEY` | Tu API key de Groq (ej: `gsk_abc123...`) |
| `ADMIN_CHAT_ID` | Tu ID de Telegram (ej: `1645060982`) |

3. Guarda los cambios con **"Save"** o **"Apply"**

---

## Paso 4 — Configurar el Comando de Inicio

En la sección **"Start Command"** o **"Run Command"** del servicio, ingresa:

```
python nora_bot.py
```

Si FPS.ms requiere instalar dependencias primero, agrega en **"Build Command"**:
```
pip install -r requirements.txt
```

---

## Paso 5 — Iniciar el Servicio

1. Haz clic en **"Start"** o **"Deploy"**
2. Espera 30-60 segundos mientras instala dependencias
3. En los logs deberías ver:

```
✅ Cliente Groq inicializado correctamente.
🚀 Nora v1.0 | NEXORA_CORE | Iniciando polling...
✅ Nora está VIVA y escuchando mensajes.
```

---

## Paso 6 — Verificar que Nora Funciona

1. Abre Telegram y busca tu bot
2. Envía `/start`
3. Deberías recibir el mensaje de bienvenida de Nora

---

## Solución de Problemas Comunes

| Error en logs | Causa | Solución |
|---|---|---|
| `BOT_TOKEN no definida` | Variable de entorno faltante | Revisar Paso 3 |
| `GROQ_API_KEY no definida` | Variable de entorno faltante | Revisar Paso 3 |
| `ModuleNotFoundError: groq` | Dependencias no instaladas | Revisar Build Command |
| `Conflict: terminated by other getUpdates` | Bot corriendo en otro servidor | Detener instancia anterior |

---

## Mantenimiento

- **Para actualizar el bot:** sube los archivos nuevos y reinicia el servicio
- **Para ver logs:** panel FPS.ms → tu servicio → **"Logs"**
- **Para detener el bot:** panel FPS.ms → **"Stop"**

---

*Nexora Visual © 2025 — Soporte: contacto@nexoravisual.com*
