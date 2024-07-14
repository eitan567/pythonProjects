from ursina import *
import random

class TerroristAI:
    def __init__(self, terrorist_entity, player, move_speed=2, attack_range=10):
        self.entity = terrorist_entity
        self.player = player
        self.move_speed = move_speed
        self.attack_range = attack_range
        self.state = 'patrol'
        self.patrol_point = self.get_random_point()
        self.attack_cooldown = 0

    def update(self, dt):
        if self.state == 'patrol':
            self.patrol(dt)
        elif self.state == 'chase':
            self.chase(dt)
        elif self.state == 'attack':
            self.attack(dt)

        # Check if player is in sight
        if self.can_see_player():
            self.state = 'chase'

    def patrol(self, dt):
        direction = self.patrol_point - self.entity.position
        if direction.length() < 1:
            self.patrol_point = self.get_random_point()
        else:
            self.entity.position += direction.normalized() * self.move_speed * dt

    def chase(self, dt):
        direction = self.player.position - self.entity.position
        if direction.length() < self.attack_range:
            self.state = 'attack'
        else:
            self.entity.position += direction.normalized() * self.move_speed * dt

    def attack(self, dt):
        self.attack_cooldown -= dt
        if self.attack_cooldown <= 0:
            print("Terrorist attacks player!")  # Replace with actual attack logic
            self.attack_cooldown = 2  # Attack every 2 seconds

        direction = self.player.position - self.entity.position
        if direction.length() > self.attack_range:
            self.state = 'chase'

    def can_see_player(self):
        direction = self.player.position - self.entity.position
        hit_info = raycast(self.entity.position, direction, distance=30)
        return hit_info.hit and hit_info.entity == self.player

    def get_random_point(self):
        return Vec3(
            random.uniform(-50, 50),
            0,  # Assume flat terrain for simplicity
            random.uniform(-50, 50)
        )