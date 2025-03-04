import os
import subprocess
import tkinter as tk

from app_config import AppConfig


def validate_sn(subnet_mask):
    # Hier die Logik zur Validierung der Subnetzmaske implementieren
    # ...
    pass  # TODO: Implementiere die Validierung der Subnetzmaske


def validate_gw(gateway):
    # Hier die Logik zur Validierung des Gateways implementieren
    # ...
    pass  # TODO: Implementiere die Validierung des Gateways


def validate_dns(dns_server):
    # Hier die Logik zur Validierung des DNS-Servers implementieren
    # ...
    pass  # TODO: Implementiere die Validierung des DNS-Servers


def open_network_to_scan():
    # Hier die Logik zum Öffnen des Fensters "Network to scan" implementieren
    # ...
    pass  # TODO: Implementiere die Funktion zum Öffnen des Fensters


def validate_ip(ip_address):
    # Hier die Logik zur Validierung der IP-Adresse implementieren
    # ...
    pass  # TODO: Implementiere die Validierung der IP-Adresse


def get_network_interface_status(interface_name: str) -> (str, str):
    try:
        result = subprocess.check_output(["ip", "addr", "show", interface_name]).decode()
    except (FileNotFoundError, subprocess.CalledProcessError):
        status = 'gray'
        ip_adresse = "Fehler"
    else:
        if "LOWER_UP" in result:
            if 'inet ' in result:
                ip_adresse = result.split("inet ")[1].split("/")[0]
                status = 'green'
            else:
                ip_adresse = "Keine IP"
                status = 'orange'
        else:
            ip_adresse = "Kein Link"
            status = 'red'

    return status, ip_adresse


def get_refresh_status(ssh_status_detail: tuple) -> tuple:
    green_count, current_status = ssh_status_detail

    try:
        result = subprocess.check_output(
            ["ss", "-tna", "state", "established", "dst", f'{AppConfig.get_value("ssh_ip_port")}'], text=True
        )

    except (FileNotFoundError, subprocess.CalledProcessError):
        # Connection error
        return 0, "gray"

    # Link down
    if "20.157.64.106:443" not in result:
        return 0, "red"

    else:
        # Line establisch
        if green_count == 0:
            return 1, 'blue'

        # Line ok
        else:
            return 1, 'green'


def start_scan(main_frame):
    from frames.scan_panel import ScanMode

    # Get scan configuration
    scan_mode = ScanMode[main_frame.scan_panel.scan_mode_var.get().split('.')[1]]

    # Reset output
    output_panel_text = main_frame.nsat_output_frame.text_area
    output_panel_text.delete("1.0", "end")

    # Network mode
    if scan_mode == ScanMode.NETWORK:
        main_frame.scan_panel.save_data()

        command = f"-f {AppConfig.get_value('network_file_path')}"

    # VLAN Mode => Always from ETH1
    else:

        min_vlan, max_vlan = main_frame.scan_panel.range_slider.get_range()
        command = f"-vs {min_vlan}-{max_vlan}"

    if command:

        input_params = ['sudo', '/home/nsat/scanner/nsat']
        input_params.extend(command.split())

        main_frame.stop_scan_asked = False
        process = subprocess.Popen(input_params, stdout=subprocess.PIPE, text=True, bufsize=1)

        for line in process.stdout:
            text = f'{line.strip()}\n'
            output_panel_text.insert("end", text)
            output_panel_text.see(tk.END)

            print(text, flush=True)
            main_frame.update()

            if main_frame.stop_scan_asked:
                process.terminate()


def check_or_create_path(network_file_path: str):
    if not (os.path.exists(network_file_path) and os.path.isfile(network_file_path)):
        os.makedirs(os.path.dirname(network_file_path), exist_ok=True)
