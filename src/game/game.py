import pygame
import numpy as np

import utils.utils as utils

class Player:
    def __init__(self, name: str, health: int, speed: int, damage: int):
        self.name = name
        self.health = health
        self.speed = speed
        self.damage = damage

class Game:
    def __init__(self, engine):
        self.engine = engine
        self.engine.add_game_queue(self)
        self.engine.set_window_caption("Damien's Doom")

        self.camera = self.engine.create_camera()
        world = World(self.engine.get_ctx(), self.engine.get_program())
        self.engine.add_render_queue(world.vao)

        player = Player("damien", 100, 10, 25)

    # to be executed in engine loop
    def events(self):
        if not hasattr(self, "camera"):
            print("game hasnt initialized camera, game events not being checked.")
        else:
            # for event in pygame.event.get():
            #     pass

            front = self.camera.get_front()
            up = np.array([0.0, 1.0, 0.0], dtype="f4")
            right = utils.normalize(np.cross(front, up))
            vel = self.camera.speed * self.engine.dt

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.camera.change_position(self.camera.get_current_position() + front * vel)
            if keys[pygame.K_a]:
                self.camera.change_position(self.camera.get_current_position() - right * vel)
            if keys[pygame.K_s]:
                self.camera.change_position(self.camera.get_current_position() - front * vel)
            if keys[pygame.K_d]:
                self.camera.change_position(self.camera.get_current_position() + right * vel)

class World:
    def __init__(self, ctx, program):
        self.ctx = ctx
        self.program = program

        self.vao = self.build_baseplate()

    def build_baseplate(self, size=40, color=(0.2, 0.2, 0.2)):
        r, g, b = color
        s = size / 2

        vertices = np.array([
            -s, 0, -s,  r, g, b,
             s, 0, -s,  r, g, b,
             s, 0,  s,  r, g, b,

            -s, 0, -s,  r, g, b,
             s, 0,  s,  r, g, b,
            -s, 0,  s,  r, g, b,
        ], dtype='f4')

        vbo = self.ctx.buffer(vertices.tobytes())
        return self.ctx.vertex_array(
            self.program, [(vbo, "3f 3f", "in_position", "in_color")]
        )

    def test(self):
        x = np.linspace(-1.0, 1.0, 50)
        y = np.random.rand(50) - 0.5
        r = np.zeros(50)
        g = np.ones(50)
        b = np.ones(50)

        vertices = np.dstack([x, y, r, g, b])
        self.vbo = self.ctx.buffer(vertices.astype("f4").tobytes())
        self.vao = self.ctx.simple_vertex_array(
            self.program, self.vbo, "in_vert", "in_color"
        )
