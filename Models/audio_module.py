from typing import Tuple, Dict, Any

from pydispatch import dispatcher
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import ShortTermFeatures
import numpy as np
from librosa import load
from scipy import signal
import asyncio

origins = []

def set_sender(sender):
    dispatcher.connect(on_origin_changed_async_wrapper, signal='origin_changed', sender=sender)
    dispatcher.connect(on_needle_changed_async_wrapper, signal='needle_changed', sender=sender)


def on_origin_changed_async_wrapper(data):
    asyncio.run(on_origin_changed_async_(data))

async def on_origin_changed_async_(data):
    if data not in origins:
        origins.append(data)

    output, file_info = await _get_output(data)
    dispatcher.send(signal='origin_changed', sender='audio_module', data=output)
    dispatcher.send(signal='origin_file_changed', sender='audio_module', data=file_info)


def on_needle_changed_async_wrapper(data):
    asyncio.run(on_needle_changed_async(data))

async def on_needle_changed_async(data):
    output, file_info = await _get_output(data)
    dispatcher.send(signal='needle_changed', sender='audio_module', data=output)
    dispatcher.send(signal='needle_file_changed', sender='audio_module', data=file_info)


async def _get_output(file_path: str) -> tuple[dict[str, dict | list], dict[str, str | Any]]:

    [F, f_names], [Fs, x] = await extract_features_safe_async(file_path)

    output = {
        "simple_features": _get_simple_features(F, f_names),
        "shazam_features": _get_shazam_features(Fs, x)
    }

    audio_length_sec = len(x) / Fs

    file_info = {
        "File Name": file_path,
        "Length": f"{int(audio_length_sec / 60)}:{int(audio_length_sec % 60)}",
        "Tags":  F.shape[0],
        "Windows": F.shape[1],
        "peaks": output["shazam_features"]["peaks"],
        "frequencies": output["shazam_features"]["frequencies"],
        "fingerprints": output["shazam_features"]["fingerprints"]
    }

    return output, file_info


#region Simple Features

def _get_simple_features(Fs, f_names) -> list:

    # центр масс спектра,
    # верхняя частотная граница,изменение спектра во времени, ширина распределения частот
    features = ['spectral_centroid', 'spectral_rolloff', 'spectral_flux', 'spectral_spread']


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

def _extract_features_safe(file_path):
    try:
        #Fs, x = aIO.read_audio_file(file_path)
        x, Fs = load(file_path, sr=None, mono=True)
        #sr=22050

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

        return [F, f_names], [Fs, x]

    except Exception as e:
        print(f"Ошибка при обработке {file_path}: {e}")
        return None, None

async def extract_features_safe_async(file_path):
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: _extract_features_safe(file_path)
        )
        return result

    except Exception as e:
        print(f"Ошибка при обработке {file_path}: {e}")
        return None, None



#endregion

#region Shazam Features

def _get_shazam_features(Fs, f_names) -> dict:

    frequencies, times, spectrogram = create_shazam_spectrogram(f_names, Fs)
    #frequencies, times, spectrogram = create_high_res_spectrogram(f_names, Fs)
    #peaks = find_spectral_peaks_improved(spectrogram)
    peaks = find_spectral_peaks_2d(spectrogram)
    fingerprints = create_audio_fingerprints(peaks, frequencies, times, fan_value=8)

    return {
        "frequencies": frequencies,
        "times": times,
        "spectrogram": spectrogram,
        "peaks": peaks,
        "fingerprints": fingerprints
    }




def create_shazam_spectrogram(audio, Fs, win_len=0.040, hop_len=0.020):
    frequencies, times, Sxx = signal.spectrogram(
        audio, Fs,
        nperseg=int(win_len * Fs),
        noverlap=int((win_len - hop_len) * Fs),
        window='hann',
        scaling='spectrum'
    )
    return frequencies, times, 10 * np.log10(Sxx + 1e-10)  # в dB

def create_high_res_spectrogram(audio, Fs, win_len=0.040, hop_len=0.010):  # hop_len было 0.020
    """Спектрограмма с большим временным разрешением"""
    frequencies, times, Sxx = signal.spectrogram(
        audio, Fs,
        nperseg=int(win_len * Fs),
        noverlap=int((win_len - hop_len) * Fs),  # больше перекрытие
        window='hann',
        scaling='spectrum'
    )
    return frequencies, times, 10 * np.log10(Sxx + 1e-10)



