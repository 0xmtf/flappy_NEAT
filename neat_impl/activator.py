import math


class Activator:
    def __init__(self, name="sigmoid"):
        self.name = name
        self.funcs = {
            "sigmoid": self._sigmoid,
            "tanh": self._tanh
        }

    def get_func(self):
        return self.funcs[self.name]

    def compute_func(self, x):
        return self.funcs[self.name](x)

    @staticmethod
    def _sigmoid(x):
        x = max(-60.0, min(60.0, 5.0 * x))
        return 1.0 / (1.0 + math.exp(-x))

    @staticmethod
    def _tanh(x):
        x = max(-60.0, min(60.0, 2.5 * x))
        return math.tanh(x)
