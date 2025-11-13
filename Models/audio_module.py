from pydispatch import dispatcher
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import ShortTermFeatures
import numpy as np


import matplotlib.pyplot as plt

origins = []

def set_sender(sender):
    dispatcher.connect(on_origin_changed, signal='origin_changed', sender=sender)
    dispatcher.connect(on_needle_changed, signal='needle_changed', sender=sender)


def on_origin_changed(data):

    if data not in origins:
        origins.append(data)

    output = _get_output(data)
    dispatcher.send(signal='origin_changed', sender='audio_module', data=output)

def on_needle_changed(data):
    output = _get_output(data)
    dispatcher.send(signal='needle_changed', sender='audio_module', data=output)


def _get_output(file_path: str) -> dict[str, list]:
    output = {
        "simple_features": _get_simple_features(file_path)
    }

    return output


#region Simple Features

def _get_simple_features(data: str) -> list:
    Fs, f_names = extract_features_safe(data)
    features = ['spectral_centroid', 'spectral_rolloff', 'spectral_flux']

    simple_features = []

    for i in range(len(features)):

        index = f_names.index(features[i])

        simple = {
            "data": Fs[index, :],
            "x_label": 'Frame no',
            "label": features[i]
        }

        simple_features.append(simple)

    return simple_features

def extract_features_safe(data):
    try:
        Fs, x = aIO.read_audio_file(data)

        if len(x.shape) > 1:
            x = x.mean(axis=1)

        x = x / np.max(np.abs(x))

        min_samples = int(0.050 * Fs)
        if len(x) < min_samples:
            print(f"Предупреждение: файл короткий, добавлен padding")
            padding = min_samples - len(x)
            x = np.pad(x, (0, padding), mode='constant')

        F, f_names = ShortTermFeatures.feature_extraction(
            x, Fs,
            int(0.050 * Fs),
            int(0.025 * Fs)
        )

        print(f"Успешно извлечено {F.shape[0]} признаков")
        print(f"Количество окон: {F.shape[1]}")

        return F, f_names

    except Exception as e:
        print(f"Ошибка при обработке {data}: {e}")
        return None, None

#endregion
