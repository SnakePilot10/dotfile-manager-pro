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
	@rm -rf $(DIST_DIR)/target
	# Instalar el paquete y dependencias en un directorio temporal para que la estructura sea plana/correcta
	./.venv/bin/pip install . -t $(DIST_DIR)/target
	# Crear el zipapp usando ese directorio como source
	./.venv/bin/shiv --site-packages $(DIST_DIR)/target --compressed -o $(DIST_DIR)/$(APP_NAME) -p "/usr/bin/env python3" -e interface.cli:app
	@chmod +x $(DIST_DIR)/$(APP_NAME)
	@echo "✅ Ejecutable creado en $(DIST_DIR)/$(APP_NAME)"

# 4. Instalación global inteligente (Detecta Termux vs Linux normal)
install: build
	@echo "📦 Detectando entorno de instalación..."
	@if [ -n "$(PREFIX)" ]; then \
		echo "📱 Entorno Termux detectado (PREFIX=$(PREFIX))"; \
		mkdir -p $(PREFIX)/bin; \
		cp $(DIST_DIR)/$(APP_NAME) $(PREFIX)/bin/; \
		chmod +x $(PREFIX)/bin/$(APP_NAME); \
		echo "✨ Instalado en $(PREFIX)/bin/$(APP_NAME)"; \
	else \
		echo "🐧 Entorno Linux estándar detectado"; \
		if [ -w /usr/local/bin ]; then \
			cp $(DIST_DIR)/$(APP_NAME) /usr/local/bin/; \
		else \
			echo "🔒 Elevando privilegios con sudo..."; \
			sudo cp $(DIST_DIR)/$(APP_NAME) /usr/local/bin/; \
		fi; \
		echo "✨ Instalado en /usr/local/bin/$(APP_NAME)"; \
	fi
	@echo "✅ ¡Listo! Ejecuta '$(APP_NAME)' para empezar."

# 5. Limpieza
clean:
	rm -rf $(BUILD_DIR) $(DIST_DIR) *.spec __pycache__ .pytest_cache .venv
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

# 6. Desinstalación
uninstall:
	@echo "🗑️ Desinstalando Dotfile Manager Pro..."
	@if [ -n "$(PREFIX)" ]; then \
		rm -f $(PREFIX)/bin/$(APP_NAME); \
		echo "✅ Eliminado de $(PREFIX)/bin/$(APP_NAME)"; \
	else \
		if [ -w /usr/local/bin ]; then \
			rm -f /usr/local/bin/$(APP_NAME); \
		else \
			echo "🔒 Elevando privilegios con sudo para desinstalar..."; \
			sudo rm -f /usr/local/bin/$(APP_NAME); \
		fi; \
		echo "✅ Eliminado de /usr/local/bin/$(APP_NAME)"; \
	fi