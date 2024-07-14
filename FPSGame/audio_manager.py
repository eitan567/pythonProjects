from ursina import *

class AudioManager:
    def __init__(self):
        self.sounds = {
            'shoot': Audio('path/to/shoot_sound.wav', loop=False, autoplay=False),
            'pickup': Audio('path/to/pickup_sound.wav', loop=False, autoplay=False),
            'hostage_rescue': Audio('path/to/rescue_sound.wav', loop=False, autoplay=False),
            'terrorist_death': Audio('path/to/death_sound.wav', loop=False, autoplay=False),
            'level_complete': Audio('path/to/level_complete_sound.wav', loop=False, autoplay=False),
        }
        self.music = Audio('path/to/background_music.wav', loop=True, autoplay=True)

    def play_sound(self, sound_name):
        self.sounds[sound_name].play()

    def stop_music(self):
        self.music.stop()