import typing as t

import customtkinter as tk

class View(tk.CTkFrame):
    def show(self) -> None:
        self.lift()

    def on_enter(self, _, __): ...
    def on_leave(self, _): ...

class ViewManager:
    def __init__(self, master: tk.CTk) -> None:
        self.master = master
        self.container = tk.CTkFrame(self.master)
        self.container.pack(side="top", fill="both", expand=True)

        self.views = {}
        self.last: t.Optional[View] = None
        self.current: t.Optional[View] = None
        
    def add_view(self, cls: t.Type[View]) -> None:
        v: View = cls(self.master)
        v.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.views[v.__class__.__name__] = v

    def goto(self, name: str, data={}) -> None:
        v: View = self.views[name]
        self.last = self.current
        self.current = v
        if self.last is not None:
            data = self.last.on_leave(self.current.__class__.__name__) or data
        self.current.on_enter(self.last.__class__.__name__, data)
        
        v.show()

    def back(self) -> None:
        self.goto(self.last.__class__.__name__)