import time
import pygame
import numpy as np
import random

import utils.utils as utils

from engine.entity import Entity

class Player:
    def __init__(self, engine, health: float, speed: float, damage: float, score: int = 0):
        self.engine = engine
        self.health = health
        self.speed = speed
        self.damage = damage

        self.score = score

        self.entity = self.engine.create_entity((0, 0, 0), (1, 2), True, None)

        self.take_damage(10)

    def get_health_stylized(self):
        return f"Health: {self.get_health()}"

    def get_health(self):
        return self.health

    def get_score_stylized(self):
        return f"Score: {self.get_score()}"

    def get_score(self):
        return self.score

    def take_damage(self, amount):
        self.health -= amount

        if self.health <= 0:
            self.over()

    def over(self):
        print("for later")

class Enemy:
    def __init__(self, engine, game, pos, texture_path, health=100.0, speed=2.0, damage=10.0, size=1.0, hitbox=(0.5, 2.0), form=None):
        self.engine = engine
        self.health = health
        self.speed = speed
        self.damage = damage
        self.game = game
        self.size = size

        self.damage_cooldown = 0.5

        self.entity = self.engine.create_entity(pos, hitbox, False, None)
        billboard = engine.create_billboard(pos, texture_path, size)
        self.entity.update_form(billboard)

    def get_separation(self, enemies):
        separation = np.array([0.0, 0.0, 0.0], dtype='f4')
        for other in enemies:
            if other is self:
                continue
            diff = self.entity.pos - other.entity.pos
            diff[1] = 0.0
            dist = np.linalg.norm(diff)
            if 0 < dist < 3.0:
                separation += utils.normalize(diff) * (1.0 - dist / 3.0)
        return separation

    # stop enemy from going outside of map and from sliding across boundary
    def _clamp_to_bounds(self, pos, bounds=19.7):
        bounds = 19.7 - self.size
        if abs(pos[0]) > bounds:
            pos[0] = float(max(-bounds, min(bounds, pos[0])))
        if abs(pos[2]) > bounds:
            pos[2] = float(max(-bounds, min(bounds, pos[2])))
        pos[1] = 0.0 # just in case
        return pos

    def update(self, dt):
        player_pos = np.array(self.engine.camera.get_current_position(), dtype='f4')
        direction = player_pos - self.entity.pos
        direction[1] = 0.0
        dist = np.linalg.norm(direction)

        separation = self.get_separation(self.game.enemies)
        sep_strength = np.linalg.norm(separation) + 5

        self.damage_cooldown = max(0.0, self.damage_cooldown - dt)

        for e in self.engine.entities:
            if e.player:
                diff = self.entity.pos[[0,2]] - e.pos[[0,2]]
                dist = np.linalg.norm(diff)
                if dist < (self.entity.hitbox_radius + e.hitbox_radius):
                    if self.damage_cooldown == 0.0:
                        self.game.player.take_damage(self.damage)
                        self.damage_cooldown = 1.0
                break

        if dist > 0.5:
            seek = utils.normalize(direction)

            if sep_strength > 0:
                weight = min(sep_strength, 1.5)
                move_dir = utils.normalize(seek + separation * weight)
            else:
                move_dir = seek

            new_pos = self.entity.pos + move_dir * self.speed * dt
            new_pos = self._clamp_to_bounds(new_pos)
            self.entity.update_pos(new_pos)

    def take_damage(self, amount):
        self.health -= amount

    def is_dead(self):
        return self.health <= 0

    def destroy(self):
        self.engine.remove_render_queue(self.entity.form)
        self.engine.remove_entity_queue(self)

class Game:
    def __init__(self, engine):
        self.engine = engine
        self.engine.add_game_queue(self)
        self.engine.set_window_caption("Damien's Doom")

        self.wave = 1
        self.wave_active = False

        self.camera = self.engine.create_camera()
        self.player = Player(self.engine, 100, 10, 25)

        self.health_text = self.engine.draw_text(self.player.get_health_stylized(), (100, 100))
        self.wave_text= self.engine.draw_text(self.get_wave_stylized(), (100, 130))
        self.score_text = self.engine.draw_text(self.player.get_score_stylized(), (100, 160))

        self.crosshair_text = self.engine.draw_text("+", (self.camera.win_size[0] / 2, self.camera.win_size[1] / 2))

        self.enemies = [ ]
        self.game = self

        self.engine.create_skybox((0.3, 0.1, 0.1), (0.1, 0.05, 0.05))
        self.create_world()

    # 1, 2, 3, 4
    def get_spawns(self, direction):
        if direction == 1:
            return (17, 0, 17)
        elif direction == 2:
            return (-17, 0, 17)
        elif direction == 3:
            return (17, 0, -17)
        elif direction == 4:
            return (-17, 0, -17)
        else:
            return (17, 0, 17)

    def get_amplif(self, wave):
        return wave * 1.25

    def get_wave_stylized(self):
        return f"Wave: {self.get_wave()}"

    def get_wave(self):
        return self.wave

    def start_wave(self, wave):
        w_amp = self.get_amplif(wave)
        for _ in range(wave):
            self.create_enemy(self.get_spawns(random.randint(1,4)), "assets/test.png", health=100 * w_amp, speed=2 * w_amp, damage=2 * w_amp)

    def create_enemy(self, pos, texture_path, health=100.0, speed=2.0, damage=10.0, size=1.0, hitbox=(0.5, 2.0)):
        enemy = Enemy(self.engine, self.game, pos, texture_path, health, speed, damage, size, hitbox)
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
        self.engine.create_billboard((35, 42, 0), "assets/overseer.png", 24, True)

    # to be executed in engine loop
    def events(self):
        if not hasattr(self, "camera"):
            print("game hasnt initialized camera, game events not being checked.")
        else:
            # handle waves
            if not self.wave_active:
                self.start_wave(self.get_wave())
                self.wave_active = True

            if len(self.enemies) == 0 and self.wave_active:
                self.wave += 1
                self.wave_active = False

            # for event in pygame.event.get():
            #     pass
            player_position = self.player.entity.pos = self.camera.get_current_position()
            self.engine.update_text(self.health_text, self.player.get_health_stylized(), (100, 100))
            self.engine.update_text(self.wave_text, self.get_wave_stylized(), (100, 130))
            self.engine.update_text(self.score_text, self.player.get_score_stylized(), (100, 160))
            self.engine.update_text(self.crosshair_text, "+", (self.camera.win_size[0] / 2, self.camera.win_size[1] / 2))
            #print(player_position)

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
