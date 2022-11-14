import sys, time
import pygame as py
from scripts import music_handler, gui
from threading import Thread
from scripts.scroll_text import scroll
from scripts.progressbar import progress_bar
from scripts.search_bar import searchbar
from scripts.buttons import play_pause, cir_bttn
#from scripts.old_import import import_old

width,height = 1020,720
dt = 0.01
sng_list = []
scroll_y = 0
scrol_sens = 15
mouse_x,mouse_y = 0,0

len_played  = 0

#pygame initialisation
py.init()
screen = py.display.set_mode((width,height), py.RESIZABLE)
py.display.set_caption('MUSC-PY 2.0')
logo = py.image.load("graphics\\logo.png")
py.display.set_icon(logo)

sng_import = True


scrollable_text = scroll(sng_list,height,width,screen)
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


def sng_inst(query): #Runs the script to install the song
    thread = Thread(target=music_handler.inst, args=(query,))
    thread.start()


def load_img(screen):
    #Load the image as a pygame object
    img = py.image.load(f"data\\track_art\\{scrollable_text.curr_song}.jpg").convert()
    #Transfor the image to specified dimensions
    img =  py.transform.scale(img, (width*gui.col_r[0]-10,width*gui.col_r[0]-10))

    #Update the display to show the image
    screen.blit(img, (4,height*(gui.row_r[0]+gui.row_r[1])-width*gui.col_r[0]+4))
    py.display.update(py.Rect
    (4,height*(gui.row_r[0]+gui.row_r[1])-width*gui.col_r[0]+4,width*gui.col_r[0]-10,width*gui.col_r[0]-10))


