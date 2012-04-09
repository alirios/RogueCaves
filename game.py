import levelgen, world, life
import pygcurse, logging, pygame, random, time, var, sys
from pygame.locals import *
pygame.font.init()

__version__ = time.strftime('%m.%d.%YA')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_formatter = logging.Formatter('%(message)s')

#fh = logging.FileHandler('log.txt')
#fh.setLevel(logging.DEBUG)
#fh.setFormatter(file_formatter)
#logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(console_formatter)
logger.addHandler(ch)
logging.debug('Rogue Caves - %s' % __version__)

#Colors...
pygcurse.colornames['darkgray'] = pygame.Color(86, 86, 86)
pygcurse.colornames['darkergray'] = pygame.Color(46, 46, 46)
pygcurse.colornames['altgray'] = pygame.Color(148, 148, 148)
pygcurse.colornames['lightgreen'] = pygame.Color(0, 150, 0)
pygcurse.colornames['altlightgreen'] = pygame.Color(0, 140, 0)
pygcurse.colornames['sand'] = pygame.Color(255, 197, 138)
pygcurse.colornames['lightsand'] = pygame.Color(255, 231, 206)
pygcurse.colornames['brown'] = pygame.Color(205, 133, 63)
pygcurse.colornames['gold'] = pygame.Color(253, 233, 16)

#Setup stuff...
var.clock = pygame.time.Clock()
var.window_size = (99,33)
var.max_fps = 10
var.fps = 0
var.view_dist = 11
var.thirst_timer_max = 75
var.hunger_timer_max = 100
var.life = []
var.history = []
var.skill_mod = 6
var.solid= [0,11,15]
var.blocking = [10]
var.items = [13,14]
var.mouse_pos = (0,0)
var.input = {'up':False,
	'down':False}
var.items = {'11':{'name':'dirt','solid':True,'type':'solid','life':2,'tile':11},
			'13':{'name':'gold','solid':False,'type':'ore','tile':13},
			'14':{'name':'coal','solid':False,'type':'ore','tile':14},
			'17':{'name':'meat','solid':False,'type':'food','tile':17},
			'18':{'name':'chest','solid':True,'type':'storage','items':[],'tile':18}}
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
	'12':{'icon':'#','color':['sand','brown']},
	'13':{'icon':'1','color':['sand','gold']},
	'14':{'icon':'c','color':['darkgray','darkergray']},
	'15':{'icon':'#','color':['white','brown']},
	'16':{'icon':'.','color':['brown','sand']},
	'17':{'icon':'F','color':['red','lightsand']},
	'18':{'icon':'#','color':['brown','lightsand']}}

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
var.world = world.World(size=(var.window_size[0],var.window_size[1]-6),depth=6)
var.world.generate()

#People
var.player = life.human(player=True)
var.player.name = 'Player'
var.player.z = 1
var.player.level = var.world.get_level(var.player.z)
var.player.pos = list(var.player.level.walking_space[0])#list(var.player.level.get_room('home')['door'])

for i in range(2):
	test = life.human()
	test.name = 'derp%s' % i
	test.z = 1
	test.speed = 1
	test.speed_max = 1
	test.level = var.world.get_level(test.z)
	test.icon['color'][0] = 'brown'
	#test.mode = {'task':'mine','who':None}
	test.add_event('mine',50)
	test.pos = list(test.level.walking_space[i])

for i in range(2):
	test = life.human()
	test.name = 'dude%s' % i
	test.z = 1
	test.speed = 2
	test.speed_max = 2
	test.level = var.world.get_level(test.z)
	#test.icon['color'][0] = 'white'
	#test.mode = {'task':'mine','who':None}
	test.add_event('follow',50)
	test.pos = list(test.level.walking_space[i])

for i in range(1,var.world.depth):
	for r in range(0,i*2):
		_temp = life.zombie()
		_temp.z = -i
		_temp.speed = var.world.depth-i
		_temp.speed_max = var.world.depth-i
		_temp.hp = i+3
		_temp.hp_max = i+3
		_temp.level = var.world.get_level(_temp.z)
		_p = random.choice(_temp.level.walking_space)
		_temp.pos = [_p[0],_p[1]]

