import os
import time
import threading
import docker
import customtkinter as ctk

CONTAINER_PLC = "openplc-runtime"
CARTELLA_OUTPUT = os.path.join(os.path.dirname(__file__), "output")
FILE_JSONL = os.path.join(CARTELLA_OUTPUT, "analisi_plc.jsonl")

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class LiveMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PLC Security Monitor - Live Viewer")
        self.geometry("1100x650")

        self.grid_columnconfigure((0, 1), weight=1, uniform="col")
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self, text="Log Container OpenPLC", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        ctk.CTkLabel(self, text="Analisi SLM (Eventi)", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=1, padx=15, pady=(15, 5), sticky="w")

        self.txt_logs = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.txt_logs.grid(row=1, column=0, padx=(15, 10), pady=(0, 15), sticky="nsew")

        self.txt_slm = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.txt_slm.grid(row=1, column=1, padx=(10, 15), pady=(0, 15), sticky="nsew")

        # Avvio dei thread di lettura
        threading.Thread(target=self.worker_logs_docker, daemon=True).start()
        threading.Thread(target=self.worker_file_output, daemon=True).start()

    def accoda_testo(self, widget, testo):
        self.after(0, lambda: (widget.insert("end", testo), widget.see("end")))

    def worker_logs_docker(self):
        while True:
            try:
                client = docker.from_env()
                container = client.containers.get(CONTAINER_PLC)
                for riga in container.logs(stream=True, follow=True, tail=0):
                    msg = riga.decode("utf-8", errors="replace").strip()
                    self.accoda_testo(self.txt_logs, msg + "\n")
            except Exception as e:
                self.accoda_testo(self.txt_logs, f"[ERRORE DOCKER] {e}\n")
                time.sleep(3)

    def worker_file_output(self):
        os.makedirs(CARTELLA_OUTPUT, exist_ok=True)
        if not os.path.exists(FILE_JSONL):
            open(FILE_JSONL, "a", encoding="utf-8").close()

        # Si posiziona subito alla fine: ignora il passato e cattura solo il futuro
        with open(FILE_JSONL, "r", encoding="utf-8") as f:
            f.seek(0, os.SEEK_END)
            while True:
                riga = f.readline()
                if not riga:
                    time.sleep(0.5)
                    continue

                # Scrive la nuova riga direttamente a schermo
                self.accoda_testo(self.txt_slm, riga)
    
if __name__ == "__main__":
    app = LiveMonitorApp()
    app.mainloop()