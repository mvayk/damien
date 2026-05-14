import engine.engine as engine
import numpy as np
import pygame

class Billboard:
    def __init__(self, ctx, program, texture_path, pos, size=1.0):
        self.ctx = ctx
        self.program = program
        self.pos = np.array(pos, dtype="f4")
        s = size / 2
        vertices = np.array([
            -s,  0.0,  0.0, 1.0,
             s,  0.0,  1.0, 1.0,
             s,  size, 1.0, 0.0,
            -s,  0.0,  0.0, 1.0,
             s,  size, 1.0, 0.0,
            -s,  size, 0.0, 0.0,
        ], dtype="f4")
        vbo = ctx.buffer(vertices.tobytes())
        self.vao = ctx.vertex_array(program, [(vbo, "2f 2f", "in_position", "in_texcoord")])
        img = pygame.image.load(texture_path).convert_alpha()
        img_data = pygame.image.tobytes(img, "RGBA", False)
        self.texture = ctx.texture(img.get_size(), 4, img_data)

    def render(self, m_proj, m_view):
        self.texture.use()
        self.program["m_proj"].write(m_proj.tobytes())
        self.program["m_view"].write(m_view.tobytes())
        self.program["enemy_pos"].write(self.pos.tobytes())
        self.vao.render()
