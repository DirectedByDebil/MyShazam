from tkinter import ttk
import customtkinter as ctk

margin = 10
padding = 10

header_font_size = 36
info_font_size = 18

#region create widgets

def create_button(master, text: str, command):
    return ctk.CTkButton(master, text=text, corner_radius=15, command=command)

def create_frame(master, row: int=1, column: int=1, rowspan: int=1, sticky: str = ''):

    frame = ctk.CTkFrame(master=master, corner_radius=15, border_width=2, border_color="gray")
    grid_element(frame, row, column, rowspan, sticky)

    return frame

def create_label(master, text: str):
    return ctk.CTkLabel(master, text=text, font=ctk.CTkFont(size=info_font_size))


#endregion

#region grid operations

def grid_element(element, row: int=1, column: int=1, rowspan: int=1, sticky: str=''):
    element.grid(row=row, column=column, rowspan=rowspan, padx=margin, pady=margin, ipadx=padding, ipady=padding, sticky=sticky)

def create_grid_config(areEqual: bool = True, equalsCount: int = 1, weights=None):

    if weights is None:
        weights = []
    config = []

    if areEqual:
        for i in range(equalsCount):
            config.append({"index": i + 1, "weight": 1})
    else:
        for i in range(len(weights)):
            config.append({"index": i + 1, "weight": weights[i]})

    return config

def grid_configure(element, rows:[], columns:[]):

    for r in rows:
        element.rowconfigure(index=r["index"], weight=r["weight"])

    for c in columns:
        element.columnconfigure(index=c["index"], weight=c["weight"])

#endregion