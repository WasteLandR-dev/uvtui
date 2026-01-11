import platform
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, Static
from textual import on

from uvtui.utils.uv_commands import install_uv
from uvtui.widgets.uv_checker import UVChecker
from uvtui.widgets.status_bar import StatusBar


class InstallScreen(Container):
    DEFAULT_CSS = """
    InstallScreen {
        border: solid $primary;
        margin: 1;
        padding: 1;
    }
    
    .panel-title {
        background: $primary;
        color: $text;
        padding: 1;
        text-align: center;
        text-style: bold;
    }
    
    .info-text {
        margin: 1 0;
    }
    
    #install_output {
        margin-top: 1;
        height: auto;
        color: $text-muted;
        min-height: 3;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("UV Installation", classes="panel-title")
        yield Static(
            f"Operating System: {platform.system()} ({platform.machine()})",
            classes="info-text",
        )
        yield Static(
            "UV is a fast Python package installer and resolver.", classes="info-text"
        )
        yield Button("Install UV", id="install_uv", variant="primary")
        yield Static("", id="install_output")

    @on(Button.Pressed, "#install_uv")
    async def install_uv_handler(self) -> None:
        output_widget = self.query_one("#install_output", Static)
        status_bar = self.app.query_one(StatusBar)

        output_widget.update("Installing UV... This may take a few minutes.")
        status_bar.set_status("Installing UV...")

        system = platform.system()
        success, message = install_uv(system)

        if success:
            output_widget.update(f"✓ {message}")
            status_bar.set_status("UV installed successfully")
            # Refresh UV checker
            uv_checker = self.app.query_one(UVChecker)
            await uv_checker.check_uv_installation()
        else:
            output_widget.update(f"✗ {message}")
            status_bar.set_status("Installation failed")
