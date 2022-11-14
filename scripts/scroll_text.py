import pygame as py
from scripts.gui import colours, font_name, font_size, col_r, row_r, font_offset, header_add, header_offset
from scripts.gui import curr_song


class scroll:

    def __init__(self,iterable,height,width,screen):
        self.iterable = iterable
        self.scroll_y = 0
        self.height = height
        self.width = width
        self.screen = screen
        self.elem_height = 40
        self.update_header = True
        self.duration = None
        self.curr_song = curr_song
        self.bttn = None
        self.y_add = 80
        self.header_h = self.elem_height+14
        self.offset = font_offset

    
    def render_header(self,x):

        py.draw.rect(self.screen,colours('black'),
        rect=(x+3,self.height*row_r[0]+self.y_add,self.width*col_r[1]-16,self.header_h))
        #Displaying header text
        font = py.font.Font(font_name, font_size+header_add)
        txt = font.render('NAME', True, colours('white'))
        self.screen.blit(txt, (x+38, self.height*row_r[0]+self.y_add+header_offset))
        txt = font.render('ARTIST', True, colours('white'))
        self.screen.blit(txt,(x+538, self.height*row_r[0]+self.y_add+header_offset))
        
        #Drwaing top and bottom white lines for the header
        py.draw.rect(self.screen, colours('white'), 
        rect=(x+3, self.height*row_r[0]+self.y_add, self.width*col_r[1]-16, 4))
        py.draw.rect(self.screen, colours('white'), 
        rect=(x+3, self.height*row_r[0]+self.elem_height+10+self.y_add, self.width*col_r[1]-16, 4))


    def render(self,mouse_x,mouse_y):
        
        font = py.font.Font(font_name, font_size)
        x,y = self.width*col_r[0],self.height*row_r[0]+self.y_add+self.header_h

        py.draw.rect(self.screen,colours('black'),
        rect=(x+3,y,self.width*col_r[1]-16,self.height*row_r[1]-self.header_h-self.y_add-2))

        sng_name_list = [i['name'] for i in self.iterable]
        sng_name_list.sort()


        for ind, song_name in enumerate(sng_name_list):

            #To change button colour if the cursor is over it
            if x+3<=mouse_x<=x+3+self.width*col_r[1]-16 and \
                y+self.scroll_y+self.elem_height*ind+3<=mouse_y<=y+self.elem_height*(ind+1)+self.scroll_y-3:
                col = colours('grey')
                if self.bttn == 1 and self.curr_song != song_name:
                    self.curr_song = song_name
                    self.duration = [i['duration'] for i in self.iterable if i['name'] == self.curr_song][0]
                    self.bttn = None
            else:
                col = colours('black')

            if y-self.header_h<=y+self.elem_height*ind+self.scroll_y<=self.height*row_r[1]+self.header_h:
                if col == colours('grey'):
                    py.draw.rect(self.screen, col, 
                    rect=(x+3, y+self.elem_height*ind+self.scroll_y+3, self.width*col_r[1]-16, self.elem_height-3))

                py.draw.rect(self.screen, colours('white'), 
                rect=(x+3, y+self.elem_height*(ind+1)+self.scroll_y, self.width*col_r[1]-16, 3))
                
                text = font.render(song_name, True, colours('white'))
                
                self.screen.blit(text,(x+38, y+self.elem_height*ind+3+self.scroll_y+self.offset))

                for track_data in self.iterable:
                    if track_data['name'] == song_name:
                        artist_name = track_data['artist']
                        break
                text = font.render(artist_name, True, colours('white'))

                self.screen.blit(text,(x+538, y+self.elem_height*ind+self.scroll_y+3+self.offset))
        

        if self.update_header:
            self.render_header(x)
            self.update_header = False
        self.bttn = None

        py.display.update(py.Rect(x+3,y,self.width*col_r[1]-16,self.height*row_r[1]-self.header_h-self.y_add-2))