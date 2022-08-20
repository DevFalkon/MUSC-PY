import math
from pygame import gfxdraw
import pygame as py
colours={
    'red':(255,0,0),
    'green': (0,255,0),
    'blue' :(0,0,255),
    'black':(0,0,0),
    'white':(255,255,255),
    'light grey':(192,192,192),
    'very dark grey':(64,64,64),
    'text grey':(160,160,160)
}

def gui_init(py):
    display = py.display
    display.init()
    py.display.set_caption('MUSC-PY')
    pygame_icon = py.image.load('logo.png')
    py.display.set_icon(pygame_icon)
    return display
    
def search_display(py,screen,search_term):
    font = py.font.SysFont('Comic Sans MS', 20)
    if len(search_term)>37:
        search_term = search_term[len(search_term)-38::]
    text = font.render(search_term, True, colours['black'], colours['white'])
    screen.blit(text, (30,10))

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

font_size = 20
song_disp_rad = (font_size+9)//2
song_title_width = 300
#renders the song names in the ui
def song_display(py,screen, song_list, song_dict):
    global font_size, song_title_width
    font = py.font.SysFont('Comic Sans MS', font_size)
    for song in song_list:
        if song_dict[song][1] >=10: #1=y coordinate in the list
            #colours--> text colour, background colour
            text = font.render(song, True, colours['white'], colours['very dark grey'])
            #making text background look neater
            py.draw.rect(surface=screen, color=colours['very dark grey'], 
            rect=(song_dict[song][0], song_dict[song][1],song_title_width,font_size+9))
            #font_size+9 because text background = font size +9
            radius = song_disp_rad
            draw_circle(screen, color=colours['very dark grey'],x=song_dict[song][0],
            y=song_dict[song][1]+radius, radius=radius)
            draw_circle(screen, color=colours['very dark grey'],x=song_dict[song][0]+song_title_width,
            y=song_dict[song][1]+radius, radius=radius)
            screen.blit(text, (song_dict[song][0], song_dict[song][1]))

play_pause_radius = 25
back_height = 125
def play_pause(py,screen, width, height,mouse_x, mouse_y, colour):
    global back_height
    x_cord = width//2
    y_cord = height-play_pause_radius-20
    #creating a black backgroung for the media controals
    py.draw.rect(surface=screen,color=colours['text grey'],rect=(0,height-back_height, width,back_height))
    #creating and rendering pause play button
    draw_circle(surface=screen,color=colour,
    x=x_cord, y=y_cord,radius=play_pause_radius)
    #detecting cursor over play pause button
    dist = circle_dist(x_cord,y_cord,mouse_x,mouse_y)
    if dist<=play_pause_radius:
        return True #returns true if cursor is inside the circle
    return False #returns false if cursor is outside the circle

skip_track_radius = 20
def skip_track(screen, width, height,mouse_x, mouse_y, colour):
    x_cord = width//2+(play_pause_radius+skip_track_radius+20)
    y_cord = height-skip_track_radius-23
    draw_circle(surface=screen,color=colour,
    x=x_cord, y=y_cord, radius=skip_track_radius)
    dist = circle_dist(x_cord,y_cord,mouse_x,mouse_y)
    if dist<=skip_track_radius:
        return True
    return False

previous_track_radius = 20
def previous_track(screen, width, height,mouse_x, mouse_y, colour):
    x_cord = width//2-(play_pause_radius+previous_track_radius+20)
    y_cord = height-previous_track_radius-23
    draw_circle(surface=screen,color=colour,
    x=x_cord, y=y_cord, radius=previous_track_radius)
    dist = circle_dist(x_cord,y_cord,mouse_x,mouse_y)
    if dist<=previous_track_radius:
        return True
    return False

def search_bar(py, screen, width, mouse_x, mouse_y):
    x_cord = 0
    y_cord = 0
    height = 46 #height to the top bar in pixels (for smoother scrolling)
    #top bar
    py.draw.rect(surface=screen,color=colours['black'],rect=(x_cord,y_cord, width, height))
    #search box
    x_cord = 30
    y_cord = 10
    search_bar_width = 400
    search_bar_height = 30
    py.draw.rect(surface=screen,color=colours['white'], 
    rect=(x_cord, y_cord, search_bar_width, search_bar_height+1))
    #+1 for height to compensate for circles radius
    radius = search_bar_height//2
    #creating the circular part of the search bar
    draw_circle(screen, color=colours['white'],x=x_cord,y=y_cord+radius, radius=radius)
    draw_circle(screen, color=colours['white'],x=x_cord+search_bar_width,y=y_cord+radius, radius=radius)