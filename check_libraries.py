import importlib.util
import subprocess
import sys

def install(package):
    """Install the specified package using pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install_libraries():
    """Check if the libraries are installed, and install them if they are not."""
    libraries = [
        'pyfirmata', 
        'pyaudio',
        'vosk',
        'pyttsx3'
    ]
    for library in libraries:
        if importlib.util.find_spec(library) is None:
            print(f"{library} not found. Installing...")
            install(library)
        else:
            print(f"{library} is already installed.")


check_and_install_libraries()

print("All required libraries are installed. Starting the application...")