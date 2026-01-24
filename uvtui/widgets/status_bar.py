from textual.widgets import Static


class StatusBar(Static):

    def __init__(self) -> None:
        super().__init__()
        self.status = "Ready"

    def set_status(self, status: str) -> None:
        self.status = status
        self.update(f"Status: {self.status}")

    def render(self) -> str:
        return f"Status: {self.status}"
