import levelgen, world, life
import pygcurse, pygame, random, time, var, sys
from pygame.locals import *
pygame.font.init()

#Colors...
pygcurse.colornames['darkgray'] = pygame.Color(86, 86, 86)
pygcurse.colornames['darkergray'] = pygame.Color(46, 46, 46)
pygcurse.colornames['altgray'] = pygame.Color(148, 148, 148)
pygcurse.colornames['lightgreen'] = pygame.Color(0, 150, 0)
pygcurse.colornames['altlightgreen'] = pygame.Color(0, 140, 0)

#Setup stuff...
var.clock = pygame.time.Clock()
var.window_size = (99,33)
var.life = []
var.history = []
var.input = {'up':False,
	'down':False}
tile_map = {'0':{'icon':'#','color':['gray','darkgray']},
	'1':{'icon':' ','color':['black','darkgray']},
	'2':{'icon':'.','color':['silver','darkgray']},
	'3':{'icon':'<','color':['white','darkgray']},
	'4':{'icon':'>','color':['white','darkgray']},
	'5':{'icon':' ','color':['white','green']},
	'6':{'icon':' ','color':['white','lightgreen']},
	'7':{'icon':' ','color':['white','altlightgreen']}}

#Fonts...
_font = pygame.font.Font('ProggyClean.ttf', 16)

#Surfaces...
var.window = pygcurse.PygcurseWindow(var.window_size[0], var.window_size[1],font=_font,caption='QuickRogue')
var.view = pygcurse.PygcurseSurface(var.window_size[0], var.window_size[1]-6,font=_font,windowsurface=var.window._windowsurface)
var.log = pygcurse.PygcurseSurface(var.window_size[0], var.window_size[1],font=_font,windowsurface=var.window._windowsurface)

#Stuff...
var.window.autoupdate = False
var.view.autoupdate = False
var.log.autoupdate = False

#Generate level
var.world = world.World(size=(var.window_size[0],var.window_size[1]-6))
var.world.generate()

#People
var.player = life.human(player=True)
var.player.name = 'Player'
var.player.z = 1
var.player.level = var.world.get_level(var.player.z)
var.player.pos = [var.player.level.walking_space[0][0],var.player.level.walking_space[0][1]]

_temp = life.human()

_p = random.choice(var.player.level.walking_space)
_temp.pos = [_p[0],_p[1]]
_temp.level = var.player.level

#_m.add_light((var.player.pos[0],var.player.pos[1]+1),(128,0,0),10,10)

def log(self,text):
	if len(var.history)>5: var.history.pop()
	
	var.history.append(text)

def draw_screen():	
	region = (0,0,var.window_size[0],var.window_size[1])
	_starttime = time.time()
	var.view.fill('black','black',region=region)
	var.view.setbrightness(0, region=region)

	var.player.level.light(var.player.pos)
	#_m.tick_lights()
	
	_xrange = [9000,-9000]
	_yrange = [9000,-9000]
	for x in range(0,var.world.size[0]):
		for y in range(0,var.world.size[1]):
			
			_tile = None
			
			for life in var.life:
				if life.pos == [x,y]:
					_tile = life.icon
			
			if var.player.level.vmap[x][y]:
				if not _tile: _tile = tile_map[str(var.player.level.map[x][y])]
				_bgcolor = tile_map[str(var.player.level.map[x][y])]['color'][1]
				
				if not _tile['color'][1]:
					var.view.putchar(_tile['icon'],x=x,y=y,fgcolor=_tile['color'][0],bgcolor=_bgcolor)
				else:
					var.view.putchar(_tile['icon'],x=x,y=y,fgcolor=_tile['color'][0],bgcolor=_tile['color'][1])
				
				if x < _xrange[0]: _xrange[0] = x
				if x > _xrange[1]: _xrange[1] = x+1
				if y < _yrange[0]: _yrange[0] = y
				if y > _yrange[1]: _yrange[1] = y+1
				
				#for light in _m.lights:
				#	for pos in _m.lmap[light[0]][light[1]]['children']:
				#		if pos == (x,y):
				#			#var.view.settint(_m.lmap[light[0]][light[1]]['color'][0],_m.lmap[light[0]][light[1]]['color'][1],\
				#			#	_m.lmap[light[0]][light[1]]['color'][2],(_x,_y,1,1))
				#			var.view.lighten(50,(_x,_y,1,1))
			elif var.player.level.fmap[x][y]:
				if not _tile: _tile = tile_map[str(var.player.level.map[x][y])]
				var.view.putchar(_tile['icon'],x=x,y=y,fgcolor=_tile['color'][0],bgcolor='altgray')
				var.view.darken(100,(x,y,1,1))
				
				if x < _xrange[0]: _xrange[0] = x
				if x > _xrange[1]: _xrange[1] = x+1
				if y < _yrange[0]: _yrange[0] = y
				if y > _yrange[1]: _yrange[1] = y+1
			else:
				var.view.putchar(' ',x=x,y=y,fgcolor='black',bgcolor='black')
	
	var.log.fill(fgcolor=(255,0,0),region=(66,var.window_size[1]-6,None,None))
	var.log.putchars('%s the %s %s' % (var.player.name,var.player.alignment,var.player.race),\
		x=0,y=var.window_size[1]-6,fgcolor='white',bgcolor='black')
	
	for entry in var.history:
		var.log.putchars(entry,x=0,y=var.window_size[1]-5+(var.history.index(entry)),fgcolor='altgray',bgcolor='black')
	
	var.log.update()
	var.view.update(_xrange=tuple(_xrange),_yrange=tuple(_yrange))
	#print time.time()-_starttime

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
			elif event.key == K_RETURN:
				var.player.enter()
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
				for life in var.life:
					life.walk(key)
					#var.player.walk(key)
				draw_screen()
				#_m.add_light((var.player.pos[0],var.player.pos[1]),(0,128,0),1,10)
	var.clock.tick(30)
				
while 1: get_input()