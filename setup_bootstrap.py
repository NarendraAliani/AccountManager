from __future__ import annotations

import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv"
VENV_PYTHON = VENV_DIR / "Scripts" / "python.exe"
SETUP_DONE = ROOT / "setup.done"
SERVER_URL = "http://127.0.0.1:8000/login/"
SERVER_LOG = ROOT / "server.log"
SERVER_ERR = ROOT / "server.err.log"


def log(message: str) -> None:
    print(message, flush=True)


def run_command(command: list[str], env: dict[str, str] | None = None) -> None:
    log(f"> {' '.join(command)}")
    subprocess.run(command, cwd=ROOT, env=env, check=True)


def get_base_python() -> str:
    base_python = Path(sys.executable)
    if base_python.exists():
        return str(base_python)
    raise RuntimeError("Could not locate Python on this PC.")


def ensure_venv() -> None:
    if VENV_PYTHON.exists():
        log("Virtual environment already exists.")
        return

    log("Creating virtual environment...")
    run_command([get_base_python(), "-m", "venv", str(VENV_DIR)])


def ensure_dependencies() -> None:
    log("Installing project dependencies...")
    run_command([str(VENV_PYTHON), "-m", "pip", "install", "--upgrade", "pip"])
    run_command([str(VENV_PYTHON), "-m", "pip", "install", "-r", "requirements.txt"])


def ensure_migrations() -> None:
    log("Applying database migrations...")
    env = os.environ.copy()
    env.setdefault("DJANGO_SETTINGS_MODULE", "AccountManager.settings")
    run_command([str(VENV_PYTHON), "manage.py", "migrate", "--noinput"], env=env)


def ensure_admin_user() -> None:
    log("Creating or updating the default admin user...")
    env = os.environ.copy()
    env.setdefault("DJANGO_SETTINGS_MODULE", "AccountManager.settings")
    code = r"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AccountManager.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
user, _created = User.objects.get_or_create(username="admin")
user.is_staff = True
user.is_superuser = True
user.is_active = True
user.set_password("admin1234")
user.save()
print("Default admin user ready.")
"""
    run_command([str(VENV_PYTHON), "-c", code], env=env)


def setup_is_done() -> bool:
    return SETUP_DONE.exists() and VENV_PYTHON.exists()


def mark_setup_done() -> None:
    SETUP_DONE.write_text(
        f"setup_completed_at={datetime.now().isoformat(timespec='seconds')}\n",
        encoding="utf-8",
    )


def server_is_running() -> bool:
    try:
        with urllib.request.urlopen(SERVER_URL, timeout=1) as response:
            return response.status in {200, 301, 302, 303, 307, 308}
    except urllib.error.URLError:
        return False
    except Exception:
        return False


def start_server() -> subprocess.Popen[str]:
    env = os.environ.copy()
    env.setdefault("DJANGO_SETTINGS_MODULE", "AccountManager.settings")
    stdout = SERVER_LOG.open("a", encoding="utf-8")
    stderr = SERVER_ERR.open("a", encoding="utf-8")
    log("Starting the local Django server...")
    return subprocess.Popen(
        [str(VENV_PYTHON), "manage.py", "runserver", "0.0.0.0:8000", "--noreload"],
        cwd=ROOT,
        env=env,
        stdout=stdout,
        stderr=stderr,
    )


def wait_for_server(proc: subprocess.Popen[str], timeout_seconds: int = 60) -> bool:
    for _ in range(timeout_seconds):
        if proc.poll() is not None:
            return False
        if server_is_running():
            return True
        time.sleep(1)
    return False


def main() -> int:
    try:
        log("AccountManager setup launcher")
        log(f"Project folder: {ROOT}")

        if not setup_is_done():
            ensure_venv()
            ensure_dependencies()
            ensure_migrations()
            ensure_admin_user()
            mark_setup_done()
            log("Setup completed.")
        else:
            log("Setup already completed. Starting the app.")

        if server_is_running():
            log("The app is already running.")
            webbrowser.open(SERVER_URL)
            return 0

        proc = start_server()
        if wait_for_server(proc):
            log("Server is ready.")
            webbrowser.open(SERVER_URL)
            return 0

        log("The server did not become ready.")
        log(f"Check {SERVER_ERR.name} for errors.")
        return 1
    except subprocess.CalledProcessError as exc:
        log("A setup command failed.")
        log(f"Check {SERVER_ERR.name} and {SERVER_LOG.name} for details.")
        log(f"Exit code: {exc.returncode}")
        return exc.returncode or 1
    except Exception as exc:
        log(f"Unexpected error: {exc}")
        log(f"Check {SERVER_ERR.name} and {SERVER_LOG.name} for details.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
