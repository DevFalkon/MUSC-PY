import pygame as py
import os, sys, time
py.init()

width = None
height = None


def setup(w,h):
    global width, height
    width = w
    height = h

    screen = py.display.set_mode((width, height), py.RESIZABLE)
    py.display.set_caption('Search')
    logo = py.image.load("graphics\\logo.png")
    py.display.set_icon(logo)

    return screen


class Bttn:
    def __init__(self, screen, colour, x,y,height,width) -> None:
        self.colour = colour
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.screen = screen
    
    def render(self):
        py.draw.rect(self.screen, self.colour, rect=(self.x,self.y,self.width,self.height))
    
    def text(self, text):
        pass


class AdvScroll:
    def __init__(self, up_lim, low_lim, iterable, screen) -> None:
        self.up_lim = up_lim
        self.low_lim = low_lim
        self.scroll = 0 #Default value = 0
        self.scroll_sens = 7 #Default value = 7
        self.iterable = iterable
        self.spacer = 3 #Default value = 3
        self.ycord = self.up_lim
        self.screen = screen
        self.left_over = 0
        self.sens = 1  #Dont change the value as it may crash the app

    #to get maximum nuber of rows that can be displayed at once
    def get_max_rows(self,height):
        row = (self.spacer+height)//(self.low_lim-self.up_lim)
        return row

    #To find the coordinate when the last button is completely vissible
    def get_max_y(self, height):
        if len(self.iterable) > self.get_max_rows(height):
            low = self.scroll+self.up_lim+len(self.iterable)*(self.spacer+height)
            return low
        return None

    def disp_scroll(self,height) -> None:
        #Displaying buttons
        for ind,elem in enumerate(self.iterable):
            bttn = Bttn(self.screen,(0,0,255),10, self.up_lim+self.scroll+ind*(self.spacer+height), height, 200)
            bttn.render()
        
        #---TESTING----
        py.draw.rect(self.screen, (0,255,0), rect=(0,0,400,self.up_lim))
        py.draw.rect(self.screen, (0,255,0), rect=(0,self.low_lim, 400,500))
        #------------------
        
        py.display.update()

    def render(self, height) -> None:
        y_max = self.get_max_y(height)

        #SMOOTH SCROLLING
        while self.left_over!=0:
            #To remove previously rendered buttons
            self.screen.fill((0,0,0))

            #Scroll down
            if self.left_over <0:
                self.left_over +=self.sens
                self.scroll-=self.sens

            #Scroll up
            if self.left_over>0:
                self.left_over-=self.sens
                self.scroll+=self.sens

            #rendering all bttns
            self.disp_scroll(height)
            time.sleep(0.003)

        else:
            #rendering the buttons without scrolling
            self.disp_scroll(height)


def get_dir():
    dir_dict = {}
    for i in range(65,91):
        try:
            dir_dict[chr(i)] = [i for i in os.listdir(f'{chr(i)}://') if i[0] != '$' and ('.' not in i or i.endswith == '.py')]
        except:
            pass
    return dir_dict

def main(width,height):
    screen = setup(width,height)

    main_dirs = get_dir()

    main_dirs = list(main_dirs.values())[0]
    scroll_txt = AdvScroll(40, height-40, main_dirs, screen)

    while 1:
        scroll_txt.render(30)

        force = 0
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            
            if event.type == py.MOUSEWHEEL:
                scroll_txt.left_over += event.y*10
                force +=event.y*5
        scroll_txt.left_over+=force
        time.sleep(0.01)
    

main(400,500)

    
