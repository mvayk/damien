import math
import os
import sys
import struct

import moderngl
import pygame
import numpy as np

# from PIL import Image;

pygame.init()
pygame.display.set_mode((800, 600), flags=pygame.OPENGL | pygame.DOUBLEBUF, vsync=False)

def initiate_vertex_shader(ctx):
    program = ctx.program(
        vertex_shader='''
            #version 330

            in vec2 in_vert;
            in vec3 in_color;

            out vec3 v_color;

            void main() {
                v_color = in_color;
                gl_Position = vec4(in_vert, 0.0, 1.0);
            }
        ''',
        fragment_shader='''
            #version 330

            in vec3 v_color;

            out vec3 f_color;

            void main() {
                f_color = v_color;
            }
        ''',
    )

    return program

def build_vao(ctx, program):
    x = np.linspace(-1.0, 1.0, 50)
    y = np.random.rand(50) - 0.5
    r = np.ones(50)
    g = np.zeros(50)
    b = np.zeros(50)

    vertices = np.dstack([x, y, r, g, b])
    vbo = ctx.buffer(vertices.astype('f4').tobytes())
    vao = ctx.simple_vertex_array(program, vbo, 'in_vert', 'in_color')

    return vao

class Engine:
    MAXIMUM_FPS = 60

    paused = False
    time = 0
    delta_time = 0

    def __init__(self):
        if moderngl.get_context() == None:
            self.ctx = moderngl.create_context()
        else:
            self.ctx = moderngl.get_context()

        pygame.event.set_grab(True)
        pygame.mouse.set_visible(True)

    def render(self, vao):
        now = pygame.time.get_ticks() / 1000.0
        self.ctx.screen.use()
        self.ctx.clear(0.0, 0.0, 0.0, 1.0)
        vao.render(moderngl.LINE_STRIP)

if __name__ == "__main__":
    print("begun")

    engine = Engine()
    program = initiate_vertex_shader(engine.ctx)
    vao = build_vao(engine.ctx, program);

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            engine.render(vao)
            pygame.display.flip()
