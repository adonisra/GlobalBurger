import customtkinter as tk
from gui.utils.font import get_default_font

class BaseButton(tk.CTkButton):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)

        self.root = self.winfo_toplevel()


        self.configure(command=self.log_callback(self.cget("command")))

    def log_callback(self, func):
        def callback():
            self.root.get_logger().log("info", "app", "Button click")
            func()

        return callback

class QuantityButton(tk.CTkSegmentedButton):
    def get_amount(self):
        return self.number
    
    def update_amount(self):
        self.number_button.configure(text=str(self.number))

    def on_decrease(self):
        self.number -= 1
        if self.number == 1: self.decrease_button.configure(state="disabled")

        self.update_amount()
        self.variable.set(self.variable.get() - self.default)
        self.callback(self.variable.get())

    def on_increase(self):
        self.number += 1
        if self.number == 2: self.decrease_button.configure(state="normal")

        self.update_amount()
        self.variable.set(self.variable.get() + self.default)
        self.callback(self.variable.get())

    def __init__(self, *args, variable, callback, **kwargs):
        super().__init__(values=["-", "1", "+"], *args, **kwargs)
        self.variable = variable
        self.default = self.variable.get()
        self.callback = callback
        self.number = 1
        self.decrease_button = self._buttons_dict["-"]
        self.decrease_button.configure(state="disabled")
        self.increase_button = self._buttons_dict["+"]
        self.number_button = self._buttons_dict["1"]
        self.DEFAULT_FONT_FAMILY = get_default_font()

        self.decrease_button.configure(command=self.on_decrease, font=tk.CTkFont(self.DEFAULT_FONT_FAMILY))
        self.increase_button.configure(command=self.on_increase, font=tk.CTkFont(self.DEFAULT_FONT_FAMILY))


        self.configure(
            selected_color=tk.ThemeManager.theme["CTkSegmentedButton"]["fg_color"],
            selected_hover_color=tk.ThemeManager.theme["CTkSegmentedButton"]["unselected_hover_color"]
        )
        self.number_button.configure(text_color_disabled=tk.ThemeManager.theme["CTkSegmentedButton"]["text_color"], state="disabled", font=tk.CTkFont(self.DEFAULT_FONT_FAMILY))