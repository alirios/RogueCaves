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
pygcurse.colornames['sand'] = pygame.Color(255, 197, 138)
pygcurse.colornames['lightsand'] = pygame.Color(255, 231, 206)
pygcurse.colornames['brown'] = pygame.Color(205, 133, 63)

#Setup stuff...
var.clock = pygame.time.Clock()
var.window_size = (99,33)
var.life = []
var.history = []
var.skill_mod = 6
var.solid= [0,11]
var.blocking = [10]
var.mouse_pos = (0,0)
var.input = {'up':False,
	'down':False}
tile_map = {'0':{'icon':'#','color':['gray','darkgray']},
	'1':{'icon':' ','color':['black','darkgray']},
	'2':{'icon':'.','color':['silver','darkgray']},
	'3':{'icon':'<','color':['white','darkgray']},
	'4':{'icon':'>','color':['white','darkgray']},
	'5':{'icon':' ','color':['white','green']},
	'6':{'icon':';','color':['altlightgreen','lightgreen']},
	'7':{'icon':';','color':['lightgreen','altlightgreen']},
	'8':{'icon':';','color':['lightsand','sand']},
	'9':{'icon':',','color':['altlightgreen','green']},
	'10':{'icon':'o','color':['blue','blue']},
	'11':{'icon':';','color':['sand','brown']},
	'12':{'icon':'#','color':['sand','brown']}}

#Fonts...
_font = pygame.font.Font('ProggyClean.ttf', 16)

#Surfaces...
var.window = pygcurse.PygcurseWindow(var.window_size[0], var.window_size[1],font=_font,caption='RogueCaves')
var.view = pygcurse.PygcurseSurface(var.window_size[0], var.window_size[1]-6,font=_font,windowsurface=var.window._windowsurface)
var.log = pygcurse.PygcurseSurface(var.window_size[0], var.window_size[1],font=_font,windowsurface=var.window._windowsurface)

#Stuff...
var.window.autoupdate = False
var.view.autoupdate = False
var.log.autoupdate = False

#Log
var.view.putchars('Generating world...',x=0,y=0)
var.view.update()

#Generate level
var.world = world.World(size=(var.window_size[0],var.window_size[1]-6))
var.world.generate()

#People
var.player = life.human(player=True)
var.player.name = 'Player'
var.player.z = 0
var.player.level = var.world.get_level(var.player.z)
var.player.pos = [var.player.level.walking_space[0][0],var.player.level.walking_space[0][1]]

for i in range(1,4):
	for r in range(0,i):
		_temp = life.zombie()
		_temp.z = -i
		_temp.level = var.world.get_level(_temp.z)
		_p = random.choice(_temp.level.walking_space)
		_temp.pos = [_p[0],_p[1]]

#_m.add_light((var.player.pos[0],var.player.pos[1]+1),(128,0,0),10,10)

