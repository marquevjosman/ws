import numpy as np
from scipy.io.wavfile import write
import musa.defaults as defs


class Wave:

    def __init__(
        self,
        duration=defs.duration,
        framerate=defs.framerate,
        channels=defs.channels,
        frames=None,
    ):
        self._framerate = framerate
        if frames is None:
            self._duration = duration
            self._channels = channels
            self._frames = np.zeros(
                (self.durtoframe(duration), channels), dtype=np.float32
            )
            return
        self._frames = frames
        self._channels = frames.shape[1]
        self._duration = self.frametodur(frames.shape[0])

    @property
    def duration(self):
        return self._duration

    @property
    def framerate(self):
        return self._framerate

    @property
    def channels(self):
        return self._channels

    @property
    def size(self):
        return self._frames.shape[0]

    def frametodur(self, frame):
        return frame / self._framerate

    def durtoframe(self, duration):
        return int(duration * self._framerate)

    def save(self, path="tmp/wave.wav"):
        write(path, self._framerate, self._frames)

    def __setitem__(self, key, value):
        self._frames[key] = value

    def __getitem__(self, key):
        return self._frames[key]

    def __add__(self, other):
        frames = np.concatenate((self._frames, other._frames))
        return Wave(framerate=self.framerate, frames=frames)

    def __mul__(self, scalar):
        frames = self._frames * scalar
        return Wave(framerate=self.framerate, frames=frames)

    def findmax(self):
        maxi = 0.0
        for frame in self._frames:
            for c in range(self.channels):
                if frame[c] > maxi:
                    maxi = frame[c]
        return maxi

    def normalize(self):
        self._frames /= self.findmax()
