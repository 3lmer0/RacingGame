import pygame as pg
import numpy as np
import sys, time

from settings import *
from mode7 import Mode7
from player import Player


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.mode7 = Mode7(self)
        self.player = Player()

        #TODO: WRITE BETTER CODE
        #This section in particular
        self.mario = pg.image.load("textures/marioBack.png")
        self.marioLeft = pg.image.load("textures/marioLeft.png")
        self.marioRight = pg.image.load("textures/marioRight.png")
        self.marioLeft = pg.transform.scale(self.marioLeft, (300, 300))
        self.marioRight = pg.transform.scale(self.marioRight, (300, 300))
        self.mario = pg.transform.scale(self.mario, (300, 300))

        self.prev_time = time.time()

    def update(self):
        # Uses python time library to make delta time frame independent
        dt = (time.time() - self.prev_time)
        self.prev_time = time.time()

        self.player.update(dt)
        self.mode7.update(self.player)
        self.clock.tick()
        
        pg.display.set_caption(str(self.player.pos))
 
    def draw(self):
        self.mode7.draw()

        key = pg.key.get_pressed()
        if key[pg.K_d] and not key[pg.K_a]:
            self.screen.blit(self.marioRight, (HALF_WIDTH - 150, 650))
        if key[pg.K_a] and not key[pg.K_d]:
            self.screen.blit(self.marioLeft, (HALF_WIDTH - 150, 650))
        if not (key[pg.K_a] or key[pg.K_d]) or (key[pg.K_a] and key[pg.K_d]):
            self.screen.blit(self.mario, (HALF_WIDTH - 150, 650))
        if key[pg.K_b]:
            self.player.set_player_pos(61.0, 29.35)
            self.player.set_player_angle(180.0)

        pg.display.flip()
 
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and not self.player.jumped: # Removes the ability of holding down the jump key
                self.player.prev_alt = self.player.alt
                self.player.is_jumping = True
                self.player.jumped = True
                
    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    app = Game()
    app.run()