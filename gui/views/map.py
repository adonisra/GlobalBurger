import customtkinter as tk
import tkintermapview

from gui.views import View
from gui.utils import font
from gui.utils.layout import CenteredGridLayout
from gui.widgets.buttons import BaseButton

class MapView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.land = None

        def save_wohnort():
            if self.land is not None:
                self.master.get_viewmanager().goto(self._next_page)
        
        header = tk.CTkLabel(self, text="WOHNORT FESTLEGEN", font=tk.CTkFont(size=40))
        map_widget = tkintermapview.TkinterMapView(self, width=350, height=200, corner_radius=10)
        buttons_container = CenteredGridLayout(self, padding=5, fg_color=("gray90", "gray13"))
        default_button = BaseButton(
            buttons_container, width=150, height=40, text="Deutschland", state="disabled",
            fg_color=tk.ThemeManager.theme["CTkSegmentedButton"]["fg_color"],
            text_color_disabled=tk.ThemeManager.theme["CTkButton"]["text_color"],
        )
        BaseButton(buttons_container, width=150, height=40, text="Weiter", font=tk.CTkFont("Anton"), command=save_wohnort)
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google tile server
        map_widget.set_position(51.1744294, 6.4469565) #Gartenstraße

        def on_click(coords):
            map_widget.delete_all_marker()
            x, y = coords
            self.land = tkintermapview.convert_coordinates_to_country(x, y)
            default_button.configure(text=self.land)
            map_widget.set_marker(x, y)
        
        map_widget.add_left_click_map_command(on_click)
        header.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        buttons_container.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        buttons_container.grid_all()

    def on_enter(self, from_view, _):
        if from_view == "SettingsView":
            self._next_page = "SettingsView"

        if from_view == "AccountView":
            self._next_page = "MenuView"

    def on_leave(self, to_view):
        settings = self.master.get_settingsmanager()
        settings.set_user("wohnort", font.font_support(self.land))

        if to_view == "MenuView":
            settings.save()