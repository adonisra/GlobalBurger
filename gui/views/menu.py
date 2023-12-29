import json
import pathlib

import customtkinter as tk
from PIL import Image

from gui.views import View
from gui.widgets.buttons import QuantityButton, BaseButton


class ItemsFrame(tk.CTkScrollableFrame):
    def __init__(self, *args, file_path: str, **kwargs):
        super().__init__(*args, **kwargs)

        with open(pathlib.Path(file_path)) as f:
            data = json.load(f)

        image_dir = pathlib.Path(data["image_path"])
        for item_name, item_data in data["items"].items():
            item_img = image_dir / (item_name.lower() + ".png")
            self.add_item(item_name, item_data["beschreibung"], item_data["preis"], item_img)

    def add_item(self, name: str, description: str, price: float, image_path: pathlib.Path):
        def increase_height():
            if amount.winfo_ismapped():
                amount.grid_forget()
                container.grid_forget()
                price_button.grid_forget()
                add_button.grid_forget()

            else:
                amount.grid(row=1, column=0, pady=8)
                container.grid(row=1, column=1)
                price_button.grid(row=0, column=0, sticky="W", padx=(0, 5))
                add_button.grid(row=0, column=1)

        item_frame = tk.CTkFrame(self)
        item_frame.pack(expand=True, fill="x", pady=3, padx=(0, 5))
        container = tk.CTkFrame(item_frame, fg_color="transparent")

        price = tk.DoubleVar(item_frame, price)

        price_button = BaseButton(
            container, text=f"{price.get()}€", state="disabled", width=50,
            fg_color=tk.ThemeManager.theme["CTkSegmentedButton"]["fg_color"],
            text_color_disabled=tk.ThemeManager.theme["CTkButton"]["text_color"]
        )
        def edit_button(value: float):
            price_button.configure(text=f"{round(value, 2)}€")

        amount = QuantityButton(item_frame, variable=price, callback=edit_button)
        def change():
            view = self.master.master.master
            given_amount = amount.get_amount()
            given_price = price.get()
            total_amount = view.get_order().get(name, (0,))[0] + given_amount
            total_price = view.get_order().get(name, (0, 0))[1] + given_price
            view.get_order()[name] = (total_amount, total_price)
            add_button.configure(text="HINZUGEFÜGT")
            add_button.after(1000, lambda: add_button.configure(text="HINZUFÜGEN"))

        add_button = BaseButton(container, text="HINZUFÜGEN", cursor="hand2", width=90, command=change)
        
        icon = tk.CTkImage(Image.open(image_path))

        item_name = BaseButton(item_frame, anchor="w", fg_color="transparent", text=name, text_color=("gray14", "#DCE4EE"), cursor="hand2", hover=False, image=icon, command=increase_height)
        item_name.grid(row=0, column=0, pady=2)

        item_description = tk.CTkLabel(item_frame, text=description, text_color="gray62")
        item_description.grid(row=0, column=1, sticky="W")

class MenuView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._order = {}

        def switch_frames(value):
            if value == "ESSEN":
                food_frame.lift()

            if value == "GETRÄNKE":
                drinks_frame.lift()
        
        auswahl = tk.CTkSegmentedButton(self, width=300, values=["ESSEN", "GETRÄNKE"], dynamic_resizing=False, command=switch_frames)
        auswahl.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        auswahl.set("ESSEN")

        drinks_frame = ItemsFrame(self, file_path="database/drinks.json", width=300, height=210)
        drinks_frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        food_frame = ItemsFrame(self, file_path="database/food.json", width=300, height=210)
        food_frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        settings_image = tk.CTkImage(Image.open(pathlib.Path("assets/icons/appearance/setting.png")))
        cart_image = tk.CTkImage(Image.open(pathlib.Path("assets/icons/appearance/cart.png")))
        settings_button = BaseButton(self, width=20, height=20, text="", image=settings_image, cursor="hand2", command=lambda: self.master.get_viewmanager().goto("SettingsView"))
        settings_button._corner_radius = 1000
        cart_button = BaseButton(self, width=20, height=20, text="", image=cart_image, cursor="hand2", command=lambda: self.master.get_viewmanager().goto("CartView", data=self._order))
        cart_button._corner_radius = 1000
        settings_button.place(relx=0.08, rely=0.073, anchor=tk.CENTER)
        cart_button.place(relx=0.92, rely=0.073, anchor=tk.CENTER)

    def get_order(self):
        return self._order

    def on_enter(self, from_view, data):
        if from_view == "CartView":
            self._order = data