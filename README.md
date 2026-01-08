# 🛠️ Dotfile Manager Pro

Un gestor de configuraciones (dotfiles) profesional, diseñado para ser **seguro, atómico y reproducible**. Funciona en cualquier distribución Linux (Arch, Debian, Fedora) y Android (Termux).

## ✨ Características Principales

- **🛡️ Operaciones Atómicas:** Prevención total de corrupción de datos.
- **📦 Single Binary:** Se compila en un solo archivo ejecutable portable.
- **🔍 Escaneo Inteligente:** Detecta configuraciones huérfanas en tu sistema.
- **🖥️ Interfaz Visual (TUI):** Edita tus configs con **resaltado de sintaxis** y guardado atómico.
- **🔗 Git Local:** Privacidad total. Tus datos no se suben a la nube por defecto.

## 🚀 Instalación

### Opción A: Desde Código Fuente (Universal)

Requisitos: `python3`, `git`, `make`.

```bash
git clone https://github.com/SnakePilot10/dotfile-manager-pro.git
cd dotfile-manager-pro

# 1. Configurar entorno
make setup

# 2. Construir ejecutable
make build

# 3. Instalar (requiere sudo en PC, directo en Termux)
make install
```

### Opción B: Arch Linux (Nativo)

```bash
makepkg -si
```

## 📖 Guía de Uso

Una vez instalado, el comando `dotfile-pro` estará disponible globalmente.

### 1. Inicializar Repositorio
Ve a la carpeta donde quieres guardar tus dotfiles (o crea una nueva):
```bash
mkdir ~/mis-dotfiles && cd ~/mis-dotfiles
dotfile-pro scan
```

### 2. Gestionar Archivos
```bash
# Escanear sistema automáticamente
dotfile-pro scan

# Añadir archivo manual
dotfile-pro add ~/.bashrc --profile Laptop

# Ver estado de enlaces
dotfile-pro status
```

### 3. Interfaz Gráfica (TUI)
Para una experiencia visual:
```bash
dotfile-pro ui
```

## 🤝 Contribución

¡Las contribuciones son bienvenidas! El proyecto sigue una arquitectura modular limpia:

- **`src/core`**: Modelos de datos (Dotfile) y configuración de rutas.
- **`src/services`**: Lógica de negocio pura (I/O, JSON, Git).
- **`src/interface`**: CLI (Typer) y TUI (Textual).

### Pasos para desarrollar:
1.  Clonar el repo.
2.  `make setup` para crear el entorno virtual.
3.  Hacer cambios.
4.  `make test` para asegurar que no rompiste nada.
5.  Enviar PR.

## 📜 Licencia
MIT License.
