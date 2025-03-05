import logging
import subprocess
import tkinter as tk
from enum import Enum

from app_config import AppConfig
from network import check_or_create_path, start_scan
from range_slider import RangeSlider


class ScanMode(Enum):
    NETWORK = 1,
    VLAN = 2,


logger = logging.getLogger(__file__)


class ScanPanel(tk.LabelFrame):

    def update_slider_label(self, low_high: [int]):
        self.slider_value.config(text=(' - '.join(map(str, low_high))))

    def set_middle_bottom_panels(self):
        scan_mode = ScanMode[self.scan_mode_var.get().split('.')[1]]

        # clear frame
        for widget in self.middle_frame.winfo_children():
            widget.destroy()

        # Hide refresh if not File mode
        if self.main_frame.menu_bar:
            if not scan_mode == ScanMode.NETWORK:
                self.main_frame.menu_bar.activate_reload(False)
            else:
                self.main_frame.menu_bar.activate_reload(True)

        if scan_mode == ScanMode.VLAN:

            self.range_slider = RangeSlider(self.middle_frame, min_val=1, max_val=4094, initial_low=1,
                                            initial_high=100, width=300, highlightthickness=0,
                                            height=50, callback=self.update_slider_label, bg=self.cget("bg"))
            self.range_slider.pack(pady=5, side="left")

            slider_range_saved = AppConfig.get_value('vlan_range')
            if slider_range_saved:
                self.range_slider.low_val, self.range_slider.high_val = slider_range_saved
                self.range_slider.draw_slider()

            self.slider_value = tk.Label(self.middle_frame, text=' - '.join(map(str, self.range_slider.get_range())),
                                         bg=self.cget("bg"))
            self.slider_value.pack(side="left")

        else:

            # Text area
            self.text_area = tk.Text(self.middle_frame, height=10, width=37)
            self.text_area.pack(side="left", padx=5)

            # Vertical Scrollbar
            scrollbar = tk.Scrollbar(self.middle_frame, orient="vertical", command=self.text_area.yview)
            scrollbar.pack(side="left", fill="y", pady=10)
            self.text_area.config(yscrollcommand=scrollbar.set)

        if scan_mode == ScanMode.NETWORK:

            # Load data
            network_file_data = AppConfig.get_value('network_file_data')
            if network_file_data:
                text = network_file_data
            else:
                text = self.get_network_file_data()
                AppConfig.save_value('network_file_data', text)
            self.text_area.insert("end", text)

            network_manual_list = AppConfig.get_value('network_manual_list')
            if not network_manual_list:
                network_manual_list = "Net 1: xxx.xxx.xxx.xxx/xx\nNet 2: xxx.xxx.xxx.xxx/xx\n" \
                                      "Net 2: xxx.xxx.xxx.xxx/xx\nNet 2: xxx.xxx.xxx.xxx/xx"

            self.text_area.insert("end", network_manual_list)

    def reload_data(self):
        text = self.get_network_file_data()
        self.text_area.delete("1.0", "end")
        self.text_area.insert("end", text)

    def save_data(self):

        scan_mode = ScanMode[self.scan_mode_var.get().split('.')[1]]

        if scan_mode == ScanMode.NETWORK:

            text = self.text_area.get("1.0", "end-1c")
            AppConfig.save_value('network_file_data', text)

            # Network file
            network_file_path = AppConfig.get_value('network_file_path')
            check_or_create_path(network_file_path)
            with open(network_file_path, "w", encoding='UTF8') as fp:
                fp.write(text)

        elif scan_mode == ScanMode.VLAN:
            AppConfig.save_value('vlan_range', self.range_slider.get_range())

    def stop_scan(self):
        self.main_frame.stop_scan_asked = True

    def open_reports(self):
        report_path = "/home/nsat/NSAT_Front/report"
        subprocess.call(["/usr/bin/pcmanfm", "/home/nsat/NSAT_Front/report"])

    def get_network_file_data(self):

        network_file_path = AppConfig.get_value('network_file_path')
        check_or_create_path(network_file_path)

        if self.local_dev_mode:
            return ""

        with open(network_file_path, "r", encoding='UTF8') as fp:
            text = fp.read()

        return text

    def __init__(self, local_dev_mode=False, main_frame=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text_area = None
        self.range_slider = None
        self.slider_value = None
        self.local_dev_mode = local_dev_mode
        self.main_frame = main_frame

        self.left_frame = tk.Frame(self, bg=self.cget("bg"))
        self.left_frame.pack(side='left', expand=True, fill="both")

        #################################
        #            Top frame          #
        #################################
        self.top_frame = tk.Frame(self.left_frame, bg=self.cget("bg"))
        self.top_frame.pack(side='top', expand=True, fill="both")

        # Scan mode selection
        self.scan_mode_var = tk.Variable(value=ScanMode.NETWORK)

        # Radio buttons
        title = tk.Label(self.top_frame, text="Scan mode:", bg=self.cget("bg"))
        title.grid(row=1, column=0, sticky="w", padx=5)

        vlan_mode_rb = tk.Radiobutton(self.top_frame, text="Vlan", variable=self.scan_mode_var, value=ScanMode.VLAN,
                                      command=self.set_middle_bottom_panels, bg=self.cget("bg"))
        vlan_mode_rb.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        network_mode_rb = tk.Radiobutton(self.top_frame, text="Network", variable=self.scan_mode_var,
                                         value=ScanMode.NETWORK,
                                         command=self.set_middle_bottom_panels, bg=self.cget("bg"))
        network_mode_rb.grid(row=1, column=2, sticky="w", padx=10, pady=5)

        #################################
        #           Middle frame        #
        #################################

        self.middle_frame = tk.Frame(self.left_frame, bg=self.cget("bg"))
        self.middle_frame.pack(side='top', expand=True, fill="both")

        #################################
        #          Right frame         #
        #################################

        # Save
        self.right_frame = tk.Frame(self, bg=self.cget("bg"))
        self.right_frame.pack(side="right", expand=True, fill="both", padx=5, pady=2)

        # Scan start
        start_bn = tk.Button(self.right_frame, text='Start Scan', command=lambda: start_scan(self.main_frame))
        start_bn.pack(pady=(80,5))

        # Scan stop
        stop_bn = tk.Button(self.right_frame, text='Stop Scan', command=self.stop_scan)
        stop_bn.pack(pady=5)

        # Report stop
        report_bn = tk.Button(self.right_frame, text='Open reports', command=self.open_reports)
        report_bn.pack(pady=5)

        self.set_middle_bottom_panels()
