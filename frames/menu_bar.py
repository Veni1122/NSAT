import subprocess
from tkinter import Menu


class MenuBar(Menu):

    def __init__(self, main_frame):
        super().__init__(main_frame)

        # Scan settings
        self.scan_settings = Menu(self, tearoff=0)
        self.scan_settings.add_command(label="Reload from file", command=main_frame.scan_panel.reload_data(),
                                       state='disabled')
        self.scan_settings.add_command(label="Save", command=main_frame.scan_panel.save_data)
        self.add_cascade(label="Scan settings", menu=self.scan_settings)

        # Network settings
        network_settings = Menu(self, tearoff=0)
        network_settings.add_command(label="Save", command=main_frame.network_panel.save_data)
        network_settings.add_command(label="Apply", command=main_frame.network_panel.apply_config)
        self.add_cascade(label="Network settings", menu=network_settings)

        # Status
        eth_status = Menu(self, tearoff=0)
        eth_status.add_command(label="Refresh ", command=main_frame.nsat_status_frame.refresh)
        self.add_cascade(label="ETH status", menu=eth_status)

        # Log
        log_status = Menu(self, tearoff=0)
        log_status.add_command(label="Log Scan ", command=main_frame.nsat_output_frame.display_logs)
        self.add_cascade(label="Log", menu=log_status)

        # App
        app = Menu(self, tearoff=0)
        app.add_command(label="Exit", command=main_frame.quit)
        app.add_command(label="Reboot", command=main_frame.reboot)
        self.add_cascade(label="Application", menu=app)
        main_frame.config(menu=self)

    def activate_reload(self, active: bool):
        self.scan_settings.entryconfigure('Reload from file', state='normal' if active else 'disabled')
