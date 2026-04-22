#!/bin/bash
# =============================================================================
# NEXORA_CORE — Script de Setup para PythonAnywhere
# =============================================================================
# USO: Copiar y pegar este script COMPLETO en la Bash de PythonAnywhere.
#      Solo necesitas ejecutarlo UNA VEZ.
# =============================================================================

set -e
echo "============================================="
echo "  NEXORA_CORE — Setup PythonAnywhere"
echo "============================================="

# --- 1. Detectar la carpeta del proyecto ---
echo ""
echo "[1/7] Buscando carpeta del proyecto..."

PROJECT_DIR=""
for dir in /home/javilo2/nexora-core /home/javilo2/NEXORA_CORE /home/javilo2/nexora-nucleo; do
    if [ -f "$dir/nora_bot.py" ]; then
        PROJECT_DIR="$dir"
        break
    fi
done

# Si no se encontró, buscar en cualquier carpeta
if [ -z "$PROJECT_DIR" ]; then
    for dir in /home/javilo2/*/; do
        if [ -f "${dir}nora_bot.py" ]; then
            PROJECT_DIR="${dir%/}"
            break
        fi
    done
fi

if [ -z "$PROJECT_DIR" ]; then
    echo "ERROR: No se encontró el proyecto. Clonando desde GitHub..."
    cd /home/javilo2
    git clone https://github.com/Javilo29/nexora-core.git
    PROJECT_DIR="/home/javilo2/nexora-core"
fi

echo "   Proyecto encontrado en: $PROJECT_DIR"

# --- 2. Actualizar código desde GitHub ---
echo ""
echo "[2/7] Actualizando codigo desde GitHub..."
cd "$PROJECT_DIR"
git pull origin master 2>/dev/null || git pull origin main 2>/dev/null || echo "   (git pull omitido)"

# --- 3. Crear .env ---
echo ""
echo "[3/7] Configurando archivo .env..."

if [ -f "$PROJECT_DIR/.env" ]; then
    echo "   .env ya existe en: $PROJECT_DIR/.env"
    echo "   Contenido actual:"
    cat "$PROJECT_DIR/.env"
else
    echo "   Creando .env... Introduce tus credenciales:"
    read -p "   BOT_TOKEN: " BOT_TOKEN_VAL
    read -p "   GROQ_API_KEY: " GROQ_KEY_VAL
    read -p "   ADMIN_CHAT_ID: " ADMIN_ID_VAL
    cat > "$PROJECT_DIR/.env" << ENVEOF
BOT_TOKEN=$BOT_TOKEN_VAL
GROQ_API_KEY=$GROQ_KEY_VAL
ADMIN_CHAT_ID=$ADMIN_ID_VAL
ENVEOF
    echo "   .env creado en: $PROJECT_DIR/.env"
fi

# --- 4. Instalar dependencias ---
echo ""
echo "[4/7] Instalando dependencias..."
pip install --user -r "$PROJECT_DIR/requirements.txt" 2>&1 | tail -3
pip install --user flask python-dotenv 2>&1 | tail -3
echo "   Dependencias OK"

# --- 5. Crear symlinks de seguridad ---
echo ""
echo "[5/7] Creando symlinks de seguridad..."
if [ "$PROJECT_DIR" != "/home/javilo2/nexora-core" ] && [ ! -e "/home/javilo2/nexora-core" ]; then
    ln -s "$PROJECT_DIR" /home/javilo2/nexora-core
    echo "   Symlink creado: /home/javilo2/nexora-core -> $PROJECT_DIR"
fi
if [ "$PROJECT_DIR" != "/home/javilo2/nexora-nucleo" ] && [ ! -e "/home/javilo2/nexora-nucleo" ]; then
    ln -s "$PROJECT_DIR" /home/javilo2/nexora-nucleo
    echo "   Symlink creado: /home/javilo2/nexora-nucleo -> $PROJECT_DIR"
fi
if [ "$PROJECT_DIR" != "/home/javilo2/NEXORA_CORE" ] && [ ! -e "/home/javilo2/NEXORA_CORE" ]; then
    ln -s "$PROJECT_DIR" /home/javilo2/NEXORA_CORE
    echo "   Symlink creado: /home/javilo2/NEXORA_CORE -> $PROJECT_DIR"
fi
echo "   Symlinks OK"

# --- 6. Configurar archivo WSGI de PythonAnywhere ---
echo ""
echo "[6/7] Configurando WSGI de PythonAnywhere..."
cat > /var/www/javilo2_pythonanywhere_com_wsgi.py << WSGIEOF
import sys
import os

# Blindaje total: buscar el proyecto en multiples ubicaciones
possible_paths = [
    '/home/javilo2/nexora-core',
    '/home/javilo2/NEXORA_CORE',
    '/home/javilo2/nexora-nucleo',
]

project_path = None
for path in possible_paths:
    if os.path.exists(os.path.join(path, 'nora_bot.py')):
        project_path = path
        break

# Ultimo recurso: escanear /home/javilo2/
if project_path is None:
    home = '/home/javilo2'
    for entry in os.listdir(home):
        candidate = os.path.join(home, entry)
        if os.path.isdir(candidate) and os.path.exists(os.path.join(candidate, 'nora_bot.py')):
            project_path = candidate
            break

if project_path is None:
    raise Exception("FATAL: No se encontro el proyecto NEXORA_CORE")

sys.path.insert(0, project_path)

from wsgi import application
WSGIEOF
echo "   WSGI configurado OK"

# --- 7. Reiniciar Web App ---
echo ""
echo "[7/7] Reiniciando Web App..."
touch /var/www/javilo2_pythonanywhere_com_wsgi.py
echo "   Web App reiniciada"

# --- Resumen ---
echo ""
echo "============================================="
echo "  SETUP COMPLETADO"
echo "============================================="
echo "  Proyecto: $PROJECT_DIR"
echo "  .env:     $PROJECT_DIR/.env"
echo "  WSGI:     /var/www/javilo2_pythonanywhere_com_wsgi.py"
echo ""
echo "  Symlinks creados para:"
ls -la /home/javilo2/ | grep "^l" || echo "    (ninguno necesario)"
echo ""
echo "  Webhook actual:"
BOT_TOKEN_CHECK=$(grep BOT_TOKEN "$PROJECT_DIR/.env" | cut -d= -f2)
curl -s "https://api.telegram.org/bot${BOT_TOKEN_CHECK}/getWebhookInfo" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'    URL: {d[\"result\"][\"url\"]}'); print(f'    Errores pendientes: {d[\"result\"].get(\"pending_update_count\",0)}'); print(f'    Ultimo error: {d[\"result\"].get(\"last_error_message\",\"ninguno\")}')" 2>/dev/null || echo "    (no se pudo verificar)"
echo ""
echo "============================================="
echo "  Proba en Telegram:"
echo "  'Nora, que servicios ofrece Nexora Visual?'"
echo "============================================="
