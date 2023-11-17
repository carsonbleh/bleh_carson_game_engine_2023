# This file was created by: Carson Bleh

# content from kids can code: http://kidscancode.org/blog/

'''
Goals: Reach the purple platform on the top left and reach the gold "crown"
Rules: move in the air and don't die
When Mobs are hit, players dies
When powerups are hit, player gains more hp/points
When player has 0 points, the player respawns
Player can't move off the screen
'''

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
import os
from settings import *
from sprites import *
import math
 
 
vec = pg.math.Vector2
 
# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')


class Game:
    def __init__(self):
        # init pygame and create a window
        pg.init()
        pg.mixer.init()
        # defines the screen and display for the game while the code is running
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game...")
        self.clock = pg.time.Clock()
        self.running = True
   
    def new(self):
        # create a group for all sprites
        # defines the score of the player
        self.score = 10
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_ice = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_powerups = pg.sprite.Group()
        self.all_crowns = pg.sprite.Group()
        # instantiate classes
        self.player = Player(self)
        # add instances to groups
        self.all_sprites.add(self.player)
 
        for p in PLATFORM_LIST:
            # instantiation of platforms
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)
       
        # coordinates for new platform
        for i in range(0,1):
            ice_plat = Ice(self, 300, 220, 150, 15, "normal")
            self.all_sprites.add(ice_plat)
            self.all_platforms.add(ice_plat)
 
        for m in range(0,6):
            # generates 6 mobs randomly on screen
            m = Mob(randint(0, WIDTH), randint(0, math.floor(HEIGHT/2)), 20, 20, "normal")
            # gives mobs their own class or sprite
            self.all_sprites.add(m)
            self.all_mobs.add(m)

        for p in range(0,2):
            # generates 2 powerups randomly on screen
            p = Powerup(randint(0, WIDTH), randint(0, math.floor(HEIGHT/2)), 20, 20, "normal")
            # gives powerups their own class or sprite
            self.all_sprites.add(p)
            self.all_powerups.add(p)

        # generates the crown to win
        for c in range(0,1):
            #paces on top of purple platform
            c = Crown(190, 75, 20, 20)
            self.all_sprites.add(c)
            self.all_crowns.add(c)
 
        self.run()
   
 
    def run(self):
        # while the program is running, the program is checking for updates across events updates and draw
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
 
    def update(self):
        # defines that the game updates if a player collides with a mob
        mhits = pg.sprite.spritecollide(self.player, self.all_mobs, False)
        # if the player hits a mob, they lose points
        if mhits:
            print('this collision happened in main')
            self.score -= 10
        # if the player hits a powerup, they gain points
        phits = pg.sprite.spritecollide(self.player, self.all_powerups, False)
        if phits:
            print('this collision happened in main')
            self.score += 10
        # if the player's score becomes 0, they respawn at the beginning with 10 points
        #if self.score == 0:
                #self.player.pos = vec(WIDTH/2, HEIGHT/2)
                #self.score = 10
        if self.score == 0:
            self.player.pos = vec(WIDTH/2, HEIGHT/2)
            self.score = 10
        # when player makes contact with crown, "you win" typed on screen
        chits = pg.sprite.spritecollide(self.player, self.all_crowns, False)
        if chits:
            self.draw_text("You Win!", 50, WHITE, WIDTH/2, HEIGHT/3)
        self.all_sprites.update()


        # make the player unable to run off the screen
        if self.player.pos.x < 0:
            self.player.pos.x = WIDTH
        if self.player.pos.x > WIDTH:
            self.player.pos.x = 0
       
        # prevents the player from falling through the platform
        if self.player.vel.y >= 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                self.player.vel.x = hits[0].speed*1.5
 
                   
         # prevents the player from jumping up through a platform
        elif self.player.vel.y <= 0:
            hits = pg.sprite.spritecollide(self.player, self.all_mobs, False)
            if hits:
                self.player.acc.y = 5
                self.player.vel.y = 0
                print("ouch")
                if self.player.rect.bottom >= hits[0].rect.top - 1:
                    self.player.rect.top = hits[0].rect.bottom
                if self.player.rect.top <= hits[0].rect.top - 1:
                    self.player.rect.bottom = hits[0].rect.bottom
            # if the player's score becomes 0, their score resets and they respawn at the beginning
            #if self.score == 0:
                #self.player.pos = vec(WIDTH/2, HEIGHT/2)
                #self.score = 10
               
                   
    def events(self):
        for event in pg.event.get():
        # check for closed window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
               
    def draw(self):
        ############ Draw ################
        # draw the background screen
        self.screen.fill(BLACK)
        # draw all sprites
        self.all_sprites.draw(self.screen)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH/2, HEIGHT/10)
        chits = pg.sprite.spritecollide(self.player, self.all_crowns, False)
        # types "you win" when player collides with crown
        if chits:
            self.draw_text("You Win!", 50, WHITE, WIDTH/2, HEIGHT/3)
        # buffer - after drawing everything, flip display
        pg.display.flip()

    # this defines the text that will appear on the screen
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
 
    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass
 

g = Game()
while g.running:
    g.new()
 
 
pg.quit()

