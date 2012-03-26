import pygcurse, pygame, levelgen, var, sys
from pygame.locals import *
pygame.font.init()

var.clock = pygame.time.Clock()
#_font = pygame.font.Font('ProggySquare.ttf', 24)
_font = pygame.font.Font('ProggyClean.ttf', 16)
var.window = pygcurse.PygcurseWindow(75, 46,font=_font,caption='Project October - Tiles')
var.view = pygcurse.PygcurseSurface(72, 40,font=_font,windowsurface=var.window._windowsurface)

var.window.autoupdate = False
var.view.autoupdate = False

_m = levelgen.LevelGen()
_m.generate()

tile_map = {'0':'#',
	'1':' ',
	'2':'.',
	'3':'>'}

def draw_map():
	var.view.setscreencolors('white','black',clear=True)
	
	for x in range(_m.size[0]):
		for y in range(_m.size[1]):
			_tile = tile_map[str(_m.map[x][y])]
			var.view.putchar(_tile,x=x,y=y,fgcolor='white',bgcolor='black')
	
	var.view.update()

def get_input():
	for event in pygame.event.get():
		if event.type == QUIT or event.type == KEYDOWN and event.key in [K_ESCAPE,K_q]:
			pygame.quit()
			sys.exit()
	
	draw_map()
				
while 1: get_input()