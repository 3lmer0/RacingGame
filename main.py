import pygame as pg
import sys, time
from settings import *
from mode7 import Mode7
from player import Player
from interface import Interface

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode(WIN_RES)
        self.mode7 = Mode7(self)
        self.player = Player()
        self.interface = Interface(self, self.player)

        self.IMAGES = {
            "mario_back": pg.transform.scale(pg.image.load("assets/textures/marioBack.png"), (300, 300)),
            "mario_left": pg.transform.scale(pg.image.load("assets/textures/marioLeft.png"), (300, 300)),
            "mario_right": pg.transform.scale(pg.image.load("assets/textures/marioRight.png"), (300, 300))
        }

        self.prev_time = time.time()

    def update(self):
        # Uses python time library to make delta time frame independent
        dt = (time.time() - self.prev_time)
        self.prev_time = time.time()

        self.player.update(dt)
        self.mode7.update(self.player)
        self.interface.update()
   
        pg.display.set_caption(str(self.player.pos))
 
    def draw(self):
        self.mode7.draw()
        self.interface.draw()

        key = pg.key.get_pressed()
        if key[pg.K_d] and not key[pg.K_a]:
            self.screen.blit(self.IMAGES["mario_right"], (HALF_WIDTH - 150, 650))
        elif key[pg.K_a] and not key[pg.K_d]:
            self.screen.blit(self.IMAGES["mario_left"], (HALF_WIDTH - 150, 650))
        else:
            self.screen.blit(self.IMAGES["mario_back"], (HALF_WIDTH - 150, 650))

        if key[pg.K_r]:
            self.reset_player()

        pg.display.flip()
    
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and not self.player.jumped: # Removes the ability of holding down the jump key
                self.player_jump()
    
    def reset_player(self):
        self.player.velocity = 0.0
        self.player.set_player_pos(61.0, -73.01)
        self.player.set_player_angle(180.0)

        self.interface.startTick = 0
        self.interface.time = 0
        self.interface.start = False

    def player_jump(self):
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