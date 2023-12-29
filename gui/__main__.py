import customtkinter

from gui.app import GlobalBurgerApp
from gui.utils.settings_manager import Settings

manager = Settings("gui/userSettings.json")

customtkinter.FontManager.load_font(manager["app"]["font"])
customtkinter.set_default_color_theme("gui/theme.json")
app = GlobalBurgerApp(settings_manager=manager)
app.mainloop()