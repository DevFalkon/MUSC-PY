import pygame as py
from scripts import gui, eventmanager

#pygame initialisation
height,width = 600,700
py.init()
display = gui.gui_init(py)
screen = display.set_mode((width,height))

while True:
    screen.fill(gui.colours['black'])
    eventmanager.event_manager(py,screen, width,height)
    py.display.update()