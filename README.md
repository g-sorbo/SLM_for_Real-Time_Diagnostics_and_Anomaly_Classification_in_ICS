# SLM for Industrial Diagnostics

A bachelor's thesis project evaluating the effectiveness of **Small Language Models (SLMs)** for automated fault detection and diagnostics in industrial control systems.

## Key Features
* **Industrial Testbed:** Real-time log monitoring of a containerized `OpenPLC` runtime (`Docker`).
* **Automated Fault Injection:** Python scripts simulating structural failures (corrupted shared plugin libraries) and resource stress (CPU/memory constraints via cgroups).
* **Local AI Pipeline:** Captures container logs and queries a local SLM (`Qwen2.5:3b` via Ollama) for zero-shot anomaly detection, exporting structured diagnostics in `JSONL` format.
