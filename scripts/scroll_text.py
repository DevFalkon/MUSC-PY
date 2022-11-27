from scripts.gui import colours, font_name, font_size
from scripts.gui import curr_song
import time
import pygame as py


class AdvScroll:
    def __init__(self, screen, x, y, width,height,iterable) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scroll = 0 #Default value = 0
        self.scroll_sens = 7 #Default value = 7
        self.iterable = iterable
        self.spacer = 3 #Default value = 3
        self.screen = screen
        self.left_over = 0
        self.sens = 1  #Dont change the value as it may crash the app
        self.sorted = None
        self.offset = 5

    #to get maximum nuber of rows that can be displayed at once
    def get_max_rows(self,height):
        max_row = (self.height)//(self.spacer+height)
        return max_row

    #To find the coordinate when the last button is completely vissible
    def get_max_y(self, height):
        if len(self.iterable) > self.get_max_rows(height):
            low = self.scroll+self.y+len(self.iterable)*(self.spacer+height)
            return low
        return None

    def disp_iter(self):
        ls = [[i['name'], i['artist']] for i in self.iterable]
        ls.sort(key = lambda x:x[0])
        return ls

    def disp_scroll(self,height) -> None:
        #To remove previously rendered buttons
        py.draw.rect(self.screen,colours('black'), rect=(self.x,self.y,self.width,self.height+2))

        #Displaying buttons
        if self.sorted:
            pass
        else:
            self.sorted = self.disp_iter()

        font = py.font.Font(font_name, font_size)
        for ind,elems in enumerate(self.sorted):
            if self.y-height<=self.y+self.scroll+ind*(self.spacer+height)<self.y+self.height:
                #Drawing the seperator for each bttn
                py.draw.rect(self.screen, colours('white'), rect=(self.x,self.y+self.scroll+ind*(self.spacer+height)+height, self.width, self.spacer))
                
                #Rendering song name and artist name
                sng_name = font.render(elems[0], True, colours('white'))
                artist_name = font.render(elems[1], True, colours('white'))
                self.screen.blit(sng_name,(self.x+38, self.y+self.scroll+ind*(self.spacer+height)+self.offset))
                self.screen.blit(artist_name,(self.x+488, self.y+self.scroll+ind*(self.spacer+height)+self.offset))

        py.draw.rect(self.screen,colours('black'), rect=(self.x,self.y+self.height,self.width,4))
        py.display.update(py.Rect(self.x,self.y,self.width,self.height+2))

    def get_sng_name(self,height, m_y):
        for ind,elems in enumerate(self.sorted):
            if m_y:
                if self.y+self.scroll+ind*(self.spacer+height)<m_y<self.y+self.scroll+ind*(self.spacer+height)+height:
                    return elems[0]
            
    def render_header(self,height)->None:
        py.draw.rect(self.screen, colours('black'), rect = (self.x,self.y-height,self.width,height))
        py.draw.rect(self.screen, colours('white'), rect = (self.x,self.y-height, self.width, 4))
        py.draw.rect(self.screen, colours('white'), rect = (self.x,self.y-4, self.width, 4))
        

        font = py.font.Font(font_name, font_size+10)
        sng_name = font.render('NAME', True, colours('white'))
        artist_name = font.render('ARTIST', True, colours('white'))
        self.screen.blit(sng_name,(self.x+38, self.y-height+5))
        self.screen.blit(artist_name,(self.x+488, self.y-height+5))

        py.display.update(py.Rect(self.x,self.y-height,self.width,height))
        
    def render(self, height) -> None:
        
        max_y = self.get_max_y(height)
        upd = True
        if self.get_max_rows(height)<len(self.iterable):

            if max_y>=self.y+self.height or self.left_over>0:
                #SMOOTH SCROLLING
                while self.left_over!=0:
                    upd =  False

                    #Scroll down
                    if self.left_over <=0:
                        self.left_over +=self.sens
                        self.scroll-=self.sens

                    #Scroll up
                    if self.left_over>0:
                        self.left_over-=self.sens
                        if self.scroll !=0:
                            self.scroll+=self.sens
                    
                    if self.scroll == 0:
                        self.left_over = 0

                    max_y = self.get_max_y(height)
                    if max_y<self.y+self.height-40:
                        self.left_over = 0

                    #rendering all the updates made
                    self.disp_scroll(height)
                    time.sleep(0.001)
            else:
                self.left_over = 0
            
            max_y = self.get_max_y(height)
            while max_y<self.y+self.height-1:
                self.scroll+=1
                self.disp_scroll(height)
                time.sleep(0.001)
                max_y = self.get_max_y(height)

        else:
            self.left_over = 0
        
        if upd:
            #rendering the buttons without scrolling
            self.disp_scroll(height)