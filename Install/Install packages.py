import subprocess
import sys

packages = ["vosk", "pyaudio", "requests"]

for package in packages:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
