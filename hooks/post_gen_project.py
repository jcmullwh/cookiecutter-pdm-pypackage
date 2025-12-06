import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path.cwd()

INSTALL_PDM = "{{ cookiecutter.install_pdm }}" == "Y"
INSTALL_DEPS = "{{ cookiecutter.install_dependencies }}" == "Y"
INIT_GIT = "{{ cookiecutter.init_git }}" == "Y"
INITIAL_COMMIT = "{{ cookiecutter.initial_commit }}" == "Y"
MKDOCS_ENABLED = "{{ cookiecutter.mkdocs }}" == "Y"
CODECOV_ENABLED = "{{ cookiecutter.codecov }}" == "Y"


def run(command: list[str]) -> None:
    print(f"Running command: {' '.join(command)}")
    subprocess.run(command, check=True)


def safe(label: str, func) -> None:
    try:
        func()
    except subprocess.CalledProcessError as exc:
        print(f"{label} failed: {exc}. Continuing without stopping project generation.")


def remove_path(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
        print(f"Removed directory {path}")
    elif path.exists():
        path.unlink()
        print(f"Removed file {path}")


def cleanup_features() -> None:
    if not MKDOCS_ENABLED:
        for path in [
            PROJECT_ROOT / "mkdocs.yml",
            PROJECT_ROOT / "docs",
            PROJECT_ROOT / ".github" / "workflows" / "documentation.yml",
        ]:
            remove_path(path)
    if not CODECOV_ENABLED:
        remove_path(PROJECT_ROOT / "codecov.yaml")


def ensure_pdm() -> bool:
    if shutil.which("pdm"):
        print("pdm is already installed.")
        return True
    if not INSTALL_PDM:
        print("pdm is not installed and install_pdm is disabled; skipping.")
        return False
    print("Installing pdm with --user...")
    run([sys.executable, "-m", "pip", "install", "--user", "pdm"])
    return True


def install_dependencies() -> None:
    if not INSTALL_DEPS:
        print("Dependency installation skipped (install_dependencies=N).")
        return
    if not shutil.which("pdm"):
        if not ensure_pdm():
            print("Could not install dependencies because pdm is unavailable.")
            return
    run(["pdm", "install"])


def init_git_repo() -> None:
    if not INIT_GIT:
        print("Git initialization skipped (init_git=N).")
        return
    if not shutil.which("git"):
        print("Git is not installed; skipping git setup.")
        return
    if (PROJECT_ROOT / ".git").is_dir():
        print("Repository already initialized; skipping git init.")
    else:
        run(["git", "init"])
    if INITIAL_COMMIT:
        run(["git", "add", "."])
        run(["git", "commit", "-m", "Initial commit"])


def main() -> None:
    cleanup_features()
    if INSTALL_PDM:
        safe("PDM installation", ensure_pdm)
    safe("Dependency installation", install_dependencies)
    if INITIAL_COMMIT and not INIT_GIT:
        print("Initial commit requested but init_git is disabled; skipping commit.")
    safe("Git initialization", init_git_repo)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print(f"An error occurred: {exc}")
        sys.exit(exc.returncode)
