from datetime import datetime
import sys

import customtkinter as tk

from gui.utils.font import get_default_font

LEVELS = {
    "info": "green",
    "error": "red"
}

class Logger:
    def __init__(self, callback):
        self.callback = callback
        self._logged_lines = []

    def log(self, level: str, path: str, msg: str) -> None:
        color = LEVELS[level]
        log_msg = f"{datetime.now()} [{level.upper()}] {path}: {msg}."
        self.callback(log_msg, color)
        self._logged_lines.append((log_msg, color))

    def get_logged_lines(self):
        return self._logged_lines

class LiveLoggerWindow(tk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry("400x350")

        self.title("GlobalBurger Logging")

        if sys.platform.startswith("win"): #Bug der library auf windows 
            self.after(200, lambda: self.iconbitmap("assets/icons/burger/logo.ico")) #Fix um eigenes icon zu benutzen

        self._textbox = tk.CTkTextbox(self, corner_radius=0, font=tk.CTkFont(get_default_font()))
        self._textbox.configure(state="disabled")
        self._textbox.pack(expand=True, fill="both")
        self._textbox.tag_config("green", foreground="green")
        self._textbox.tag_config("red", foreground="red")

    def get_textbox(self):
        return self._textbox
    
    def insert(self, lines: list[str]):
        for text, color in lines:
            self._textbox.configure(state="normal")
            self._textbox.insert("end", text + "\n", color)
            self._textbox.configure(state="disabled")