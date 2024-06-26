import pygame as pg
import numpy as np

from settings import *
from numba import njit, prange
from collisions import CollisionRect

# Load and convert images once
FLOOR_TEX = pg.image.load("assets/textures/bowsaaFixed.png")
CEIL_TEX = pg.image.load("assets/textures/wispy.png")
CEIL_TEX = pg.transform.scale(CEIL_TEX, FLOOR_TEX.get_size())

class Mode7:
    def __init__(self, app):
        self.app = app
        self.textures = {
            'floor': FLOOR_TEX.convert(),
            'ceil': CEIL_TEX.convert()
        }
        self.tex_size = self.textures['floor'].get_size()
        self.floor_array = pg.surfarray.array3d(self.textures['floor'])
        self.ceil_array = pg.surfarray.array3d(self.textures['ceil'])
        self.screen_array = pg.surfarray.array3d(pg.Surface(WIN_RES))

    def update(self, player):
        self.screen_array = self.render_frame(floor_array = self.floor_array,
                                              ceil_array =  self.ceil_array,
                                              screen_array = self.screen_array, 
                                              tex_size = self.tex_size,
                                              angle = player.angle,
                                              player_pos  = player.pos,
                                              alt = player.alt)

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
                fog = (1 - depth) * 125

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

    