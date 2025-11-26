from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem, Label, TextArea, Button
from textual.containers import Horizontal, Vertical, Container
from pathlib import Path
import shutil
from .config_manager import ConfigManager

class DotfileItem(ListItem):
    def __init__(self, label_text: str, source_path: str) -> None:
        super().__init__(Label(label_text))
        self.source_path = source_path

class DotfileTUI(App):
    """Gestor Visual de Dotfiles (Modo Local)."""
    
    CSS = """
    Screen { layout: vertical; }
    #sidebar { width: 30; background: $panel; border-right: solid $accent; height: 100%; }
    #editor-area { height: 1fr; border: solid $success; margin: 0 0 1 0; }
    .file-item { padding: 1; }
    
    /* Botonera inferior */
    #buttons { 
        height: 3; 
        dock: bottom; 
        layout: horizontal; 
        align: center middle; 
        background: $surface; 
        margin: 0 0 1 0; 
    }
    Button { margin: 0 1; min-width: 22; border: none; }
    
    /* Colores para diferenciar funciones */
    #btn-save { background: $success; color: black; text-style: bold; }
    #btn-backup { background: $primary; color: white; }
    #btn-restore { background: $warning; color: black; }
    """

    BINDINGS = [
        ("q", "quit", "Salir"),
        ("s", "save_file", "Guardar"),
        ("b", "backup_file", "Crear Backup"),
        ("r", "restore_file", "Restaurar"),
    ]

    def __init__(self):
        super().__init__()
        self.manager = ConfigManager()
        self.current_dotfile = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label(" 📂 Archivos Gestionados", classes="file-item")
                self.list_view = ListView()
                yield self.list_view
            with Vertical():
                self.editor = TextArea(language="bash", theme="dracula", id="editor-area")
                yield self.editor
                with Container(id="buttons"):
                    yield Button("💾 GUARDAR (Disco)", id="btn-save")
                    yield Button("🛡️ CREAR BACKUP", id="btn-backup")
                    yield Button("↩️ RESTAURAR (.bak)", id="btn-restore")
        yield Footer()

    def on_mount(self) -> None:
        self.refresh_file_list()

    def refresh_file_list(self):
        self.list_view.clear()
        if not self.manager.dotfiles:
            self.list_view.append(ListItem(Label("⚠️ Lista vacía. Usa 'add' o 'scan' primero.")))
            return
        for dotfile in self.manager.dotfiles:
            item = DotfileItem(f"{dotfile.profile} | {dotfile.source_path.name}", str(dotfile.source_path))
            self.list_view.append(item)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        REPO_DIR = Path(__file__).resolve().parent.parent
        # Buscar el objeto dotfile basado en la ruta seleccionada
        for df in self.manager.dotfiles:
            if str(df.source_path) == event.item.source_path:
                self.current_dotfile = df
                full_path = REPO_DIR / df.source_path
                try:
                    content = full_path.read_text(encoding="utf-8")
                    self.editor.text = content
                    self.editor.border_title = f"Editando: {df.source_path.name}"
                    
                    # Detección de sintaxis
                    ext = df.source_path.suffix
                    if ext == ".json": self.editor.language = "json"
                    elif ext == ".py": self.editor.language = "python"
                    elif ext in [".yml", ".yaml", ".toml"]: self.editor.language = "yaml"
                    elif ext == ".lua": self.editor.language = "python" 
                    else: self.editor.language = "bash"
                except Exception as e:
                    self.editor.text = f"Error leyendo archivo: {e}"
                break

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-save": self.action_save_file()
        elif event.button.id == "btn-backup": self.action_backup_file()
        elif event.button.id == "btn-restore": self.action_restore_file()

    def action_save_file(self):
        """Guarda SOLO en el disco duro (Modifica el archivo real)."""
        if not self.current_dotfile: return
        REPO_DIR = Path(__file__).resolve().parent.parent
        full_path = REPO_DIR / self.current_dotfile.source_path
        
        try:
            full_path.write_text(self.editor.text, encoding="utf-8")
            self.notify(f"✅ Guardado en disco: {full_path.name}")
        except Exception as e:
            self.notify(f"❌ Error: {e}", severity="error")

    def action_backup_file(self):
        """Crea una copia .bak oculta en la misma carpeta."""
        if not self.current_dotfile: return
        REPO_DIR = Path(__file__).resolve().parent.parent
        full_path = REPO_DIR / self.current_dotfile.source_path
        # Crea un archivo .bak (ej: alacritty.toml.bak)
        backup_path = full_path.with_suffix(full_path.suffix + ".bak")
        
        try:
            # Primero guardamos el estado actual del editor
            full_path.write_text(self.editor.text, encoding="utf-8")
            # Luego duplicamos el archivo
            shutil.copy2(full_path, backup_path)
            self.notify(f"🛡️ Backup local creado exitosamente", severity="information")
        except Exception as e:
            self.notify(f"❌ Error creando backup: {e}", severity="error")

    def action_restore_file(self):
        """Recupera el contenido desde el archivo .bak local."""
        if not self.current_dotfile: return
        REPO_DIR = Path(__file__).resolve().parent.parent
        full_path = REPO_DIR / self.current_dotfile.source_path
        backup_path = full_path.with_suffix(full_path.suffix + ".bak")
        
        if not backup_path.exists():
            self.notify("⚠️ No existe un backup local (.bak) para este archivo", severity="warning")
            return

        try:
            # Copiamos del backup hacia el archivo real
            shutil.copy2(backup_path, full_path)
            # Recargamos el editor visualmente
            content = full_path.read_text(encoding="utf-8")
            self.editor.text = content
            self.notify(f"↩️ Restaurado desde copia local", severity="warning")
        except Exception as e:
            self.notify(f"❌ Error al restaurar: {e}", severity="error")
