import sys, time,pygame as py
from scripts import music_handler, gui
from threading import Thread
from scripts.scroll_text import AdvScroll
from scripts.progressbar import progress_bar
from scripts.search_bar import searchbar
from scripts.buttons import play_pause, cir_bttn
#from scripts.old_import import import_old

width,height = 1020,720
dt = 0.01
sng_list = []
scroll_y = 0
mouse_x,mouse_y = 0,0

len_played  = 0

#pygame initialisation
py.init()
screen = py.display.set_mode((width,height), py.RESIZABLE)
py.display.set_caption('MUSC-PY 2.0')
logo = py.image.load("graphics\\logo.png")
py.display.set_icon(logo)

sng_import = True


def scroll():
    header_x,header_y  = width*gui.col_r[0]+5,height*gui.row_r[0]+60
    header_height = 50
    
    x,y = header_x, height*gui.row_r[0]+header_y+header_height
    wid, y_height = width*gui.col_r[1]-10,height*gui.row_r[1]-header_height-header_y-2

    scrollable_text = AdvScroll(screen, x,y,wid,y_height,sng_list)

    return scrollable_text


sng_progress = progress_bar(screen,width,height)
search_bar = searchbar(screen,width,height)

rad = 32
pause_play = play_pause(screen,rad,width,height)

rad = 24
skip = cir_bttn(screen,rad,'skip.png')

prev = cir_bttn(screen,rad,'prev.png')
prev.add = 2


sng_overlay=False
currently_playing = None
curr_change = False


def sng_inst(query): #Runs the script to install the song
    thread = Thread(target=music_handler.inst, args=(query,))
    thread.start()


def load_img(screen):
    #Load the image as a pygame object
    img = py.image.load(f"data\\track_art\\{currently_playing}.jpg").convert()
    #Transfor the image to specified dimensions
    img =  py.transform.scale(img, (width*gui.col_r[0]-10,width*gui.col_r[0]-10))

    #Blit the image on the screen
    screen.blit(img, (4,height*(gui.row_r[0]+gui.row_r[1])-width*gui.col_r[0]+4))
    #Update the display to show the image
    py.display.update(py.Rect
    (4,height*(gui.row_r[0]+gui.row_r[1])-width*gui.col_r[0]+4,width*gui.col_r[0]-10,width*gui.col_r[0]-10))