def find_spectral_peaks(spectrogram, threshold_db=-30):
    peaks = []
    height = np.max(spectrogram) + threshold_db

    print(f"Максимум спектрограммы: {np.max(spectrogram):.1f} dB")
    print(f"Порог для пиков: {height:.1f} dB")

    for time_idx in range(spectrogram.shape[1]):
        for freq_idx in range(1, spectrogram.shape[0] - 1):
            current = spectrogram[freq_idx, time_idx]
            # Проверяем локальный максимум
            if (current > height and
                    current > spectrogram[freq_idx - 1, time_idx] and
                    current > spectrogram[freq_idx + 1, time_idx]):
                peaks.append((freq_idx, time_idx))
    return peaks


def find_spectral_peaks_improved(spectrogram, prominence=3, width=2):
    from scipy.signal import find_peaks
    peaks = []

    # Ищем пики в каждом временном срезе
    for time_idx in range(spectrogram.shape[1]):
        # Берем спектр в момент времени time_idx
        spectrum = spectrogram[:, time_idx]

        # Ищем пики с заданной prominence (выдающиеся над окружением)
        freq_indices, properties = find_peaks(
            spectrum,
            prominence=prominence,  # минимальная prominence
            width=width,  # минимальная ширина пика
            distance=5  # минимальное расстояние между пиками
        )

        for freq_idx in freq_indices:
            peaks.append((freq_idx, time_idx))

    print(f"Найдено {len(peaks)} пиков с prominence={prominence}")
    return peaks


def find_spectral_peaks_2d(spectrogram, freq_prominence=2, time_prominence=1):
    """Ищем пики и по частоте и по времени"""
    from scipy.signal import find_peaks
    peaks = []

    # Сначала ищем кандидатов по частоте
    for time_idx in range(spectrogram.shape[1]):
        spectrum = spectrogram[:, time_idx]
        freq_indices, _ = find_peaks(spectrum, prominence=freq_prominence, distance=3)

        for freq_idx in freq_indices:
            # Проверяем что это также пик по времени
            if time_idx > 0 and time_idx < spectrogram.shape[1] - 1:
                time_slice = spectrogram[freq_idx, :]
                if (spectrogram[freq_idx, time_idx] > spectrogram[freq_idx, time_idx - 1] and
                        spectrogram[freq_idx, time_idx] > spectrogram[freq_idx, time_idx + 1]):
                    peaks.append((freq_idx, time_idx))

    print(f"2D поиск пиков: {len(peaks)}")
    return peaks


# Попробуйте это сразу - более агрессивный поиск пиков
def find_spectral_peaks_simple(spectrogram, threshold_ratio=0.7):
    """Ищем пики как локальные максимумы выше порога"""
    peaks = []
    threshold = np.max(spectrogram) * threshold_ratio

    for time_idx in range(spectrogram.shape[1]):
        for freq_idx in range(1, spectrogram.shape[0] - 1):
            current = spectrogram[freq_idx, time_idx]
            # Проверяем что это локальный максимум по частоте
            if (current > threshold and
                    current > spectrogram[freq_idx - 1, time_idx] and
                    current > spectrogram[freq_idx + 1, time_idx]):
                peaks.append((freq_idx, time_idx))

    print(f"Порог: {threshold:.1f}, найдено пиков: {len(peaks)}")
    return peaks


def create_audio_fingerprints(peaks, frequencies, times, fan_value=5):
    fingerprints = []

    for i, (freq_idx1, time_idx1) in enumerate(peaks):
        freq1 = frequencies[freq_idx1]
        time1 = times[time_idx1]

        # Берем больше следующих пиков для создания пар
        for j in range(i + 1, min(i + fan_value + 1, len(peaks))):
            freq_idx2, time_idx2 = peaks[j]
            freq2 = frequencies[freq_idx2]
            time2 = times[time_idx2]
            time_delta = time2 - time1

            # Расширяем временные рамки для пар
            if 0.05 <= time_delta <= 2.0:  # было 0.1-1.0
                hash_key = hash((int(freq1), int(freq2), round(time_delta, 2)))
                fingerprints.append((hash_key, time1))

    print(f"Пиков: {len(peaks)}, fan_value: {fan_value}, отпечатков: {len(fingerprints)}")
    return fingerprints


#endregion