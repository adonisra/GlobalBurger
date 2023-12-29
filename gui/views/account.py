import customtkinter as tk
from tkinter import ttk

from gui.views import View
from gui.widgets.buttons import BaseButton

class AccountView(View):
   def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         header_2 = tk.CTkLabel(self, text="ERSTELLEN", font=tk.CTkFont(size=40))
         header_1 = tk.CTkLabel(self, text="ACCOUNT", font=tk.CTkFont(size=40))
         vorname_input = tk.CTkEntry(self, width=150, height=40, placeholder_text="Vorname")
         nachname_input = tk.CTkEntry(self, width=150, height=40, placeholder_text="Nachname")
         email_input = tk.CTkEntry(self, width=150, height=40, placeholder_text="E-Mail")
         passwort_input = tk.CTkEntry(self, width=150, height=40, placeholder_text="Passwort", show="*")
         sep = ttk.Separator(self, orient='vertical')

         def create():
            entries = (vorname_input, nachname_input, email_input, passwort_input)
            invalid = False
            for entry in entries:
                if entry.get() == "":
                    entry.configure(placeholder_text_color="#B00020")
                    invalid = True

            if not invalid:
               self.master.get_viewmanager().goto("MapView")

         erstellen_button = BaseButton(self, width=150, height=40, text="ERSTELLEN", command=create)
         back_button = BaseButton(self, width=150, height=40, text="ZURÜCK", command=self.master.get_viewmanager().back)

         header_1.place(relx=0.25, rely=0.35, anchor=tk.CENTER)
         header_2.place(relx=0.25, rely=0.5, anchor=tk.CENTER)
         vorname_input.place(relx=0.75, rely=0.2, anchor=tk.CENTER)
         nachname_input.place(relx=0.75, rely=0.35, anchor=tk.CENTER)
         email_input.place(relx=0.75, rely=0.5, anchor=tk.CENTER)
         passwort_input.place(relx=0.75, rely=0.65, anchor=tk.CENTER)
         erstellen_button.place(relx=0.3, rely=0.85, anchor=tk.CENTER)
         back_button.place(relx=0.7, rely=0.85, anchor=tk.CENTER)
         sep.place(relx=0.5, rely=0.1, width=1, height=230)