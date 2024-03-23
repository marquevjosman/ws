import numpy as np
from crawlitos.math import normalizeVector
from crawlitos.visuals import VisualType, Triangle


class Ray:
    def __init__(self, o: np.ndarray, dir: np.ndarray) -> None:
        self.o = o
        self.dir = normalizeVector(dir)


class Camera:
    def __init__(
        self,
        gm,
        pixels: np.ndarray,
        width: float,
        pos: np.ndarray,
        mindis: float,
        maxdis: float,
        dir: np.ndarray = np.array((0, 0, 1)),
    ) -> None:
        # h / w = ph / pw -> h = w * ph / pw
        self.size = (width, width * pixels.shape[1] / pixels.shape[0])
        self.pixels = pixels
        self.pos = pos
        self.mindis = mindis
        self.maxdis = maxdis
        self.gm = gm
        self.vm = self.gm.vm
        print(pixels.shape)
        self.dir = normalizeVector(dir)
        self.cell = (
            self.size[0] / pixels.shape[0],
            self.size[1] / pixels.shape[1],
        )
        self.points = self.calculatePoints()
        self.rays = self.calculateRays()

    def calculateRays(self) -> np.ndarray:
        rays = np.empty(
            (
                self.pixels.shape[0],
                self.pixels.shape[1],
            ),
            object,
        )
        for y in range(rays.shape[1]):
            for x in range(rays.shape[0]):
                rays[x, y] = Ray(np.zeros(3), self.points[x, y] - np.zeros(3))
        return rays

    def calculatePoints(self) -> np.ndarray:
        points = np.empty(self.pixels.shape)
        pos = (-self.size[0] / 2, self.size[1] / 2)
        delta = (self.cell[0] / 2, -self.cell[1] / 2)
        for y in range(points.shape[1]):
            for x in range(points.shape[0]):
                points[x, -y] = (pos[0] + delta[0], pos[1] + delta[1], self.mindis)
                pos = (pos[0] + self.cell[0], pos[1] - self.cell[1], self.mindis)
        return points

    def draw(self):
        for y in range(self.pixels.shape[1]):
            for x in range(self.pixels.shape[0]):
                color = self.pixelAt(x, y)
                if color:
                    print(x, y)
                if color:
                    self.pixels[x, y] = color
                else:
                    self.pixels[x, y] = (0, 0, 0)

    def pixelAt(self, x, y):
        ray = self.rays[x, -y]
        for visual in self.vm.visuals:
            if visual.vtype() == VisualType.Triangle:
                return self.raytrace(ray, visual)
            if visual.vtype() == VisualType.Rectangle:
                color = self.raytrace(ray, visual.br)
                if color:
                    return color
                return self.raytrace(ray, visual.ul)

    def raytrace(self, ray: Ray, tri: Triangle):
        denom = np.dot(tri.normal, ray.dir)
        if denom < 1e-6:
            return None
        t = np.dot(tri.a - ray.o, tri.normal) / denom
        return (255, 255, 255) if t > self.mindis and t < self.maxdis else None
