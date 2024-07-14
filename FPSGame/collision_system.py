from ursina import Entity, destroy

class CollisionSystem:
    def __init__(self, game):
        self.game = game

    def update(self):
        self.check_player_collisions()
        self.check_bullet_collisions()

    def check_player_collisions(self):
        hit_info = self.game.player.intersects()
        if hit_info.hit:
            hit_entity = hit_info.entity
            if hasattr(hit_entity, 'on_player_collision'):
                hit_entity.on_player_collision(self.game)

    def check_bullet_collisions(self):
        for bullet in self.game.bullets[:]:  # Use a copy of the list to safely remove items
            hit_info = bullet.intersects()
            if hit_info.hit:
                hit_entity = hit_info.entity
                if hasattr(hit_entity, 'on_bullet_collision'):
                    hit_entity.on_bullet_collision(self.game)
                self.game.bullets.remove(bullet)
                destroy(bullet)