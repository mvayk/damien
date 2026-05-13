import math
import os
import struct
import sys

import moderngl
import numpy as np
import pygame

import engine.camera as camera
import utils.utils as utils

# from PIL import Image;

# constants
class Engine:
    def __init__(self):
        self.games = [ ]
        self.render_queue = []

        self.mouse_captured = True;

        self.WIN_SIZE = (800, 600)

        pygame.init()
        pygame.display.set_mode(
            (self.WIN_SIZE), flags=pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE, vsync=False
        )
        pygame.display.set_caption("")
        pygame.event.set_grab(True)

        # camera movement breaks when cursor reaches edge of window border
        pygame.mouse.set_visible(False)

        if moderngl.get_context() == None:
            self.ctx = moderngl.create_context()
        else:
            self.ctx = moderngl.get_context()

        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.DEPTH_TEST)
        self.clock = pygame.time.Clock()

        self.program = self.ctx.program(
            vertex_shader=utils.load_file_contents("engine/shaders/default.vert"),
            fragment_shader=utils.load_file_contents("engine/shaders/default.frag"),
        )

    def set_window_caption(self, caption: str):
        pygame.display.set_caption(caption)

    def create_camera(self):
        self.camera = camera.Camera(self.WIN_SIZE)
        return self.camera

    def get_ctx(self):
        return self.ctx

    def get_program(self):
        return self.program

    def add_render_queue(self, vao):
        self.render_queue.append(vao)

    def remove_render_queue(self, vao):
        self.render_queue.remove(vao)

    def add_game_queue(self, game):
        self.games.append(game)

    def remove_game_queue(self, game):
        self.games.remove(game)

    def handle_events(self):
        if not hasattr(self, "camera"):
            print("game hasnt initialized camera, events not being checked.")
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("[ENGINE] Exiting")
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_F1:
                        print("[ENGINE] Releasing Cursor")
                        self.mouse_captured = not self.mouse_captured
                        pygame.mouse.set_visible(not self.mouse_captured)
                        pygame.event.set_grab(self.mouse_captured)
                if event.type == pygame.MOUSEMOTION and self.mouse_captured:
                    cx, cy = self.camera.win_size[0] // 2, self.camera.win_size[1] // 2
                    if event.pos != (cx, cy):
                        pygame.mouse.set_pos(cx, cy)
                    else:
                        continue
                    dx, dy = event.rel
                    self.camera.mouse_look(dx, dy)
                if event.type == pygame.VIDEORESIZE:
                    self.camera.win_size = (event.w, event.h)
                    self.ctx.viewport = (0, 0, event.w, event.h)

    def render(self, vao):
        now = pygame.time.get_ticks() / 1000.0

        # self.ctx.screen.use()
        self.ctx.clear(0.3, 0.2, 0.2, 1.0)

        self.program['m_proj'].write(self.camera.get_proj_matrix().tobytes()) # type: ignore
        self.program['m_view'].write(self.camera.get_view_matrix().tobytes()) # type: ignore
        self.program['m_model'].write(np.eye(4, dtype='f4').tobytes()) # type: ignore

        vao.render()

    def run(self):
        while True:
            self.dt = self.clock.tick(60) / 1000.0

            self.handle_events()

            for v in self.games:
                v.events()

            for v in self.render_queue:
                self.render(v)

            pygame.display.flip()
