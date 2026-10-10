import subprocess

CONTAINER = "openplc-runtime"

def run(cmd):
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("=== [INIEZIONE] Riduzione risorse in corso ===")

# Applica limiti severi di CPU e RAM
run(f'docker update --cpus="0.1" --memory-swap="512m" --memory="128m" {CONTAINER}')

print("[FATTO] Risorse del container limitate (CPU: 0.1, RAM: 128m).")
