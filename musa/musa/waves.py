import numpy as np
from scipy.io.wavfile import write


class Wave:
    duration = 3.0
    framerate = 44_100
    channels = 2

    def __init__(self, duration=duration, framerate=framerate, channels=channels):
        self.duration = duration
        self.framerate = framerate
        self.channels = channels
        self.frames = np.zeros((self.durtoframe(duration), channels), dtype=np.float32)

    def frametodur(self, frame):
        return frame / self.framerate

    def durtoframe(self, duration):
        return int(duration * self.framerate)

    @staticmethod
    def static():
        print(Wave.duration)
        print(Wave.framerate)
        print(Wave.channels)

    def save(self, path="tmp/wave.wav"):
        write(path, self.framerate, self.frames)

    def __setitem__(self, key, value):
        self.frames[key] = value

    def __getitem__(self, key):
        return self.frames[key]
