import levelgen, life
import pygcurse, pygame, random, var, sys
from pygame.locals import *
pygame.font.init()

#Setup stuff...
var.clock = pygame.time.Clock()
var.life = []
var.input = {'up':False,
	'down':False}
tile_map = {'0':{'icon':'#','color':'gray'},
	'1':{'icon':' ','color':'black'},
	'2':{'icon':'.','color':'silver'},
	'3':{'icon':'>','color':'white'}}

#Colors...
pygcurse.colornames['darkgray'] = pygame.Color(86, 86, 86)
pygcurse.colornames['altgray'] = pygame.Color(148, 148, 148)

#Fonts...
_font = pygame.font.Font('ProggyClean.ttf', 16)

#Surfaces...
var.window = pygcurse.PygcurseWindow(76, 46,font=_font,caption='QuickRogue')
var.view = pygcurse.PygcurseSurface(100, 100,font=_font,windowsurface=var.window._windowsurface)

#Stuff...
var.window.autoupdate = False
var.view.autoupdate = False

#Generate level
_m = levelgen.LevelGen()
_m.generate(entrance=(random.randint(4,_m.size[0]-4),random.randint(4,_m.size[1]-4)))
_m.decompose(4)

#People
var.player = life.human(player=True)
var.player.pos = [_m.walking_space[0][0],_m.walking_space[0][1]]#[4,4]
var.player.level = _m

def draw_screen():
	var.view.setscreencolors('white','black',clear=True)
	
	_m.light(var.player.pos)
	
	for __x in range(var.player.pos[0]-38,var.player.pos[0]+38):
		for __y in range(var.player.pos[1]-23,var.player.pos[1]+23):
			x = int(__x)
			y = int(__y)
			_x = int(__x)-(var.player.pos[0]-38)
			_y = int(__y)-(var.player.pos[1]-23)
			
			if x>=_m.size[0]-1: x=_m.size[0]-1
			if y>=_m.size[1]-1: y=_m.size[1]-1
			
			try:
				_tile = tile_map[str(_m.map[x][y])]
			except:
				print x,y
			
			for life in var.life:
				if life.pos == [x,y]:
					_tile = life.icon
			
			if _m.lmap[x][y]:
				var.view.putchar(_tile['icon'],x=_x,y=_y,fgcolor=_tile['color'],bgcolor='darkgray')
			elif _m.fmap[x][y]:
				var.view.putchar(_tile['icon'],x=_x,y=_y,fgcolor=_tile['color'],bgcolor='altgray')
				var.view.darken(100,(_x,_y,1,1))
	
	var.view.update()

def get_input():
	for event in pygame.event.get():
		if event.type == QUIT or event.type == KEYDOWN and event.key in [K_ESCAPE,K_q]:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == K_UP or event.key == K_KP8:
				var.input['up'] = True
			elif event.key == K_DOWN or event.key == K_KP2:
				var.input['down'] = True
			elif event.key == K_LEFT or event.key == K_KP4:
				var.input['left'] = True
			elif event.key == K_RIGHT or event.key == K_KP6:
				var.input['right'] = True
		elif event.type == KEYUP:
			if event.key == K_UP or event.key == K_KP8:
				var.input['up'] = False
			elif event.key == K_DOWN or event.key == K_KP2:
				var.input['down'] = False
			elif event.key == K_LEFT or event.key == K_KP4:
				var.input['left'] = False
			elif event.key == K_RIGHT or event.key == K_KP6:
				var.input['right'] = False
		
	for key in var.input:
		if key in ['up','down','left','right']:
			if var.input[key]:
				var.player.walk(key)
				draw_screen()
	
	var.clock.tick(12)
				
while 1: get_input()