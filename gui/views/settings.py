import customtkinter as tk
from tkinter import filedialog as fd

from gui.views import View
from gui.utils.layout import CenteredGridLayout
from gui.utils import font, darken
from gui.widgets.buttons import BaseButton

class RequiresRestartFrame(tk.CTkFrame):
    def __init__(self, *args, message: str, **kwargs):
        super().__init__(*args, **kwargs)

        label = tk.CTkLabel(self, text=message, font=tk.CTkFont(size=20))
        label.pack(side="top", anchor=tk.CENTER, pady=(20, 30))

class ItemsFrame(tk.CTkScrollableFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = self.winfo_toplevel()

        self.settings = self.root.get_settingsmanager()

        self.wohnort_var = tk.StringVar(value=font.font_support(self.settings["user"]["wohnort"]))
        self.font_var = tk.StringVar(value=font.font_support(font.get_font_name(self.settings["app"]["font"])))
        self.dark_mode_check_var = tk.BooleanVar(value=self.settings["app"]["live_logging"])
        self.live_logging_check_var = tk.BooleanVar(value=self.settings["app"]["dark_mode"])

        self.checkbox_setting("dark_mode", "Dark Mode", self.dark_mode_check_var)
        self.checkbox_setting("live_logging", "Live Logging", self.live_logging_check_var)
        self.customfont_setting()
        self.wohnort_setting()

    def new_item(self, name):
        item_frame = tk.CTkFrame(self, fg_color=("gray85", "gray16"))
        item_frame.pack(expand=True, fill="x", pady=3, padx=(0, 5))

        setting_name = tk.CTkLabel(item_frame, text=name.replace("_", " ").title())
        setting_name.pack(side="left")
        setting_name.grid(row=0, column=0, pady=2, padx=10, sticky="W")

        return item_frame, setting_name
    
    def checkbox_setting(self, setting_name: str, display_name: str, check_var):
        item_frame, setting_label = self.new_item(display_name)
        def on_change():
            self.settings.set_app(setting_name, check_var.get())

        checkbox = tk.CTkCheckBox(item_frame, variable=check_var, text="", command=on_change)

        item_frame.update()
        padding = 5
        checkbox.grid(row=0, column=1, padx=350 - setting_label.winfo_reqwidth() - 2 * 10 - padding)

    def choose_string_setting(self, display_name: str, text_var, callback):
        item_frame, _ = self.new_item(display_name)

        item_frame.grid_columnconfigure(0, weight=1)

        choose_button = BaseButton(item_frame, width=100, text="Auswaehlen", command=callback)
        default_button = BaseButton(
            item_frame, width=100, textvariable=text_var, state="disabled",
            fg_color=tk.ThemeManager.theme["CTkSegmentedButton"]["fg_color"],
            text_color_disabled=tk.ThemeManager.theme["CTkButton"]["text_color"]
        )
        choose_button.grid(row=0, column=1, pady=5, sticky="E", padx=(0, 5))
        default_button.grid(row=0, column=2, sticky="E", padx=(0, 5))

        return default_button
    
    def customfont_setting(self):
        def get_file():
            filename = fd.askopenfilename(
                title='Wähle eine Font aus',
                initialdir='/',
                filetypes=(("Font Dateien", ".ttf"), ("Alle Dateien", "*"))
            )

            if filename != "":
                self.settings.set_app("font", filename)
                self.font_var.set(font.font_support(font.get_font_name(filename)))

        self.choose_string_setting("Font", self.font_var, callback=get_file)

    def wohnort_setting(self):
        self.choose_string_setting("Wohnort", self.wohnort_var, callback=lambda: self.root.get_viewmanager().goto("MapView"))

class SettingsView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._last_page = None
        self.settings = self.master.get_settingsmanager()

        self.settings_frame = ItemsFrame(self, height=270, fg_color=("gray90", "gray13"))
        self.settings_frame.pack(side="top", fill="x")

        def save_settings():
            settings = self.master.get_settingsmanager()
            if settings["app"]["font"] != settings.get_app("font"):
                cvs = darken(self.master)
                info_frame = RequiresRestartFrame(self.master, message="Nach Speichern wird\nein Neustart benötigt.", width=300, border_width=2, height=300, corner_radius=0)
                buttons_container = CenteredGridLayout(info_frame, padding=10, fg_color=info_frame.cget("fg_color"))
                def destroy_all():
                    cvs.destroy()
                    info_frame.destroy()

                def restart():
                    import sys, os
                    os.execv(sys.executable, [sys.executable, "-m", "gui"])

                BaseButton(buttons_container, text="Jetzt neustarten", command=restart)
                BaseButton(buttons_container, text="Später neustarten", command=destroy_all)
                buttons_container.grid_all()
                buttons_container.pack(side="top", padx=10, pady=(0, 20))
                info_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            settings.save()
            self.master.updateWithSettings()

        self.buttons_container = CenteredGridLayout(self, padding=5, fg_color=("gray90", "gray13"))
        self.buttons_container.pack(side="bottom", pady=(0, 15))

        BaseButton(self.buttons_container, width=100, height=40, text="ZURÜCK", command=lambda: self.master.get_viewmanager().goto(self._last_page))
        BaseButton(self.buttons_container, width=100, height=40, text="SPEICHERN", command=save_settings)
        self.logout_button = BaseButton(self.buttons_container, width=100, height=40, text="LOGOUT",  command=lambda: self.master.get_viewmanager().goto("StartView"))

        self.buttons_container.grid_all()
        self.logout_button.grid_forget()

    def add_logout_button(self):
        self.buttons_container.regrid(self.logout_button)

    def remove_logout_button(self):
        self.logout_button.grid_forget()
            
    def on_enter(self, from_view, _):
        self.settings_frame.wohnort_var.set(self.settings["user"]["wohnort"])
        self.settings_frame.font_var.set(font.font_support(font.get_font_name(self.settings["app"]["font"])))
        self.settings_frame.live_logging_check_var.set(self.settings["app"]["live_logging"])
        self.settings_frame.dark_mode_check_var.set(self.settings["app"]["dark_mode"])

        if from_view != "MapView":
            self._last_page = from_view

        else:
            self.settings_frame.wohnort_var.set(self.settings.get_user("wohnort"))

    def on_leave(self, _):
        self.settings.reset()