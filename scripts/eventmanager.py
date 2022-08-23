import sys, os, time
from scripts import inst,gui
from threading import Thread

#variables to be used as global
x_cord,y_cord = 35, 50
search_term = ''
play  = False
currently_playing = ''
skip = False
prev = False
sound = None
total_length = 0
elapsed_time=0

#Getting colours from gui.coulours dictionary
white = gui.colours['white']
light_grey = gui.colours['light grey']
skip_track_colour = white
previous_track_colour = white


def play_pause_button(py,screen, width, height,mouse_x, mouse_y):
    global play_pause_colour, play
    play_puase = gui.play_pause(py,screen, width, height,mouse_x, mouse_y)
    play_logo = py.image.load("dependancies\\play.png")
    pause_logo = py.image.load("dependancies\\pause.png")
    if play:
        if gui.play_pause_radius == 25:
            screen.blit(pause_logo, (320,520))
        if gui.play_pause_radius ==30:
            screen.blit(pause_logo, (320,515))
    else:
        if gui.play_pause_radius == 25:
            screen.blit(play_logo, (320,520))
        if gui.play_pause_radius == 30:
            screen.blit(play_logo, (320,515))
    return play_puase

def skip_track_button(py, screen, width, height,mouse_x, mouse_y):
    global skip_track_colour
    skip_track = gui.skip_track(py, screen, width, height,mouse_x, mouse_y, skip_track_colour)
    if skip_track:
        pass
    else:
        pass
    return skip_track

def previous_track_button(py, screen, width, height,mouse_x, mouse_y):
    global previous_track_colour
    previous_track = gui.previous_track(py, screen, width, height,mouse_x, 
    mouse_y, previous_track_colour)
    if previous_track:
        pass
    else:
        pass
    return previous_track

def click_on_songs(song_list,song_dict,height,mouse_x,mouse_y):
    for song in song_list:
        if song_dict[song][1]<=height-gui.back_height-25:
            if song_dict[song][0]<=mouse_x<=song_dict[song][0]+gui.song_title_width:
                if song_dict[song][1]<=mouse_y<=song_dict[song][1]+gui.font_size+9:
                    song_dict[song][2]=True
            if gui.circle_dist(song_dict[song][0], song_dict[song][1]+gui.song_disp_rad,
            mouse_x,mouse_y)<=gui.song_disp_rad:
                song_dict[song][2]=True
            if gui.circle_dist(song_dict[song][0]+gui.song_title_width, song_dict[song][1]+gui.song_disp_rad,
            mouse_x,mouse_y)<=gui.song_disp_rad:
                song_dict[song][2]=True

def load_songs(song_list,song_dict):
    #Getting the name of all song files from bin, runs after each iteration of while loop in main
    dist_between_song_titles = 0
    for file in os.listdir('bin'): #going thorugh all files in the /bin directory
        if file.endswith('.rick_roll'):
            song_name = file[:len(str(file))-10] #removing .rick_roll from the name while displaying
            song_list.append(song_name)
            song_dict[song_name]=[x_cord,y_cord+dist_between_song_titles,False]
            dist_between_song_titles += 40

def play_song(py,song,vol):
    global play, total_length
    sound = py.mixer.Sound(f"bin\\{song}.rick_roll")
    total_length = sound.get_length()
    sound.stop()
    py.mixer.quit()
    time.sleep(0.02)
    py.mixer.init()
    py.mixer.music.load(f"bin\\{song}.rick_roll")
    py.mixer.music.set_volume(vol)
    py.mixer.music.play()
    play = True

def render_text(py,screen):
    font = py.font.SysFont('Comic Sans MS', 15)
    py.draw.rect(screen, gui.colours['very dark grey'],(500,35,100,10))
    py.draw.rect(screen,gui.colours['white'],(500,35,inst.completed,10))
    text = font.render(inst.text, True, gui.colours['white'], gui.colours['black'])
    screen.blit(text,(500,5))

