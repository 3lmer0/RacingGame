import pygame as pg
import sys
from settings import *
from mode7 import Mode7


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.mode7 = Mode7(self)

        #TODO: WRITE BETTER CODE
        #This section in particular
        self.mario = pg.image.load("textures/marioBack.png")
        self.marioLeft = pg.image.load("textures/marioLeft.png")
        self.marioRight = pg.image.load("textures/marioRight.png")
        self.marioLeft = pg.transform.scale(self.marioLeft, (300, 300))
        self.marioRight = pg.transform.scale(self.marioRight, (300, 300))
        self.mario = pg.transform.scale(self.mario, (300, 300))

        self.set_time()
        self.last_time = self.time

    def update(self):
        dt = self.time - self.last_time
        self.last_time = self.time

        self.mode7.update(dt)
        self.clock.tick()
        
        pg.display.set_caption(f'{self.clock.get_fps() : .1f}')
 
    def draw(self):
        self.mode7.draw()

        key = pg.key.get_pressed()
        if key[pg.K_d] and not key[pg.K_a]:
            self.screen.blit(self.marioRight, (HALF_WIDTH - 150, 650))
        if key[pg.K_a] and not key[pg.K_d]:
            self.screen.blit(self.marioLeft, (HALF_WIDTH - 150, 650))
        if not (key[pg.K_a] or key[pg.K_d]) or (key[pg.K_a] and key[pg.K_d]):
            self.screen.blit(self.mario, (HALF_WIDTH - 150, 650))

        pg.display.flip()

    def set_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def check_event(self):
        for i in pg.event.get():
            if i.type == pg.QUIT or (i.type == pg.KEYDOWN and i.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_event()
            self.set_time()
            self.update()
            self.draw()


if __name__ == '__main__':
    app = Game()
    app.run()