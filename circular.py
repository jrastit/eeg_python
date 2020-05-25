import numpy as np


class Circular:
    def __init__(self, size):
        self.size = size
        self.array = np.array([None] * self.size, np.float64)
        self.ptr = 0

    def add(self, val):
        if self.ptr < self.size:
            self.array[self.ptr] = val
            self.ptr += 1
        else:
            self.array = np.roll(self.array, -1)
            self.array[self.size - 1] = val

    def last(self):
        return self.array[self.ptr - 1]

    def is_not_empty(self):
        if self.ptr > 0:
            return True
        return False
