import numpy as np


class Recorder:
    def __init__(self, path):
        self.file = open(path, 'wb')

    def add_float(self, val):
        self.write(np.array(val))

    def write(self, float_array):
        self.file.write(float_array.tobytes())
        # float_array.tofile(self.file)

    def close(self):
        self.file.close()
