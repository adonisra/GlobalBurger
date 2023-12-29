import pathlib

import customtkinter as tk
from PIL import Image

from gui.views import View
from gui.utils.layout import CenteredGridLayout
from gui.widgets.buttons import BaseButton

delete_image = tk.CTkImage(Image.open(pathlib.Path("assets/icons/appearance/mulleimer.png")))

class ItemsFrame(tk.CTkScrollableFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.items = []

    def add_item(self, name, value):
        item_frame = tk.CTkFrame(self, fg_color=("gray85", "gray16"))
        self.items.append(item_frame)
        item_frame.pack(expand=True, fill="x", pady=3, padx=(0, 5))

        left_padding = 10

        item_name = tk.CTkLabel(item_frame, text=f"{value}x {name}")
        item_name.grid(row=0, column=0, pady=2, padx=left_padding, sticky="W")

        def remove_self():
            item_frame.destroy()
            self.master.master.master.delete_item(name)

        delete_button = BaseButton(item_frame, fg_color="transparent", hover=False, text="", image=delete_image, command=remove_self, width=20, height=20)

        item_frame.update()
        padding = 15
        delete_button.grid(row=0, column=1, padx=350 - item_name.winfo_reqwidth() - 2 * left_padding - padding)

    def forget_all(self):
        for item in self.items:
            item.pack_forget()

class CartView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._buttons_container = CenteredGridLayout(self, padding=5, fg_color=("gray90", "gray13"))
        self._buttons_container.pack(side="bottom", pady=(0, 15))
        BaseButton(self._buttons_container, width=100, height=40, text="ZURÜCK", command=lambda: self.master.get_viewmanager().goto("MenuView"))
        self._order_button = BaseButton(self._buttons_container, width=100, height=40, text="BESTELLEN", command=lambda: self.master.get_viewmanager().goto("OrderView"))
        self._price_button = BaseButton(
            self._buttons_container, width=100, height=40, text="", state="disabled",
            fg_color=tk.ThemeManager.theme["CTkSegmentedButton"]["fg_color"],
            text_color_disabled=tk.ThemeManager.theme["CTkButton"]["text_color"]
        )
        self._buttons_container.grid_all()
        self._order_button.grid_forget()
        self._price_button.grid_forget()

        self._empty_cart_label = tk.CTkLabel(self, text="Warenkorb ist leer", font=tk.CTkFont(size=30))
        self._items_frame = ItemsFrame(self, height=270, fg_color=("gray90", "gray13"))

        self.data = {}

    def delete_item(self, name):
        _, price = self.data.pop(name, None)
        self._total_price -= price
        if self.data == {}:
            self._items_frame.pack_forget()
            self._order_button.grid_forget()
            self._price_button.grid_forget()
            self._empty_cart_label.pack(fill="none", expand=True)
        else:
            self._price_button.configure(text=f"{round(self._total_price, 2)}€")

    def on_enter(self, _, data):
        self._total_price = 0
        self.data = data
        if data == {}:
            self._empty_cart_label.pack(fill="none", expand=True)
            self._order_button.grid_forget()

        else:
            self._empty_cart_label.pack_forget()
            self._items_frame.forget_all()
            for item, (amount, price) in data.items():
                self._total_price += price
                self._items_frame.add_item(item, amount)

            self._price_button.configure(text=f"{round(self._total_price, 2)}€")

            self._buttons_container.grid_all()

            self._items_frame.pack(side="top", fill="x")

    def on_leave(self, _):
        return self.data