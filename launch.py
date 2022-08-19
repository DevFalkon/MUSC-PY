import subprocess

DETACHED_PROCESS = 0x00000008
subprocess.call('venv\\Scripts\\pythonw.exe main.pyw', creationflags=DETACHED_PROCESS)