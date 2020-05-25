import numpy as np


class SourceFile:
    def __init__(self, path):
        self.file = open(path, 'rb')

    def read_all(self):
        float_array = np.fromfile(self.file, dtype=np.float64)
        float_array = np.reshape(float_array, (-1, 4))
        return float_array

    def close(self):
        self.file.close()