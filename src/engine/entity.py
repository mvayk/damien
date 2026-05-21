import numpy as np
import pygame

class Entity:
    def __init__(self, engine, pos, hitbox, form=None):
        self.engine = engine
        self.hitbox_radius = hitbox[0]
        self.hitbox_height = hitbox[1]
        self.form = form
        self.pos = np.array(pos, dtype='f4')

    def update_form(self, form):
        self.form = form

    def update_pos(self, new_pos):
        self.pos = np.array(new_pos, dtype='f4')
        if self.form:
            self.form.pos = self.pos

    def _update(self, dt):
        entities = self.engine.entities

        for e in entities:
            print(f"{e.form}, {e.pos}")
