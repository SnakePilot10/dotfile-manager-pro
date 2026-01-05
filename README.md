# 🚀 Dotfile Manager Profesional (v2.0.0)

> **Gestor de entornos de ingeniería.** Combina una CLI robusta con una Interfaz Gráfica de Terminal (TUI) para administrar configuraciones en Linux y Android (Termux) de forma segura y nativa.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Termux-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Stable-success)

## ✨ Características Principales

- **🖥️ TUI Interactiva:** Navega, edita y gestiona archivos visualmente (`dotfile-pro ui`). **Compatible con móviles**.
- **📂 Arquitectura XDG:** Tus datos y configuraciones viven en `~/.config/dotfile-manager-pro`, separados de la instalación.
- **🛡️ Modo Sandbox:** Edita con seguridad. Usa **Backups Locales** (`.bak`) y restaura al instante sin ensuciar Git.
- **🔍 Auto-Descubrimiento:** El comando `scan` detecta automáticamente apps instaladas (Zsh, Neovim, etc.) y sugiere importarlas.
- **☁️ Cloud Sync:** Sincronización Git automática e inteligente.

## 📦 Instalación

### Requisitos Previos
- Python 3.10+
- Git

### Opción A: Universal (Pip) - Recomendado
Funciona en cualquier distribución Linux y Termux.

```bash
git clone https://github.com/SnakePilot10/dotfile-manager-pro.git
cd dotfile-manager-pro
pip install .
```

### Opción B: Arch Linux (PKGBUILD)
```bash
git clone https://github.com/SnakePilot10/dotfile-manager-pro.git
cd dotfile-manager-pro
makepkg -si
```

### Opción C: Android (Termux)
```bash
pkg install python git
git clone https://github.com/SnakePilot10/dotfile-manager-pro.git
cd dotfile-manager-pro
pip install .
```

## 🎮 Uso

### Iniciar Interfaz Gráfica (TUI)
Es la forma más sencilla de gestionar tus archivos.
```bash
dotfile-pro ui
```

### Comandos CLI

| Comando | Descripción |
|---------|-------------|
| `dotfile-pro scan` | Escanea el sistema y busca archivos de configuración conocidos. |
| `dotfile-pro add <archivo>` | Agrega un archivo específico al repositorio. |
| `dotfile-pro status` | Ver el estado de los enlaces simbólicos y sincronización. |
| `dotfile-pro save "mensaje"` | Guardar cambios y subir a Git (Commit & Push). |
| `dotfile-pro update` | Descargar cambios remotos (Pull). |
| `dotfile-pro link` | Restaurar enlaces simbólicos (útil en instalaciones nuevas). |

## 📁 Estructura de Datos
El programa sigue el estándar XDG.
- **Configuración y Repositorio:** `~/.config/dotfile-manager-pro/`
- **Dotfiles:** `~/.config/dotfile-manager-pro/dotfiles/`

---
*Desarrollado con ingeniería de precisión por SnakePilot10.*
