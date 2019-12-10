import tkinter.font as ttf
import tkinter as ttk

class Font:

    TitleFont: ttf.Font = None
    NormalFont: ttf.Font = None
    MenuButtonFont: ttf.Font = None
    PawnGridFont: ttf.Font = None

    @staticmethod
    def Initialize(tk: ttk.Tk):
        Font.TitleFont = ttf.Font(tk, family="Roboto", size=20, weight="bold")
        Font.NormalFont = ttf.Font(tk, family="Roboto", size=10)
        Font.MenuButtonFont = ttf.Font(tk, family="Roboto", size=16)
        Font.PawnGridFont = ttf.Font(tk, family="Consolas", size=10)