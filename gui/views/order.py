import customtkinter as tk

from gui.views import View
from gui.widgets.buttons import BaseButton

class OrderView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ordered_label = tk.CTkLabel(self, text="BESTELLUNG AUFGEGEBEN", font=tk.CTkFont(size=30))
        ordered_label.pack(fill="none", expand=True)
        back_button = BaseButton(self, width=100, height=40, text="ZURÜCK", command=self.master.get_viewmanager().back)
        back_button.pack(side="bottom", pady=(0, 15))

