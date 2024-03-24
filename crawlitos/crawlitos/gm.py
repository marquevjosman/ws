import pygame
from crawlitos.globals import *
from crawlitos.raycast import Camera
from crawlitos.visuals import VisualsManager, Triangle
import numpy as np


class GameManager:
    _instance = None

    @staticmethod
    def build():
        GameManager._instance = GameManager()

    @staticmethod
    def instance():
        return GameManager._instance

    def __init__(self) -> None:
        print("crawlitos")
        pygame.init()
        self.screen = pygame.display.set_mode(DISPLAY_SIZE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.origsurf = pygame.Surface(SURFACE_SIZE, 0, 24)
        self.origsurf.fill((16, 16, 16))
        self.scalsurf = pygame.Surface(SCALED_SIZE, 0, 24)
        pixels = pygame.surfarray.pixels3d(self.origsurf)
        # self.pixels[0, 0] = (255, 255, 255)
        self.vm = VisualsManager()
        self.camera = Camera(self, pixels, 24.0, 12.0, 60.0)
        x = 12.0
        y = 12.0
        z = 6.0
        tri = Triangle((x, -y, -z), (x, y, -z), (x, y, z))
        # print(tri)
        self.vm.append(tri)

    def run(self):
        self.loop()
        self.cleanup()

    def cleanup(self):
        pygame.quit()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self):
        self.startdraw()
        self.camera.draw()
        self.enddraw()

    def startdraw(self):
        self.screen.fill((64, 16, 32))

    def enddraw(self):
        pygame.transform.scale(self.origsurf, self.scalsurf.get_size(), self.scalsurf)
        self.screen.blit(self.scalsurf, (0, 0))
        pygame.display.flip()

    def loop(self):
        while self.running:
            self.update()
            self.draw()
            self.clock.tick(30)
