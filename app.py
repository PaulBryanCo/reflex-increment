import os
import sys
import psutil
from subprocess import Popen, PIPE

# Determine the base directory (PyInstaller temp directory or script directory)
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

print("Base Directory:", base_dir)

# Path to the virtual environment folder
venv_dir = os.path.join(base_dir, ".venv")

# Check if .venv exists and is valid
def is_venv_valid(venv_path):
    activate_script = os.path.join(venv_path, "Scripts", "activate")
    return os.path.exists(activate_script)

if not os.path.exists(venv_dir) or not is_venv_valid(venv_dir):
    print("Virtual environment not found or invalid. Creating .venv...")
    try:
        # Create the virtual environment
        create_venv_command = f"python -m venv {venv_dir}"
        create_venv_process = Popen(create_venv_command, cwd=base_dir, shell=True)
        create_venv_process.communicate()
        if create_venv_process.returncode == 0:
            print(".venv created successfully.")
        else:
            print("Error creating .venv.")
            sys.exit(1)
    except Exception as e:
        print(f"Exception while creating .venv: {e}")
        sys.exit(1)
else:
    print(".venv already exists and is valid. Skipping creation.")

# Ensure .venv activation script exists
venv_activate = os.path.join(venv_dir, "Scripts", "activate")
if not os.path.exists(venv_activate):
    print(f"Activation script not found in {venv_activate}. Exiting.")
    sys.exit(1)

# Install dependencies from requirements.txt
requirements_file = os.path.join(base_dir, "requirements.txt")
if os.path.exists(requirements_file):
    print("Installing dependencies from requirements.txt...")
    try:
        install_command = f'pip install -r {requirements_file}'
        process = Popen(f'cmd /c "{venv_activate} & {install_command}"', shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            print("Dependencies installed successfully.")
            print(stdout.decode().strip())
        else:
            print(f"Error installing dependencies:\n{stderr.decode().strip()}")
            sys.exit(1)
    except Exception as e:
        print(f"Exception while installing dependencies: {e}")
        sys.exit(1)
else:
    print("requirements.txt not found. Skipping dependency installation.")

# Run the Reflex command
reflex_command = f'cmd /c "{venv_activate} & reflex run"'
print("Running Reflex with the following command:")
print(reflex_command)

# Launch Reflex
try:
    process = Popen(reflex_command, cwd=base_dir, shell=True)
    
    # Keep the process alive for demonstration (or replace with your logic)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Cleaning up processes...")
    finally:
        # Terminate all child processes
        print("Terminating child processes...")
        for child in psutil.Process(process.pid).children(recursive=True):
            child.terminate()
        process.terminate()  # Terminate the parent process
        print("Processes terminated.")
except Exception as e:
    print(f"Error running Reflex: {e}")
    # Clean up child processes in case of failure
    for child in psutil.Process(process.pid).children(recursive=True):
        child.terminate()
    process.terminate()
    sys.exit(1)
