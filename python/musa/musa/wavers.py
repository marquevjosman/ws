from musa.waves import Wave
import musa.defaults as defs
import numpy as np


class Basic:
    def __init__(
        self,
        frequency=defs.frequency,
        duration=defs.duration,
        generator=defs.generator,
        framerate=defs.framerate,
        channels=defs.channels,
    ):
        self.generator = generator
        self.frequency = frequency
        self.duration = duration
        self.framerate = framerate
        self.channels = channels

    def gen(
        self,
        frequency=None,
        duration=None,
        generator=None,
        framerate=None,
        channels=None,
    ):
        if generator is None:
            generator = self.generator
        if frequency is None:
            frequency = self.frequency
        if duration is None:
            duration = self.duration
        if framerate is None:
            framerate = self.framerate
        if channels is None:
            channels = self.channels
        wave = Wave(duration, framerate, channels)
        for frame in range(wave.size):
            seconds = wave.frametodur(frame)
            x = seconds * frequency % 1.0
            wave[frame] = np.full(channels, generator(x), np.float32)
        return wave
