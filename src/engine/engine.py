import math
import os
import struct
import sys
import time

import moderngl
import numpy as np
import pygame

from engine.text import Text
from engine.nonentity import Nonentity
from engine.billboard import Billboard
from engine.entity import Entity

import engine.camera as camera
import utils.utils as utils

# from PIL import Image;

# constants
class Engine:
    def __init__(self):
        self.games = [ ]
        self.render_queue = [ ]
        self.entities = [ ]

        self.mouse_captured = True;
        self.dt = 0

        self.WIN_SIZE = (800, 600)

        pygame.init()
        pygame.display.set_mode(
            (self.WIN_SIZE), flags=pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE, vsync=False
        )
        pygame.display.set_caption("")
        pygame.event.set_grab(True)

        # same in vertex shader
        self.scale = 1

        pygame.mouse.set_visible(False)

        if moderngl.get_context() == None:
            self.ctx = moderngl.create_context()
        else:
            self.ctx = moderngl.get_context()

        self.ctx.enable(moderngl.DEPTH_TEST)
        self.clock = pygame.time.Clock()

        self.program = self.ctx.program(
            vertex_shader=utils.load_file_contents("engine/shaders/nonentities.vert"),
            fragment_shader=utils.load_file_contents("engine/shaders/nonentities.frag"),
        )
        self.billboard_program = self.ctx.program(
            vertex_shader=utils.load_file_contents("engine/shaders/billboard.vert"),
            fragment_shader=utils.load_file_contents("engine/shaders/billboard.frag"),
        )
        self.skybox_program = self.ctx.program(
            vertex_shader=utils.load_file_contents("engine/shaders/skybox.vert"),
            fragment_shader=utils.load_file_contents("engine/shaders/skybox.frag"),
        )
        self.text_program = self.ctx.program(
            vertex_shader=utils.load_file_contents("engine/shaders/text.vert"),
            fragment_shader=utils.load_file_contents("engine/shaders/text.frag"),
        )

        self.program["light_pos"].value = (0, 0, 0) # type: ignore

    def set_sun_position(self, position):
        self.program["light_pos"].value = (position) # type: ignore

    def get_sun_position(self):
        return self.program["light_pos"].value # type: ignore

    def scalify(self, value):
        try:
            return tuple(v * self.scale for v in value)
        except TypeError:
            return value * self.scale if value != 0 else 0

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

    def create_entity(self, pos, hitbox, player, form):
        entity = Entity(self, pos, hitbox, player, form)
        self.add_entity_queue(entity)
        return entity

    def get_ctx(self):
        return self.ctx

    def add_render_queue(self, thing):
        self.render_queue.append(thing)

    def remove_render_queue(self, thing):
        try:
            self.games.remove(thing)
            print(f"[ENGINE] Removed {thing}")
        except ValueError:
            print(f"[ENGINE] Attempted to remove {thing} from game queue")
            pass

    def add_game_queue(self, game):
        self.games.append(game)

    def remove_game_queue(self, thing):
        try:
            self.games.remove(thing)
            print(f"[ENGINE] Removed {thing}")
        except ValueError:
            print(f"[ENGINE] Attempted to remove {thing} from game queue")
            pass

    def add_entity_queue(self, entity):
        self.entities.append(entity)

    def remove_entity_queue(self, entity):
        try:
            self.games.remove(entity)
            print(f"[ENGINE] Removed {entity}")
        except ValueError:
            print(f"[ENGINE] Attempted to remove {entity} from entity queue")
            pass

    def create_billboard(self, pos, texture_path, size=1.0, follow_camera=False):
        billboard = Billboard(self.ctx, self.billboard_program, texture_path, pos, size, follow_camera)
        self.add_render_queue(billboard)
        return billboard

    def create_structure(self, p1, p2, p3, p4, color):
        nonentity = Nonentity(self, p1, p2, p3, p4, color)
        self.add_render_queue(nonentity)
        return nonentity

    def draw_text(self, value, position=(0, 0), font_size=32, color=(255, 255, 255)):
        text = Text(self, position, str(value), font_size, color)
        self.add_render_queue(text)
        return text

    def update_text(self, text, new_value):
        text.update_text(new_value)

    # todo: idek
    #       collisions

    def handle_events(self):
        if not hasattr(self, "camera"):
            print("[ENGINE] game hasnt initialized camera, events not being handled.")
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type== pygame.KEYDOWN:
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
                    self.WIN_SIZE = (event.w, event.h)
                    self.camera.win_size = (event.w, event.h)
                    self.ctx.viewport = (0, 0, event.w, event.h)

    def run(self):
        while True:
            self.dt = self.clock.tick(60) / 1000.0
            #time.sleep(self.dt)

            self.handle_events()

            for v in self.games:
                v.events()

            #self.ctx.screen.use()
            self.ctx.clear(0.0, 0.0, 0.0, 1.0)

            m_proj = self.camera.get_proj_matrix()
            m_view = self.camera.get_view_matrix()

            # why is text so hard to render
            for v in self.render_queue:
                if not isinstance(v, Text):
                    v.render(m_proj, m_view)

            for v in self.render_queue:
                if isinstance(v, Text):
                    v.render(m_proj, m_view)

            for e in self.entities:
                e._update(self.dt)

            pygame.display.flip()
