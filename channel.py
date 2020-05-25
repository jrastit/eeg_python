import numpy as np
from circular import Circular

from frequency import FrequencyList
from wave import Wave


class Channel:
    def __init__(self, parent, db=None):
        self.parent = parent
        self.figure = {}
        self.wave_list = [
            Wave(0.5, 4.0, db),
            Wave(4.0, 8.0),
            Wave(8.0, 12.0),
            Wave(12.0, 35.0),
            Wave(35.0, 50.0)]
        # self.wave_list = []
        # for i in range(16):
        #     self.wave_list.append(Wave(i/2.0, i/2.0 + 0.5))
        self.nb_point_s = 220
        self.duration = 10
        self.nb_fft = 2

        self.val_list = Circular(self.nb_point_s * self.duration + self.nb_fft - 1)
        self.filter_channel = None

        self.mean = 0
        self.short_mean = 0
        self.max = 0
        self.short_max = 0
        self.min = 0
        self.short_min = 0
        self.state = 0
        self.y = np.array([0], dtype=np.float64)
        self.freq = np.array([0], dtype=np.float64)
        self.frequency_list = FrequencyList([
            int(round(self.nb_point_s / 2.0)),
            int(round(self.nb_point_s / 6.0)),
            int(round(self.nb_point_s / 10.0)),
            int(round(self.nb_point_s / 24.0)),
            int(round(self.nb_point_s / 42.0))])

    def add_value(self, val):
        self.val_list.add(val)
        self.frequency_list.add_value(self.val_list.array)
        if self.filter_channel is not None:
            self.filter_channel.add_value(self.val_list.array[-11] -
                                          np.mean(self.val_list.array[-22:]) +
                                          np.median(self.val_list.array[-2200:]))

    def update_wave(self):
        for w in self.wave_list:
            w.clear()

        for l in range(self.nb_fft):
            start = l - self.val_list.size
            stop = -(self.nb_fft - 1 - l)
            if stop < 0:
                my_list = self.val_list.array[start:stop]
            else:
                my_list = self.val_list.array[start:]
            if len(my_list) >= self.nb_point_s:
                self.y = np.fft.fft(my_list)
                self.freq = np.fft.fftfreq(len(my_list), 1.0 / self.nb_point_s)

                for w in self.wave_list:
                    w.min_index = 0
                    w.max_index = 0
                    for i in range(len(my_list)):
                        if w.max >= self.freq[i] >= w.min:
                            if w.min_index == 0:
                                w.min_index = i
                            w.max_index = i
                    # print w.min, w.min_index, w.max_index
                    w.val_array.append(np.percentile(self.y[w.min_index:w.max_index + 1], [75]))
                    # w.val_array.append(np.mean(self.y[w.min_index:w.max_index + 1]))

        for w in self.wave_list:
            w.update()

    def refresh(self):
        if self.val_list.is_not_empty:
            self.mean = np.mean(self.val_list.array)
            self.max = np.max(self.val_list.array)
            self.min = np.min(self.val_list.array)
            short = self.val_list.array[-self.nb_point_s:]
            self.short_mean = np.mean(short)
            self.short_max = np.max(short)
            self.short_min = np.min(short)

            if 900 > self.mean > 800:
                self.state = 3
                if self.max - self.min < 100:
                    self.state = 2
                if self.max - self.min < 25:
                    self.state = 1
            else:
                self.state = 4

            self.frequency_list.update()
