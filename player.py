import pygame as pg
import numpy as np

from settings import *
from collisions import CollisionRect
from barriers import Barriers


def lerp(a, b, t):
    return a + (b - a) * t

class Player:
    def __init__(self):
        self.playerCollision = None 
        self.barriers = Barriers()

        #Initialize movement values
        self.pos = np.array([0.0, 0.0])
        self.alt = 1.0
        self.angle = 0.0
        self.velocity = 0.0

        self.steer_time_elapsed = 0.0
        self.jump_time_elapsed = 0.0

        self.jumped = False
        self.is_jumping = False
        self.is_falling = False

        self.gear_selection = ["D", "R"]
        self.gear = 0
    
    def update(self, dt):
        #current collRect
        self.playerCollision = CollisionRect(self.pos, PLAYER_WIDTH, PLAYER_HEIGHT)

        #self.devMovement()
        self.movement(dt)

    def movement(self, dt):
        keys = pg.key.get_pressed()
        
        # Gear selection
        if np.floor(self.velocity) == 0.0: # Use floor to allow a little leniency
            if keys[pg.K_q] and self.gear > 0:
                self.gear -= 1
            elif keys[pg.K_e] and self.gear < (len(self.gear_selection) - 1):
                self.gear += 1

        # Car acceleration and braking
        if self.gear == 0: # Drive
            if keys[pg.K_w] and self.velocity <= MAX_SPEED:
                self.velocity += ACCELERATION * dt
            elif keys[pg.K_s]:
                if self.velocity > 0.0:
                    self.velocity -= BRAKE * dt
                else:
                    self.velocity = 0.0
            else:
                if self.velocity > 0.0:
                    self.velocity -= SPEED_LOSS * dt
                else:
                    self.velocity = 0.0
        elif self.gear == 1: # Reverse
            if keys[pg.K_w] and self.velocity >= -MAX_REVERSE_SPEED:
                self.velocity -= REVERSE_ACCELERATION * dt
            elif keys[pg.K_s]:
                if self.velocity < 0.0:
                    self.velocity += BRAKE * dt
                else:
                    self.velocity = 0.0
            else:
                if self.velocity < 0.0:
                    self.velocity += SPEED_LOSS * dt
                else:
                    self.velocity = 0.0

        # Steering that smoothly transitions to the angle using lerp
        if keys[pg.K_a]:
            self.steer_time_elapsed += dt
        if keys[pg.K_d]:
            self.steer_time_elapsed -= dt
        if not (keys[pg.K_a] or keys[pg.K_d]) or (keys[pg.K_a] and keys[pg.K_d]):
            # Adds + or - dt in conditional statement to remove overcompensation otherwise car has a jittering effect
            if self.steer_time_elapsed - dt > 0.0:
                self.steer_time_elapsed -= dt
            elif self.steer_time_elapsed + dt < 0.0:
                self.steer_time_elapsed += dt
            else:
                self.steer_time_elapsed = 0.0
        self.steer_time_elapsed = np.clip(self.steer_time_elapsed, -STEERING_DURATION, STEERING_DURATION)

        # Sigmoid function with contained angular velocity
        new_angle = ((MAX_STEERING * 2) / (1 + np.exp(-STEERING_SPEED * self.velocity)) - MAX_STEERING) * dt
        self.angle = lerp(self.angle, self.angle - new_angle, self.steer_time_elapsed / STEERING_DURATION)

        # Jumping (controlled in main.py) using lerp to smoothen the change in jump height
        if self.jumped:
            if self.jump_time_elapsed <= JUMP_LERP_DURATION:
                # Checks current state and lerps values accordingly
                if self.is_jumping and not self.is_falling:
                    self.alt = lerp(self.prev_alt, self.prev_alt - MAX_JUMP_HEIGHT, self.jump_time_elapsed / JUMP_LERP_DURATION)
                else:
                    self.alt = lerp(self.alt, self.prev_alt, self.jump_time_elapsed / JUMP_LERP_DURATION)
                self.jump_time_elapsed += dt
            else:
                # Controls player jump states
                if self.is_jumping and not self.is_falling:
                    self.is_jumping = False
                    self.is_falling = True
                else:
                    self.jumped = False
                    self.is_falling = False
                self.jump_time_elapsed = 0.0

        # Apply basic movement computations
        sin_a = np.sin(np.deg2rad(self.angle))
        cos_a = np.cos(np.deg2rad(self.angle))

        speed_sin = self.velocity * sin_a * dt
        speed_cos = self.velocity * cos_a * dt

        self.pos[0] += speed_cos
        self.pos[1] += speed_sin

        # Collision testing
        if(self.playerCollision.overlap(
            CollisionRect(
                np.array([25.0, 25.0]),
                w = 25,
                h = 25
            )
        )):
            pass
            #print("COLLISION!!!")
        else:
            pass
            #print("NO Collision")

    def set_player_angle(self, angle):
        if angle == 0.0: angle = 360.0
        self.angle = angle
    
    def set_player_pos(self, x, y):
        self.pos[0], self.pos[1] = x, y

    def devMovement(self):
        keys = pg.key.get_pressed()
        
        sin_a = np.sin(np.deg2rad(self.angle))
        cos_a = np.cos(np.deg2rad(self.angle))

        speed_sin, speed_cos = MAX_SPEED * sin_a, MAX_SPEED * cos_a
        dy, dx = 0.0, 0.0
        if keys[pg.K_w]:
            dx += speed_sin
            dy += speed_cos
        if keys[pg.K_s]:
            dx -= speed_sin
            dy -= speed_cos
        if keys[pg.K_a]:
            dx -= speed_sin
            dy += speed_cos
        if keys[pg.K_d]:
            dx += speed_sin
            dy -= speed_cos

        self.pos[0] += dx
        self.pos[1] += dy

        if keys[pg.K_LEFT]:
            self.angle += 0.2 #Rotation speed
        if keys[pg.K_RIGHT]:
            self.angle -= 0.2 