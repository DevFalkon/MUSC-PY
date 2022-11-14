from scripts.gui import colours, draw_circle, col_r, row_r, circle_dist
import pygame as py
from pygame import gfxdraw

class play_pause:

    def __init__(self,screen,rad,width, height) -> None:
        self.rad = rad
        self.x = None
        self.y = None
        self.screen = screen
        self.height = height
        self.width = width
        self.play = False

    def render(self):

        x = int(self.width//2)
        y = int(self.height*(1-row_r[2]/2))+14

        self.x,self.y=x,y

        #Draw the button
        py.draw.rect(self.screen, colours('grey'), rect=(x-self.rad-2,y-self.rad-2,2*self.rad+9,2*self.rad+9))
        draw_circle(self.screen, x, y,self.rad,colours('white'))

        if self.play:
            img = py.image.load('graphics\\pause.png').convert_alpha()
            self.screen.blit(img, (self.x-30,self.y-34))
        else:
            img = py.image.load('graphics\\play.png').convert_alpha()
            self.screen.blit(img, (self.x-30,self.y-34))

        py.display.update(py.Rect(x-self.rad-2,y-self.rad-2,2*self.rad+9,2*self.rad+9))


class cir_bttn:
    def __init__(self,screen,rad,img) -> None:
        self.screen = screen
        self.img = img
        self.rad = rad
        self.add = 0

    def render(self,x,height):
        self.x = x
        self.y = int(height*(1-row_r[2]/2))+14

        py.draw.rect(self.screen, colours('grey'), rect=(x-self.rad-2,self.y-self.rad-2,2*self.rad+9,2*self.rad+9))
        draw_circle(self.screen, self.x, self.y,self.rad,colours('white'))

        img = py.image.load(f'graphics\\{self.img}').convert_alpha()
        self.screen.blit(img, (self.x-30-self.add,self.y-30))

        py.display.update(py.Rect(x-self.rad-2,self.y-self.rad-2,2*self.rad+9,2*self.rad+9))

