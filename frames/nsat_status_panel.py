import logging
import tkinter as tk

from network import get_network_interface_status, get_refresh_status


def draw_color_circle(canvas: tk.Canvas, color: str):
    canvas.delete("all")
    canvas.create_oval(8, 8, 22, 22, fill=color, outline="")


logger = logging.getLogger(__file__)


class NSATStatutPanel(tk.LabelFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #################################
        #              ETH0             #
        #################################

        eth0_status_label = tk.Label(self, text="ETH0 Status: ", bg=self.cget("bg"))
        eth0_status_label.grid(row=0, column=0, sticky='w', pady=(10, 0))

        self.canvas_eth0_status = tk.Canvas(self, width=30, height=30, highlightthickness=0, bg=self.cget("bg"))
        draw_color_circle(self.canvas_eth0_status, 'gray')
        self.canvas_eth0_status.grid(row=0, column=1, sticky='w', pady=(10, 0))

        eth0_ip_label = tk.Label(self, text="ETH0 IP: ", bg=self.cget("bg"))
        eth0_ip_label.grid(row=1, column=0, sticky='w')

        self.eth0_ip_value_label = tk.Label(self, text="xxx.xxx.xxx.xxx", bg=self.cget("bg"))
        self.eth0_ip_value_label.grid(row=1, column=1, sticky='w')

        #################################
        #              ETH1             #
        #################################

        eth1_status_label = tk.Label(self, text="ETH1 Status: ", bg=self.cget("bg"))
        eth1_status_label.grid(row=3, column=0, sticky='w', pady=(10, 0))

        self.canvas_eth1_status = tk.Canvas(self, width=30, height=30, highlightthickness=0, bg=self.cget("bg"))
        draw_color_circle(self.canvas_eth1_status, 'gray')
        self.canvas_eth1_status.grid(row=3, column=1, sticky='w', pady=(10, 0))

        eth1_ip_label = tk.Label(self, text="ETH1 IP: ", bg=self.cget("bg"))
        eth1_ip_label.grid(row=4, column=0, sticky='w')

        self.eth1_ip_value_label = tk.Label(self, text="No IP", bg=self.cget("bg"))
        self.eth1_ip_value_label.grid(row=4, column=1, sticky='w')

        #################################
        #              RAS              #
        #################################

        self.ssh_status_detail = (0, '')  # Greed count, status color

        ras_status_label = tk.Label(self, text="RAS Connection: ", bg=self.cget("bg"))
        ras_status_label.grid(row=5, column=0, sticky='w', pady=(10, 0))

        self.canvas_ras_status = tk.Canvas(self, width=30, height=30, highlightthickness=0, bg=self.cget("bg"))
        draw_color_circle(self.canvas_ras_status, 'gray')
        self.canvas_ras_status.grid(row=5, column=1, sticky='w', pady=(10, 0))

        self.refresh()

    def refresh(self):
        eth0_status, et0_ip = get_network_interface_status('eth0')
        self.eth0_ip_value_label.config(text=et0_ip)
        draw_color_circle(self.canvas_eth0_status, eth0_status)

        eth1_status, eth1_ip = get_network_interface_status('eth1')
        self.eth1_ip_value_label.config(text=eth1_ip)
        draw_color_circle(self.canvas_eth1_status, eth1_status)
        self.ssh_status_detail = get_refresh_status(self.ssh_status_detail)
        draw_color_circle(self.canvas_ras_status, self.ssh_status_detail[1])

    def auto_refresh(self):
        self.refresh()
        self.after(5000, self.auto_refresh)
