import os
import sys
import subprocess

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(BACKEND_DIR, '.venv')
REQUIREMENTS = os.path.join(BACKEND_DIR, 'requirements.txt')
APP = os.path.join(BACKEND_DIR, 'app.py')

def get_python():
    if sys.platform == 'win32':
        return os.path.join(VENV_DIR, 'Scripts', 'python.exe')
    return os.path.join(VENV_DIR, 'bin', 'python')

def main():
    if not os.path.exists(VENV_DIR):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', VENV_DIR], check=True)

    python = get_python()
    print("Installing dependencies...")
    subprocess.run([python, '-m', 'pip', 'install', '-r', REQUIREMENTS], check=True)

    os.chdir(BACKEND_DIR)
    subprocess.run([python, APP])

if __name__ == '__main__':
    main()
