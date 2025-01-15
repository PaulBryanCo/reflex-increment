import os
import sys
from subprocess import Popen

# Determine the base directory (PyInstaller temp directory or script directory)
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

print("Base Directory:", base_dir)

# Virtual environment activation script
venv_activate = os.path.join(base_dir, ".venv", "Scripts", "activate")

# Run the Reflex command
reflex_command = f'cmd /c "{venv_activate} & reflex run"'
print("Running Reflex with the following command:")
print(reflex_command)

# Launch Reflex
process = Popen(reflex_command, cwd=base_dir, shell=True)
process.communicate()