def screen_update(screen, width, height,mouse_x,mouse_y,len_played):

    screen.fill(gui.colours('black'))

    scrollable_text.update_header = True
    scrollable_text.width,scrollable_text.height = width,height
    scrollable_text.render(mouse_x,mouse_y)

    gui.layout_update(width,height,screen,gui.colours('grey'))

    search_bar.width, search_bar.height = width, height
    search_bar.render()

    sng_progress.width,sng_progress.height = width,height
    sng_progress.render_bar(mouse_x,mouse_y,len_played)

    pause_play.width,pause_play.height = width, height
    pause_play.render()

    skip.render(int(width//2+32+rad+16),height)
    prev.render(int(width//2-32-rad-16),height)

    py.display.flip()
    if currently_playing:
        load_img(screen)


def load_sng():
    with open("data\\track_data.txt", 'r') as file:
        return [eval(i) for i in file.read().split('\n') if i]


def play_sng(sng_name):
    load_img(screen)
    py.mixer.music.load(f"data\\tracks\\{sng_name}.rick_roll")
    py.mixer.music.play()


def search_bar_ev(event):
    if event:
        if event.unicode.isalnum():
            if search_bar.search_term == 'search': 
                search_bar.search_term = ''
            search_bar.search_term+=event.unicode
        elif event.key == 32:
            if search_bar.search_term == 'search': 
                search_bar.search_term = ''
            search_bar.search_term += ' '
        elif event.key == 39:
            if search_bar.search_term == 'search': 
                search_bar.search_term = ''
            search_bar.search_term+='\''
        elif event.key == 8 and search_bar.search_term!='search':
            if len(search_bar.search_term)<=1:
                search_bar.search_term = 'search'
            if len(search_bar.search_term)>0 and search_bar.search_term!='search':
                search_bar.search_term = search_bar.search_term[:-1]
        elif event.key == 13 and search_bar.search_term!='search':
            sng_inst(search_bar.search_term)
            search_bar.search_term = 'search'
        search_bar.render()

screen_update(screen, width, height, mouse_x, mouse_y,len_played)
maximised = True


while 1:

    #To update the songs in the gui if a new one is insatlled
    if music_handler.update == True:
        sng_list = load_sng()
        scrollable_text.iterable = sng_list
        scrollable_text.render(mouse_x,mouse_y)
        music_handler.update = False

    curr_width, curr_height = py.display.get_window_size()
    #Update the screen if the windows size changes
    if curr_width!= width or curr_height!=height:
        width,height = curr_width, curr_height
        if curr_height<720:
            height = 720
        if curr_width <1020:
            width = 1020
        screen = py.display.set_mode((width,height), py.RESIZABLE)
        screen_update(screen, width, height, mouse_x, mouse_y,len_played)

        
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        
        mouse_x, mouse_y = py.mouse.get_pos()

        #Highlighitng the song button under the cursor 
        if width*gui.col_r[0]+3<=mouse_x<=width*(gui.col_r[0]+gui.col_r[1])-13 and \
            scrollable_text.height*gui.row_r[0]+scrollable_text.y_add+scrollable_text.header_h\
                <=mouse_y<=scrollable_text.height*gui.row_r[1]+scrollable_text.header_h:
            scrollable_text.render(mouse_x,mouse_y)
            sng_overlay = True
        #To remove the highlight
        else:
            scrollable_text.bttn = None
            if sng_overlay:
                sng_overlay = False
                scrollable_text.render(mouse_x,mouse_y)

        if event.type == py.MOUSEBUTTONDOWN:

            scrollable_text.bttn = event.button
            sng_progress.bttn = event.button

            if event.button == 1 and currently_playing:
                if gui.circle_dist(pause_play.x, pause_play.y, mouse_x, mouse_y) <= pause_play.rad:
                    if pause_play.play:
                        pause_play.play = False
                        py.mixer.music.pause()
                    else:
                        pause_play.play = True
                        py.mixer.music.unpause()
                    pause_play.render()

                #Skip track
                if gui.circle_dist(skip.x,skip.y, mouse_x, mouse_y) <= skip.rad:
                    sng_name = [i['name'] for i in sng_list]
                    sng_name.sort()
                    if sng_name.index(currently_playing) == len(sng_name)-1:
                        scrollable_text.curr_song = sng_name[0]
                    else:
                        scrollable_text.curr_song = sng_name[sng_name.index(currently_playing)+1]

                #Previous track
                if gui.circle_dist(prev.x,prev.y, mouse_x, mouse_y) <= prev.rad:
                    sng_name = [i['name'] for i in sng_list]
                    sng_name.sort()
                    scrollable_text.curr_song = sng_name[sng_name.index(currently_playing)-1]
            

            #To check if the cursor is over the scrollable text
            if width*gui.col_r[0]+3<=mouse_x<=width*(gui.col_r[0]+gui.col_r[1])-13 and \
            scrollable_text.height*gui.row_r[0]+scrollable_text.y_add+scrollable_text.header_h\
                <=mouse_y<=scrollable_text.height*gui.row_r[1]+scrollable_text.header_h:

                #Scroll up
                if event.button == 5:

                    if scrollable_text.y_add+(scrollable_text.elem_height+3)*(len(sng_list)+1)+\
                        scrollable_text.scroll_y+scrol_sens>\
                        scrollable_text.height*gui.row_r[1]+scrollable_text.header_h:
                        scrollable_text.scroll_y -= scrol_sens

                    elif scrollable_text.y_add+(scrollable_text.elem_height+3)*(len(sng_list)+1)+\
                        scrollable_text.scroll_y+scrol_sens<\
                            scrollable_text.height*gui.row_r[1]+scrollable_text.header_h:

                        scrollable_text.scroll_y-=(scrollable_text.y_add+(scrollable_text.elem_height+3)*\
                            (len(sng_list)+1)+scrollable_text.scroll_y+scrol_sens)-(scrollable_text.height*\
                                gui.row_r[1]+scrollable_text.header_h)+2

                #Scroll down
                elif event.button == 4:
                    if scrollable_text.scroll_y < 0:
                        scrollable_text.scroll_y += scrol_sens
                    
                    if scrollable_text.scroll_y > 0:
                        scrollable_text.scroll_y = 0
        
        if event.type == py.KEYDOWN:
            search_bar_ev(event)

    if currently_playing != scrollable_text.curr_song and scrollable_text.curr_song:
        play_sng(scrollable_text.curr_song)
        currently_playing = scrollable_text.curr_song
        py.mixer.music.set_volume(0.25)
        sng_progress.bar_len = 0
        sng_progress.play_len = 0

        pause_play.play = True
        pause_play.render()
        
        sng_progress.duration = [i['duration'] for i in sng_list if i['name'] == currently_playing][0]
        sng_progress.curr_song = currently_playing
        

    if currently_playing:

        #Set song poition while using song progress bar
        if sng_progress.seek:
            py.mixer.music.unload()
            py.mixer.music.load(f'data\\tracks\\{currently_playing}.rick_roll')
            py.mixer.music.play()
            if not pause_play.play:
                py.mixer.music.pause()
            py.mixer.music.set_pos(sng_progress.seek)
            sng_progress.seek = None

        len_played = py.mixer.music.get_pos()

        if len_played == -1:
            scrollable_text.curr_song = None
            sng_progress.curr_song = None
            pause_play.play = False
            pause_play.render()

            sng_name = [i['name'] for i in sng_list]
            sng_name.sort()
            if sng_name.index(currently_playing) == len(sng_name)-1:
                scrollable_text.curr_song = sng_name[0]
            else:
                scrollable_text.curr_song = sng_name[sng_name.index(currently_playing)+1]

        sng_progress.render_bar(mouse_x,mouse_y,len_played)
    
    #To set frame rate
    time.sleep(dt)

    if py.key.get_focused():
        if not maximised:
            screen = py.display.set_mode((width,height), py.RESIZABLE)
            screen_update(screen, width, height, mouse_x, mouse_y,len_played)
            maximised = True
    else:
        maximised = False

    """if sng_import:
        get_old_sng = import_old(screen)
        get_old_sng.render(height,width)
        get_old_sng.inst_old()
        sng_import = False"""