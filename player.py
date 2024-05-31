import numpy as np
import pygame as pg
from settings import *

from collisions import CollisionRect
from barriers import Barriers

def lerp(a, b, t):
    return a + (b - a) * t

class Player:

    def __init__(self):   
        #Initialize movement values
        self.pos = np.array([61.0, -73.01])
        self.alt = 1.0
        self.angle = 180.0
        self.velocity = 0.0

        self.steer_time_elapsed = 0.0
        self.jump_time_elapsed = 0.0

        self.jumped = False
        self.is_jumping = False
        self.is_falling = False

        self.gear_selection = ["D", "R"]
        self.gear = 0

        self.player_collision = CollisionRect(self.spritePos, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.barriers = Barriers()
    
    @property
    def spritePos(self):
        return np.array([self.pos[0] + OFFSET * np.sin(np.deg2rad(90 - self.angle)),
                         self.pos[1] + OFFSET * np.cos(np.deg2rad(90 - self.angle))])

    def update(self,dt):
        # Update collRect
        self.player_collision.position = self.spritePos

        #self.devMovement(dt)
        self.movement(dt)

    def devMovement(self, dt):
        keys = pg.key.get_pressed()
        sin_a = np.sin(np.deg2rad(self.angle))
        cos_a = np.cos(np.deg2rad(self.angle))
    
        speed_sin, speed_cos = DEV_MAX_SPEED * sin_a, DEV_MAX_SPEED * cos_a
        dy, dx = 0, 0
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx -= speed_cos
            dy -= speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy -= speed_cos
        if keys[pg.K_d]:
            dx -= speed_sin
            dy += speed_cos

        self.pos[0] += dx
        self.pos[1] += dy

        if keys[pg.K_LEFT]:
            self.angle -= 0.7 #Rotation speed
        if keys[pg.K_RIGHT]:
            self.angle += 0.7 

        if(self.player_collision.overlap(
            CollisionRect(
                np.array([49.95, -36.45]),
                w = 47.6,
                h = 5.0
            )
        )):
            print("COLLISION!!!")
        else:
            print("NO Collision")

    def movement(self, dt):
        keys = pg.key.get_pressed()
        
        # Gear selection
        if int(self.velocity) == 0.0: # Use floor to allow a little leniency
            if keys[pg.K_q] and self.gear > 0:
                self.gear -= 1
            elif keys[pg.K_e] and self.gear < (len(self.gear_selection) - 1):
                self.gear += 1

        # Car acceleration and braking
        gear_actions = {
            0: self.drive,
            1: self.reverse
        }

        if self.gear in gear_actions:
            gear_actions[self.gear](keys, dt)

        # Pre-calculate constant values
        steering_duration_inv = 1 / STEERING_DURATION
        jump_lerp_duration_inv = 1 / JUMP_LERP_DURATION

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
        self.angle = lerp(self.angle, self.angle - new_angle, self.steer_time_elapsed * steering_duration_inv)

        # Jumping (controlled in main.py) using lerp to smoothen the change in jump height
        if self.jumped:
            if self.jump_time_elapsed <= JUMP_LERP_DURATION:
                # Checks current state and lerps values accordingly
                if self.is_jumping and not self.is_falling:
                    self.alt = lerp(self.prev_alt, self.prev_alt - MAX_JUMP_HEIGHT, self.jump_time_elapsed * jump_lerp_duration_inv)
                else:
                    self.alt = lerp(self.alt, self.prev_alt, self.jump_time_elapsed * jump_lerp_duration_inv)
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

        # Below portion is for collision detection
        barrCtr = any(self.player_collision.overlap(colls) for colls in self.barriers.rects)
        if not barrCtr:
            # Velocity plus additional bounceback force is added so player doesn't get stuck
            self.velocity = -(self.velocity * OBSTACLE_HIT_SPEED_RETENTION + BOUNCE_FORCE)
            if int(self.velocity) == 0.0:
                self.velocity = 0.0

        # Apply computations
        sin_a = np.sin(np.deg2rad(self.angle))
        cos_a = np.cos(np.deg2rad(self.angle))

        speed_sin = self.velocity * dt * sin_a
        speed_cos = self.velocity * dt * cos_a

        self.pos[0] += speed_cos
        self.pos[1] += speed_sin
    
    def drive(self, keys, dt):
        is_jumping_or_falling = self.is_jumping or self.is_falling

        # Player moves forwards
        if keys[pg.K_w] and self.velocity <= MAX_SPEED and not is_jumping_or_falling:
            self.velocity += ACCELERATION * dt
        # Player brakes
        elif keys[pg.K_s] and not is_jumping_or_falling:
            # Currently moving forwards
            if self.velocity > 0.0:
                self.velocity = max(self.velocity - BRAKE * dt, 0.0)
            # Currently moving backwards from bouncing back
            elif self.velocity < 0.0:
                self.velocity = min(self.velocity + BRAKE * dt, 0.0)
        else:
            # Don't lose speed while jumping
            if not is_jumping_or_falling:
                # Speed loss
                if self.velocity > 0.0:
                    self.velocity = max(self.velocity - SPEED_LOSS * dt, 0.0)
                elif self.velocity < 0.0:
                    self.velocity = min(self.velocity + SPEED_LOSS * dt, 0.0)
    
    def reverse(self, keys, dt):
        is_jumping_or_falling = self.is_jumping or self.is_falling

        # Player moves backwards
        if keys[pg.K_w] and self.velocity <= MAX_SPEED and not is_jumping_or_falling:
            self.velocity -= REVERSE_ACCELERATION * dt
        # Player brakes
        elif keys[pg.K_s] and not is_jumping_or_falling:
            # Currently moving backwards
            if self.velocity < 0.0:
                self.velocity = max(self.velocity + BRAKE * dt, 0.0)
            # Currently moving forwards from bouncing back
            elif self.velocity > 0.0:
                self.velocity = min(self.velocity - BRAKE * dt, 0.0)
        else:
            # Don't lose speed while jumping
            if not is_jumping_or_falling:
                # Speed loss
                if self.velocity > 0.0:
                    self.velocity = max(self.velocity - SPEED_LOSS * dt, 0.0)
                elif self.velocity < 0.0:
                    self.velocity = min(self.velocity + SPEED_LOSS * dt, 0.0)

    def set_player_angle(self, angle):
        if angle == 0.0: angle = 360.0
        self.angle = angle
    
    def set_player_pos(self, x, y):
        self.pos[0], self.pos[1] = x, y

    def get_player_gear(self):
        return self.gear_selection, self.gear