#!/bin/bash
# Instalador simple para Dotfile Manager Pro
APP_DIR="$(pwd)"
SHELL_CONFIG=""

# Detectar Shell
if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
else
    SHELL_CONFIG="$HOME/.bashrc"
fi

echo "🔧 Instalando Dotfile Manager Pro..."
echo "📂 Directorio: $APP_DIR"

# Permisos
chmod +x cli.py

# Crear Alias
echo "" >> "$SHELL_CONFIG"
echo "# Alias para Dotfile Manager Pro" >> "$SHELL_CONFIG"
echo "alias dotfile-pro='$APP_DIR/.venv/bin/python $APP_DIR/cli.py'" >> "$SHELL_CONFIG"

echo "✅ Alias 'dotfile-pro' agregado a $SHELL_CONFIG"
echo "⚠️  Por favor, ejecuta: source $SHELL_CONFIG"
echo "🚀 Uso: dotfile-pro [status|link|save|update]"
