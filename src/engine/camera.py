import math
import os
import struct
import sys
import moderngl
import numpy as np
import pygame
import utils.utils as utils

class Camera:
    def __init__(self, win_size, fov=60, near=0.1, far=500):
        self.win_size = win_size
        self.fov = fov
        self.near = near
        self.far = far
        self.x, self.y, self.z = 0.0, 1.0, 4.0
        self.yaw = -90.0
        self.pitch = 0.0
        self.sensitivity = 0.1

    def get_current_position(self):
        return np.array([self.x, self.y, self.z], dtype="f4")

    def change_position(self, new_position):
        self.x = float(new_position[0])
        self.y = 1.0  # locked
        self.z = float(new_position[2])

    def get_view_matrix(self):
        pos = self.get_current_position()
        front = self.get_front()
        up = np.array([0.0, 1.0, 0.0], dtype="f4")
        return utils.look_at(pos, pos + front, up)

    def get_proj_matrix(self):
        aspect = self.win_size[0] / self.win_size[1]
        return utils.perspective(self.fov, aspect, self.near, self.far)

    def get_front(self):
        yaw_r = np.radians(self.yaw)
        pitch_r = np.radians(self.pitch)
        front = np.array([
            np.cos(yaw_r) * np.cos(pitch_r),
            np.sin(pitch_r),
            np.sin(yaw_r) * np.cos(pitch_r),
        ], dtype="f4")
        return utils.normalize(front)

    def get_up(self):
        return np.array([0.0, 1.0, 0.0], dtype="f4")

    def get_right(self):
        return utils.normalize(np.cross(self.get_front(), self.get_up()))

    def mouse_look(self, dx, dy):
        self.yaw += dx * self.sensitivity
        self.pitch -= dy * self.sensitivity
        self.pitch = max(-89.9, min(89.9, self.pitch))
