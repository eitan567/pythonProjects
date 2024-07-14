from ursina import *

class AssetManager:
    def __init__(self):
        self.models = {
            'player': 'assets/models/player.obj',
            'terrorist': 'assets/models/terrorist.obj',
            'hostage': 'assets/models/hostage.obj',
            'pistol': 'assets/models/pistol.obj',
            'rifle': 'assets/models/rifle.obj',
            'shotgun': 'assets/models/shotgun.obj',
        }
        self.textures = {
            'player': 'assets/textures/player.png',
            'terrorist': 'assets/textures/terrorist.png',
            'hostage': 'assets/textures/hostage.png',
            'pistol': 'assets/textures/pistol.png',
            'rifle': 'assets/textures/rifle.png',
            'shotgun': 'assets/textures/shotgun.png',
            'terrain': 'assets/textures/terrain.png',
        }
        self.sounds = {
            'pistol_shot': 'assets/audio/pistol_shot.wav',
            'rifle_shot': 'assets/audio/rifle_shot.wav',
            'shotgun_shot': 'assets/audio/shotgun_shot.wav',
            'pickup': 'assets/audio/pickup.wav',
            'hostage_rescue': 'assets/audio/hostage_rescue.wav',
            'terrorist_death': 'assets/audio/terrorist_death.wav',
            'level_complete': 'assets/audio/level_complete.wav',
            'background_music': 'assets/audio/background_music.wav',
        }

    def load_model(self, name):
        return load_model(self.models[name])

    def load_texture(self, name):
        return load_texture(self.textures[name])

    def load_sound(self, name):
        return Audio(self.sounds[name])

    def get_weapon_shot_sound(self, weapon_type):
        return self.load_sound(f'{weapon_type}_shot')