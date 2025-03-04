import subprocess
import tkinter as tk


class NSATOutputPanel(tk.LabelFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text_area = tk.Text(self, height=15, width=60)

        # Vertical Scrollbar
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.text_area.yview)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0,5))
        self.text_area.pack(side="right", padx=5)
        self.text_area.config(yscrollcommand=scrollbar.set)

    def display_logs(self):
        self.text_area.delete("1.0", "end")
        text = subprocess.check_output(["cat", "/home/nsat/scanner/log/log.txt"], ).decode()
        self.text_area.insert("end", text)
