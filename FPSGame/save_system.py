import json
import os

class SaveSystem:
    def __init__(self, game):
        self.game = game
        self.save_file = 'game_save.json'

    def save_game(self):
        save_data = {
            'level': self.game.level,
            'score': self.game.score,
            'hostages_rescued': self.game.hostages_rescued,
            'terrorists_killed': self.game.terrorists_killed,
            'player_position': self.game.player.position.tuple(),
            'player_weapon': self.game.player.current_weapon,
            'player_ammo': self.game.player.ammo
        }
        with open(self.save_file, 'w') as f:
            json.dump(save_data, f)

    def load_game(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as f:
                save_data = json.load(f)
            self.game.level = save_data['level']
            self.game.score = save_data['score']
            self.game.hostages_rescued = save_data['hostages_rescued']
            self.game.terrorists_killed = save_data['terrorists_killed']
            self.game.player.position = Vec3(*save_data['player_position'])
            self.game.player.current_weapon = save_data['player_weapon']
            self.game.player.ammo = save_data['player_ammo']
            self.game.generate_level()  # Regenerate the level based on loaded data
            return True
        return False