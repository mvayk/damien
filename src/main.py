import math
import os
import sys

import moderngl
import pygame

pygame.init()
pygame.display.set_mode((800, 600), flags=pygame.OPENGL | pygame.DOUBLEBUF, vsync=False)


class Scene:
    def __init__(self):
        self.ctx = moderngl.get_context()

    def render(self):
        now = pygame.time.get_ticks() / 1000.0
        self.ctx.clear(255, 255, 255)


if __name__ == "__main__":
    print("begun")

    scene = Scene()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            scene.render()
            # pygame.display.flip()