#_m.add_light((var.player.pos[0],var.player.pos[1]+1),(128,0,0),10,10)
var.temp_fps = 0
var.fpstime = time.time()

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
		_xrange = [var.player.pos[0]-var.view_dist,var.player.pos[0]+var.view_dist]
		_yrange = [var.player.pos[1]-var.view_dist,var.player.pos[1]+var.view_dist]
		
		if _xrange[0]<0: _xrange[0]=0
		if _xrange[1]>var.world.size[0]: _xrange[1]=var.world.size[0]
		
		if _yrange[0]<0: _yrange[0]=0
		if _yrange[1]>var.world.size[1]: _yrange[1]=var.world.size[1]
	
	for x in range(_xrange[0],_xrange[1]):
		for y in range(_yrange[0],_yrange[1]):
			
			_tile = None
			
			if var.player.level.items[x][y]:
				_tile = tile_map[str(var.player.level.items[x][y][0]['tile'])]
			
			for life in var.life:
				if life.z == var.player.z and life.pos == [x,y]:
					_tile = life.icon
			
			if var.player.level.vmap[x][y]:
				if not _tile: _tile = tile_map[str(var.player.level.map[x][y])]
				_bgcolor = tile_map[str(var.player.level.map[x][y])]['color'][1]
				
				if not _tile['color'][1]:
					if _tile['color'][0]=='white' and _bgcolor in ['white','sand','lightsand','brown']:
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
			else:
				var.view.putchar(' ',x=x,y=y,fgcolor='black',bgcolor='black')
	
	var.log.fill(fgcolor=(255,0,0),region=(0,var.window_size[1]-6,var.window_size[0],6))
	#_char = '%s the %s %s' % (var.player.name,var.player.alignment,var.player.race)
	_char = '%s' % (var.player.name)
	_health = 'HP: (%s\%s)' % (var.player.hp,var.player.hp_max)
	_depth = 'Depth: %s' % (-var.player.z)
	_skill = 'Level %s (%s\%s)' % (var.player.skill_level,var.player.xp,\
		var.player.skill_level*var.skill_mod)
	_thirst = 'Thirst (%s\\100)' % (var.player.thirst)
	_hunger = 'Hunger (%s\\100)' % (var.player.hunger)
	
	if var.player.level.outside:
		for room in var.player.level.rooms:
			if tuple(var.player.pos) in room['walking_space']:
				_depth += ' (%s)' % (room['name'])
	
	var.log.putchars(_char,x=0,y=var.window_size[1]-6,fgcolor='white',bgcolor='black')
	var.log.putchars(_health,x=len(_char)+1,y=var.window_size[1]-6,fgcolor='green',bgcolor='black')
	var.log.putchars(_depth,x=len(_char)+len(_health)+2,y=var.window_size[1]-6,fgcolor='gray',bgcolor='black')
	var.log.putchars(_skill,x=len(_char)+len(_health)+len(_depth)+3,y=var.window_size[1]-6,fgcolor='white',bgcolor='black')
	var.log.putchars(_thirst,x=len(_char)+len(_health)+len(_depth)+len(_skill)+4,y=var.window_size[1]-6,fgcolor='blue',bgcolor='black')
	var.log.putchars(_hunger,x=len(_char)+len(_health)+len(_depth)+len(_skill)+len(_thirst)+5,y=var.window_size[1]-6,fgcolor='maroon',bgcolor='black')
	var.log.putchars('FPS: %s' % str(var.fps),x=var.window_size[0]-7,y=var.window_size[1]-6,fgcolor='white')
	
	_i=0
	for entry in var.history:
		_fgcolor = 'altgray'
		
		if entry.count('gold'):
			_fgcolor = 'gold'
		
		var.log.putchars(entry,x=0,y=var.window_size[1]-5+(_i),fgcolor=_fgcolor,bgcolor='black')
		_i+=1
	
	var.log.update()
	var.view.update(_xrange=tuple(_xrange),_yrange=tuple(_yrange))
	if time.time()-var.fpstime>=1:
		var.fpstime=time.time()
		var.fps = var.temp_fps
		var.temp_fps = 0
	else:
		var.temp_fps += 1

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
			elif event.key == K_1:
				var.player.teleport(1)
			elif event.key == K_2:
				var.player.teleport(0)
			elif event.key == K_3:
				var.player.teleport(-1)
			elif event.key == K_4:
				var.player.teleport(-2)
			elif event.key == K_5:
				var.player.teleport(-3)
		elif event.type == KEYUP:
			if event.key == K_UP:
				var.input['up'] = False
			elif event.key == K_DOWN:
				var.input['down'] = False
			elif event.key == K_LEFT:
				var.input['left'] = False
			elif event.key == K_RIGHT:
				var.input['right'] = False
			elif event.key == K_z:
				var.max_fps = 10
			elif event.key == K_x:
				var.max_fps = 30
		elif event.type == MOUSEMOTION:
			var.mouse_pos = var.view.getcoordinatesatpixel(event.pos)
		elif event.type == MOUSEBUTTONDOWN:
			#var.player.level.map[var.mouse_pos[0]][var.mouse_pos[1]] = 1
			for life in var.life:
				if life.z == var.player.z:
					if life.pos == list(var.mouse_pos):
						print 'Task: %s' % life.task
						print 'Path: %s' % life.path
						print 'Path dest: %s' % str(life.path_dest)
						print 'Path type: %s' % life.path_type
						print 'Position: %s' % str(life.pos)
						print 'Inventory: '
						print life.items
			
			for item in var.player.level.items[var.mouse_pos[0]][var.mouse_pos[1]]:
				if item['pos'] == var.mouse_pos:
					print item
		
	for key in var.input:
		if key in ['up','down','left','right']:
			if var.input[key]:
				var.player.walk(key)
	
	_atime = time.time()
	for life in var.life:
		life.tick()
		if life.player: continue
		life.walk(None)
	
	if var.mouse_pos == (None,None):
		var.mouse_pos = (0,0)
	if var.player.level.outside:
		draw_screen(refresh=True)
	else:
		draw_screen()
	var.clock.tick(var.max_fps)

draw_screen()
while 1: get_input()