import pygame
import numpy as np

import utils.utils as utils

class Player:
    def __init__(self, health: int, speed: int, damage: int, score: int = 0):
        self.health = health
        self.speed = speed
        self.damage = damage

        self.score = score

        self.position = (0, 0, 0)

class Enemy:
    def __init__(self, engine, health, speed, damage, pos, texture_path, size=2.0):
        self.health = health
        self.speed = speed
        self.damage = damage
        self.pos = np.array(pos, dtype='f4')
        self.billboard = engine.create_billboard(pos, texture_path, size)

    def update(self, player_pos, dt):
        direction = player_pos - self.pos
        direction[1] = 0.0
        dist = np.linalg.norm(direction)
        if dist > 0.5:
            direction = utils.normalize(direction)
            self.pos += direction * self.speed * dt
            self.billboard.pos = self.pos

    def is_dead(self):
        return self.health <= 0

    def take_damage(self, amount):
        self.health -= amount

class Game:
    def __init__(self, engine):
        self.engine = engine
        self.engine.add_game_queue(self)
        self.engine.set_window_caption("Damien's Doom")

        self.camera = self.engine.create_camera()
        self.player = Player(100, 10, 25)

        self.enemies = [ ]
        self.create_world()

    def create_enemy(self, health, speed, damage, pos, texture_path):
        enemy = Enemy(self.engine, health, speed, damage, pos, texture_path)
        self.enemies.append(enemy)
        return enemy

    def create_world(self):
        # baseplate
        self.engine.create_structure(
            (-20, 0, -20), (20, 0, -20), (20, 0, 20), (-20, 0, 20),
            color=(0.2, 0.2, 0.2)
        )

        height = 10

        # walls
        self.engine.create_structure((-20, 0, -20), (20, 0, -20), (20, height, -20), (-20, height, -20), color=(0.4, 0.4, 0.4))
        self.engine.create_structure((-20, 0, 20), (20, 0, 20), (20, height, 20), (-20, height, 20), color=(0.4, 0.4, 0.4))
        self.engine.create_structure((-20, 0, -20), (-20, 0, 20), (-20, height, 20), (-20, height, -20), color=(0.3, 0.3, 0.3))
        self.engine.create_structure((20, 0, -20), (20, 0, 20), (20, height, 20), (20, height, -20), color=(0.1, 0.1, 0.1))

        # self.engine.create_billboard((2, 2, 2), "assets/test.jpg", 8)
        self.create_enemy(100, 2, 2, (0, 0, 0), "assets/test.jpg")

    # to be executed in engine loop
    def events(self):
        if not hasattr(self, "camera"):
            print("game hasnt initialized camera, game events not being checked.")
        else:
            # for event in pygame.event.get():
            #     pass

            player_position = self.player.position = self.camera.get_current_position()

            for e in self.enemies:
                e.update(player_position, self.engine.dt)

            front = self.camera.get_front()
            up = np.array([0.0, 1.0, 0.0], dtype="f4")
            right = utils.normalize(np.cross(front, up))
            #vel = self.camera.speed * self.engine.dt
            vel = self.player.speed * self.engine.dt

            keys = pygame.key.get_pressed()
            move = np.array([0.0, 0.0, 0.0], dtype='f4')
            if keys[pygame.K_w]:
                move += front
            if keys[pygame.K_a]:
                move -= right
            if keys[pygame.K_s]:
                move -= front
            if keys[pygame.K_d]:
                move += right

            if np.linalg.norm(move) > 0:
                move = utils.normalize(move)
            self.camera.change_position(player_position + move * vel)
