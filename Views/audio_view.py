from pydispatch import dispatcher
import matplotlib.pyplot as plt
from numpy import max
import asyncio

row_count = 2
column_count = 2
max_amount = row_count * column_count

def set_sender(sender):
    dispatcher.connect(_draw_audio_outputs, signal='audio_changed', sender=sender)


def _draw_audio_outputs(data: dict[str, dict]):

    origin = data["origin"]
    needle = data["needle"]

    try:
        loop = asyncio.get_event_loop()

        loop.create_task(_draw_simple_features(origin_simple=origin["simple_features"], needle_simple=needle["simple_features"]))
        loop.create_task(_draw_shazam_features(origin_shazam=origin["shazam_features"], needle_shazam=needle["shazam_features"]))

    except RuntimeError:
        pass


async def _draw_simple_features(origin_simple, needle_simple):

    subplot_index = 1

    for i in range(len(origin_simple)):

        if subplot_index > max_amount:
            plt.figure()
            subplot_index = 1

        origin_obj = origin_simple[i]
        needle_obj = needle_simple[i]

        plt.subplot(row_count, column_count, subplot_index)
        plt.plot(origin_obj["data"], label='Исходник')
        plt.plot(needle_obj["data"], label='Фрагмент')

        plt.legend(frameon=True, fancybox=True, shadow=True)
        plt.title(origin_obj["label"])
        plt.grid(True)

        subplot_index += 1


async def _draw_shazam_features(origin_shazam, needle_shazam):

    plt.figure()

    samples = [origin_shazam, needle_shazam]

    subplot_index = 1
    for sample in samples:
        if subplot_index > max_amount:
            plt.figure()
            subplot_index = 1

        frequencies = sample["frequencies"]
        times = sample["times"]
        spectrogram = sample["spectrogram"]
        peaks = sample["peaks"]
        fingerprints = sample["fingerprints"]

        plt.subplot(row_count, column_count, subplot_index)

        # Спектрограмма
        plt.pcolormesh(times, frequencies, spectrogram, shading='gouraud', cmap='hot')
        plt.colorbar(label='dB')

        # Пики
        if len(peaks) > 0:
            peak_freqs = [frequencies[f] for f, t in peaks]
            peak_times = [times[t] for f, t in peaks]
            plt.scatter(peak_times, peak_freqs, c='cyan', s=1, alpha=0.5)

        plt.title(f'Спектрограмма + {len(peaks)} пиков')
        plt.xlabel('Время (сек)')
        plt.ylabel('Частота (Hz)')
        plt.legend(frameon=True, fancybox=True, shadow=True)
        plt.grid(True)


        plt.subplot(row_count, column_count, subplot_index+2)
        plt.hist(spectrogram.flatten(), bins=100, alpha=0.7)
        plt.axvline(max(spectrogram) * 0.01, color='red', linestyle='--', label='1% порог')
        plt.title('Распределение амплитуд спектрограммы')
        plt.xlabel('Амплитуда (dB)')
        plt.ylabel('Частота')
        plt.legend(frameon=True, fancybox=True, shadow=True)
        plt.grid(True)

        subplot_index += 1

    plt.show()
