import time
import pygame
import numpy as np
import random

import utils.utils as utils

from engine.entity import Entity

class Player:
    def __init__(self, health: int, speed: int, damage: int, score: int = 0):
        self.health = health
        self.speed = speed
        self.damage = damage

        self.score = score

        self.position = (0, 0, 0)

    def get_health_stylized(self):
        return f"Health: {self.health}"

    def take_damage(self, amount):
        self.health -= amount

class Enemy(Entity):
    def __init__(self, engine, pos, texture_path, health=100, speed=2, damage=10, size=1.0, hitbox=(0.5, 2.0)):
        super().__init__(engine, pos, hitbox, form=None)
        self.health = health
        self.speed = speed
        self.damage = damage
        self.form = None

        self.engine.create_entity(pos, hitbox, self.form)

        billboard = engine.create_billboard(pos, texture_path, size)
        self.update_form(billboard)

    def update(self, dt):
        player_pos = np.array(self.engine.camera.get_current_position(), dtype='f4')
        direction = player_pos - self.pos
        direction[1] = 0.0
        dist = np.linalg.norm(direction)
        if dist > 0.5:
            self.update_pos(self.pos + utils.normalize(direction) * self.speed * dt)

    def take_damage(self, amount):
        self.health -= amount

    def is_dead(self):
        return self.health <= 0

    def destroy(self):
        self.engine.remove_render_queue(self.form)
        self.engine.remove_entity_queue(self)

class Game:
    def __init__(self, engine):
        self.engine = engine
        self.engine.add_game_queue(self)
        self.engine.set_window_caption("Damien's Doom")

        self.camera = self.engine.create_camera()
        self.player = Player(100, 10, 25)

        self.health_text = self.engine.draw_text(self.player.get_health_stylized(), (100, 100))

        self.enemies = [ ]

        self.engine.create_skybox((0.3, 0.1, 0.1), (0.1, 0.05, 0.05))
        self.create_world()

    def create_enemy(self, pos, texture_path, health=100, speed=2, damage=10, size=1.0, hitbox=(0.5, 2.0)):
        enemy = Enemy(self.engine, pos, texture_path, health, speed, damage, size, hitbox)
        self.enemies.append(enemy)
        return enemy

    def destroy_enemy(self, enemy):
        self.enemies.remove(enemy)
        enemy.destroy()

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

        #self.engine.set_sun_position(self.engine.scalify((35, 42, 0)))
        self.engine.set_sun_position((35, 42, 0))
        self.engine.create_billboard((35, 40, 0), "assets/overseer.png", 24, True)

        self.create_enemy((0, 0, 0), "assets/test.png", health=100, speed=2, damage=2)

    # to be executed in engine loop
    def events(self):
        if not hasattr(self, "camera"):
            print("game hasnt initialized camera, game events not being checked.")
        else:
            # for event in pygame.event.get():
            #     pass
            player_position = self.player.position = self.camera.get_current_position()
            self.engine.update_text(self.health_text, self.player.get_health_stylized())

            for e in self.enemies:
                e.update(self.engine.dt)

            front = self.camera.get_front()
            front_dir = self.camera.get_front_dir()
            up = np.array([0.0, 1.0, 0.0], dtype="f4")
            right = utils.normalize(np.cross(front, up))
            #vel = self.camera.speed * self.engine.dt
            vel = self.player.speed * self.engine.dt

            keys = pygame.key.get_pressed()
            move = np.array([0.0, 0.0, 0.0], dtype='f4')
            if keys[pygame.K_w]:
                move += front_dir
            if keys[pygame.K_a]:
                move -= right
            if keys[pygame.K_s]:
                move -= front_dir
            if keys[pygame.K_d]:
                move += right
            if keys[pygame.K_f]:
                for e in self.enemies:
                    self.destroy_enemy(e)

            if np.linalg.norm(move) > 0:
                move = utils.normalize(move)
            self.camera.change_position(player_position + move * vel)
