# Makefile para Dotfile Manager Pro
# Genera un ejecutable portable .pyz (zipapp) compatible con cualquier Linux/Termux

APP_NAME = dotfile-pro
SRC_DIR = src
MAIN_ENTRY = src.interface.cli:app
BUILD_DIR = build
DIST_DIR = dist

.PHONY: all setup clean test build install

all: build

# 1. Configuración del entorno de desarrollo
setup:
	python3 -m venv .venv
	./.venv/bin/pip install -r requirements.txt

# 2. Ejecutar pruebas
test:
	./.venv/bin/pytest tests/

# 3. Construir ejecutable portable (Shiv)
# Crea un archivo único con todas las dependencias incluidas.
build:
	@echo "🔨 Construyendo ejecutable portable (ZipApp)..."
	@mkdir -p $(DIST_DIR)
	./.venv/bin/shiv -c dotfile-pro -o $(DIST_DIR)/$(APP_NAME) -p "/usr/bin/env python3" .
	@chmod +x $(DIST_DIR)/$(APP_NAME)
	@echo "✅ Ejecutable creado en $(DIST_DIR)/$(APP_NAME)"

# 4. Instalación global
install: build
	@echo "📦 Instalando en /usr/local/bin..."
	@if [ -w /usr/local/bin ]; then \
		cp $(DIST_DIR)/$(APP_NAME) /usr/local/bin/; \
	else \
		echo "⚠️  Se requieren permisos de root para instalar en /usr/local/bin"; \
		sudo cp $(DIST_DIR)/$(APP_NAME) /usr/local/bin/; \
	fi
	@echo "✨ Instalación completada. Ejecuta '$(APP_NAME)' desde cualquier lugar."

# 5. Limpieza
clean:
	rm -rf $(BUILD_DIR) $(DIST_DIR) *.spec __pycache__ .pytest_cache .venv
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete