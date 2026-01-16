import pygame
import math
import random
import time
import Bullet


class Weapon:
    def __init__(self, weapon_data):
        self.name = weapon_data["name"]
        self.mag_size = weapon_data["mag_size"]
        self.accel = weapon_data["accel"]
        self.DMG = weapon_data["DMG"]
        self.lifetime = weapon_data["lifetime"]
        self.spread = weapon_data["spread"]
        self.pellets = weapon_data["pellets"]
        self.fire_rate = weapon_data["fire_rate"]
        self.barrel = weapon_data["barrel"]
        self.radius = weapon_data["radius"]
        self.recoil = weapon_data["recoil"]
        self.shake_strength = weapon_data["shake_strength"]

        self.is_reloaded = True
        self.current_ammo = weapon_data["mag_size"]
        self.last_shot_time = 0

        self.gun_x = 0
        self.gun_y = 0
        self.recoil_x = 0
        self.recoil_y = 0
        self.gun_angle = 0
        
    
    def fire(self, aim_pos, owner, level, cam, sfx):
            time_now = int(time.time() * 1000)
            #screen_pos = cam.world_to_screen(self.pos)

            if self.current_ammo > 0 and (time_now - self.last_shot_time) > self.fire_rate:
                cam.add_shake(self.shake_strength)
                sfx.play_sound(self.name, 0.8)
                self.recoil_x = -math.cos(self.gun_angle) * self.recoil
                self.recoil_y = math.sin(self.gun_angle) * self.recoil
                self.last_shot_time = time_now
                self.current_ammo -= 1
                if self.name == "Shotgun":
                    for i in range(self.pellets):
                        spread = random.uniform(-self.spread, self.spread)
                        angle = self.gun_angle + math.radians(spread)

                        level.add_bullet(
                            Bullet.Bullet((self.gun_x, self.gun_y), self.accel, self.radius, self.lifetime, angle, owner)
                        )
                else:
                    level.add_bullet( Bullet.Bullet((self.gun_x, self.gun_y), self.accel, self.radius, self.lifetime, self.gun_angle, owner) )
    
    #this function will later call on a more robust system
    def reload(self):
        self.current_ammo = self.mag_size

    def update_weapon(self, plyr_pos, mouse_pos, window, cam):
        self.draw_weapon(plyr_pos, mouse_pos, window, cam)

    def draw_weapon(self, plyr_pos, mouse_pos, window, cam):
        dx = mouse_pos[0] - plyr_pos[0]
        dy = mouse_pos[1] - plyr_pos[1]

        self.gun_angle = math.atan2(-dy, dx)

        offset_x = math.cos(self.gun_angle) * self.radius
        offset_y = -math.sin(self.gun_angle) * self.radius

        self.gun_x = plyr_pos[0] + offset_x
        self.gun_y = plyr_pos[1] + offset_y

        if self.recoil_x < 0:
            self.recoil_x += 1
        if self.recoil_x > 0:
            self.recoil_x -= 1
        if self.recoil_y < 0:
            self.recoil_y += 1
        if self.recoil_y > 0:
            self.recoil_y -= 1

        self.gun_x += self.recoil_x
        self.gun_y += self.recoil_y

        end_x = self.gun_x + math.cos(self.gun_angle) * self.barrel
        end_y = self.gun_y - math.sin(self.gun_angle) * self.barrel

        # Convert world → camera
        start = cam.world_to_screen((self.gun_x, self.gun_y))
        end = cam.world_to_screen((end_x, end_y))

        # Mouse world pos (use this for crosshair)
        pygame.draw.circle(window, (255,255,0), cam.world_to_screen(mouse_pos), 3)

        # Gun origin
        #pygame.draw.circle(window, (0,255,255), cam.world_to_screen((self.gun_x, self.gun_y)), 2)


        pygame.draw.line(window, (255,0,0), start, end, 5)

        

