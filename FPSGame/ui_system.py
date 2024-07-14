from ursina import *

class UISystem:
    def __init__(self, game):
        self.game = game
        self.score_text = Text(text="Score: 0", position=(-0.85, 0.45))
        self.level_text = Text(text="Level: 1", position=(-0.85, 0.4))
        self.hostages_text = Text(text="Hostages: 0/5", position=(-0.85, 0.35))
        self.ammo_text = Text(text="Ammo: 30", position=(0.7, -0.45))
        self.weapon_text = Text(text="Weapon: Pistol", position=(0.7, -0.4))

    def update(self):
        self.score_text.text = f"Score: {self.game.score}"
        self.level_text.text = f"Level: {self.game.level}"
        self.hostages_text.text = f"Hostages: {self.game.hostages_rescued}/{self.game.total_hostages}"
        self.ammo_text.text = f"Ammo: {self.game.player.ammo}"
        self.weapon_text.text = f"Weapon: {self.game.player.current_weapon}"