import numpy as np
import pygame
import moderngl

class Text:
    def __init__(self, engine, position, text, font_size=32, color=(255, 255, 255)):
        self.engine = engine
        self.ctx = self.engine.get_ctx()
        self.program = self.engine.text_program
        self.position = position
        self.font_size = font_size
        self.color = color
        self.vao = None
        self.vbo = None

        pygame.font.init()
        self._font = pygame.font.SysFont("Arial", font_size)

        self.texture = None
        self.update_text(text)

    def _make_texture(self, text):
        surf = self._font.render(text, True, self.color)
        w, h = surf.get_size()
        raw = pygame.image.tobytes(surf, "RGBA", True)
        tex = self.ctx.texture((w, h), 4, raw)
        tex.filter = (moderngl.LINEAR, moderngl.LINEAR)
        return tex, w, h

    def _rebuild_vao(self):
        if self.vao:
            self.vao.release()
        if self.vbo:
            self.vbo.release()
        x, y = self.position
        w, h = self.w, self.h
        verts = np.array([
            x,   y,   0.0, 0.0,
            x+w, y,   1.0, 0.0,
            x+w, y+h, 1.0, 1.0,
            x,   y,   0.0, 0.0,
            x+w, y+h, 1.0, 1.0,
            x,   y+h, 0.0, 1.0,
        ], dtype=np.float32)
        self.vbo = self.ctx.buffer(verts.tobytes())
        self.vao = self.ctx.vertex_array(
            self.program, [(self.vbo, "2f 2f", "in_position", "in_uv")]
        )

    def update_text(self, new_value):
        if self.texture:
            self.texture.release()
        self.texture, self.w, self.h = self._make_texture(str(new_value))
        self._rebuild_vao()

    def render(self, m_proj, m_view):
        self.program["screen_size"] = (
            float(self.engine.camera.win_size[0]),
            float(self.engine.camera.win_size[1])
        )
        self.ctx.disable(moderngl.DEPTH_TEST)
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
        self.texture.use(location=0) # type: ignore
        self.program["text_texture"] = 0
        # print("vao:", self.vao)
        # print("vbo:", self.vbo)
        # print("texture:", self.texture)
        # print("ctx error before render:", self.ctx.error)
        # print("ctx error after render:", self.ctx.error)
        self.vao.render() # type: ignore
        self.ctx.enable(moderngl.DEPTH_TEST)
