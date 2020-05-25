import matplotlib.pyplot as plt


class Figure:
    def __init__(self, name):
        self.fig = plt.figure(name)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_title(name)
        self.ax.plot([])
        self.fig.canvas.draw()
        plt.show(block=False)

    def clear(self):
        self.ax.clear()

    def draw(self):
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def plot(self, data):
        self.ax.plot(data)

    def plot2(self, data, y):
        self.ax.plot(data, y)

    def semilogy(self, data):
        self.ax.semilogy(data)

    def semilogy2(self, data, data2):
        self.ax.semilogy(data, data2)

    def set_xlim(self, val):
        self.ax.set_xlim(val)

    def set_ylim(self, val):
        self.ax.set_ylim(val)
