'''
Распознавание сигналов, голоса и т.п.
Представить образец сигнала для анализа и осуществлять поиск в текущем сигнале.
Сигнал может содержать несколько частот.
Программа должна сообщать, когда образец сигнала соответствует текущему сигналу

'''

import Models.input_module as inp
import Models.audio_module as aud
import Models.audio_compare as auc
import Views.input_form as form
import Views.audio_view as auv

behaviour = {
    "on_origin_picked": inp.on_origin_picked,
    "on_needle_picked": inp.on_needle_picked
}


aud.set_sender('input_module')
auc.set_sender('audio_module')
auv.set_sender('audio_compare')


form.draw_form(behaviour)
form.start_main_loop()

