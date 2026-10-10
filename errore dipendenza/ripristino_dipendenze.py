import subprocess

CONTAINER = "openplc-runtime"
TARGET_DEP = "/workdir/build/plugins/libs7comm_plugin.so"

print("=== [RIPRISTINO SISTEMA] In corso ===")

# 1. Assicura che il container sia acceso (necessario se era crashato)
subprocess.run(f"docker start {CONTAINER}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 2. Ripristina il file rinominandolo correttamente
result = subprocess.run(
    f"docker exec -u 0 {CONTAINER} sh -c 'if [ -f {TARGET_DEP}.broken ]; then mv {TARGET_DEP}.broken {TARGET_DEP}; echo \"[OK] Libreria ripristinata.\"; else echo \"[AVVISO] Nessun file .broken trovato.\"; fi'",
    shell=True,
    capture_output=True,
    text=True
)
print(result.stdout.strip())

# 3. Riavvia il container per ripulire lo stato di errore
subprocess.run(f"docker restart {CONTAINER}", shell=True, stdout=subprocess.DEVNULL)

print("=== [FATTO] Sistema ripristinato e container riavviato. ===")