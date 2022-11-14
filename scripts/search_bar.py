import pygame as py
from scripts.gui import colours, draw_circle, font_name,font_size, col_r, row_r

class searchbar:

    def __init__(self,screen,width,height) -> None:
        self.width = width
        self.height = height
        self.screen = screen
        self.search_term = 'search'
        self.font = py.font.SysFont(font_name, font_size)

    def render(self) -> None:
        rad = int(self.height*row_r[0]*0.75//2)
        py.draw.rect(self.screen, colours('grey'), rect = (self.width*col_r[0]-2,7,self.width*0.45+2*rad+5,rad*2+1))
        py.draw.rect(self.screen, colours('white'), rect =(self.width*col_r[0]+rad,7,self.width*0.45,rad*2+1))
        draw_circle(self.screen, int(self.width*col_r[0]+rad), 7+rad, rad, colours('white'))
        draw_circle(self.screen, int(self.width*(col_r[0]+0.45)+rad), 7+rad, rad, colours('white'))
        if self.search_term == 'search':
            text = self.font.render(self.search_term, True, colours('grey'))
        else:
            text = self.font.render(self.search_term, True, colours('black'))
        self.screen.blit(text,(self.width*col_r[0]+rad,7))
        py.display.update(py.Rect(self.width*col_r[0]-2,7,self.width*0.45+2*rad+5,rad*2+1))