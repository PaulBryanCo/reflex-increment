import os
import sys
from subprocess import Popen, call

# Determine the base directory (PyInstaller temp directory or script directory)
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

print("Base Directory:", base_dir)

# Path to the virtual environment folder
venv_dir = os.path.join(base_dir, ".venv")

# Check if .venv exists
if not os.path.exists(venv_dir):
    print("Virtual environment not found. Creating .venv...")
    call([sys.executable, "-m", "venv", venv_dir])
    print(".venv created successfully.")
else:
    print(".venv already exists. Skipping creation.")

# Path to the virtual environment activation script
venv_activate = os.path.join(venv_dir, "Scripts", "activate")

# Install dependencies from requirements.txt
requirements_file = os.path.join(base_dir, "requirements.txt")
if os.path.exists(requirements_file):
    print("Installing dependencies from requirements.txt...")
    install_command = f'cmd /c "{venv_activate} & pip install -r {requirements_file}"'
    call(install_command, shell=True)
    print("Dependencies installed successfully.")
else:
    print("requirements.txt not found. Skipping dependency installation.")

# Run the Reflex command
reflex_command = f'cmd /c "{venv_activate} & reflex run"'
print("Running Reflex with the following command:")
print(reflex_command)

# Launch Reflex
process = Popen(reflex_command, cwd=base_dir, shell=True)
process.communicate()
