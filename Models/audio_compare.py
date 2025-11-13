from pydispatch import dispatcher

_audio_outputs = {
    "origin": {},
    "needle": {}
}


def set_sender(sender):
    dispatcher.connect(set_origin, signal='origin_changed', sender=sender)
    dispatcher.connect(set_needle, signal='needle_changed', sender=sender)



def set_origin(data):
    _audio_outputs["origin"] = data
    _try_update_plots()

def set_needle(data):
    _audio_outputs["needle"] = data
    _try_update_plots()


def _try_update_plots():

    if _audio_outputs["origin"] and _audio_outputs["needle"]:
        dispatcher.send(signal='audio_changed', sender='audio_compare', data=_audio_outputs)







