import pathlib

import customtkinter as tk
from PIL import Image

from gui.views import View
from gui.widgets.buttons import BaseButton

settings_image = tk.CTkImage(Image.open(pathlib.Path("assets/icons/appearance/setting.png")))
logo_image = tk.CTkImage(Image.open(pathlib.Path("assets/icons/burger/logo.png")), size=(100, 74))

class StartView(View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        logo_text = tk.CTkLabel(
            self, text="GlobalBurger", image=logo_image, padx=10,
            compound="right", font=tk.CTkFont(size=40)
        )
        
        self.settings_view = self.master.get_viewmanager().views["SettingsView"]
        
        accountpage_button = BaseButton(self, width=150, height=40, text="ACCOUNT ERSTELLEN", command=lambda: self.master.get_viewmanager().goto("AccountView"))
        loginpage_button = BaseButton(self, width=150, height=40, text="LOGIN", command=lambda: self.master.get_viewmanager().goto("LoginView"))

        settings_button = BaseButton(self, width=20, height=20, text="", image=settings_image, command=lambda: self.master.get_viewmanager().goto("SettingsView"))
        settings_button._corner_radius = 1000

        logo_text.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
        settings_button.place(relx=0.08, rely=0.06, anchor=tk.CENTER)
        accountpage_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        loginpage_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

    def on_enter(self, from_view, _):
        if from_view == "SettingsView":
            self.settings_view.remove_logout_button()

    def on_leave(self, to_view):
        if to_view != "SettingsView":
            self.settings_view.add_logout_button()