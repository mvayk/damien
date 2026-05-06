import math
import os
import sys
import struct

import moderngl
import pygame
import numpy as np

import utils.utils as utils

# from PIL import Image;

class Engine:
    MAXIMUM_FPS = 60
    paused = False
    time = 0
    delta_time = 0

    def __init__(self):
        pygame.init()
        pygame.display.set_mode((800, 600), flags=pygame.OPENGL | pygame.DOUBLEBUF, vsync=False)
        pygame.display_set_caption("Damien's Doom")
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(True)

        if moderngl.get_context() == None:
            self.ctx = moderngl.create_context()
        else:
            self.ctx = moderngl.get_context()

        self.ctx.enable(mgl.DEPTH_TEST | mgl.CULL_FACE)
        self.clock = pygame.time.Clock()

        self.program = self.ctx.program(
            vertex_shader=utils.load_file_contents("engine/shaders/default.vert"),
            fragment_shader=utils.load_file_contents("engine/shaders/default.frag")
        )

        x = np.linspace(-1.0, 1.0, 50)
        y = np.random.rand(50) - 0.5
        r = np.zeros(50)
        g = np.ones(50)
        b = np.ones(50)

        vertices = np.dstack([x, y, r, g, b])
        self.vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
        self.vao = self.ctx.simple_vertex_array(self.program, self.vbo, 'in_vert', 'in_color')

    def render(self, vao):
        now = pygame.time.get_ticks() / 1000.0
        self.ctx.screen.use()
        self.ctx.clear(0.0, 0.0, 0.0, 1.0)
        vao.render(moderngl.TRIANGLE_STRIP)

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                self.render(self.vao)
                pygame.display.flip()
