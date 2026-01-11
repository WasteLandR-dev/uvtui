from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Button, Static, DataTable, Input, Label
from textual import on

from uvtui.utils.uv_commands import (
    list_python_versions,
    list_installed_python,
    install_python,
    uninstall_python,
    find_python,
    pin_python,
)
from uvtui.widgets.status_bar import StatusBar


class PythonScreen(Container):
    DEFAULT_CSS = """
    PythonScreen {
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
    
    Horizontal {
        height: auto;
        align: center middle;
        margin: 1 0;
    }
    
    Button {
        margin: 0 1;
    }
    
    Input {
        margin: 0 1;
        width: 30;
    }
    
    DataTable {
        height: 12;
        margin: 1 0;
    }
    
    #python_output {
        margin-top: 1;
        height: auto;
        color: $text-muted;
        min-height: 3;
    }
    
    .section-label {
        margin: 1 0;
        text-style: bold;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("Python Version Management", classes="panel-title")

        yield Horizontal(
            Button("List Available", id="list_python", variant="primary"),
            Button("Refresh Installed", id="refresh_installed", variant="success"),
        )

        yield Label("Installed Python Versions:", classes="section-label")
        yield DataTable(id="python_versions_table")

        yield Label("Version Operations:", classes="section-label")
        yield Horizontal(
            Input(placeholder="Version (e.g., 3.12)", id="python_version_input"),
            Button("Install", id="install_python", variant="success"),
            Button("Uninstall", id="uninstall_python", variant="error"),
        )

        yield Horizontal(
            Button("Find Installed", id="find_python"),
            Button("Pin Version", id="pin_python"),
        )

        yield Static("", id="python_output")

    async def on_mount(self) -> None:
        table = self.query_one("#python_versions_table", DataTable)
        table.add_columns("Version", "Status")
        table.cursor_type = "row"
        await self.refresh_installed_versions()

    @on(Button.Pressed, "#list_python")
    async def list_available_python(self) -> None:
        output = self.query_one("#python_output", Static)
        status_bar = self.app.query_one(StatusBar)

        output.update("Fetching available Python versions...")
        status_bar.set_status("Fetching Python versions...")

        success, result = list_python_versions()

        if success:
            output.update(f"Available versions:\n{result}")
            status_bar.set_status("Python versions listed")
        else:
            output.update(f"✗ Error: {result}")
            status_bar.set_status("Failed to list versions")

    @on(Button.Pressed, "#refresh_installed")
    async def refresh_installed_versions(self) -> None:
        table = self.query_one("#python_versions_table", DataTable)
        output = self.query_one("#python_output", Static)
        status_bar = self.app.query_one(StatusBar)

        table.clear()
        output.update("Refreshing installed versions...")
        status_bar.set_status("Refreshing...")

        success, result = list_installed_python()

        if success:
            lines = result.strip().split("\n")
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 1:
                        version = parts[0]
                        status = "Installed"
                        table.add_row(version, status)

            output.update(f"Found {table.row_count} installed version(s)")
            status_bar.set_status(f"{table.row_count} Python version(s) installed")
        else:
            output.update(f"✗ Error: {result}")
            status_bar.set_status("Failed to refresh")

    @on(Button.Pressed, "#install_python")
    async def install_python_version(self) -> None:
        version_input = self.query_one("#python_version_input", Input)
        output = self.query_one("#python_output", Static)
        status_bar = self.app.query_one(StatusBar)

        version = version_input.value.strip()
        if not version:
            output.update("⚠ Please enter a version number")
            return

        output.update(f"Installing Python {version}... This may take several minutes.")
        status_bar.set_status(f"Installing Python {version}...")

        success, message = install_python(version)

        if success:
            output.update(f"✓ {message}")
            status_bar.set_status(f"Python {version} installed")
            await self.refresh_installed_versions()
        else:
            output.update(f"✗ {message}")
            status_bar.set_status("Installation failed")

    @on(Button.Pressed, "#uninstall_python")
    async def uninstall_python_version(self) -> None:
        version_input = self.query_one("#python_version_input", Input)
        output = self.query_one("#python_output", Static)
        status_bar = self.app.query_one(StatusBar)

        version = version_input.value.strip()
        if not version:
            output.update("⚠ Please enter a version number")
            return

        output.update(f"Uninstalling Python {version}...")
        status_bar.set_status(f"Uninstalling Python {version}...")

        success, message = uninstall_python(version)

        if success:
            output.update(f"✓ {message}")
            status_bar.set_status(f"Python {version} uninstalled")
            await self.refresh_installed_versions()
        else:
            output.update(f"✗ {message}")
            status_bar.set_status("Uninstallation failed")

    @on(Button.Pressed, "#find_python")
    async def find_python_handler(self) -> None:
        version_input = self.query_one("#python_version_input", Input)
        output = self.query_one("#python_output", Static)
        status_bar = self.app.query_one(StatusBar)

        version = version_input.value.strip() if version_input.value else None
        status_bar.set_status("Finding Python...")

        success, result = find_python(version)

        if success:
            output.update(f"Found:\n{result}")
            status_bar.set_status("Python found")
        else:
            output.update(f"✗ Error: {result}")
            status_bar.set_status("Python not found")

    @on(Button.Pressed, "#pin_python")
    async def pin_python_version(self) -> None:
        version_input = self.query_one("#python_version_input", Input)
        output = self.query_one("#python_output", Static)
        status_bar = self.app.query_one(StatusBar)

        version = version_input.value.strip()
        if not version:
            output.update("⚠ Please enter a version number")
            return

        status_bar.set_status(f"Pinning Python {version}...")
        success, message = pin_python(version)

        if success:
            output.update(f"✓ {message}")
            status_bar.set_status(f"Python {version} pinned")
        else:
            output.update(f"✗ {message}")
            status_bar.set_status("Failed to pin version")
