import engine.engine as engine
import numpy as np
import pygame

class Nonentity:
    def __init__(self, ctx, program, size, color):
        self.ctx = ctx
        self.program = program

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
        self.vao =  self.ctx.vertex_array(
            self.program, [(vbo, "3f 3f", "in_position", "in_color")]
        )

    def render(self, m_proj, m_view):
        self.program['m_proj'].write(m_proj.tobytes())
        self.program['m_view'].write(m_view.tobytes())
        self.program['m_model'].write(np.eye(4, dtype='f4').tobytes())
        self.vao.render()
