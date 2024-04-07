import random
import pygame
from math import atan2, cos, sin
from settings import SPEED, WIDTH, HEIGHT

proj_speed = 0


class Projectile:

    def __init__(self):
        self.delay_number: int = 0
        self.animation_frame: int = 0
        self.all_bullets = []
        self.destination_place: int = 1
        self.pictures_init()
        self.crop_pictures()
        self.resize_pictures()

    def pictures_init(self):
        self.proj_animation = [
            pygame.image.load("assets/sprites/projectile (1).png"),
            pygame.image.load("assets/sprites/projectile (2).png"),
            pygame.image.load("assets/sprites/projectile (3).png"),
            pygame.image.load("assets/sprites/projectile (4).png"),
            pygame.image.load("assets/sprites/projectile (5).png"),
            pygame.image.load("assets/sprites/projectile (6).png"),
            pygame.image.load("assets/sprites/projectile (7).png"),
            pygame.image.load("assets/sprites/projectile (8).png"),
            pygame.image.load("assets/sprites/projectile (9).png"),
            pygame.image.load("assets/sprites/projectile (10).png"),
            pygame.image.load("assets/sprites/projectile (11).png"),
        ]

    def crop_pictures(self):
        self.cropped_animation = []
        for item in range(len(self.proj_animation)):
            cropped_item = self.proj_animation[item].subsurface(
                400, 200, 900, 600)
            self.cropped_animation.append(cropped_item)

    def resize_pictures(self):
        self.resized_animation = []
        for item in range(len(self.cropped_animation)):
            resized_item = pygame.transform.scale(
                self.cropped_animation[item], [75, 45]
            )
            self.resized_animation.append(resized_item)

    def _spawn_place(self):
        _side: int = random.randint(1, 4)
        if _side == 1:
            self.proj_x, self.proj_y = (random.randint(0, WIDTH), 0)
        elif _side == 2:
            self.proj_x, self.proj_y = (0, random.randint(0, HEIGHT))
        elif _side == 3:
            self.proj_x, self.proj_y = (random.randint(0, WIDTH), HEIGHT - 50)
        else:
            self.proj_x, self.proj_y = (WIDTH - 50, random.randint(0, HEIGHT))

    def update(self, delta: float):
        self.delay_number += 1
        print(self.delay_number)
        if self.delay_number % 250 == 0:
            self._spawn_place()
            self.destination_place = random.randint(1, 200)
            self.projectile_logic()
        self.proj_movement(delta)

    def render(self, screen: pygame.Surface):
        self.spawn(screen)
        self.despawn()

    def destination_logic(self, pl_x: float, pl_y: float, pl_speed_x: float, pl_speed_y: float, delta: float):
        self.proj_dest_x = pl_x + pl_speed_x * delta * self.destination_place
        self.proj_dest_y = pl_y + pl_speed_y * delta * self.destination_place

    def projectile_logic(self):
        distance_x: float = self.proj_dest_x - self.proj_x
        distance_y: float = self.proj_dest_y - self.proj_y
        angle: float = atan2(distance_y, distance_x)
        self.rotation_math()
        speed_x: float = 2 * cos(angle)
        speed_y: float = 2 * sin(angle)
        self.all_bullets.append(
            [
                self.proj_x,
                self.proj_y,
                speed_x,
                speed_y,
                self.rotation_vector,
            ]
        )

    def rotation_math(self):
        destination = pygame.Vector2(self.proj_dest_x, self.proj_dest_y)
        self_pos = pygame.Vector2(self.proj_x, self.proj_y)
        self.rotation_vector = destination - self_pos

    def proj_movement(self, delta: float):
        for item in self.all_bullets:
            item[0] += item[2] * delta
            item[1] += item[3] * delta

    def spawn(self, screen: pygame.Surface):
        for pos_x, pos_y, speed_x, speed_y, angle in self.all_bullets:
            speed_x += speed_y
            self.animation()
            degree = angle.as_polar()[1]
            rotated_proj = pygame.transform.rotate(
                self.resized_animation[self.animation_frame], -degree
            )
            screen.blit(rotated_proj, ((pos_x, pos_y), (100, 100)))

    def animation(self):
        if self.delay_number % 15 == 0:
            self.animation_frame += 1
            if self.animation_frame >= len(self.resized_animation):
                self.animation_frame = 0

    def despawn(self):
        for pos_x, pos_y, speed_x, speed_y, angle in self.all_bullets:
            if pos_x > WIDTH or pos_x < 0 or pos_y > HEIGHT or pos_y < 0:
                self.all_bullets.remove(
                    [pos_x, pos_y, speed_x, speed_y, angle])
