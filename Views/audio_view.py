from pydispatch import dispatcher
import matplotlib.pyplot as plt

row_count = 2
column_count = 2

def set_sender(sender):
    dispatcher.connect(_draw_audio_outputs, signal='audio_changed', sender=sender)


def _draw_audio_outputs(data: dict[str, dict]):

    origin = data["origin"]
    needle = data["needle"]

    _draw_simple_features(origin_simple=origin["simple_features"], needle_simple=needle["simple_features"])

def _draw_simple_features(origin_simple, needle_simple):

    max_amount = row_count * column_count

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

    plt.show()





