import os
import sys
import subprocess
import platform
import shutil

def is_pdm_installed():
    """Check if pdm is installed."""
    return shutil.which("pdm") is not None

def install_pdm():
    """Install pdm using pip."""
    print("Installing pdm...")
    run_command([sys.executable, "-m", "pip", "install", "pdm"])

def run_command(command, shell=False):
    """Utility function to run a shell command."""
    print(f"Running command: {' '.join(command) if isinstance(command, list) else command}")
    subprocess.run(command, shell=shell, check=True)

def main():
    current_os = platform.system()
    print(f"Detected OS: {current_os}")

    if not is_pdm_installed():
        install_pdm()
    else:
        print("pdm is already installed.")

    # Install project dependencies
    run_command(["pdm", "install"])

    # Add the current project as an editable dev dependency
    run_command(["pdm", "add", "--dev", "--editable", "."])

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
