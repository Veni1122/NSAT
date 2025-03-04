import subprocess
import tkinter as tk
from tkinter import ttk

from frames.menu_bar import MenuBar
from frames.network_settings_panel import NetworkSettings
from frames.nsat_output_panel import NSATOutputPanel
from frames.nsat_status_panel import NSATStatutPanel
from frames.scan_panel import ScanPanel


class MainFrame(tk.Tk):

    def __init__(self, local_dev_mode: bool = False):
        super().__init__()

        self.menu_bar = None

        self.title("NSAT Frontend")
        self.tk.call('tk', 'scaling', 1.25)
        self.attributes('-fullscreen', False)
        self.geometry("800x480")

        if local_dev_mode:
            self.resizable(False, False)

        # Styles
        frame_bg_color = "#e0e0e0"
        highlight_color = "#0078d7"
        style = ttk.Style()
        style.configure("TFrame", background=frame_bg_color)
        style.configure("TButton", font=("Arial", 12))
        style.map("TButton",
                  foreground=[('pressed', 'red'), ('active', highlight_color)],
                  background=[('pressed', '!disabled', highlight_color),
                              ('active', highlight_color)])

        #################################
        #       Half top frame          #
        #################################

        top_frame = tk.Frame(self)
        top_frame.pack(side="top", expand=True, fill="both", padx=5, pady=2)

        # Scan Settings
        self.scan_panel = ScanPanel(master=top_frame, local_dev_mode=local_dev_mode,
                                    text="Scan Settings", bg="lightblue", main_frame=self)
        self.scan_panel.pack(side="left", expand=True, fill="both", padx=2)

        # Network Setting
        self.network_panel = NetworkSettings(master=top_frame, main_frame=self, text="Network Settings",
                                             bg="lightyellow")
        self.network_panel.pack(side="left", expand=True, fill="both")

        #################################
        #       Half bottom frame       #
        #################################
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side="bottom", expand=True, fill="both", padx=5, pady=2)

        # NSAT Status
        self.nsat_status_frame = NSATStatutPanel(master=bottom_frame, text="NSAT Status", bg="khaki")
        self.nsat_status_frame.pack(side="left", expand=True, fill="both", padx=2)

        # NSAT Output
        self.nsat_output_frame = NSATOutputPanel(master=bottom_frame, text="NSAT Output", bg="violet")
        self.nsat_output_frame.pack(side="left", expand=True, fill="both")

        MenuBar(self)
        self.nsat_status_frame.auto_refresh()
        self.stop_scan_asked = False
        self.mainloop()

    @staticmethod
    def reboot():
        subprocess.call(["sudo", "reboot"])

