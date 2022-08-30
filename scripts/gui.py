import math
from pygame import gfxdraw

user_font = 'Comic Sans MS'
loop = False
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
    pygame_icon = py.image.load('dependancies\\logo.png')
    py.display.set_icon(pygame_icon)
    return display
    
def search_display(py,screen,search_term):
    font = py.font.SysFont(user_font, 20)
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
    font = py.font.SysFont(user_font, font_size)
    for song in song_list:
        if song_dict[song][1] >=10: #1=y coordinate in the list
            #colours--> text colour, background colour
            if len(song)>28:
                play_song = song[:29]+'...'
            else:
                play_song = song
            text = font.render(play_song, True, colours['white'], colours['very dark grey'])
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

def play_pause(py,screen, width, height,mouse_x, mouse_y):
    global back_height, play_pause_radius
    x_cord = width//2
    y_cord = height-play_pause_radius-20
    #creating a black backgroung for the media controals
    py.draw.rect(surface=screen,color=colours['text grey'],rect=(0,height-back_height, width,back_height))
    #creating and rendering pause play button
    draw_circle(surface=screen,color=colours['white'],
    x=x_cord, y=y_cord,radius=play_pause_radius)
    #detecting cursor over play pause button
    dist = circle_dist(x_cord,y_cord,mouse_x,mouse_y)
    if dist<=play_pause_radius:
        if play_pause_radius==25:
                play_pause_radius +=5
        return True #returns true if cursor is inside the circle
    else:
        if play_pause_radius == 30:
            play_pause_radius -=5
    return False #returns false if cursor is outside the circle

skip_track_radius = 20
def skip_track(py, screen, width, height,mouse_x, mouse_y, colour):
    x_cord = width//2+(play_pause_radius+skip_track_radius+20)
    y_cord = height-skip_track_radius-23
    skip_logo = py.image.load("dependancies\\skip.png")
    draw_circle(surface=screen,color=colour,
    x=x_cord, y=y_cord, radius=skip_track_radius)
    if play_pause_radius == 25:
        screen.blit(skip_logo, (386,527))
    if play_pause_radius == 30:
        screen.blit(skip_logo, (391,527))
    dist = circle_dist(x_cord,y_cord,mouse_x,mouse_y)
    if dist<=skip_track_radius:
        return True
    return False

previous_track_radius = 20
def previous_track(py, screen, width, height,mouse_x, mouse_y, colour):
    x_cord = width//2-(play_pause_radius+previous_track_radius+20)
    y_cord = height-previous_track_radius-23
    prev_logo = py.image.load("dependancies\\prev.png")
    draw_circle(surface=screen,color=colour,
    x=x_cord, y=y_cord, radius=previous_track_radius)
    if play_pause_radius == 25:
        screen.blit(prev_logo, (251,524))
    if play_pause_radius == 30:
        screen.blit(prev_logo, (246,524))
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


def song_bar(py, screen, width, height):
    global back_height
    py.draw.rect(surface=screen, color = colours['very dark grey'], rect = 
    (20, height-back_height+20, width-40,10))

completed = 0
curr_song = ''
pixels_per_second = 0
skip_time = 0
elapsed_time = 0
prev_time = 0

def render_playback_time(py,screen, total_length,height,width):
    font = py.font.SysFont(user_font, 15)
    elapsed_time_sec = skip_time
    if elapsed_time_sec%60>=10:
        elapsed_time_str = f"{elapsed_time_sec//60}:{elapsed_time_sec%60}"
    else:
        elapsed_time_str = f"{elapsed_time_sec//60}:0{elapsed_time_sec%60}"
    if elapsed_time == -1:
        elapsed_time_str = "0:00"
    if total_length%60>=10:
        total_time_str = f"{total_length//60}:{total_length%60}"
    else:
        total_time_str = f"{total_length//60}:0{total_length%60}"
    if elapsed_time == -1:
        total_time_str = "0:00"
    elapsed_time_sec = font.render(elapsed_time_str, True, 
    colours['white'],colours['text grey'])
    total_time = font.render(total_time_str, True, colours['white'],
    colours['text grey'])
    total_time_len = len(total_time_str)
    screen.blit(total_time, (width-40-total_time_len-6, height-back_height+30))
    screen.blit(elapsed_time_sec, (20, height-back_height+30))
    

def song_bar_overlay(py, screen, width, height, total_length,currently_playing,
mouse_x,mouse_y):
    global elapsed_time, prev_time, completed, curr_song,skip_time
    elapsed_time = py.mixer.music.get_pos()
    if elapsed_time//1000-prev_time==1:
        prev_time = elapsed_time//1000
        skip_time+=1
    render_playback_time(py,screen,int(total_length),height,width)

    pixels_per_second = (width-40)/int(total_length)
    completed = skip_time*pixels_per_second

    #To reset the bar
    if curr_song != currently_playing or elapsed_time < 100:
        prev_time = 0
        completed = 0
        skip_time = 0
        curr_song = currently_playing

    py.draw.rect(surface=screen, color = colours['white'], rect = 
    (20, height-back_height+20, int(completed),10))
    draw_circle(screen, int(completed)+20, height-back_height+24,7,colours['white'])

    if 20<=mouse_x<=width-20:
        if height-back_height+20<=mouse_y<=height-back_height+30:
            py.draw.rect(surface=screen, color = colours['white'], rect = 
            (mouse_x-1, height-back_height+20, 2,10))
            for event in py.event.get():
                if event.type == py.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        skip_time = int((mouse_x-21)/pixels_per_second)
                        py.mixer.music.rewind()
                        py.mixer.music.set_pos(skip_time)
    return skip_time

vol = 0.5
def volume_bar(py, screen, width, height,mouse_x,mouse_y):
    global vol
    py.draw.rect(surface=screen,color=colours['very dark grey'],rect=(width-120, height-45, 100, 10))
    py.draw.rect(surface=screen,color=colours['white'],rect=(width-120,height-45,vol*100,10))
    if width-120<=mouse_x<=width-20:
        if height-45<=mouse_y<=height-35:
            py.draw.rect(surface=screen, color = colours['white'], rect =
            (mouse_x-1, height-45, 2,10))
            for event in py.event.get():
                if event.type == py.MOUSEBUTTONDOWN:
                    vol = (mouse_x-580)/100
                    py.mixer.music.set_volume(vol)
    return vol

def currenly_playing_display(py, screen, currently_playing, height):
    font = py.font.SysFont(user_font, 25)
    if len(currently_playing)>16:
        currently_playing = currently_playing[:17]+'...'
    curr_playing = font.render(currently_playing, True, colours['white'],
    colours['text grey'])
    screen.blit(curr_playing, (20, height-back_height+60))


loop_colour = colours['text grey']
def loop_song(py, surface, mouse_x, mouse_y):
    global song_title_width, loop_colour, loop

    loop_logo = py.image.load('dependancies\\loop_grey.png')
    x_cord = 470
    y_cord = 557
    draw_circle(surface, x_cord, y_cord, song_disp_rad+5, loop_colour)
    surface.blit(loop_logo, (455,541))
    dist = circle_dist(x_cord, y_cord, mouse_x, mouse_y)
    if dist<(song_disp_rad+5):
        return True
    return False