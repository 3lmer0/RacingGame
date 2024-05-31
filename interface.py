import pygame as pg
from settings import *
from barriers import Barriers

WHITE = (255, 255, 255)

class Interface:
    def __init__(self, app, player):
        pg.init()
        pg.font.init()

        self.clock = pg.time.Clock()
        self.startTick = 0.0
        self.barriers = Barriers()
        self.time = 0.0
        self.start = False

        self.app = app
        self.player = player
        
        self.gear_font = pg.font.Font("assets/font/public_pixel.ttf", 100)
        self.controls_font = pg.font.Font("assets/font/public_pixel.ttf", 15)

    def update(self):
        self.clock.tick(60)
        if (self.player.playerCollision.overlap(self.barriers.finishLine) and self.time < 10):
            self.startTick = pg.time.get_ticks()
            self.start = True
        elif (self.player.playerCollision.overlap(self.barriers.finishLine) and self.time > 10):
            self.start = False
        if (self.start == True):
            self.time = pg.time.get_ticks() - self.startTick
    
    def draw(self):
        gear_selection, gear = self.player.get_player_gear()

        gear_text = self.gear_font.render(gear_selection[gear], True, WHITE)
        gear_text_rect = gear_text.get_rect()
        gear_text_rect.center = (WIDTH - 100, HEIGHT - 100)

        controls_text = self.controls_font.render("Controls: WASD to drive | Space to jump | Q/E to change gears (must be stopped) | R to restart | Escape to quit", True, WHITE)
        controls_text_rect = controls_text.get_rect()
        controls_text_rect.topleft = (20, 20)

        time_text = self.controls_font.render(f"TIME: {(self.time / 1000) : .3f}", True, WHITE)
        time_rect = time_text.get_rect()
        time_rect.center = (HALF_WIDTH, HALF_HEIGHT - 100)

        self.app.screen.blit(gear_text, gear_text_rect)
        self.app.screen.blit(controls_text, controls_text_rect)
        self.app.screen.blit(time_text, time_rect)