import tkinter as tk


def disable_frame(frame):
    for widget in frame.winfo_children():
        if isinstance(widget, (tk.Button, tk.Entry, tk.Text, tk.Checkbutton, tk.Radiobutton)):
            widget.config(state="disabled")


def enable_frame(frame):
    for widget in frame.winfo_children():
        if isinstance(widget, (tk.Button, tk.Entry, tk.Text, tk.Checkbutton, tk.Radiobutton)):
            widget.config(state="normal")
