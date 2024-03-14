from musa.generators import sin


class Basic:
    def __init__(self, generator=sin, frequency=360.0, duration=1.0):
        self.generator = generator
        self.frequency = frequency
        self.duration = duration

    def gen(self):
        pass
