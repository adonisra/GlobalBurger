from tkinter import font

def get_default_font():
    return font.nametofont("TkDefaultFont").actual()["family"]

def font_support(text: str) -> str:
    return (
        text
        .replace("ö", "oe")
        .replace("Ö", "OE")
        .replace("ä", "ae")
        .replace("Ä", "AE")
        .replace("ü", "ue")
        .replace("Ü", "UE")
    )

def get_font_name(path: str) -> str:
    return (path.split("/")[-1]).split(".")[0]