def draw_screen(refresh=False):	
	region = (0,0,var.window_size[0]+1,var.window_size[1]+1)
	_starttime = time.time()
	var.view.fill('black','black',region=region)
	var.view.setbrightness(0, region=region)

	var.player.level.light(var.player.pos)
	#_m.tick_lights()
	
	if refresh:
		_xrange = [0,var.world.size[0]]
		_yrange = [0,var.world.size[1]]
	else:
		_xrange = [9000,-9000]
		_yrange = [9000,-9000]
	for x in range(0,var.world.size[0]):
		for y in range(0,var.world.size[1]):
			
			_tile = None
			
			for life in var.life:
				if life.z == var.player.z and life.pos == [x,y]:
					_tile = life.icon
			
			if var.player.level.vmap[x][y]:
				if not _tile: _tile = tile_map[str(var.player.level.map[x][y])]
				_bgcolor = tile_map[str(var.player.level.map[x][y])]['color'][1]
				
				if not _tile['color'][1]:
					if _tile['color'][0]=='white' and _bgcolor in ['white','sand','lightsand']:
						var.view.putchar(_tile['icon'],x=x,y=y,fgcolor='black',bgcolor=_bgcolor)
					else:
						var.view.putchar(_tile['icon'],x=x,y=y,fgcolor=_tile['color'][0],bgcolor=_bgcolor)
				
				elif _tile['color'][1]=='blue':
					var.view.putchar(_tile['icon'],x=x,y=y,fgcolor=_tile['color'][0],bgcolor=pygame.Color(0, 0, random.randint(150,200)))
				else:
					var.view.putchar(_tile['icon'],x=x,y=y,fgcolor=_tile['color'][0],bgcolor=_tile['color'][1])
				
				_dist = abs(var.player.pos[0]-var.mouse_pos[0])+abs(var.player.pos[1]-var.mouse_pos[1])
				if (x,y)==var.mouse_pos:
					if _dist<=5:
						var.view.lighten(50,(x,y,1,1))
					else:
						var.view.darken(50,(x,y,1,1))
				
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
	
	var.log.fill(fgcolor=(255,0,0),region=(0,var.window_size[1]-6,var.window_size[0],6))
	_char = '%s the %s %s' % (var.player.name,var.player.alignment,var.player.race)
	_health = 'HP: (%s\%s)' % (var.player.hp,var.player.hp_max)
	_depth = 'Depth: %s' % (-var.player.z)
	_skill = 'Level %s (%s\%s)' % (var.player.skill_level,var.player.xp,\
		var.player.skill_level*var.skill_mod)
	
	var.log.putchars(_char,x=0,y=var.window_size[1]-6,fgcolor='white',bgcolor='black')
	var.log.putchars(_health,x=len(_char)+1,y=var.window_size[1]-6,fgcolor='green',bgcolor='black')
	var.log.putchars(_depth,x=len(_char)+len(_health)+2,y=var.window_size[1]-6,fgcolor='gray',bgcolor='black')
	var.log.putchars(_skill,x=len(_char)+len(_health)+len(_depth)+3,y=var.window_size[1]-6,fgcolor='white',bgcolor='black')
	
	_i=0
	for entry in var.history:
		var.log.putchars(entry,x=0,y=var.window_size[1]-5+(_i),fgcolor='altgray',bgcolor='black')
		_i+=1
	
	var.log.update()
	var.view.update(_xrange=tuple(_xrange),_yrange=tuple(_yrange))
	#print time.time()-_starttime

def get_input():
	for event in pygame.event.get():
		if event.type == QUIT or event.type == KEYDOWN and event.key in [K_ESCAPE,K_q]:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == K_UP:
				var.input['up'] = True
			elif event.key == K_DOWN:
				var.input['down'] = True
			elif event.key == K_LEFT:
				var.input['left'] = True
			elif event.key == K_RIGHT:
				var.input['right'] = True
			elif event.key == K_RETURN:
				var.player.enter()
				draw_screen(refresh=True)
			elif event.key == K_w:
				var.player.place((0,-1),12)
			elif event.key == K_a:
				var.player.place((-1,0),12)
			elif event.key == K_d:
				var.player.place((1,0),12)
			elif event.key == K_s:
				var.player.place((0,1),12)
		elif event.type == KEYUP:
			if event.key == K_UP:
				var.input['up'] = False
			elif event.key == K_DOWN:
				var.input['down'] = False
			elif event.key == K_LEFT:
				var.input['left'] = False
			elif event.key == K_RIGHT:
				var.input['right'] = False
		elif event.type == MOUSEMOTION:
			var.mouse_pos = var.view.getcoordinatesatpixel(event.pos)
		elif event.type == MOUSEBUTTONDOWN:
			var.player.level.map[var.mouse_pos[0]][var.mouse_pos[1]] = 1
		
	for key in var.input:
		if key in ['up','down','left','right']:
			if var.input[key]:
				var.player.walk(key)
				#var.player.walk(key)
	
	for life in var.life:
		if life.player: continue
		life.walk(None)
	
	if var.mouse_pos == (None,None):
		var.mouse_pos = (0,0)
	draw_screen()
	var.clock.tick(10)

draw_screen()
while 1: get_input()