skip_time = 0
def event_manager(py, screen, width, height):
    #Declaring global variables
    global play, x_cord, y_cord, search_term, play_pause_colour, \
    currently_playing,skip,prev, sound, total_length,elapsed_time, song_skip, skip_time
    
    mouse_x, mouse_y = py.mouse.get_pos()

    py.mixer.init()

    #song lsit to store all song names in alphabetical order (descending)
    song_list = []
    #song disctionary to store varous value required to display song in the ui
    song_dict = {}
    load_songs(song_list,song_dict)
    click_on_songs(song_list,song_dict,height,mouse_x,mouse_y)

    #rendering all the song names
    gui.song_display(py,screen=screen,song_list=song_list,song_dict=song_dict)

    #rendering media controal buttons
    play_pause = play_pause_button(py,screen, width, height,mouse_x, mouse_y)
    skip_track = skip_track_button(py, screen, width, height,mouse_x, mouse_y)
    previous_track = previous_track_button(py, screen, width, height,mouse_x, mouse_y)
    gui.song_bar(py,screen, width, height)

    #rendering the search bar
    gui.search_bar(py,screen,width,mouse_x,mouse_y)
    gui.search_display(py,screen,search_term)
    vol = gui.volume_bar(py, screen, width, height,mouse_x,mouse_y)
    
    if currently_playing:
        skip_time = gui.song_bar_overlay(py, screen, width, height, total_length, currently_playing,
        mouse_x,mouse_y)
    
    if inst.text:
        render_text(py,screen)
        
    if currently_playing:
        if skip_time == int(total_length):
            for song in song_list:
                if song == currently_playing and not skip:
                    if song_list.index(song)<len(song_list)-1:
                        currently_playing = song_list[song_list.index(song)+1]
                        play_song(py,currently_playing,vol)
                        break

    gui.currenly_playing_display(py, screen, currently_playing, height)

    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        if event.type == py.MOUSEBUTTONDOWN:
            if len(song_list)>0:
                song1_ypos = song_dict[song_list[0]][1]
                songl_ypos = song_dict[song_list[-1]][1]
                #scroll up (40 because 50 is the max value for song 1 y coordinate)
                if event.button == 4 and song1_ypos<=40: 
                    y_cord +=10
                #scroll down 
                if event.button == 5 and songl_ypos>=height-gui.back_height-25:
                    y_cord-=10
                if event.button == 1: #1 for left click
                    for song in song_list:
                        if song_dict[song][2]:
                            play_song(py,song,vol)
                            currently_playing = song

                    if currently_playing:                            
                        if skip_track:
                            for song in song_list:
                                if song == currently_playing and not skip:
                                    if song_list.index(song)<len(song_list)-1:
                                        currently_playing = song_list[song_list.index(song)+1]
                                        play_song(py,currently_playing,vol)
                                        skip = True
                        
                        if previous_track:
                            for song in song_list:
                                if song == currently_playing and not prev:
                                    if song_list.index(song) >0:
                                        currently_playing = song_list[song_list.index(song)-1]
                                        play_song(py,currently_playing,vol)
                                        prev = True

                        if play == True and play_pause:
                            py.mixer.music.pause()
                            play = False

                        elif play == False and play_pause:
                            py.mixer.music.unpause()
                            play = True
        else:
            skip = False
            prev = False

        #User input to text for search
        if event.type == py.KEYDOWN:
            #checking if the key pressed corresponds to munbers or alphabets
            if 96<=event.key<=172 or 48<=event.key<=57:
                search_term += chr(event.key)
            #askii 32 = sapce
            elif event.key == 32:
                search_term+= ' '
            #askii 8 = back space
            elif event.key == 8:
                search_term = search_term[:len(search_term)-1]
            #askii 13 = enter
            elif event.key == 13 and search_term != '':#check if the string is empty or not
                song_name = search_term
                search_term = ''
                #downloading the song on a different thread so that the program may continue to run
                thread = Thread(target=inst.inst, args=(song_name,py,screen))
                thread.start()