# 🛠️ Dotfile Manager Pro

Un gestor de configuraciones (dotfiles) profesional, diseñado para ser **seguro, atómico y reproducible**, inspirado en la filosofía declarativa.

## ✨ Características Principales

- **🛡️ Operaciones Atómicas:** Los cambios en la configuración se realizan mediante escrituras atómicas para prevenir corrupción de datos.
- **🛡️ Importación Segura:** Implementa una estrategia de `Copia -> Verificación -> Enlace` en lugar de mover archivos directamente.
- **📦 Backups Automáticos:** Crea respaldos con marca de tiempo en `.backups/` antes de realizar cualquier operación destructiva.
- **🔍 Escaneo Inteligente:** Detecta automáticamente configuraciones comunes en tu sistema que aún no están siendo gestionadas.
- **🖥️ Interfaz Visual (TUI):** Incluye una potente interfaz de terminal para editar tus archivos directamente.
- **🔗 Git Local:** Gestión de versiones integrada de forma local para privacidad total.

## 🚀 Instalación

Clona el repositorio y ejecuta el instalador:

```bash
git clone https://github.com/tu-usuario/dotfile-manager-pro.git
cd dotfile-manager-pro
./install.sh
source ~/.bashrc  # O ~/.zshrc
```

## 📖 Uso Rápido

### 1. Escanear el sistema
Encuentra archivos de configuración conocidos y agrégalos fácilmente:
```bash
dotfile-pro scan
```

### 2. Añadir un archivo manualmente
```bash
dotfile-pro add ~/.config/alacritty/alacritty.toml --profile Desktop --folder terminal
```

### 3. Verificar estado
```bash
dotfile-pro status
```

### 4. Vincular archivos (en una máquina nueva)
```bash
dotfile-pro link --force
```

### 5. Interfaz Visual
```bash
dotfile-pro ui
```

## 🏗️ Arquitectura

El proyecto está dividido en capas para máxima mantenibilidad:
- `src/core`: Modelos de datos y definiciones base.
- `src/services`: Lógica de negocio (File system, Config, Scanner).
- `src/interface`: Capas de interacción (CLI con Typer, TUI con Textual).

## 🔒 Privacidad

Este proyecto está configurado para **no subir tus datos personales** a GitHub por defecto. El archivo `.gitignore` excluye:
- `dotfiles.json`
- Carpeta `dotfiles/`
- Carpeta `.backups/`

Esto permite compartir el **código de la herramienta** sin exponer tus secretos o rutas de sistema.