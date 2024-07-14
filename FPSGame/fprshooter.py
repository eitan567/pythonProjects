from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import perlin_noise

# Import our new systems
from terrorist_ai import TerroristAI
from asset_manager import AssetManager
from collision_system import CollisionSystem
from audio_manager import AudioManager
from ui_system import UISystem
from save_system import SaveSystem

class Game(Ursina):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.score = 0
        self.hostages_rescued = 0
        self.terrorists_killed = 0
        self.total_hostages = 5  # This will increase with each level
        self.total_terrorists = 10  # This will increase with each level
        self.bullets = []

        # Initialize our new systems
        self.asset_manager = AssetManager()
        self.audio_manager = AudioManager()
        self.ui = UISystem(self)
        self.save_system = SaveSystem(self)

    def start_game(self):
        window.fullscreen = True
        Sky()
        self.player = FirstPersonController()
        self.player.ammo = 30
        self.player.current_weapon = 'Pistol'
        self.collision_system = CollisionSystem(self)
        self.generate_level()

    def generate_level(self):
        # Clear existing level
        for entity in scene.entities:
            if not isinstance(entity, FirstPersonController) and not isinstance(entity, Sky):
                destroy(entity)

        # Generate terrain using Perlin noise
        terrain = Entity(model=Terrain(heightmap=self.generate_heightmap(), skip=8),
                         scale=(100, 5, 100), texture=self.asset_manager.load_texture('terrain'))

        # Place hostages, terrorists, and weapons
        self.place_hostages()
        self.place_terrorists()
        self.place_weapons()

    def generate_heightmap(self):
        noise = perlin_noise.PerlinNoise(octaves=3, seed=self.level)
        heightmap = [[noise([i/100, j/100]) for j in range(100)] for i in range(100)]
        return heightmap

    def place_hostages(self):
        for _ in range(self.total_hostages):
            x, y, z = self.get_random_position()
            Hostage(self.asset_manager, position=(x, y, z))

    def place_terrorists(self):
        for _ in range(self.total_terrorists):
            x, y, z = self.get_random_position()
            Terrorist(self.asset_manager, self.player, position=(x, y, z))

    def place_weapons(self):
        weapons = ['pistol', 'rifle', 'shotgun']
        for weapon in weapons:
            x, y, z = self.get_random_position()
            Weapon(self.asset_manager, weapon, position=(x, y, z))

    def get_random_position(self):
        x = random.uniform(-50, 50)
        z = random.uniform(-50, 50)
        y = self.get_terrain_height(x, z)
        return x, y, z

    def get_terrain_height(self, x, z):
        # This is a placeholder. In a real implementation, you'd raycast to find the terrain height.
        return 0

    def update(self):
        super().update()
        self.ui.update()
        self.collision_system.update()
        if self.hostages_rescued == self.total_hostages:
            self.next_level()

    def next_level(self):
        self.level += 1
        self.score += 100
        self.hostages_rescued = 0
        self.terrorists_killed = 0
        self.total_hostages += 2
        self.total_terrorists += 5
        if self.level > 10:
            self.end_game()
        else:
            self.generate_level()
        self.audio_manager.play_sound('level_complete')

    def end_game(self):
        print(f"Game Over! Final Score: {self.score}")
        application.quit()

    def shoot(self):
        if self.player.ammo > 0:
            self.player.current_weapon.shoot()  # This will play the weapon-specific sound
            bullet = Entity(model='sphere', color=color.black, scale=0.1, position=self.player.position)
            bullet.animate_position(bullet.position + bullet.forward * 100, duration=1, curve=curve.linear)
            self.bullets.append(bullet)
            invoke(lambda: self.bullets.remove(bullet), delay=1)
            self.player.ammo -= 1
        else:
            print("Out of ammo!")

    def rescue_hostage(self, hostage):
        self.hostages_rescued += 1
        self.score += 10
        destroy(hostage)
        self.audio_manager.play_sound('hostage_rescue')

    def pickup_weapon(self, weapon):
        self.player.current_weapon = weapon.weapon_type
        self.player.ammo = 30  # Reset ammo on weapon pickup
        print(f"Picked up {weapon.weapon_type}")
        destroy(weapon)
        self.audio_manager.play_sound('pickup')

    def kill_terrorist(self, terrorist):
        self.terrorists_killed += 1
        self.score += 1
        destroy(terrorist)
        self.audio_manager.play_sound('terrorist_death')

    def save_game(self):
        self.save_system.save_game()
        print("Game saved!")

    def load_game(self):
        if self.save_system.load_game():
            print("Game loaded!")
        else:
            print("No saved game found.")

    def input(self, key):
        if key == 'left mouse down':
            self.shoot()
        elif key == 'f5':
            self.save_game()
        elif key == 'f9':
            self.load_game()

class Hostage(Entity):
    def __init__(self, asset_manager, **kwargs):
        super().__init__(
            model=asset_manager.load_model('hostage'),
            texture=asset_manager.load_texture('hostage'),
            scale=0.5,
            **kwargs
        )

    def on_player_collision(self, game):
        game.rescue_hostage(self)

class Terrorist(Entity):
    def __init__(self, asset_manager, player, **kwargs):
        super().__init__(
            model=asset_manager.load_model('terrorist'),
            texture=asset_manager.load_texture('terrorist'),
            scale=0.5,
            **kwargs
        )
        self.ai = TerroristAI(self, player)

    def update(self):
        self.ai.update(time.dt)

    def on_bullet_collision(self, game):
        game.kill_terrorist(self)

class Weapon(Entity):
    def __init__(self, asset_manager, weapon_type, **kwargs):
        super().__init__(
            model=asset_manager.load_model(weapon_type),
            texture=asset_manager.load_texture(weapon_type),
            scale=0.3,
            **kwargs
        )
        self.weapon_type = weapon_type
        self.shot_sound = asset_manager.get_weapon_shot_sound(weapon_type)

    def shoot(self):
        self.shot_sound.play()
        # Add other shooting logic here

if __name__ == '__main__':
    game = Game()
    game.start_game()
    game.run()