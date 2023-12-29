import customtkinter as tk

from gui.views import View
from gui.widgets.buttons import BaseButton

class LoginView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        email_input = tk.CTkEntry(self, width=150, height=40, placeholder_text="E-Mail")
        passwort_input = tk.CTkEntry(self, width=150, height=40, placeholder_text="Passwort", show="*")
        login_button = BaseButton(self, width=150, height=40, text="LOGIN", command=lambda: self.master.get_viewmanager().goto("MenuView"))
        back_button = BaseButton(self, width=150, height=40, text="ZURÜCK", command=self.master.get_viewmanager().back)

        email_input.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        passwort_input.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
        login_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        back_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
