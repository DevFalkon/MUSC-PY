import sys, os
from scripts import inst,gui
from threading import Thread

x_cord,y_cord = 35, 50
search_term = ''
play = False
#Getting colours from gui.coulours dictionary
white = gui.colours['white']
light_grey = gui.colours['light grey']
play_pause_colour = white
skip_track_colour = white
previous_track_colour = white
song_selected = False
play  = False
currently_playing = ''
skip = False
prev = False

def play_pause_button(py,screen, width, height,mouse_x, mouse_y):
    global play_pause_colour, play
    play_puase = gui.play_pause(py,screen, width, height,mouse_x, mouse_y, play_pause_colour)
    if play_puase:
        play_pause_colour = light_grey
    else:
        play_pause_colour = white
    return play_puase

def skip_track_button(screen, width, height,mouse_x, mouse_y):
    global skip_track_colour
    skip_track = gui.skip_track(screen, width, height,mouse_x, mouse_y, skip_track_colour)
    if skip_track:
        skip_track_colour = light_grey
    else:
        skip_track_colour = white
    return skip_track

def previous_track_button(screen, width, height,mouse_x, mouse_y):
    global previous_track_colour
    previous_track = gui.previous_track(screen, width, height,mouse_x, 
    mouse_y, previous_track_colour)
    if previous_track:
        previous_track_colour = light_grey
    else:
        previous_track_colour = white
    return previous_track


def event_manager(py, screen, width, height):
    #Declaring global variables
    global play, x_cord, y_cord, search_term, play_pause_colour, song_selected, currently_playing,skip,prev

    mouse_x, mouse_y = py.mouse.get_pos()
    #song lsit to store all song names in alphabetical order (descending)
    song_list = []
    #song disctionary to store varous value required to display song in the ui
    song_dict = {}
    #Getting the name of all song files from bin, runs after each iteration of while loop in main
    dist_between_song_titles = 0
    for file in os.listdir('bin'): #going thorugh all files in the /bin directory
        if file.endswith('.rick_roll'):
            song_name = file[:len(str(file))-10] #removing .rick_roll from the name while displaying
            song_list.append(song_name)
            song_dict[song_name]=[x_cord,y_cord+dist_between_song_titles,False]
            dist_between_song_titles += 40
            
    #rendering all the song names 
    for song in song_list:
        if song_dict[song][1]<=height-gui.back_height-25:
            if song_dict[song][0]<=mouse_x<=song_dict[song][0]+gui.song_title_width:
                if song_dict[song][1]<=mouse_y<=song_dict[song][1]+gui.font_size+9:
                    song_dict[song][2]=True
                elif gui.circle_dist(song_dict[song][0], song_dict[song][1],mouse_x,mouse_y)<gui.song_disp_rad:
                    song_dict[song][2]=True
    gui.song_display(py,screen=screen,song_list=song_list,song_dict=song_dict)
    #rendering media controal buttons
    play_pause = play_pause_button(py,screen, width, height,mouse_x, mouse_y)
    skip_track = skip_track_button(screen, width, height,mouse_x, mouse_y)
    previous_track = previous_track_button(screen, width, height,mouse_x, mouse_y)

    #rendering the search bar
    gui.search_bar(py,screen,width,mouse_x,mouse_y)
    gui.search_display(py,screen,search_term)

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
                            py.mixer.init()
                            py.mixer.music.load(f"bin\\{song}.rick_roll")
                            py.mixer.music.play()
                            song_selected = True
                            play = True
                            currently_playing = song

                    if song_selected:
                        if skip_track:
                            for song in song_list:
                                if song == currently_playing and not skip:
                                    if song_list.index(song)<len(song_list)-1:
                                        currently_playing = song_list[song_list.index(song)+1]
                                        py.mixer.music.unload()
                                        py.mixer.music.load(f"bin\\{currently_playing}.rick_roll")
                                        py.mixer.music.play()
                                        skip = True
                        
                        if previous_track:
                            for song in song_list:
                                if song == currently_playing and not prev:
                                    if song_list.index(song) >0:
                                        currently_playing = song_list[song_list.index(song)-1]
                                        py.mixer.music.unload()
                                        py.mixer.music.load(f"bin\\{currently_playing}.rick_roll")
                                        py.mixer.music.play()
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
                thread = Thread(target=inst.inst, args=(song_name,))
                thread.start()