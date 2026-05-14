import numpy as np
import pygame

class Nonentity:
    def __init__(self, engine, p1, p2, p3, p4, color, normal=(0, 1, 0)):
        self.engine = engine
        self.camera = self.engine.camera

        self.ctx = engine.get_ctx()
        self.program = engine.get_program()

        p1 = self.engine.scalify(p1)
        p2 = self.engine.scalify(p2)
        p3 = self.engine.scalify(p3)
        p4 = self.engine.scalify(p4)

        # self.r, self.g, self.b = color
        # self.nx, self.ny, self.nz = normal
        # self.p1, self.p2, self.p3, self.p4 = p1, p2, p3, p4
        #vertices = self.subdivide(100)

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

        self.m_model = np.eye(4, dtype='f4')
        self.m_normal = np.linalg.inv(self.m_model).T.astype('f4')[:3, :3]

    # def subdivde(self, subdivisions):
    #     self.p1, self.p2, self.p3, self.p4 = np.array(self.p1), np.array(self.p2), np.array(self.p3), np.array(self.p4)
    #     verts = []
    #     n = subdivisions
    #     for i in range(n):
    #         for j in range(n):
    #             def sample(fi, fj):
    #                 top = self.p1 + (self.p2 - self.p1) * (fi / n)
    #                 bot = self.p4 + (self.p3 - self.p4) * (fi / n)
    #                 return top + (bot - top) * (fj / n)
    #             a = sample(i,   j)
    #             b = sample(i+1, j)
    #             c = sample(i+1, j+1)
    #             d = sample(i,   j+1)
    #             for v in [a, b, c, a, c, d]:
    #                 verts.extend([*v, self.r, self.g, self.b, self.nx, self.ny, self.nz])
    #     return np.array(verts, dtype='f4')

    def render(self, m_proj, m_view):
        self.program['m_proj'].write(m_proj.tobytes())
        self.program['m_view'].write(m_view.tobytes())
        self.program['m_model'].write(self.m_model.tobytes())
        self.program['m_normal'].write(self.m_normal.tobytes())
        #self.program["view_pos"].write(self.camera.get_current_position().astype("f4").tobytes())
        self.program["light_pos"].write((np.array([self.engine.get_sun_position()], dtype="f4") / self.engine.scale ).tobytes())
        self.vao.render()
