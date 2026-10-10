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
<img width="1178" height="397" alt="image" src="https://github.com/user-attachments/assets/4d86af23-c175-4f4b-8f3d-917adfc1be16" />

L'ambiente si configura in modo automatico compilando il docker compose, eseguendo da terminale il seguente comando:
```
docker compose up -d --build
```


## Video Dimostrativo del Funzionamento
[![Anteprima Demo](./anteprima.gif)](.video_dimostrativo.mp4)
