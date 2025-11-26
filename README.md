# 🚀 Dotfile Manager Profesional (CLI/TUI)

> Herramienta de ingeniería para la gestión de entornos en Linux (Arch/Debian) y Android (Termux). Combina la potencia de la línea de comandos con una interfaz gráfica de terminal (TUI) para una gestión segura.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Stable%20v2.0-orange)

## ✨ Características Principales

- **🖥️ Interfaz Visual (TUI):** Navega, edita y gestiona tus archivos de configuración sin salir de la terminal.
- **🛡️ Sandbox Local:** Sistema de seguridad con copias `.bak`. Edita sin miedo a romper tu sistema; los cambios no tocan Git hasta que tú lo decides.
- **🔍 Escáner Inteligente:** Detecta automáticamente aplicaciones instaladas (Zsh, Neovim, Git, etc.) y sugiere importarlas.
- **🔗 Gestión de Symlinks:** Motor robusto que maneja enlaces simbólicos, conflictos y rutas absolutas/relativas.
- **☁️ Sincronización Opcional:** Tú decides cuándo subir cambios a la nube. El repositorio se mantiene limpio de configuraciones personales por defecto.

## 📦 Instalación

### Requisitos Previos
- Python 3.10 o superior.
- Git.

### Instalación Rápida
Clona el repositorio y ejecuta el script de instalación. Esto configurará el entorno virtual y creará el alias `dotfile-pro`.

```bash
git clone https://github.com/SnakePilot10/dotfile-manager-pro.git
cd dotfile-manager-pro
./install.sh
source ~/.zshrc  # O source ~/.bashrc
```

## 🎮 Uso

Una vez instalado, usa el comando global `dotfile-pro`.

### Modo Gráfico (Recomendado)
Lanza la interfaz interactiva:

```bash
dotfile-pro ui
```

**Controles de la TUI:**
- **🖱️ Navegación:** Usa el mouse o las flechas del teclado para seleccionar archivos.
- **💾 GUARDAR (Disco):** Escribe los cambios en tu sistema en tiempo real (sin commit).
- **🛡️ BACKUP LOCAL:** Crea una copia de seguridad oculta (`.bak`) del estado actual.
- **↩️ RESTAURAR:** Si rompes algo, este botón recupera la versión del backup local instantáneamente.

### Modo CLI (Comandos Rápidos)

| Comando | Descripción |
| :--- | :--- |
| `dotfile-pro scan` | **Escanea** tu sistema buscando configs conocidas para importar. |
| `dotfile-pro status` | Muestra una tabla con el estado de todos los enlaces (Linked/Broken). |
| `dotfile-pro add <archivo>` | Agrega manualmente un archivo al repositorio y crea el enlace. |
| `dotfile-pro link` | Restaura todos los enlaces simbólicos (Ideal para instalaciones nuevas). |
| `dotfile-pro save "msg"` | Realiza un **Commit & Push** a tu repositorio remoto (Nube). |
| `dotfile-pro update` | Descarga cambios del remoto (Pull). |

## 📂 Estructura del Proyecto

El repositorio está diseñado para ser "forkeable".

- `src/`: Código fuente de la herramienta (Python).
- `dotfiles.json`: Base de datos de tus enlaces (Se genera automáticamente).
- `dotfiles/`: Carpeta donde se almacenarán tus archivos reales.

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor, abre un Issue o Pull Request para sugerir mejoras en el motor lógico.

---
*Desarrollado con ❤️ y Python por SnakePilot10.*
