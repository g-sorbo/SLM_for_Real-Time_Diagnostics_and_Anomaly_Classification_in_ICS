import docker, requests, json, time, threading, sys, os
from datetime import datetime, timezone

OLLAMA_URL = "http://ollama:11434/api/generate"
MODELLO_SLM = "qwen2.5:3b"
FINESTRA_TEMPORALE = 15
CONTAINER_TARGET = "openplc-runtime"
FILE_PROMPT = "prompt.txt"
CARTELLA_OUTPUT = "/output"
FILE_JSONL = os.path.join(CARTELLA_OUTPUT, "analisi_plc.jsonl")

def recupero_prompt():
    try:
        with open(FILE_PROMPT, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {FILE_PROMPT} mancante.")
        sys.exit(1)

def recupero_logs(container, lock, buffer_logs):
    print("[THREAD LOGS] In ascolto su Docker...")
    while True:
        try:
            for riga in container.logs(stream=True, follow=True, tail=10, stdout=True, stderr=True):
                msg = riga.decode("utf-8", errors="replace").strip()
                if msg:
                    with lock:
                        buffer_logs.append(msg)
        except Exception as e:
            print(f"[THREAD LOGS ERRORE] Connessione persa: {e}. Prova di Riconnessione...")
            time.sleep(1)

def invio_richiesta_ollama(prompt, lock, buffer_logs):
    with lock:
        logs = list(buffer_logs)
        buffer_logs.clear()

    # Se non ci sono log durante il monitoraggio si evita di inoltrare la richiesta al modello SLM
    if not logs:
        print("Nessun log accumulato.")
        return
    # Pre-filtro: scarta le chiamate di routine 200 OK
    logs_utili = [r for r in logs if not (any(ep in r for ep in ["/api/status", "/api/runtime-logs", "/api/plugin-command"]) and " 200 " in r)]
    # Se c'è solo polling normale prendi le ultime 3 righe, altrimenti prendi i log anomali
    selezione = logs_utili[-15:] if logs_utili else logs[-3:]
    testo_logs = "\n".join(selezione)

    payload = {
        "model": MODELLO_SLM,
        "prompt": f"{prompt}\n" + testo_logs,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_ctx": 4096,
            "num_thread": 4
        }
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=90)
        res.raise_for_status()
        raw_text = res.json().get("response", "")

        with open(FILE_JSONL, "a", encoding="utf-8") as f:
            f.write(raw_text.strip() + "\n")
            f.flush()

        print(f"Analisi completata ({len(logs)} log intercettati) -> Risposta salvata.")

    except Exception as e:
        print(f"Errore chiamata Ollama: {e}")


if __name__ == "__main__":
    template_prompt = recupero_prompt()

    try:
        client = docker.from_env()
        container = client.containers.get(CONTAINER_TARGET)
        print("[PLC] Risponde: container trovato e attivo.")
    except Exception as e:
        print(f"[PLC] NON risponde: {e}")
        sys.exit(1)

    try:
        requests.get("http://ollama:11434", timeout=5)
        print("[SLM] Risponde: Ollama è pronto.")
    except Exception as e:
        print(f"[SLM] NON risponde: {e}")
        sys.exit(1)

    while True:
        comando = input("Scrivi 'start' per avviare l'orchestratore: ").strip().lower()
        if comando == "start":
            print("Avvio dell'orchestratore...")
            break

    buffer_logs = [] # Lista condivisa per accumulare i log
    lock = threading.Lock() # Lock di threading per sincronizzare l'accesso alla lista dei log
    threading.Thread(target=recupero_logs, args=(container, lock, buffer_logs), daemon=True).start()

    print(f"Monitoraggio attivo su {CONTAINER_TARGET} ogni {FINESTRA_TEMPORALE}s...")
    while True:
        time.sleep(FINESTRA_TEMPORALE)
        invio_richiesta_ollama(template_prompt, lock, buffer_logs)