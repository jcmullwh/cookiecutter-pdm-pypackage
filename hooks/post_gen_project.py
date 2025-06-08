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

def is_git_installed():
    """Check if Git is installed."""
    return shutil.which("git") is not None

def initialize_git_repo():
    """Initialize a new Git repository."""
    print("Initializing Git repository...")
    run_command(["git", "init"])

def create_gitignore():
    """Create a .gitignore file with common Python and PDM exclusions."""
    gitignore_content = """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environment
.env/
venv/
ENV/
env/
.venv/

# PDM specific
__pypackages__/
pdm.lock

# Distribution / packaging
build/
dist/
*.egg-info/
.eggs/

# IDEs and editors
.vscode/
.idea/
*.sublime-project
*.sublime-workspace

# OS files
.DS_Store
Thumbs.db
"""
    gitignore_path = os.path.join(os.getcwd(), ".gitignore")
    if not os.path.exists(gitignore_path):
        print("Creating .gitignore file...")
        with open(gitignore_path, "w") as f:
            f.write(gitignore_content.strip() + "\n")
    else:
        print(".gitignore already exists. Skipping creation.")

def make_initial_commit():
    """Make the initial Git commit."""
    print("Making initial Git commit...")
    run_command(["git", "add", "."])
    run_command(["git", "commit", "-m", "Initial commit"])

def run_command(command, shell=False):
    """Utility function to run a shell command."""
    print(f"Running command: {' '.join(command) if isinstance(command, list) else command}")
    subprocess.run(command, shell=shell, check=True)

def main():
    current_os = platform.system()
    print(f"Detected OS: {current_os}")

    # Ensure Git is installed
    if not is_git_installed():
        print("Git is not installed. Please install Git and re-run the script.")
        sys.exit(1)
    else:
        print("Git is already installed.")

    # Ensure PDM is installed
    if not is_pdm_installed():
        install_pdm()
    else:
        print("pdm is already installed.")

    # Install project dependencies
    run_command(["pdm", "install"])

    # Add the current project as an editable dev dependency
    run_command(["pdm", "add", "--dev", "--editable", "."])

    # Initialize Git repository
    # Check if the current directory is already a Git repository
    if not os.path.isdir(os.path.join(os.getcwd(), ".git")):
        initialize_git_repo()
        create_gitignore()
        make_initial_commit()
    else:
        print("Git repository already initialized. Skipping Git setup.")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
