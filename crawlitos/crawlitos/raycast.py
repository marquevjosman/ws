import numpy as np
from crawlitos.math import normalizeVector
from crawlitos.visuals import VisualType, Triangle
from crawlitos.globals import EPSILON


class Ray:
    def __init__(self, o: np.ndarray, dir: np.ndarray) -> None:
        self.o = o
        self.dir = normalizeVector(dir)

    def __str__(self) -> str:
        return f"ray({self.o}, {self.dir})"


class Camera:
    def __init__(
        self,
        gm,
        pixels: np.ndarray,
        width: float,
        mindis: float,
        maxdis: float,
    ) -> None:
        # h / w = ph / pw -> h = w * ph / pw
        self.dir = np.array((1, 0, 0))
        self.size = (width, width * pixels.shape[1] / pixels.shape[0])
        self.pos = np.zeros(3)
        self.mindis = mindis
        self.maxdis = maxdis
        self.gm = gm
        self.vm = self.gm.vm
        self.cell = (
            self.size[0] / pixels.shape[0],
            self.size[1] / pixels.shape[1],
        )
        self.pixels = pixels
        self.points = self.calculatePoints()
        self.rays = self.calculateRays()
        # self.writerays()
        # self.writepoints()

    def writerays(self):
        with open("tmp/rays.txt", "w") as file:
            for y in range(self.rays.shape[1]):
                for x in range(self.rays.shape[0]):
                    file.write(f"{self.rays[x, y]}\n")
        print("writerays done")

    def writepoints(self):
        with open("tmp/points.txt", "w") as file:
            for y in range(self.points.shape[1]):
                for x in range(self.points.shape[0]):
                    file.write(
                        f"Point({self.points[x, y, 0]}, {self.points[x, y, 1]}, {self.points[x, y, 2]})\n"
                    )
        print("writepoints done")

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
                rays[x, y] = Ray(np.zeros(3), self.points[x, y])
        return rays

    def calculatePoints(self) -> np.ndarray:
        points = np.empty(self.pixels.shape)
        init = (self.mindis, -self.size[0] / 2, self.size[1] / 2)
        pos = np.array(init)
        delta = (0, self.cell[0] / 2, -self.cell[1] / 2)
        for y in range(points.shape[1]):
            pos[1] = init[1]
            for x in range(points.shape[0]):
                points[x, y] = (pos[0], pos[1] + delta[1], pos[2] + delta[2])
                pos[1] += self.cell[0]
            pos[2] -= self.cell[1]
        return points

    def draw(self):
        for y in range(self.pixels.shape[1]):
            for x in range(self.pixels.shape[0]):
                self.pixels[x, y] = self.pixelAt(x, y)

    def pixelAt(self, x, y):
        ray = self.rays[x, y]
        for visual in self.vm.visuals:
            if visual.vtype() == VisualType.Triangle:
                return self.raytrace(ray, visual)

    def raytrace(self, ray: Ray, tri: Triangle):
        inter = self.intersectTriangle(ray, tri)
        if inter is None:
            return (0, 0, 0)
        else:
            return (255, 255, 255)

    def intersectTriangle(self, ray: Ray, tri: Triangle) -> bool:
        edge1 = tri.b - tri.a
        edge2 = tri.c - tri.a
        raycrosse2 = np.cross(ray.dir, edge2)
        det = np.dot(edge1, raycrosse2)
        if det > -EPSILON and det < EPSILON:
            return None
        inv_det = 1.0 / det
        s = ray.o - tri.a
        u = inv_det * np.dot(s, raycrosse2)
        if u < 0 or u > 1:
            return None
        s_cross_e1 = np.cross(s, edge1)
        v = inv_det * np.dot(ray.dir, s_cross_e1)
        if v < 0 or u + v > 1:
            return None

        t = inv_det * np.dot(edge2, s_cross_e1)
        if t > EPSILON:
            return ray.o + ray.dir * t
        return None
