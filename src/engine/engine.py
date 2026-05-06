import math
import os
import sys
import struct

import moderngl
import pygame
import numpy as np

import utils.utils as utils

# from PIL import Image;

# constants
WIN_HEIGHT, WIN_WIDTH = 800, 600

class Engine:
    MAXIMUM_FPS = 60
    paused = False
    time = 0
    delta_time = 0

    def __init__(self):
        self.render_queue = [ ]

        pygame.init()
        pygame.display.set_mode((800, 600), flags=pygame.OPENGL | pygame.DOUBLEBUF, vsync=False)
        pygame.display.set_caption("Damien's Doom")
        pygame.event.set_grab(False)
        pygame.mouse.set_visible(True)

        if moderngl.get_context() == None:
            self.ctx = moderngl.create_context()
        else:
            self.ctx = moderngl.get_context()

        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        self.clock = pygame.time.Clock()

        self.program = self.ctx.program(
            vertex_shader=utils.load_file_contents("engine/shaders/default.vert"),
            fragment_shader=utils.load_file_contents("engine/shaders/default.frag")
        )

    def get_ctx(self):
        return self.ctx

    def get_program(self):
        return self.program

    def add_render_queue(self, vao):
        self.render_queue.append(vao)

    def remove_render_queue(self, vao):
        self.render_queue.remove(vao)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("mousebuttondown")
            if event.type == pygame.MOUSEMOTION:
                # dx, dy = event.rel
                print("mouse moved")

    def render(self, vao):
        now = pygame.time.get_ticks() / 1000.0

        self.ctx.screen.use()
        self.ctx.clear(0.0, 0.0, 0.0, 1.0)

        vao.render(moderngl.TRIANGLE_STRIP)

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000.0
            # print(game.health)

            self.handle_events()

            for v in self.render_queue:
                self.render(v)

            pygame.display.flip()