def screen_update(screen, width, height,mouse_x,mouse_y,len_played):
    global scrollable_text
    screen.fill(gui.colours('black'))

    gui.layout_update(width,height,screen,gui.colours('grey'))

    search_bar.width, search_bar.height = width, height
    search_bar.render()

    sng_progress.width,sng_progress.height = width,height
    sng_progress.render_bar(mouse_x,mouse_y,len_played)

    pause_play.width,pause_play.height = width, height
    pause_play.render()

    skip.render(int(width//2+32+rad+16),height)
    prev.render(int(width//2-32-rad-16),height)

    #Update the entire display
    py.display.flip()

    #Rendering the scrollable text
    try:
        prev_scroll = scrollable_text.scroll
    except:
        prev_scroll = 0
    scrollable_text = scroll()
    scrollable_text.scroll = prev_scroll
    scrollable_text.render(40)

    scrollable_text.render_header(50)

    #Loding song art if a song is playing
    if currently_playing:
        load_img(screen)


def load_sng():
    with open("data\\track_data.txt", 'r') as file:
        return [eval(i) for i in file.read().split('\n') if i]


def play_sng(sng_name):
    load_img(screen)
    py.mixer.music.load(f"data\\tracks\\{sng_name}.rick_roll")
    py.mixer.music.play()


#Updating the search bar
def search_bar_ev(event):
    if event:
        #To check if the key pressed corresponds to a letter to number
        if event.unicode.isalnum():
            if search_bar.search_term == 'search': 
                search_bar.search_term = ''
            search_bar.search_term+=event.unicode
        #32 is the askii for space
        elif event.key == 32:
            if search_bar.search_term == 'search': 
                search_bar.search_term = ''
            search_bar.search_term += ' '
        #39 is the askii for '
        elif event.key == 39:
            if search_bar.search_term == 'search': 
                search_bar.search_term = ''
            search_bar.search_term+='\''
        #8 is the askii for backspace
        elif event.key == 8 and search_bar.search_term!='search':
            if len(search_bar.search_term)<=1:
                search_bar.search_term = 'search'
            if len(search_bar.search_term)>0 and search_bar.search_term!='search':
                search_bar.search_term = search_bar.search_term[:-1]
        #13 is the askii for enter
        elif event.key == 13 and search_bar.search_term!='search':
            #To run the song installer by passing the search term
            sng_inst(search_bar.search_term)
            search_bar.search_term = 'search'
        search_bar.render()

screen_update(screen, width, height, mouse_x, mouse_y,len_played)
maximised = True


#---MAIN LOOP---
while 1:

    #To update the songs in the gui if a new one is insatlled
    if music_handler.update == True:
        sng_list = load_sng()
        try:
            prev_scroll = scrollable_text.scroll
        except:
            prev_scroll = 0
        scrollable_text = scroll()
        scrollable_text.scroll = prev_scroll
        scrollable_text.render(40)
        music_handler.update = False

    #Getting the current width and height of the screen
    curr_width, curr_height = py.display.get_window_size()

    #Update the screen if the windows size is less than intended(DEFAULT: width = 1020, HEIGHT = 720)
    #and updating the gui
    #Otherwise uptading the gui if screen size is changed 
    if curr_width!= width or curr_height!=height:
        width,height = curr_width, curr_height
        if curr_height<720:
            height = 720
        if curr_width <1020:
            width = 1020
        screen = py.display.set_mode((width,height), py.RESIZABLE)
        screen_update(screen, width, height, mouse_x, mouse_y,len_played)
        
    for event in py.event.get():

        #Exiting the app
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        
        #getting x and y coords of the cursor
        mouse_x, mouse_y = py.mouse.get_pos()

        #Scrolling text
        force = 0
        if event.type == py.MOUSEWHEEL:
            #To check if the cursor is within the bounds of scrolling text
            if scrollable_text.x<=mouse_x<=scrollable_text.x+scrollable_text.width:
                if scrollable_text.y<=mouse_y<=scrollable_text.y+scrollable_text.height:
                    scrollable_text.left_over += event.y*15
                    #force -> used to continue scrolling after a long scroll
                    force +=event.y*2
                    scrollable_text.left_over+=force
                    scrollable_text.render(40)

        #Events when mouse buttons are clicked
        if event.type == py.MOUSEBUTTONDOWN:
            sng_progress.bttn = event.button
            if event.button == 1:
                if scrollable_text.x<=mouse_x<=scrollable_text.x+scrollable_text.width:
                    if scrollable_text.y<=mouse_y<=scrollable_text.y+scrollable_text.height:
                        new_sng = scrollable_text.get_sng_name(40, mouse_y)
                        if currently_playing!=new_sng and new_sng:
                            curr_change = True
                            currently_playing = new_sng
            #Pause/Play song
            if event.button == 1 and currently_playing:
                if gui.circle_dist(pause_play.x, pause_play.y, mouse_x, mouse_y) <= pause_play.rad:
                    #Pausing the song if it is playing
                    if pause_play.play:
                        pause_play.play = False
                        py.mixer.music.pause()
                    #Playing the song if it is paused
                    else:
                        pause_play.play = True
                        py.mixer.music.unpause()
                    pause_play.render() #To update the pause/play bttn

                #Skip track
                if gui.circle_dist(skip.x,skip.y, mouse_x, mouse_y) <= skip.rad:
                    sng_name = [i['name'] for i in sng_list]
                    sng_name.sort()
                    if sng_name.index(currently_playing) == len(sng_name)-1:
                        currently_playing = sng_name[0]
                        curr_change = True
                    else:
                        currently_playing = sng_name[sng_name.index(currently_playing)+1]
                        curr_change = True

                #Previous track
                if gui.circle_dist(prev.x,prev.y, mouse_x, mouse_y) <= prev.rad:
                    sng_name = [i['name'] for i in sng_list]
                    sng_name.sort()
                    currently_playing = sng_name[sng_name.index(currently_playing)-1]
                    curr_change = True
            
        #For typing in the search bar
        if event.type == py.KEYDOWN:
            search_bar_ev(event)

    #if a new song is played
    if curr_change:
        #play the new song
        play_sng(currently_playing)
        #set volume to 25%
        py.mixer.music.set_volume(0.25)
        #rest progress bar length
        sng_progress.bar_len = 0
        sng_progress.play_len = 0

        #The song is playing -> The pause/Play bttn needs to be in play state
        pause_play.play = True
        pause_play.render()
        
        #To get the length of currently playing song
        sng_progress.duration = [i['duration'] for i in sng_list if i['name'] == currently_playing][0]
        sng_progress.curr_song = currently_playing
        #Changing curr_change to False as the new song is now playing
        curr_change = False
        
    #If a song is being played
    if currently_playing:
        #Seek song using progress bar
        if sng_progress.seek:
            #To unlad the song
            py.mixer.music.unload()
            #To releoad the song to and start playing from begining
            py.mixer.music.load(f'data\\tracks\\{currently_playing}.rick_roll')
            py.mixer.music.play()
            if not pause_play.play:
                py.mixer.music.pause()
            #To seek track
            py.mixer.music.set_pos(sng_progress.seek)
            sng_progress.seek = None
        #Get the length of song played to update the progress bar
        len_played = py.mixer.music.get_pos()

        #To check if the song is done playing and play the next song
        if len_played == -1:
            sng_name = [i['name'] for i in sng_list]
            sng_name.sort()
            if sng_name.index(currently_playing) == len(sng_name)-1:
                currently_playing = sng_name[0]
                curr_change = True
            else:
                currently_playing = sng_name[sng_name.index(currently_playing)+1]
                curr_change = True

        #Rendering the updated song progress bar
        sng_progress.render_bar(mouse_x,mouse_y,len_played)
    
    #To set frame rate
    time.sleep(dt)

    #To re-render the app when it is maximised from the dock
    if py.key.get_focused():
        if not maximised:
            screen = py.display.set_mode((width,height), py.RESIZABLE)
            screen_update(screen, width, height, mouse_x, mouse_y,len_played)
            maximised = True
    else:
        maximised = False
