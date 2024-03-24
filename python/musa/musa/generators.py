import math


def sin(x):
    return math.sin(2.0 * math.pi * x)


def sqr(x):
    return 1.0 if x < 0.5 else -1.0


def saw(x):
    return 1 - 2.0 * x


def tri(x):
    if x < 0.25:
        return 4.0 * x
    if x < 0.75:
        return 2.0 - 4.0 * x
    return 4.0 * x - 4
