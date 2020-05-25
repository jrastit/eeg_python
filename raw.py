import threading
import numpy as np
from sqlite import Sqlite

from channel import Channel
from figure import Figure


class Raw:
    def __init__(self, db_path=None):
        self.channel = []
        for i in range(4):
            self.channel.append(Channel(self))
        for i in range(4):
            filter_channel = Channel(self)
            self.channel[i].filter_channel = filter_channel
            self.channel.append(filter_channel)
        self.freq = 220
        self.duration = 10
        self.lock = threading.Lock()
        self.figure = {}
        self.nb_val = 0
        self.plot = [1]
        self.db_path = db_path
        self.db = None

    def add_float(self, val):
        self.lock.acquire()
        for i in range(4):
            self.channel[i].add_value(val[i])
        self.nb_val += 1
        if self.nb_val % self.freq == 0:
            self.refresh()
            self.refresh_plot()
        if self.nb_val % (self.freq * self.duration) == 0:
            self.refresh_plot2()
        self.lock.release()

    def get_figure(self, name):
        figure = self.figure.get(name)
        if not figure:
            figure = Figure(name)
            self.figure.update({name: figure})
        return figure

    def refresh(self):
        if not self.db:
            self.db = Sqlite(self.db_path)
        for channel in self.channel:
            channel.refresh()
            # channel.update_wave()

        i = 1
        val = (4 - self.channel[i].frequency_list.frequency_list[0].history.last()) * 100 / 4
        if self.db and not np.isnan(val):
            print "val", val
            self.db.add("wave", int(val))

    def plot_raw(self):
        for i in self.plot:
            figure = self.get_figure('raw_' + str(i))
            figure.clear()
            nb_point = self.channel[i].val_list.size
            y = np.arange(-nb_point, 0.0, 1)
            y = y / self.channel[i].nb_point_s
            figure.plot2(y, self.channel[i].val_list.array)
            figure.plot2([y[0], y[-1]], [[self.channel[i].mean], [self.channel[i].mean]])
            figure.plot2([y[0], y[-1]], [[self.channel[i].max], [self.channel[i].max]])
            figure.plot2([y[0], y[-1]], [[self.channel[i].min], [self.channel[i].min]])
            figure.plot2([y[-1] - 1, y[-1]], [[self.channel[i].short_mean], [self.channel[i].short_mean]])
            figure.plot2([y[-1] - 1, y[-1]], [[self.channel[i].short_max], [self.channel[i].short_max]])
            figure.plot2([y[-1] - 1, y[-1]], [[self.channel[i].short_min], [self.channel[i].short_min]])
            # figure.set_xlim([0, -2])
            figure.draw()

    def plot_freq(self):
        for i in self.plot:
            figure = self.get_figure('freq_' + str(i))
            figure.clear()
            figure.semilogy2(self.channel[i].freq, self.channel[i].y)
            for w in self.channel[i].wave_list:
                if w.min_index > 0:
                    figure.semilogy2(
                        self.channel[i].freq[w.min_index:w.max_index + 1],
                        [w.val] * (w.max_index + 1 - w.min_index))
            figure.set_xlim([0, 50])
            figure.set_ylim([0.1, 10000])
            figure.draw()

    def plot_freq2(self):
        for i in self.plot:
            figure = self.get_figure('freq2_' + str(i))
            figure.clear()
            for frequency in self.channel[i].frequency_list.frequency_list:
                # result = [np.median(delta.array) for delta in frequency.delta_list]
                # figure.plot(np.concatenate((result, result)))
                figure.plot(frequency.history.array)
            # figure.set_ylim([-5, 5])
            figure.set_ylim([0, 5])
            figure.draw()


    def plot_history(self):
        for i in self.plot:
            figure = self.get_figure('hist_' + str(i))
            figure.clear()
            for w in self.channel[i].wave_list:
                figure.semilogy(w.history_list.array)
            figure.set_ylim([10, 10000])
            figure.draw()

    def plot_compare(self):
        for i in self.plot:
            figure = self.get_figure('comp_' + str(i))
            figure.clear()
            figure.semilogy(
                self.channel[i].wave_list[0].history_list.array / self.channel[i].wave_list[1].history_list.array)
            figure.semilogy(
                self.channel[i].wave_list[2].history_list.array / self.channel[i].wave_list[3].history_list.array)
            figure.draw()

    def refresh_plot(self):
        print 'plot'
        # self.plot_raw()
        # self.plot_freq()
        # self.plot_freq2()

    def refresh_plot2(self):
        print 'plot2'
        # self.plot_history()
        # self.plot_compare()
