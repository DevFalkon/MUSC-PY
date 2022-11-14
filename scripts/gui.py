import pygame as py
from pygame import gfxdraw
import math

row_r,col_r = [0.075,0.775,0.15],[0.2,0.8]

with open("settings.txt", 'r') as file:
    dat = [eval(i) for i in file.read().split('\n') if i]


font_name = dat[0]['Font name']
font_size = dat[1]['Font size']

elem_height = 40

curr_select = None
bttn = None
curr_song = None
duration = None
sng_name_list = []


def colours(colour):
    col={
        'black':(0,0,0),
        'white':(255,255,255),
        'grey':(150,150,150),
        'red':(255,0,0),
        'blue':(0,0,255),
        'dark grey':(70,70,70)
    }
    return col[colour]


#uses pygames antialiasing to render circles with smoother perimeter
def draw_circle(surface, x, y, radius, color):
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)

#calculating the distace of the cursor from centre of the circle using distance formula
def circle_dist(x_cord,y_cord,mouse_x,mouse_y):
    x_dist = (x_cord-mouse_x)**2
    y_dist = (y_cord-mouse_y)**2
    dist = math.sqrt(x_dist+y_dist)
    return dist


def top_bar(width,height,screen, colour):
    global row_r,col_r
    x,y = 0,0
    py.draw.rect(screen,colour,rect=(x,y,width,height*row_r[0]-2))


def side_bar(width,height,screen, colour):
    global row_r,col_r
    x,y =0,height*row_r[0]
    py.draw.rect(screen,colour,rect=(x,y,width*col_r[0]-2,height*row_r[1]-2))


def lower_bar(width,height,screen, colour):
    global row_r,col_r
    x,y = 0,height*(row_r[0]+row_r[1])
    py.draw.rect(screen,colours('black'),rect=(x,y-2,width,2))
    py.draw.rect(screen,colour,rect=(x,y,width,height*row_r[2]))


def layout_update(width,height,screen,colour):
    top_bar(width,height,screen,colour)
    side_bar(width,height,screen,colour)
    lower_bar(width,height,screen,colour)
