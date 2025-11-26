# 🚀 Dotfile Manager Profesional (v2.0.0)

> **Gestor de entornos de ingeniería.** Combina una CLI robusta con una Interfaz Gráfica de Terminal (TUI) para administrar configuraciones en Linux y Android de forma segura y nativa.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Arch Linux](https://img.shields.io/badge/Arch-Native%20Package-1793d1)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Stable-success)

## ✨ Características Principales

- **🖥️ TUI Interactiva:** Navega, edita y gestiona archivos visualmente (`dotfile-pro ui`).
- **🛡️ Modo Sandbox:** Edita con seguridad. Usa **Backups Locales** (`.bak`) y restaura al instante sin ensuciar Git.
- **🔍 Auto-Descubrimiento:** El comando `scan` detecta automáticamente apps instaladas y sugiere importarlas.
- **📦 Paquete Nativo:** Se instala en el sistema (`/usr/bin`), funcionando en cualquier shell.
- **☁️ Cloud Sync:** Sincronización Git bajo demanda.

## 📦 Instalación

### Opción A: Arch Linux (Nativo)
```bash
git clone https://github.com/SnakePilot10/dotfile-manager-pro.git
cd dotfile-manager-pro
makepkg -si
```

### Opción B: Universal (Pip)
```bash
git clone https://github.com/SnakePilot10/dotfile-manager-pro.git
cd dotfile-manager-pro
pip install .
```

## 🎮 Uso

- **GUI:** `dotfile-pro ui` (Recomendado)
- **CLI:** `dotfile-pro scan`, `add`, `status`, `save`

---
*Desarrollado con ingeniería de precisión por SnakePilot10.*
