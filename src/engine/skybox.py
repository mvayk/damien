import numpy as np

class Skybox:
    def __init__(self, ctx, program, top=(0.0, 0.0, 0.0), bottom=(0.0, 0.0, 0.0)):
        self.ctx = ctx
        self.program = program
        self.top = top
        self.bottom = bottom
        vertices = np.array([
            -1, -1, -1,  1, -1, -1,  1,  1, -1, -1, -1, -1,  1,  1, -1, -1,  1, -1,
            -1, -1,  1,  1, -1,  1,  1,  1,  1, -1, -1,  1,  1,  1,  1, -1,  1,  1,
            -1, -1, -1, -1,  1, -1, -1,  1,  1, -1, -1, -1, -1,  1,  1, -1, -1,  1,
             1, -1, -1,  1,  1, -1,  1,  1,  1,  1, -1, -1,  1,  1,  1,  1, -1,  1,
            -1, -1, -1, -1, -1,  1,  1, -1,  1, -1, -1, -1,  1, -1,  1,  1, -1, -1,
            -1,  1, -1, -1,  1,  1,  1,  1,  1, -1,  1, -1,  1,  1,  1,  1,  1, -1,
        ], dtype='f4')
        vbo = ctx.buffer(vertices.tobytes())
        self.vao = ctx.vertex_array(program, [(vbo, '3f', 'in_position')])

    def render(self, m_proj, m_view):
        self.program["m_proj"].write(m_proj.tobytes())
        self.program["m_view"].write(m_view.tobytes())
        self.program["sky_top"].value = self.top
        self.program["sky_bottom"].value = self.bottom
        self.ctx.depth_func = '<='
        self.vao.render()
        self.ctx.depth_func = '<'
