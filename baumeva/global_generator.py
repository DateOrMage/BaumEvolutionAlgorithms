
class GlobalGenerator:
    def __init__(self):
        self._rnd_seed = None

    @property
    def rnd_seed(self):
        return self._rnd_seed

    @rnd_seed.setter
    def rnd_seed(self, value):
        self._rnd_seed = value


generator = GlobalGenerator()
