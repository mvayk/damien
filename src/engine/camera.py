import math
import os
import struct
import sys

import moderngl
import numpy as np
import pygame

from utils.utils import look_at, normalize, perspective


class Camera:
    def __init__(self, win_size, fov=60, near=0.1, far=500):
        self.win_size = win_size
        self.fov = fov
        self.near = near
        self.far = far

        self.pos = np.array([0.0, 1.0, 4.0], dtype="f4")
        self.yaw = -90.0
        self.pitch = 0.0
        self.speed = 5.0
        self.sensitivity = 0.1

    def get_view_matrix(self):
        front = self.get_front()
        up = np.array([0.0, 1.0, 0.0], dtype="f4")
        return look_at(self.pos, self.pos + front, up)

    def get_proj_matrix(self):
        aspect = self.win_size[0] / self.win_size[1]
        return perspective(self.fov, aspect, self.near, self.far)

    def get_front(self):
        yaw_r = np.radians(self.yaw)
        pitch_r = np.radians(self.pitch)
        front = np.array(
            [
                np.cos(yaw_r) * np.cos(pitch_r),
                np.sin(pitch_r),
                np.sin(yaw_r) * np.cos(pitch_r),
            ],
            dtype="f4",
        )
        return normalize(front)

    # def update(self, dt):
    #     self._mouse_look()
    #     self._keyboard_move(dt)

    def mouse_look(self, dx, dy):
        self.yaw += dx * self.sensitivity
        self.pitch -= dy * self.sensitivity
        self.pitch = max(-89, min(89, self.pitch))

    def keyboard_move(self, dt):
        keys = pygame.key.get_pressed()
        front = self.get_front()
        up = np.array([0.0, 1.0, 0.0], dtype="f4")
        right = normalize(np.cross(front, up))
        vel = self.speed * dt

        if keys[pygame.K_w]:
            self.pos += front * vel
        if keys[pygame.K_s]:
            self.pos -= front * vel
        if keys[pygame.K_a]:
            self.pos -= right * vel
        if keys[pygame.K_d]:
            self.pos += right * vel
        if keys[pygame.K_SPACE]:
            self.pos[1] += vel
        if keys[pygame.K_LSHIFT]:
            self.pos[1] -= vel
