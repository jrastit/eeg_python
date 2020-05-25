import numpy as np

from circular import Circular


class Wave:

    def __init__(self, min_frequency, max_frequency, db=None):
        self.min = min_frequency
        self.max = max_frequency
        self.min_index = 0
        self.max_index = 0
        self.val_array = []
        self.val = 0
        self.short_history_list = []
        self.history_list = Circular(6 * 30)
        self.db = db

    def clear(self):
        self.val_array = []
        self.val = 0

    def update(self):
        self.val = np.median(self.val_array)
        self.short_history_list += [self.val]
        if len(self.short_history_list) >= 10:
            history_ptr = np.median(self.short_history_list)
            self.short_history_list = []
            self.history_list.add(history_ptr)
            if self.db and history_ptr and not isinstance(history_ptr, complex):
                value = int((np.log10(history_ptr) - 2) * 100 / 2)
                if value < 0:
                    value = 0
                if value > 100:
                    value = 100
                print value
                # self.db.add("wave", value)
