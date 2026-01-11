from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, TabbedContent, TabPane

from uvtui.widgets.status_bar import StatusBar
from uvtui.widgets.uv_checker import UVChecker
from uvtui.screens.install_screen import InstallScreen
from uvtui.screens.python_screen import PythonScreen
from uvtui.screens.help_screen import HelpScreen


class UVTUIApp(App):
    CSS = """
        Screen {
            background: $surface;
        }
        
        TabbedContent {
            margin: 1 0;
        }
        
        TabPane {
            padding: 0;
        }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("ctrl+q", "quit", "Quit", show=False),
        Binding("h", "show_help", "Help"),
        Binding("ctrl+c", "cancel", "Cancel", show=False),
        Binding("d", "toggle_dark", "Toggle Dark Mode"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield UVChecker()

        with TabbedContent():
            with TabPane("Installation", id="tab_install"):
                yield InstallScreen()

            with TabPane("Python Versions", id="tab_python"):
                yield PythonScreen()

            with TabPane("Help", id="tab_help"):
                yield HelpScreen()

        yield StatusBar()
        yield Footer()

    async def on_mount(self) -> None:
        """Called when app is mounted"""
        self.title = "uvtui - UV Package Manager TUI"
        status_bar = self.query_one(StatusBar)
        status_bar.set_status("Ready - Press 'h' for help")

    def action_show_help(self) -> None:
        tabbed_content = self.query_one(TabbedContent)
        tabbed_content.active = "tab_help"

    def action_cancel(self) -> None:
        status_bar = self.query_one(StatusBar)
        status_bar.set_status("Operation cancelled")

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
