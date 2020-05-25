from circular import Circular

import numpy as np


class FrequencyList:
    def __init__(self, step_range):
        self.frequency_list = []
        self.step_range = step_range
        for step in self.step_range:
            self.frequency_list.append(Frequency(step))

    def add_value(self, array):
        for frequency in self.frequency_list:
            index_ceil = int(np.ceil(frequency.step / 2))
            index_floor = int(np.floor(frequency.step / 2))
            index = np.array([- frequency.step - frequency.step,
                              -frequency.step - index_ceil,
                              -frequency.step - index_floor,
                              - frequency.step,
                              - index_ceil,
                              - index_floor,
                              0]) - 1
            avg_base = (np.mean(array[index[0]:index[3]]) - np.mean(array[index[3]:index[6]])) / 2
            delta = np.mean(array[index[2]:index[3]]) - np.mean(array[index[3]:index[4]])
            frequency.add_value(delta - avg_base)

    def update(self):
        for frequency in self.frequency_list:
            frequency.update()


class Frequency:
    def __init__(self, step):
        self.step = step
        self.delta_list = []
        for i in range(self.step):
            self.delta_list.append(Circular(10))
        self.ptr = 0
        self.median = 0
        self.val = 0
        self.history = Circular(60)

    def add_value(self, value):
        self.delta_list[self.ptr].add(value)
        self.ptr += 1
        if self.ptr == self.step:
            self.ptr = 0

    def update(self):
        self.median = [np.median(delta.array) for delta in self.delta_list]
        self.val = np.max(np.abs(self.median))
        self.history.add(self.val)
