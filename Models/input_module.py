from tkinter import filedialog
from pydispatch import dispatcher

def on_origin_picked():
    orig_path = select_file()
    dispatcher.send(signal='origin_changed', sender='input_module', data=orig_path)


def on_needle_picked():
    needle_path = select_file()
    dispatcher.send(signal='needle_changed', sender='input_module', data=needle_path)


def select_file() -> str:
    path = filedialog.askopenfilename(
        title="Select audio file",
        filetypes=[("WAV files", "*.wav"), ("MP3 files", "*.mp3")]
    )

    if path and is_file_valid(path):
        print(f"Выбран файл: {path}")
        # здесь анализ файла
    return path

def is_file_valid(path: str) -> bool:

    #todo add file validation
    return True