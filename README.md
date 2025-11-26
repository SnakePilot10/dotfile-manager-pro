# 🚀 Dotfile Manager Profesional (v2.0.0)

> **Gestor de entornos de ingeniería.** Combina una CLI robusta con una Interfaz Gráfica de Terminal (TUI) para administrar configuraciones en Linux y Android de forma segura y nativa.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Arch Linux](https://img.shields.io/badge/Arch-Native%20Package-1793d1)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Stable-success)

## ✨ Características Principales

- **🖥️ TUI Interactiva:** Navega, edita y gestiona archivos visualmente (`dotfile-pro ui`).
- **🛡️ Modo Sandbox:** Edita con seguridad. Usa **Backups Locales** (`.bak`) y restaura al instante sin ensuciar Git.
- **🔍 Auto-Descubrimiento:** El comando `scan` detecta apps instaladas (Zsh, Neovim, Kitty, etc.) y sugiere importarlas.
- **📦 Paquete Nativo:** Se instala en el sistema (`/usr/bin`), funcionando en cualquier shell (Bash, Zsh, Fish, Nushell).
- **☁️ Cloud Sync:** Sincronización Git bajo demanda (`save`, `update`).

## 📦 Instalación

### Opción A: Arch Linux (Nativo)
Esta herramienta incluye un `PKGBUILD` oficial. Instálala como cualquier paquete del sistema.

```bash
git clone https://github.com/SnakePilot10/dotfile-manager-pro.git
cd dotfile-manager-pro
makepkg -si
```

### Opción B: Universal (Ubuntu, Fedora, Termux, macOS)
Instalación mediante el gestor de paquetes de Python (PIP).

```bash
git clone https://github.com/SnakePilot10/dotfile-manager-pro.git
cd dotfile-manager-pro
pip install .
```
*(Nota: En algunos sistemas puede requerir `pip install --user .` o usar `pipx`)*

## 🎮 Uso

Una vez instalado, el comando `dotfile-pro` estará disponible globalmente.

### 1. Interfaz Gráfica (Recomendado)
```bash
dotfile-pro ui
```
* Navega con Mouse o Teclado.
* **Save:** Guarda en disco (Hot-reload).
* **Backup:** Crea snapshot local.
* **Restore:** Recupera snapshot.

### 2. Línea de Comandos (CLI)
| Comando | Acción |
| :--- | :--- |
| `dotfile-pro scan` | Busca configuraciones no gestionadas e impórtalas. |
| `dotfile-pro status` | Ver tabla de estado (Linked / Broken / Missing). |
| `dotfile-pro add <file>` | Agrega un archivo manual al sistema. |
| `dotfile-pro save "msg"` | Commit & Push a GitHub. |
| `dotfile-pro update` | Pull desde GitHub. |

## 📂 Estructura del Repositorio

Este repositorio está diseñado como una **plantilla limpia**.
- `src/`: Código fuente inmutable.
- `PKGBUILD` & `pyproject.toml`: Definiciones de empaquetado.
- `dotfiles.json`: Base de datos de tus enlaces (Inicialmente vacía).

## 🤝 Contribuir
Si encuentras un bug o quieres mejorar el motor de escaneo, por favor abre un Issue o PR.

---
*Desarrollado con ingeniería de precisión por SnakePilot10.*
