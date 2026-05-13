import pygame
import numpy as np

import utils.utils as utils

class Entity:
    def __init__(self, health: int, speed: int, damage: int):
        self.health = health
        self.speed = speed
        self.damage = damage

class Player(Entity):
    def __init__(self, health: int, speed: int, damage: int, score: int = 0):
        super().__init__(health, speed, damage)

        self.score = score

class Enemy(Entity):
    def __init__(self, health: int, speed: int, damage: int):
        super().__init__(health, speed, damage)

class Game:
    def __init__(self, engine):
        self.engine = engine
        self.engine.add_game_queue(self)
        self.engine.set_window_caption("Damien's Doom")

        self.camera = self.engine.create_camera()
        self.player = Player(100, 10, 25)

        self.create_world()

    def create_world(self):
        self.engine.create_nonentity(0, 40, (0.2, 0.2, 0.2))

    # to be executed in engine loop
    def events(self):
        if not hasattr(self, "camera"):
            print("game hasnt initialized camera, game events not being checked.")
        else:
            # for event in pygame.event.get():
            #     pass

            front = self.camera.get_front()
            up = np.array([0.0, 1.0, 0.0], dtype="f4")
            right = utils.normalize(np.cross(front, up))
            #vel = self.camera.speed * self.engine.dt
            vel = self.player.speed * self.engine.dt

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.camera.change_position(self.camera.get_current_position() + front * vel)
            if keys[pygame.K_a]:
                self.camera.change_position(self.camera.get_current_position() - right * vel)
            if keys[pygame.K_s]:
                self.camera.change_position(self.camera.get_current_position() - front * vel)
            if keys[pygame.K_d]:
                self.camera.change_position(self.camera.get_current_position() + right * vel)
