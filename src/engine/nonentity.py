import engine.engine as engine
import numpy as np
import pygame

class Nonentity:
    def __init__(self, ctx, program, p1, p2, p3, p4, color, normal=(0, 1, 0)):
        # currently only generates flat planes
        self.ctx = ctx
        self.program = program
        r, g, b = color
        nx, ny, nz = normal
        vertices = np.array([
           *p1, r, g, b, nx, ny, nz,
           *p2, r, g, b, nx, ny, nz,
           *p3, r, g, b, nx, ny, nz,
           *p1, r, g, b, nx, ny, nz,
           *p3, r, g, b, nx, ny, nz,
           *p4, r, g, b, nx, ny, nz,
        ], dtype='f4')
        vbo = self.ctx.buffer(vertices.tobytes())
        self.vao = self.ctx.vertex_array(
            self.program, [(vbo, "3f 3f 3f", "in_position", "in_color", "in_normal")]
        )

    def render(self, m_proj, m_view):
        self.program['m_proj'].write(m_proj.tobytes())
        self.program['m_view'].write(m_view.tobytes())
        self.program['m_model'].write(np.eye(4, dtype='f4').tobytes())
        self.vao.render()
