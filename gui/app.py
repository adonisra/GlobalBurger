import customtkinter as tk
from PIL import ImageFont

from gui.views import ViewManager, account, login, start, map as map_, menu, cart, settings, order
from gui.utils.live_logger import LiveLoggerWindow, Logger

class GlobalBurgerApp(tk.CTk):
    def __init__(self, *args, settings_manager, **kwargs):
        super().__init__(*args, **kwargs)

        self._logging_window = None
        self._logger = Logger(self._logging_callback) 

        self.geometry("400x350")
        self.title("GlobalBurger")
        self.resizable(False, False)
        self.iconbitmap("assets/icons/burger/logo.ico")

        self._viewmanager = ViewManager(self)
        self._logging_window = None
        self._settings = settings_manager
        self.updateWithSettings()

        self._viewmanager.add_view(settings.SettingsView)
        self._viewmanager.add_view(account.AccountView)
        self._viewmanager.add_view(login.LoginView)
        self._viewmanager.add_view(start.StartView)
        self._viewmanager.add_view(map_.MapView)
        self._viewmanager.add_view(menu.MenuView)
        self._viewmanager.add_view(cart.CartView)
        self._viewmanager.add_view(order.OrderView)
        self._logger.log("info", "app", "Alle Seiten geladen")

        self._viewmanager.goto("StartView")

        tk.CTk.report_callback_exception = self.error_handler

    def error_handler(self, exc, value, tb):
        value = ", ".join(value.args)
        self._logger.log("error", "app", f"{exc.__name__}({value})")

    def _logging_callback(self, text, color):
        if self._logging_window is not None:
            self._logging_window.insert(((text, color),))

    def get_logger(self):
        return self._logger

    def get_viewmanager(self):
        return self._viewmanager
    
    def get_settingsmanager(self):
        return self._settings

    def updateWithSettings(self):
        is_darkmode_enabled = self._settings["app"]["dark_mode"]
        if is_darkmode_enabled: tk.set_appearance_mode("Dark")
        else: tk.set_appearance_mode("Light")
        self._logger.log("info", "app", "Farbschema aktualisiert")

        is_livelogging_enabled = self._settings["app"]["live_logging"]
        if is_livelogging_enabled:
            if self._logging_window is None: 
                self._logging_window = LiveLoggerWindow(self)
                self._logger.log("info", "app", "Live Logging Fenster geöffnet")
                self._logging_window.insert(self._logger.get_logged_lines())

        elif self._logging_window is not None:
            self._logging_window.destroy()
            self._logger.log("info", "app", "Live Logging Fenster geschlossen")
            self._logging_window = None

        font_path = self._settings["app"]["font"]
        font = ImageFont.truetype(font_path)
        tk.ThemeManager.theme["CTkFont"]["family"] = font.getname()[0]
        self._logger.log("info", "app", f"Font aktualisiert auf {font_path}")

