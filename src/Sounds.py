import pygame, random

class SoundManager:
    def __init__(self):
        self.sounds = {
            "Pistol": [],
            "Shotgun": [],
            "MAC-10": [],
            "hit": [],
            "reload": [],
            "empty": [],
            "UI": []    
        }

        self.volumes = {
            "SFX": 0.8,
            "UI": 0.6
        }

    def load_sounds(self):
        self.sounds["Shotgun"].append(
            pygame.mixer.Sound("Assets/SFX/Shotgun.wav")
        )
        self.sounds["Pistol"].append(
            pygame.mixer.Sound("Assets/SFX/Pistol.wav")
        )
        self.sounds["MAC-10"].append(
            pygame.mixer.Sound("Assets/SFX/MAC-10.wav")
        )

    def play_sound(self, name, vol = .8):
        if name not in self.sounds:
            return
        sound = random.choice(self.sounds[name])
        sound.set_volume(vol)
        sound.play()

    def variate(self, base_vol):
        return base_vol * random.uniform(0.85, 1.0)

    