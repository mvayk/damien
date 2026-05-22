import numpy as np
import pygame

# entity controls anything dynamic, collisions, etc
class Entity:
    def __init__(self, engine, pos, hitbox, player=False, form=None):
        self.engine = engine
        self.hitbox_radius = hitbox[0]
        self.hitbox_height = hitbox[1]
        self.form = form
        self.pos = np.array(pos, dtype='f4')
        self.player = player

    def update_form(self, form):
        self.form = form

    def update_pos(self, new_pos):
        self.pos = np.array(new_pos, dtype='f4')
        if self.form:
            self.form.pos = self.pos

    def _update(self, dt):
        entities = self.engine.entities

        # handle collisions
        for e in entities:
            if e is self:
                continue

            diff = self.pos[[0,2]] - e.pos[[0,2]]
            dist_xz = np.linalg.norm(diff)
            min_dist = self.hitbox_radius + e.hitbox_radius

            y_overlap = (self.pos[1] + self.hitbox_height > e.pos[1]) and \
                        (self.pos[1] < e.pos[1] + e.hitbox_height)

            if dist_xz < min_dist and y_overlap:
                if dist_xz == 0:
                    push_dir = np.array([1.0, 0.0])
                else:
                    push_dir = diff / dist_xz

                penetration = min_dist - dist_xz
                push = push_dir * (penetration / 2)

                self.pos[0] += push[0]
                self.pos[2] += push[1]
                e.pos[0]    -= push[0]
                e.pos[2]    -= push[1]

                if self.form: self.form.pos = self.pos
                if e.form:    e.form.pos    = e.pos
