import inst, sys, os, pygame as py
from threading import Thread
from gui import colours, fonts

#pygame initialisation
py.init()
display = py.display
display.init()
py.display.set_caption('MUSC-PY')
pygame_icon = py.image.load('logo.png')
py.display.set_icon(pygame_icon)

height,width = 600,700
pause_play_button = (500,50,50,50)
screen = display.set_mode((width,height))

mouse_x,mouse_y,mouse_button=0,0,(False,False,False)
font = fonts(py)

def pause_play(surface, color):
    py.draw.rect(surface, color, rect = pause_play_button)

def song_disp(t_str, x_cord,y_cord):
    if y_cord >=40:
        text = font.render(t_str, True, colours['black'], colours['white'])
        py.draw.rect(screen, colours['white'], rect=(x_cord,y_cord, 300, 30))
        screen.blit(text, (x_cord, y_cord))

s_temp = ''
play = False
x_cord, y_cord = 10, 40

while True:
    text = font.render(s_temp, True, colours['white'], colours['black'])
    screen.fill(colours['black'])
    screen.blit(text, (10,0))

    s_list = []
    s_pos_dict = {}
    for file in os.listdir('msc_bin'):
        if file.endswith('.rick_roll'):
            t_str = file[:len(str(file))-10]
            s_list.append(t_str)
    jmp = 0
    for song in s_list:
        s_pos_dict[song] = [x_cord, y_cord+jmp]
        jmp+=40

    for i in s_list:
        song_disp(i, s_pos_dict[i][0], s_pos_dict[i][1])

    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        if event.type == py.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = py.mouse.get_pos()
            if event.button == 4 and len(s_list) > 10:
                y_cord +=10
            if event.button == 5 and len(s_list) > 10:
                y_cord-=10
            if 10<=mouse_x<=300 and event.button == 1:
                for i in s_list:
                    if mouse_y in range(s_pos_dict[i][1],s_pos_dict[i][1]+31):
                        py.mixer.init()
                        py.mixer.music.load(f"msc_bin\\{i}.rick_roll")
                        py.mixer.music.play()
                        play = True
            if pause_play_button[0]<=mouse_x<=pause_play_button[0]+pause_play_button[2]:
                if pause_play_button[1]<=mouse_y<=pause_play_button[1]+pause_play_button[3]:
                    if play:
                        py.mixer.music.pause()
                        play = False
                    else:
                        py.mixer.music.unpause()
                        play = True

        if event.type == py.KEYDOWN:
            if 96<=event.key<=172 or 48<=event.key<=57:
                s_temp += chr(event.key)
            elif event.key == 32:
                s_temp+= ' '
            elif event.key == 8:
                s_temp = s_temp[:len(s_temp)-1]
            elif event.key == 13 and s_temp != '':
                s_name = s_temp
                s_temp = ''
                thread = Thread(target=inst.inst, args=(s_name, py))
                thread.start()
    if play:
        pause_play(screen, colours['blue'])
    elif not play:
        pause_play(screen, colours['red'])
    py.display.update()