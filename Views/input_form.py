import Views.ui_helper as ui
import tkinter.ttk as ttk
from tkinter import *
from tkinter import filedialog

global root

intro_text = "Привет, это мини-приложение Volsu Shazam! Выберите источник и звук"
root_column_config = ui.create_grid_config(areEqual=False, weights=[1, 4])
root_row_config = ui.create_grid_config(equalsCount=5)


#region public methods

def draw_form():

    _init_root()
    _init_left_frame()
    _init_right_frame()

def start_main_loop():

    global root
    root.mainloop()

#endregion


def _init_root():
    global root
    root = Tk()
    root.title("Volsu Shazam")
    root.state('zoomed')
    #root.attributes("-alpha", 0.9)

    ui.grid_configure(root, rows=root_row_config, columns=root_column_config)


#region left frame

def _init_left_frame():

    left_frame = ui.create_frame(root, row=2, column=1, rowspan=2, sticky=NS)

    row_config = ui.create_grid_config(equalsCount=2)
    column_config = ui.create_grid_config(equalsCount=1)
    ui.grid_configure(left_frame, rows=row_config, columns=column_config)

    intro_label = ui.create_label(master=left_frame, text=intro_text)
    ui.grid_element(intro_label, row=1, column=1)

    _init_buttons(left_frame)

def _init_buttons(frame):

    button_frame = ui.create_frame(frame, row=2, column=1)

    row_config = ui.create_grid_config(equalsCount=1)
    column_config = ui.create_grid_config(equalsCount=2)
    ui.grid_configure(button_frame, rows=row_config, columns=column_config)

    pick_orig_button = ui.create_button(button_frame, 'Исходник', select_file)
    ui.grid_element(pick_orig_button, 1, 1)

    pick_part_button = ui.create_button(button_frame, 'кусочек', select_file)
    ui.grid_element(pick_part_button, 1, 2)

def select_file():
    path = filedialog.askopenfilename(
        title="Select audio file",
        filetypes=[("WAV files", "*.wav"), ("MP3 files", "*.mp3")]
    )

    if path:
        print(f"Выбран файл: {path}")
        # здесь анализ файла

#endregion


#region right frame

def _init_right_frame():
    right_frame = ui.create_frame(root, row=1, column=2, rowspan=5, sticky=NSEW)

    row_config = ui.create_grid_config(areEqual=False, weights=[1, 10, 10])
    column_config = ui.create_grid_config(equalsCount=1)
    ui.grid_configure(right_frame, rows=row_config, columns=column_config)

    for i in range(3):
        #intro_label = ttk.Label(master=right_frame, text=intro_text)
        #intro_label.grid(row=(i+1), column=1)
        pick_orig_button = ui.create_button(right_frame, 'Исходник', select_file)
        ui.grid_element(pick_orig_button, row=(i+1), column=1, sticky='NSEW')

#endregion




