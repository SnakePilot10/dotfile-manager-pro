from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem, Label, TextArea, Button
from textual.containers import Horizontal, Vertical, Container
from src.services.config_service import ConfigService
from src.services.file_service import FileService
from src.core.paths import context

class DotfileItem(ListItem):
    def __init__(self, label: str, dotfile) -> None:
        super().__init__(Label(label))
        self.dotfile = dotfile

class DotfileTUI(App):
    CSS = """
    Screen { layout: vertical; }
    #sidebar { width: 30; background: $panel; border-right: solid $accent; }
    #editor-area { height: 1fr; border: solid $success; }
    #buttons { height: 3; dock: bottom; layout: horizontal; align: center middle; }
    Button { margin: 0 1; }
    """
    
    BINDINGS = [("q", "quit", "Quit"), ("s", "save", "Save")]

    def __init__(self):
        super().__init__()
        self.config_service = ConfigService()
        self.current_dotfile = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label(" Managed Files")
                self.list_view = ListView()
                yield self.list_view
            with Vertical():
                self.editor = TextArea(language="bash", id="editor-area")
                yield self.editor
                with Container(id="buttons"):
                    yield Button("Save", id="btn-save", variant="success")
        yield Footer()

    def on_mount(self):
        self.load_files()

    def load_files(self):
        self.list_view.clear()
        for df in self.config_service.load_config():
            # Logic to extract a friendly "App Name" from the path
            parts = df.source.parts
            filename = df.source.name
            
            if len(parts) > 1:
                # Use parent folder as category (e.g. "nvim" from "nvim/init.lua")
                category = parts[-2]
                # Cleanup if it's directly in auto-scan without subfolder (legacy)
                if category == "auto-scan":
                    category = "Misc"
            else:
                category = "Root"
            
            # Formatting: "Neovim: init.lua"
            category_display = category.replace("-", " ").title()
            label = f"{category_display}: {filename}"
            
            self.list_view.append(DotfileItem(label, df))

    def on_list_view_selected(self, event: ListView.Selected):
        self.current_dotfile = event.item.dotfile
        path = context.get_absolute_source(self.current_dotfile.source)
        if path.exists():
            content = path.read_text(encoding="utf-8")
            self.editor.text = content
            
            # Dynamic Syntax Highlighting
            ext = path.suffix.lower()
            if ext in [".py", ".pyw"]: self.editor.language = "python"
            elif ext in [".json", ".js"]: self.editor.language = "json"
            elif ext in [".md", ".markdown"]: self.editor.language = "markdown"
            elif ext in [".yml", ".yaml", ".toml", ".conf", ".ini"]: self.editor.language = "yaml"
            elif ext in [".lua"]: self.editor.language = "python" # Textual might not have lua, python is close enough
            elif ext in [".css"]: self.editor.language = "css"
            else: self.editor.language = "bash"

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn-save" and self.current_dotfile:
            path = context.get_absolute_source(self.current_dotfile.source)
            try:
                # Atomic Write
                import tempfile
                import os
                dir_name = path.parent
                with tempfile.NamedTemporaryFile("w", delete=False, dir=dir_name, encoding="utf-8") as tmp:
                    tmp.write(self.editor.text)
                    tmp_path = Path(tmp.name)
                
                os.replace(tmp_path, path)
                self.notify(f"File saved: {path.name}")
            except Exception as e:
                self.notify(f"Error: {e}", severity="error")
