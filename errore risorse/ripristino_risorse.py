import subprocess

CONTAINER = "openplc-runtime"

def run(cmd):
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("=== [RIPRISTINO] Rimozione limiti risorse ===")

# Rimuove i limiti di CPU e RAM impostandoli a zero (illimitati/default)
run(f'docker update --cpus=0 --memory=0 {CONTAINER}')

print("[FATTO] Risorse del container riportate allo stato nominale.")