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
        self.billboard_program = self.ctx.program(
            vertex_shader=utils.load_file_contents("engine/shaders/billboard.vert"),
            fragment_shader=utils.load_file_contents("engine/shaders/billboard.frag"),
        )
        self.skybox_program = self.ctx.program(
            vertex_shader=utils.load_file_contents("engine/shaders/skybox.vert"),
            fragment_shader=utils.load_file_contents("engine/shaders/skybox.frag"),
        )

        self.program["light_pos"].value = (0, 20, 0) # type: ignore

    def create_skybox(self, top, bottom):
        from engine.skybox import Skybox
        skybox = Skybox(self.ctx, self.skybox_program, top, bottom)
        self.add_render_queue(skybox)
        return skybox

    def set_window_caption(self, caption: str):
        pygame.display.set_caption(caption)

    def create_camera(self):
        self.camera = camera.Camera(self.WIN_SIZE)
        return self.camera

    def get_ctx(self):
        return self.ctx

    def get_program(self):
        return self.program

    def add_render_queue(self, thing):
        self.render_queue.append(thing)

    def remove_render_queue(self, thing):
        self.render_queue.remove(thing)

    def add_game_queue(self, game):
        self.games.append(game)

    def remove_game_queue(self, game):
        self.games.remove(game)

    def create_billboard(self, pos, texture_path, size=1.0):
        from engine.billboard import Billboard
        billboard = Billboard(self.ctx, self.billboard_program, texture_path, pos, size)
        self.add_render_queue(billboard)
        return billboard

    def create_structure(self, p1, p2, p3, p4, color):
        from engine.nonentity import Nonentity
        nonentity = Nonentity(self.ctx, self.program, p1, p2, p3, p4, color)
        self.add_render_queue(nonentity)
        return nonentity

    def handle_events(self):
        if not hasattr(self, "camera"):
            print("[ENGINE] game hasnt initialized camera, events not being handled.")
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
                        print("[ENGINE] Releasing Cursor" if self.mouse_captured else "[ENGINE] Capturing Cursor")
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
        self.program['m_proj'].write(self.camera.get_proj_matrix().tobytes()) # type: ignore
        self.program['m_view'].write(self.camera.get_view_matrix().tobytes()) # type: ignore
        self.program['m_model'].write(np.eye(4, dtype='f4').tobytes())        # type: ignore

        vao.render()

    def run(self):
        while True:
            self.dt = self.clock.tick(60) / 1000.0

            self.handle_events()

            for v in self.games:
                v.events()

            self.ctx.clear(0.0, 0.0, 0.0, 0.0)

            m_proj = self.camera.get_proj_matrix()
            m_view = self.camera.get_view_matrix()

            for v in self.render_queue:
                #self.render(v)
                v.render(m_proj, m_view)

            pygame.display.flip()
