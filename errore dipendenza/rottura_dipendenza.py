import subprocess

CONTAINER = "openplc-runtime"
TARGET_DEP = "/workdir/build/plugins/libs7comm_plugin.so"

print("=== [INIEZIONE GUASTO] Rottura dipendenza in corso ===")

# Rinomina il file della libreria nativa per renderlo indisponibile
result = subprocess.run(
    f"docker exec -u 0 {CONTAINER} sh -c 'if [ -f {TARGET_DEP} ]; then mv {TARGET_DEP} {TARGET_DEP}.broken; echo \"[OK] Libreria {TARGET_DEP} corrotta/rinominata.\"; else echo \"[ERRORE] File non trovato o già compromesso.\"; fi'",
    shell=True,
    capture_output=True,
    text=True
)

print(result.stdout.strip())
print("=== [FATTO] Guasto applicato. Il sistema reagirà al prossimo avvio o transizione. ===")