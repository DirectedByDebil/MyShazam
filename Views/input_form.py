import Views.ui_helper as ui
import tkinter.ttk as ttk
from tkinter import *
from tkinter import filedialog
from pydispatch import dispatcher

intro_text = "Привет, это мини-приложение Volsu Shazam! Выберите источник и звук"
root_column_config = ui.create_grid_config(equalsCount=1)
root_row_config = ui.create_grid_config(equalsCount=5)

root = Tk()
form_behaviour = {}
elements = {}

#region public methods

def draw_form(behaviour: {}):
    global form_behaviour
    form_behaviour = behaviour

    _init_root()
    _init_control_frame()

def start_main_loop():
    root.mainloop()

def set_sender (sender):
    dispatcher.connect(_on_origin_changed, signal='origin_file_changed', sender=sender)
    dispatcher.connect(_on_needle_changed, signal='needle_file_changed', sender=sender)

#endregion


def _init_root():
    root.title("Volsu Shazam")
    root.state('zoomed')
    #root.attributes("-alpha", 0.9)

    ui.grid_configure(root, rows=root_row_config, columns=root_column_config)


#region control frame

def _init_control_frame():

    control_frame = ui.create_frame(root, row=2, column=1, rowspan=2, sticky=NS)

    row_config = ui.create_grid_config(equalsCount=3)
    column_config = ui.create_grid_config(equalsCount=1)
    ui.grid_configure(control_frame, rows=row_config, columns=column_config)

    intro_label = ui.create_label(master=control_frame, text=intro_text)
    ui.grid_element(intro_label, row=1, column=1)

    _init_buttons(control_frame)
    _init_files_info(control_frame)

def _init_buttons(frame):
    button_frame = ui.create_frame(frame, row=2, column=1)

    row_config = ui.create_grid_config(equalsCount=1)
    column_config = ui.create_grid_config(equalsCount=2)
    ui.grid_configure(button_frame, rows=row_config, columns=column_config)

    pick_orig_button = ui.create_button(button_frame, 'Исходник', form_behaviour["on_origin_picked"])
    ui.grid_element(pick_orig_button, 1, 1)

    pick_needle_button = ui.create_button(button_frame, 'Фрагмент', form_behaviour["on_needle_picked"])
    ui.grid_element(pick_needle_button, 1, 2)

def _init_files_info(frame):
    files_frame = ui.create_frame(frame, row=3, column=1)

    row_config = ui.create_grid_config(equalsCount=1)
    column_config = ui.create_grid_config(equalsCount=2)
    ui.grid_configure(files_frame, rows=row_config, columns=column_config)

    origin_label = ui.create_label(files_frame, '')
    ui.grid_element(origin_label, 1, 1)

    needle_label = ui.create_label(files_frame, '')
    ui.grid_element(needle_label, 1, 2)

    elements["origin_label"] = origin_label
    elements["needle_label"] = needle_label

#endregion

#region view file info

def _on_origin_changed(data):
    origin_info = _get_file_info(data)
    elements["origin_label"].configure(text=origin_info)

def _on_needle_changed(data):
    needle_info = _get_file_info(data)
    elements["needle_label"].configure(text=needle_info)

def _get_file_info(data) -> str:

    reversed_file_name = data['File Name'][::-1]
    index = reversed_file_name.index('/')
    file_name = reversed_file_name[0:index][::-1]

    output = [
        file_name,
        f"Длительность {data['Length']}",
        f"{data['Tags']} свойств",
        f"{data['Windows']} окон",
        f"{len(data['peaks'])} пиков",
        f"{len(data['frequencies'])} частот",
        f"{len(data['fingerprints'])} отпечатков"
    ]

    info = '\n'.join(output)
    return info

#endregion



