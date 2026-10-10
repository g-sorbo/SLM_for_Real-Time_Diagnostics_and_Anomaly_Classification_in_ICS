# SLM Industrial Fault Detection

Progetto di tesi per valutare l'efficacia dei **Small Language Models (SLM)** nel rilevamento guasti nei sistemi di controllo industriale.

## Caratteristiche
* **Testbed:** Monitoraggio log di `OpenPLC` via `Docker`.
* **Iniezione Guasti:** Script Python per simulare guasti e stress di sistema.
* **Pipeline IA:** Interrogazione di `Qwen2.5:3b` (tramite Ollama) per il rilevamento anomalie e salvataggio riposte in file `JSONL`.

## Prerequisiti
Prima di avviare il progetto, assicurati di avere installato:
* **Docker** e Docker Compose (per il testbed OpenPLC).
* **Ollama** con il modello `Qwen2.5:3b` attivo in locale (`ollama run qwen2.5:3b`).

## Configurazione
1. Importa il programma PLC: Carica la cartella PLC del nostro prototipo in OpenPLC.
2. Configura Task e Instances: Aggiungi un task ciclico (ad esempio Task0 con intervallo T#20ms) e crea la relativa istanza (instance0) associata al programma main, come illustrato nell'immagine sottostante.
<img width="1162" height="390" alt="image" src="https://github.com/user-attachments/assets/2a3c402e-087a-453e-baf8-4cdfd4ab80aa" />

3. L'ambiente si configura in modo automatico compilando il docker compose, eseguendo da terminale il seguente comando:
```
docker compose up -d --build
```
4. Esegui attachment all'orchestratore: Lancia il seguente comando per inviare comandi e visualizzare le stampe a video:
```
docker attach orchestrator
```
5. (Opzionale) Avvia la dashboard per visualizzare logs e risposte dello SLM.

## Video Dimostrativo del Funzionamento
[![Anteprima Demo](./anteprima.gif)](.video_dimostrativo.mp4)
