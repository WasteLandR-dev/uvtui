import subprocess
from typing import Optional, Tuple


class UVCommandError(Exception):
    pass


def check_uv_installed() -> Tuple[bool, Optional[str]]:
    try:
        result = subprocess.run(
            ["uv", "--version"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, None
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False, None


def install_uv(system: str) -> Tuple[bool, str]:
    try:
        if system == "Windows":
            cmd = [
                "powershell",
                "-Command",
                "irm https://astral.sh/uv/install.ps1 | iex",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        else:
            result = subprocess.run(
                "curl -LsSf https://astral.sh/uv/install.sh | sh",
                shell=True,
                capture_output=True,
                text=True,
                timeout=120,
            )

        if result.returncode == 0:
            return True, "UV installed successfully! Please restart your terminal."
        return False, f"Installation failed: {result.stderr}"
    except subprocess.TimeoutExpired:
        return False, "Installation timed out"
    except Exception as e:
        return False, f"Error: {str(e)}"


def list_python_versions() -> Tuple[bool, str]:
    try:
        result = subprocess.run(
            ["uv", "python", "list"], capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return True, result.stdout
        return False, result.stderr
    except Exception as e:
        return False, str(e)


def list_installed_python() -> Tuple[bool, str]:
    try:
        result = subprocess.run(
            ["uv", "python", "list", "--only-installed"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return True, result.stdout
        return False, result.stderr
    except Exception as e:
        return False, str(e)


def install_python(version: str) -> Tuple[bool, str]:
    try:
        result = subprocess.run(
            ["uv", "python", "install", version],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode == 0:
            return True, f"Python {version} installed successfully"
        return False, result.stderr
    except subprocess.TimeoutExpired:
        return False, "Installation timed out"
    except Exception as e:
        return False, str(e)


def uninstall_python(version: str) -> Tuple[bool, str]:
    try:
        result = subprocess.run(
            ["uv", "python", "uninstall", version],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode == 0:
            return True, f"Python {version} uninstalled successfully"
        return False, result.stderr
    except Exception as e:
        return False, str(e)


def find_python(version: Optional[str] = None) -> Tuple[bool, str]:
    try:
        cmd = ["uv", "python", "find"]
        if version:
            cmd.append(version)

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return True, result.stdout
        return False, result.stderr
    except Exception as e:
        return False, str(e)


def pin_python(version: str) -> Tuple[bool, str]:
    try:
        result = subprocess.run(
            ["uv", "python", "pin", version], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return True, f"Pinned Python {version} for this project"
        return False, result.stderr
    except Exception as e:
        return False, str(e)
