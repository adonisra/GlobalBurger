import customtkinter as tk
from PIL import ImageTk, ImageGrab, ImageEnhance

def darken(widget):
    box = (widget.winfo_rootx(), widget.winfo_rooty(), widget.winfo_rootx()+widget.winfo_width(), widget.winfo_rooty()+widget.winfo_height())
    grab = ImageGrab.grab(bbox=box)
    enhancer = ImageEnhance.Brightness(grab)
    img = enhancer.enhance(0.5)
    widget.overlay = ImageTk.PhotoImage(img)
    cvs = tk.CTkCanvas(widget, width=widget.winfo_width(), height=widget.winfo_height(), bd=0, highlightthickness=0)
    cvs.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    cvs.create_image(0, 0, anchor='nw', image=widget.overlay)
    return cvs