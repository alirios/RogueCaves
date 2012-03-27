import levelgen, life
import pygcurse, pygame, random, time, var, sys
from pygame.locals import *
pygame.font.init()

#Setup stuff...
var.clock = pygame.time.Clock()
var.window_size = (84,32)
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
var.window = pygcurse.PygcurseWindow(var.window_size[0], var.window_size[1],font=_font,caption='QuickRogue')
var.view = pygcurse.PygcurseSurface(100, 100,font=_font,windowsurface=var.window._windowsurface)

#Stuff...
var.window.autoupdate = False
var.view.autoupdate = False

#Generate level
_m = levelgen.LevelGen()
_m.generate(entrance=(random.randint(4,_m.size[0]-4),random.randint(4,_m.size[1]-4)))
_m.decompose(2)

#People
var.player = life.human(player=True)
var.player.pos = [_m.walking_space[0][0],_m.walking_space[0][1]]#[4,4]
var.player.level = _m

_m.add_light((var.player.pos[0],var.player.pos[1]),(128,0,0),10)

def draw_screen():	
	region = (0,0,var.window_size[0],var.window_size[1])
	var.view.fill('black','black',region=region)
	var.view.setbrightness(0, region=region)
	
	_m.light(var.player.pos)
	_m.tick_lights()
	
	for __x in range(var.player.pos[0]-(var.window_size[0]/2),var.player.pos[0]+(var.window_size[0]/2)):
		x = __x
		_x = __x-(var.player.pos[0]-(var.window_size[0]/2))
		
		if x>=_m.size[0]-1: x=_m.size[0]-1
		if x<0: x=0
		
		for __y in range(var.player.pos[1]-(var.window_size[1]/2),var.player.pos[1]+(var.window_size[1]/2)):
			y = __y
			_y = __y-(var.player.pos[1]-(var.window_size[1]/2))
			
			if y>=_m.size[1]-1: y=_m.size[1]-1
			if y<0: y=0
			
			_tile = None
			
			for life in var.life:
				if life.pos == [x,y]:
					_tile = life.icon
			
			if _m.vmap[x][y]:
				if not _tile: _tile = tile_map[str(_m.map[x][y])]
				var.view.putchar(_tile['icon'],x=_x,y=_y,fgcolor=_tile['color'],bgcolor='darkgray')
				
				if _m.lmap[x][y]['brightness']:
					var.view.settint(_m.lmap[x][y]['color'][0],_m.lmap[x][y]['color'][1],\
						_m.lmap[x][y]['color'][2],(_x,_y,1,1))
			elif _m.fmap[x][y]:
				if not _tile: _tile = tile_map[str(_m.map[x][y])]
				var.view.putchar(_tile['icon'],x=_x,y=_y,fgcolor=_tile['color'],bgcolor='altgray')
				var.view.darken(100,(_x,_y,1,1))
			else:
				var.view.putchar(' ',x=_x,y=_y,fgcolor='black',bgcolor='black')
	
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
	
	var.clock.tick(30)
				
while 1: get_input()