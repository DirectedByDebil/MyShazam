import Views.ui_helper as ui
import tkinter.ttk as ttk
from tkinter import *
from tkinter import filedialog

intro_text = "Привет, это мини-приложение Volsu Shazam! Выберите источник и звук"
root_column_config = ui.create_grid_config(equalsCount=1)
root_row_config = ui.create_grid_config(equalsCount=5)

root = Tk()
form_behaviour = {}

#region public methods

def draw_form(behaviour: {}):
    global form_behaviour
    form_behaviour = behaviour

    _init_root()
    _init_control_frame()

def start_main_loop():
    root.mainloop()

#endregion


def _init_root():
    root.title("Volsu Shazam")
    root.state('zoomed')
    #root.attributes("-alpha", 0.9)

    ui.grid_configure(root, rows=root_row_config, columns=root_column_config)


#region control frame

def _init_control_frame():

    control_frame = ui.create_frame(root, row=2, column=1, rowspan=2, sticky=NS)

    row_config = ui.create_grid_config(equalsCount=2)
    column_config = ui.create_grid_config(equalsCount=1)
    ui.grid_configure(control_frame, rows=row_config, columns=column_config)

    intro_label = ui.create_label(master=control_frame, text=intro_text)
    ui.grid_element(intro_label, row=1, column=1)

    _init_buttons(control_frame)

def _init_buttons(frame):
    button_frame = ui.create_frame(frame, row=2, column=1)

    row_config = ui.create_grid_config(equalsCount=1)
    column_config = ui.create_grid_config(equalsCount=2)
    ui.grid_configure(button_frame, rows=row_config, columns=column_config)

    pick_orig_button = ui.create_button(button_frame, 'Исходник', form_behaviour["on_origin_picked"])
    ui.grid_element(pick_orig_button, 1, 1)

    pick_needle_button = ui.create_button(button_frame, 'Фрагмент', form_behaviour["on_needle_picked"])
    ui.grid_element(pick_needle_button, 1, 2)

#endregion




