import copy
import numpy as np
from enum import Enum
from crawlitos.math import normalizeVector


class VisualType(Enum):
    Triangle = 1
    Rectangle = 2


class VisualsManager:
    def __init__(self) -> None:
        self.visuals = []

    def append(self, visual):
        self.visuals.append(visual)


class Triangle:
    def __init__(self, a, b, c) -> None:
        self.a = np.array(a)
        self.b = np.array(b)
        self.c = np.array(c)
        self.updateNormal()

    def updateNormal(self):
        a: np.ndarray = self.b - self.a
        b: np.ndarray = self.c - self.a
        self.normal = normalizeVector(np.cross(a, b))

    def vtype(self):
        return VisualType.Triangle


class Rectangle:
    def __init__(self, a, b, c) -> None:
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        self.br = Triangle(a, b, c)
        self.ul = Triangle(a, c, c + a - b)

    def vtype(self):
        return VisualType.Rectangle
