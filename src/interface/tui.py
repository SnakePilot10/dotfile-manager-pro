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
            self.list_view.append(DotfileItem(f"{df.profile} | {df.source.name}", df))

    def on_list_view_selected(self, event: ListView.Selected):
        self.current_dotfile = event.item.dotfile
        path = context.get_absolute_source(self.current_dotfile.source)
        if path.exists():
            self.editor.text = path.read_text(encoding="utf-8")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn-save" and self.current_dotfile:
            path = context.get_absolute_source(self.current_dotfile.source)
            try:
                path.write_text(self.editor.text, encoding="utf-8")
                self.notify("File saved!")
            except Exception as e:
                self.notify(f"Error: {e}", severity="error")
