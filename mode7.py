import pygame as pg
import numpy as np
from settings import *
from numba import njit, prange


class Mode7:
    def __init__(self, app):
        self.app = app
        self.floor_tex = pg.image.load("textures/gameCourse.png").convert()
        self.tex_size = self.floor_tex.get_size()
        self.floor_array = pg.surfarray.array3d(self.floor_tex)

        self.ceil_tex = pg.image.load("textures/sky.png").convert()
        self.ceil_tex = pg.transform.scale(self.ceil_tex, self.tex_size)
        self.ceil_array = pg.surfarray.array3d(self.ceil_tex)

        self.screen_array = pg.surfarray.array3d(pg.Surface(WIN_RES))

        self.pos = np.array([0.0, 0.0])
        self.alt = 1
        self.angle = 0
        self.velocity = 0

    def update(self, dt):
        self.movement(dt)
        self.screen_array = self.render_frame(self.floor_array, self.ceil_array, self.screen_array, 
                                              self.tex_size, self.angle, self.pos, self.alt)

    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)
    
    #Static method and njit used for reasonable frame rates
    #Reason for slowdown without jit is python dynamic typing
    @staticmethod
    @njit(fastmath=True, parallel=True)
    def render_frame(floor_array, ceil_array, screen_array, tex_size, angle, player_pos, alt):
        sin, cos = np.sin(np.deg2rad(angle)), np.cos(np.deg2rad(angle))

        # iterating over the screen array
        for i in prange(WIDTH):
            new_alt = alt
            for j in range(HALF_HEIGHT, HEIGHT):
                x = HALF_WIDTH - i
                y = j + FOCAL_LEN
                z = j - HALF_HEIGHT + new_alt

                # rotation
                px = (x * cos - y * sin)
                py = (x * sin + y * cos)

                # floor projection and transformation
                floor_x = px / z - player_pos[1]
                floor_y = py / z + player_pos[0]

                # floor pos and color
                floor_pos = int(floor_x * SCALE % tex_size[0]), int(floor_y * SCALE % tex_size[1])
                floor_col = floor_array[floor_pos]

                # ceil projection and transformation
                ceil_x = alt * px / z - player_pos[1] * 0.3
                ceil_y = alt * py / z + player_pos[0] * 0.3

                # ceil pos and color
                ceil_pos = int(ceil_x * SCALE % tex_size[0]), int(ceil_y * SCALE % tex_size[1])
                ceil_col = ceil_array[ceil_pos]

                # shading
                depth = 2 * abs(z) / HALF_HEIGHT
                depth = min(max(2.5 * (abs(z) / HALF_HEIGHT), 0), 1)
                fog = (1 - depth) * 230

                floor_col = (floor_col[0] * depth + fog,
                             floor_col[1] * depth + fog,
                             floor_col[2] * depth + fog)

                ceil_col = (ceil_col[0] * depth + fog,
                            ceil_col[1] * depth + fog,
                            ceil_col[2] * depth + fog)

                # fill screen array
                screen_array[i, j] = floor_col
                screen_array[i, -j] = ceil_col

                # next depth
                new_alt += alt

        return screen_array

    def movement(self, dt):
        keys = pg.key.get_pressed()
        
        # Car acceleration and braking
        if keys[pg.K_w] and not self.velocity > MAX_SPEED:
            self.velocity += ACCELERATION * dt
        elif keys[pg.K_s]:
            if self.velocity > 0:
                self.velocity -= BRAKE * dt
            else:
                self.velocity = 0
        else:
            if self.velocity > 0:
                self.velocity -= SPEED_LOSS * dt
            else:
                self.velocity = 0

        # Car steering using Sigmoid function with contained angular velocity
        new_angle = (MAX_STEERING * 2) / (1 + np.exp(-STEERING_SPEED * self.velocity)) - MAX_STEERING
        
        if keys[pg.K_a]:
            self.angle -= new_angle
        if keys[pg.K_d]:
            self.angle += new_angle

        # Apply computations
        sin_a = np.sin(np.deg2rad(self.angle))
        cos_a = np.cos(np.deg2rad(self.angle))

        speed_sin = self.velocity * dt * sin_a
        speed_cos = self.velocity * dt * cos_a

        self.pos[0] += speed_cos
        self.pos[1] += speed_sin