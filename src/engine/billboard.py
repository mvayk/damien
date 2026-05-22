# stutter upon creation of billboard
import engine.engine as engine
import numpy as np
import pygame

class Billboard:
    def __init__(self, ctx, program, texture_path, pos, engine, size=1.0, follow_camera=False):
        self.ctx = ctx
        self.program = program
        self.pos = np.array(pos, dtype="f4")
        self.follow_camera = follow_camera
        self.size = size
        self.engine = engine

        vbo = self.engine.get_billboard_vbo(ctx, program, size)
        self.vao = ctx.vertex_array(program, [(vbo, "2f 2f", "in_position", "in_texcoord")])
        self.texture = self.engine.get_texture(ctx, texture_path)

    def render(self, m_proj, m_view):
        self.texture.use()
        self.program["m_proj"].write(m_proj.tobytes())
        self.program["m_view"].write(m_view.tobytes())
        self.program["enemy_pos"].write(self.pos.tobytes())
        self.program["follow_camera"] = self.follow_camera
        self.vao.render()
