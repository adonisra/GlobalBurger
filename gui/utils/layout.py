import customtkinter as tk

class CenteredGridLayout(tk.CTkFrame):
    def __init__(self, *args, padding: int, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.padding = padding

    def grid_all(self):
        children = self.winfo_children()
        self.grid_columnconfigure(list(range(len(children))), weight=1)
        for i, child in enumerate(children):
            child.grid(row=0, column=i, sticky="EW", padx=self.padding)

    def regrid(self, widget):
        children = self.winfo_children()
        widget.grid(row=0, column=children.index(widget), sticky="EW", padx=self.padding)