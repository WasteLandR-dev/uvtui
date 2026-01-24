from textual.widgets import Static
from uvtui.utils.uv_commands import check_uv_installed


class UVChecker(Static):

    def __init__(self) -> None:
        super().__init__()
        self.uv_installed = False
        self.uv_version = None

    async def on_mount(self) -> None:
        await self.check_uv_installation()

    async def check_uv_installation(self) -> None:
        self.uv_installed, self.uv_version = check_uv_installed()
        self.refresh()

    def render(self) -> str:
        if self.uv_installed:
            return f"✓ UV Installed: {self.uv_version}"
        return "✗ UV not found - Please install UV to continue"
