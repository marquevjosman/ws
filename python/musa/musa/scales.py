from fractions import Fraction
import numpy as np


def limitfrac(f):
    while f < 1:
        f *= 2
    while f >= 2:
        f /= 2
    return f


def getarm(length=3, mul=Fraction(3, 2)):
    arm = np.empty(length, object)
    f = Fraction(1)
    for i in range(length):
        f *= mul
        f = limitfrac(f)
        arm[i] = f
    return arm


def genscale(length=3):
    left = getarm(length, Fraction(2, 3))
    rigth = getarm(length, Fraction(3, 2))
    scale = np.empty(length * 2 + 1, object)
    scale[0] = Fraction(1)
    for i in range(1, 1 + length):
        scale[i] = left[i - 1]
    for i in range(1 + length, scale.size):
        scale[i] = rigth[i - 1 - length]
    scale.sort()
    return scale


def printfracs(scale=[Fraction(1)]):
    for f in scale:
        print(f"({f})", end=" ")
    print()


def getintervals(scale=np.array([Fraction(1)])):
    intervals = np.empty_like(scale)
    for i in range(scale.size):
        right = Fraction(2) if i + 1 == scale.size else scale[i + 1]
        intervals[i] = right / scale[i]
    return intervals


def extscale(scale=np.array([Fraction(1)])):
    ext = np.empty(scale.size * 2, object)
    for i in range(scale.size):
        ext[2 * i] = scale[i]
        ext[2 * i + 1] = limitfrac(scale[i] * Fraction(9, 8))
    ext.sort()
    return ext
