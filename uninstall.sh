#!/usr/bin/env bash
# Script de desinstalación para Dotfile Manager Pro

echo "🗑️ Iniciando desinstalación de Dotfile Manager Pro..."

# Intentar usar Make si está disponible
if command -v make &> /dev/null; then
    make uninstall
else
    # Fallback manual para Termux
    if [ -n "$PREFIX" ]; then
        if [ -f "$PREFIX/bin/dotfile-pro" ]; then
            rm "$PREFIX/bin/dotfile-pro"
            echo "✅ Eliminado de $PREFIX/bin/dotfile-pro"
        else
            echo "⚠️ No se encontró la instalación en $PREFIX/bin"
        fi
    else
        # Fallback manual para Linux
        TARGET="/usr/local/bin/dotfile-pro"
        if [ -f "$TARGET" ]; then
            if [ -w "$(dirname "$TARGET")" ]; then
                rm "$TARGET"
            else
                echo "🔒 Se requieren permisos de root para eliminar $TARGET"
                sudo rm "$TARGET"
            fi
            echo "✅ Eliminado de $TARGET"
        else
            echo "⚠️ No se encontró la instalación en $TARGET"
        fi
    fi
fi

# Eliminar alias si existen (Intento básico)
SHELL_CONFIG="$HOME/.bashrc"
[ -n "$ZSH_VERSION" ] && SHELL_CONFIG="$HOME/.zshrc"

if grep -q "alias dotfile-pro" "$SHELL_CONFIG"; then
    echo "⚠️ Se detectó un alias en $SHELL_CONFIG. Por favor, elimínalo manualmente."
fi

echo "✨ Desinstalación completa."
