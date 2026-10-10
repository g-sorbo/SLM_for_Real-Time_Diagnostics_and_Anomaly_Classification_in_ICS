# SLM Industrial Fault Detection

Progetto di tesi per valutare l'efficacia dei **Small Language Models (SLM)** nel rilevamento guasti nei sistemi di controllo industriale.

## Caratteristiche
* **Testbed:** Monitoraggio log di `OpenPLC` via `Docker`.
* **Iniezione Guasti:** Script Python per simulare guasti e stress di sistema.
* **Pipeline IA:** Interrogazione di `Qwen2.5:3b` (tramite Ollama) per il rilevamento anomalie con output in `JSONL`.

## Video Dimostrativo

[![Anteprima Demo](./anteprima.gif)](.video_dimostrativo.mp4)
