import json

from .utils import obj_to_ref


class Callback(object):

    def __init__(self, func: None, data: None):
        if isinstance(func, str):
            self.callback_func = func
        else:
            self.callback_func = obj_to_ref(func)
        self.callback_data = data

    def as_json(self):
        return json.dumps({
            'callback_func': self.callback_func,
            'callback_data': self.callback_data,
        })
