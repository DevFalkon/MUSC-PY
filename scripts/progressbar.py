from scripts.gui import colours
from pygame import draw, display, Rect

class progress_bar:

    def __init__(self,screen,width,height) -> None:
        self.bar_len = 0
        self.seek = None
        self.play_len = 0
        self.screen = screen
        self.width = width
        self.height = height
        self.row_r = [0.075,0.775,0.15]
        self.col_r = [0.2,0.8]
        self.curr_song = None
        self.duration = None
        self.bttn = None

    def render_bar(self,mouse_x,mouse_y,len_played):

        draw.rect(self.screen, colours('dark grey'),rect = (20,self.height*(1-self.row_r[2])+20,self.width-40,10))
        if self.curr_song:
            self.prev_pos = len_played
            self.bar_len = ((self.width-40)/(self.duration+15))*(len_played/1000)+self.play_len
            draw.rect(self.screen, colours('white'),rect = (20,self.height*(1-self.row_r[2])+20,self.bar_len,10))
            if 20<=mouse_x<=self.width-20 and self.height*(1-self.row_r[2])+10<=mouse_y<=self.height*(1-self.row_r[2])+40:
                draw.rect(self.screen, colours('white'),rect=(mouse_x,self.height*(1-self.row_r[2])+20,1,10))
                if self.bttn == 1:
                    self.bttn = 0
                    self.seek =((mouse_x-20)*(self.duration))/(self.width-20)
                    self.play_len = mouse_x-20
        self.bttn = None
        display.update(Rect(20,self.height*(1-self.row_r[2])+20,self.width-40,10))