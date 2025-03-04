import logging
import subprocess
import tkinter as tk

from app_config import AppConfig
from toolbox import disable_frame, enable_frame

logger = logging.getLogger(__file__)


class NetworkSettings(tk.LabelFrame):
    field_names = ["IP", "SN", "GW", "DNS1", "DNS2", "VID"]

    def on_option_change(self, *args):
        if self.selected_option.get() == 'DHCP':
            disable_frame(self.bottom_frame)
        else:
            enable_frame(self.bottom_frame)

    def __init__(self, main_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_frame = main_frame

        # Interface Settings
        middle_frame = tk.Frame(self, bg=self.cget("bg"))
        middle_frame.pack(side='top', expand=True, fill="both")

        options = ["Static", "DHCP"]
        tk.Label(middle_frame, text=f'Mode:', bg=self.cget("bg")).grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.selected_option = tk.StringVar(value=options[0])
        self.selected_option.trace_add("write", self.on_option_change)
        dropdown = tk.OptionMenu(middle_frame, self.selected_option, *options)
        dropdown.grid(row=0, column=1, padx=10, pady=5)

        self.interface_settings = {}
        self.bottom_frame = tk.Frame(self, bg=self.cget("bg"))
        self.bottom_frame.pack(side='bottom', expand=True, fill="both")

        row = 1
        for i, name in enumerate(self.field_names):

            if i % 2 == 0:
                row += 1

            tk.Label(self.bottom_frame, text=f'{name}:', bg=self.cget("bg")).grid(
                row=row, column=0 + i % 2 * 2, sticky="w", padx=5, pady=5)
            entry = tk.Entry(self.bottom_frame, width=12)
            entry.grid(row=row, column=1 + i % 2 * 2, padx=5, pady=5)

            self.interface_settings[name] = entry

        self.load_settings()

    def save_data(self):
        eth_config = {field_name: self.interface_settings[field_name].get() for field_name in self.field_names}
        eth_config['mode'] = self.selected_option.get()
        AppConfig.save_value(f"ETH0_settings", eth_config)

    def load_settings(self):
        saved_config = AppConfig.get_value(f"ETH0_settings")
        if saved_config:
            for field_name, field_value in saved_config.items():
                if field_name != 'mode':
                    entry = self.interface_settings[field_name]
                    entry.delete(0, tk.END)
                    entry.insert(0, field_value)

            self.selected_option.set(saved_config.get('mode', 'Static'))

    def apply_config(self):
        self.save_data()
        output_panel_text = self.main_frame.nsat_output_frame.text_area
        output_panel_text.delete("1.0", "end")
        interface_name = 'eth0'

        saved_config = AppConfig.get_value(f"ETH0_settings")
        command = f"sudo ip addr flush dev {interface_name}"
        text = command + '\n'
        subprocess.call(command, shell=True)

        if saved_config['mode'] == 'Static':

            command = f"sudo ip addr add {saved_config['IP']}/{saved_config['SN']} dev {interface_name}"
            subprocess.call(command, shell=True)
            text += command + '\n'

            # Gateway
            command = f"sudo ip route add default via {saved_config['GW']}"
            subprocess.call(command, shell=True)
            text += command + '\n'

            # DNS-Server in /etc/resolv.conf
            dns_config = f"nameserver {saved_config['DNS1']}\n"
            if saved_config['DNS2']:
                dns_config += f"nameserver {saved_config['DNS2']}\n"

            subprocess.run(
                ["sudo", "tee", "/etc/resolv.conf"],
                input=dns_config.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            text += f'/etc/resolv.conf overwritten {dns_config}'

        else:
            command = f"sudo dhclient {interface_name}"
            subprocess.call(command, shell=True)
            text += command + '\n'

        print(text, flush=True)
        output_panel_text.insert("end", text)
        output_panel_text.see(tk.END)
        self.main_frame.update()
