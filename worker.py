import subprocess, os, time

process = subprocess.Popen("python3 main.py", shell=True)

while True:
    if os.popen("git pull").read() != 'Déjà à jour.\n':
        process.kill()
        process = subprocess.Popen("python3 main.py", shell=True)
        
    time.sleep(7)