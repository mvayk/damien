import numpy as np


class Player:
    def __init__(self, name: str, health: int, speed: int, damage: int):
        self.name = name
        self.health = health
        self.speed = speed
        self.damage = damage


class Game:
    def __init__(self, engine):
        self.engine = engine
        print("yes")

        self.camera = self.engine.create_camera()

        world = World(self.engine.get_ctx(), self.engine.get_program())
        self.engine.add_render_queue(world.vao)

        player = Player("damien", 100, 10, 25)


class World:
    def __init__(self, ctx, program):
        self.ctx = ctx
        self.program = program

        self.vao = self.build_baseplate()

    def build_baseplate(self, size=20, color=(0.3, 0.6, 0.3)):
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
