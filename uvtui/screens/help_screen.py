from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Static, Markdown


class HelpScreen(Container):
    DEFAULT_CSS = """
    HelpScreen {
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
    
    VerticalScroll {
        height: 100%;
        margin: 1 0;
    }
    """

    HELP_TEXT = """
# uvtui - UV Package Manager TUI

## Keyboard Shortcuts

### Navigation
- `Tab` / `Shift+Tab` - Navigate between elements
- `Arrow Keys` - Move between items in lists/tables
- `Enter` - Activate button or selection
- `Esc` - Cancel or go back

### Global Shortcuts
- `q` / `Ctrl+Q` - Quit application
- `Ctrl+C` - Cancel current operation
- `h` - Show this help screen

## UV Python Commands

### List Versions
```bash
uv python list                 # List all available Python versions
uv python list --only-installed # List only installed versions
```

### Install & Uninstall
```bash
uv python install <version>    # Install a Python version
uv python uninstall <version>  # Uninstall a Python version
```

### Find & Pin
```bash
uv python find [version]       # Find installed Python
uv python pin <version>        # Pin Python version for project
```

## Version Format Examples
- `3.12` - Latest 3.12.x version
- `3.11.5` - Specific version
- `3.10` - Latest 3.10.x version

## Tips
- Ensure UV is installed before managing Python versions
- Pinning creates/updates `.python-version` file in current directory
- Use `Refresh Installed` to update the version table
- Installation may take several minutes depending on version

## About UV
UV is an extremely fast Python package installer and resolver, written in Rust.
It's designed as a drop-in replacement for pip and pip-tools workflows.

For more information, visit: https://github.com/astral-sh/uv
    """

    def compose(self) -> ComposeResult:
        yield Static("Help & Documentation", classes="panel-title")
        with VerticalScroll():
            yield Markdown(self.HELP_TEXT)
