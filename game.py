import levelgen, tiles, functions, world, draw, cache, life
import logging, random, time, var, sys, os

try:
	import psyco
	psyco.full()
except:
	pass

if '-pygame' in sys.argv:
	var.output = 'pygame'
else:
	var.output = 'libtcod'

if '-server' in sys.argv:
	var.server = True
else:
	if var.output == 'pygame':
		import pygcurse, pygame
		from pygame.locals import *
		pygame.font.init()
	else:	
		import libtcodpy as libtcod
	
	var.server = False

__release__ = None
if not __release__: __version__ = time.strftime('%m.%d.%YA')
else: __version__ = 'Release %s' % __release__

logger = logging.getLogger()
if '-debug' in sys.argv: logger.setLevel(logging.DEBUG)
else: logger.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_formatter = logging.Formatter('%(message)s')

if '-log' in sys.argv:
	fh = logging.FileHandler(os.path.join('data','log.txt'))
	fh.setLevel(logging.DEBUG)
	fh.setFormatter(file_formatter)
	logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(console_formatter)
logger.addHandler(ch)

if var.server: logging.info('Rogue Caves Server - %s' % __version__)
else: logging.info('Rogue Caves - %s' % __version__)

#Setup stuff...
#var.window_size = (100,50)
var.window_size = (100,80)
var.world_size = (300,300)
var.camera = [0,0]
var.scroll_speed = 1
var.max_fps = 20
var.tick_history = []
var.timer = 0
var.ticks = 0
var.id = 0
var.fps = 0

if '-tickrate' in sys.argv:
	try: var.server_tick_rate = int(sys.argv[sys.argv.index('-tickrate')+1])
	except: var.server_tick_rate = 60
else:
	var.server_tick_rate = 60
	
var.time = 0
var.view_dist = 11
var.life = []
var.history = []
var.skill_mod = 6
var.cache = cache.cache()
var.mouse_pos = (0,0)
var.in_menu = None
var.menu_index = 0
var.menu_name = ''
var.names_female = []
var.names_male = []
var.names_female_dogs = []
var.names_male_dogs = []
var.phrases = []
var.input = {'up':False,
	'down':False}
var.temp_fps = 0
var.gametime = time.time()
var.fpstime = time.time()
var.dirty = []

if not var.server and var.output=='pygame':
	#Colors...
	for color in var.color_codes:
		pygcurse.colornames[color] = pygame.Color(var.color_codes[color][0],
			var.color_codes[color][1],
			var.color_codes[color][2])
	
	#Setup
	var.clock = pygame.time.Clock()
	var.buffer = [[0] * var.world_size[1] for i in range(var.world_size[0])]
	
	#Fonts...
	_font = pygame.font.Font(os.path.join('data','ProggyClean.ttf'), 16)

	#Surfaces...
	var.window = pygcurse.PygcurseWindow(var.window_size[0],
		var.window_size[1],
		font=_font,
		caption='RogueCaves')
	var.view = pygcurse.PygcurseSurface(var.window_size[0],
		var.window_size[1],
		font=_font,
		windowsurface=var.window._windowsurface)
	var.menu = pygcurse.PygcurseSurface(var.window_size[0],
		var.window_size[1]-6,
		font=_font,
		windowsurface=var.window._windowsurface)
	var.log = pygcurse.PygcurseSurface(var.window_size[0],
		var.window_size[1],
		font=_font,
		windowsurface=var.window._windowsurface)

	#Stuff...
	var.window.autoupdate = False
	var.view.autoupdate = False
	var.log.autoupdate = False

	#Draw title
	for x in range(var.window_size[0]):
		for y in range(var.window_size[1]):
			var.view.putchar('#',
				x=x,
				y=y,
				fgcolor=pygame.Color((x/2)+(y),(x/2)+(y),(x/2)+(y)))
	
	_logofile = open(os.path.join('data','logo.txt'),'r')
	_y=11
	for line in _logofile.readlines():
		_x=-1
		for char in line:
			_x+=1
			if char in [' ','\n']: continue
			var.view.putchar(char,
				x=_x,
				y=_y,
				fgcolor=pygame.Color((_x/2)+(_y*6),(_x/2)+(_y*6),(_x/2)+(_y*6)))
		_y+=1
	_logofile.close()
	
	var.view.putchars(__version__,
		x=(var.window_size[0]/2)-(len(__version__)/2),
		y=20,
		fgcolor='white')
	
	var.view.update()
elif not var.server and var.output=='libtcod':
	var.buffer = [[0] * var.world_size[1] for i in range(var.world_size[0])]
	
	if '-small' in sys.argv:
		libtcod.console_set_custom_font(os.path.join('data','terminal8x8_aa_tc.png'), libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
	elif '-font' in sys.argv:
		try:
			_font = sys.argv[sys.argv.index('-font')+1]
			libtcod.console_set_custom_font(_font, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
		except:
			logging.error('Failed to load font!')
			sys.exit()
	else:
		var.window_size = (80,50)
		libtcod.console_set_custom_font(os.path.join('data','terminal16x16_aa_tc.png'), libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
	libtcod.console_init_root(var.window_size[0], var.window_size[1], 'Rogue Caves - %s' % __version__, False)
	var.view = libtcod.console_new(var.window_size[0], var.window_size[1]-6)
	var.tree = libtcod.console_new(var.window_size[0], var.window_size[1]-6)
	var.splatter = libtcod.console_new(var.window_size[0], var.window_size[1]-6)
	libtcod.console_set_key_color(var.splatter,libtcod.Color(0,0,0))
	libtcod.console_set_key_color(var.tree,libtcod.Color(0,0,0))
	var.log = libtcod.console_new(var.window_size[0], 6)
	libtcod.console_set_keyboard_repeat(100,1)
	libtcod.sys_set_fps(var.max_fps)
	
	_logofile = open(os.path.join('data','logo.txt'),'r')
	_y=18
	for line in _logofile.readlines():
		_i = 1
		for char in line:
			if char == '\n': continue
			libtcod.console_set_char_foreground(0,_i,_y,libtcod.Color(_y*6,_y*6,_y*6))
			#libtcod.console_print(0, _i, _y, char)
			libtcod.console_set_char(0, _i, _y, char)
			_i+=1
		_y+=1
	libtcod.console_print(0,(var.window_size[0]/2)-(len(__version__)/2),
		28,
		str(__version__))
	_logofile.close()
	libtcod.console_flush()

#Load dictionary files
logging.debug('Loading dictionaries')

_fnames = open(os.path.join('data','names_female.txt'),'r')
for line in _fnames.readlines():
	var.names_female.append(line)
_fnames.close()

_mnames = open(os.path.join('data','names_male.txt'),'r')
for line in _mnames.readlines():
	var.names_male.append(line)
_mnames.close()

_phrases = open(os.path.join('data','phrases.txt'),'r')
for line in _phrases.readlines():
	_line = line.split(':')
	var.phrases.append({'type':_line[0],'text':_line[1].strip()})
_phrases.close()

_mdnames = open(os.path.join('data','names_male_dogs.txt'),'r')
for line in _mdnames.readlines():
	var.names_male_dogs.append(line)
_mdnames.close()

_fdnames = open(os.path.join('data','names_female_dogs.txt'),'r')
for line in _fdnames.readlines():
	var.names_female_dogs.append(line)
_fdnames.close()

#Generate level
var.world = world.World(size=(var.world_size[0],var.world_size[1]),depth=5)

if '-load' in sys.argv:
	var.world.load()
else:
	var.world.generate()
	
	#Gods
	var.ivan = life.god()
	var.ivan.name = 'Ivan'
	var.ivan.purpose = 'death'
	var.ivan.alignment = 'evil'
	var.ivan.accepts = ['human']

	#People
	var.player = life.human(player=True)
	var.player.name = 'flags'
	var.player.z = 1
	var.player.speed = 1
	var.player.speed_max = 1
	var.player.level = var.world.get_level(var.player.z)
	var.player.pos = list(var.player.level.get_open_buildings_of_type('bar')[0]['door'])
	#list(var.player.level.exits[0])
	#list(var.player.level.get_open_buildings_of_type('bar')[0]['door'])
	var.player.god = var.ivan
	var.player.talents.append('Animal Husbandry')
	
	var.camera = [var.player.pos[0]-(var.window_size[0]/2),var.player.pos[1]-(var.window_size[1]/2)]
	if var.camera[0]<0: var.camera[0]=0
	if var.camera[1]<0: var.camera[1]=0
	var.camera_last = [-1,-1]

	for i in range(9):
		var.player.add_item_raw(21)
	
	_i = var.player.add_item_raw(33)
	var.player.equip_item(_i)
	
	for r in range(4):
		functions.generate_dog(wild=True,z=-r)

def draw_tile(tile,pos,color):
	_x = pos[0]-var.camera[0]
	_y = pos[1]-var.camera[1]
	
	if var.output=='libtcod':# and var.player.level.outside:
		#print var.player.level.tmap
		if var.player.level.tmap[pos[0]][pos[1]]:
			libtcod.console_set_char_background(var.tree,_x,_y,libtcod.Color(var.player.level.tmap[pos[0]][pos[1]],0,0), flag=libtcod.BKGND_SET)
	
	if var.player.level.outside:
		if tile.has_key('id'):
			_icon = False
			if var.buffer[_x][_y] == tile['id'] and var.player.level.outside: return
			else: var.buffer[_x][_y] = tile['id']
		elif tile.has_key('icon'):
			_icon = True
			if tile.has_key('limbs') and var.output=='libtcod':
				for __x in xrange(-6,7):
					for __y in xrange(-6,7):
						if tile['limbs'][__x][__y]:
							libtcod.console_set_char_background(var.tree, _x+__x, _y+__y, libtcod.Color(50,50,50), flag=libtcod.BKGND_SET)
							libtcod.console_set_char_foreground(var.tree, _x+__x, _y+__y, libtcod.Color(50,50,50))
							libtcod.console_set_char(var.tree, _x+__x, _y+__y, '#')
				
			if var.buffer[_x][_y] == tile['icon'] and var.player.level.outside: return
			else: var.buffer[_x][_y] = tile['icon']
	
	var.dirty.append((_x,_y))
	
	if isinstance(tile['icon'],unicode):
		tile['icon'] = str(tile['icon'])
	
	if var.output=='pygame':
		var.view.putchar(tile['icon'],x=_x,y=_y,fgcolor=color[0],bgcolor=color[1])
	else:
		_color = (var.color_codes[color[0]],var.color_codes[color[1]])
		if not var.player.level.outside:
			libtcod.console_set_char_background(var.view, _x, _y, libtcod.Color(_color[1][0],_color[1][1],_color[1][2]), flag=libtcod.BKGND_SET)
		libtcod.console_set_char_foreground(var.view, _x, _y, libtcod.Color(_color[0][0],_color[0][1],_color[0][2]))
		libtcod.console_set_char(var.view, _x, _y, tile['icon'])

def draw_screen(refresh=False):	
	region = (0,0,var.window_size[0]+1,var.window_size[1]+1)
	_starttime = time.time()
	#var.view.fill('black','black',region=region)
	if not var.player.level.outside:
		if var.output=='pygame': var.view.setbrightness(0, region=region)
	
	if not var.camera == var.camera_last and var.output=='libtcod':
		libtcod.console_clear(var.tree)
		
		if not var.player.level.outside:
			libtcod.console_clear(var.view)
	
	var.player.level.light(var.player.pos)
	#_m.tick_lights()
	var.dirty = []
	
	if refresh:
		_xrange = [var.camera[0],var.camera[0]+var.window_size[0]]
		_yrange = [var.camera[1],var.camera[1]+var.window_size[1]]
		
		if _xrange[1]>=var.player.level.size[0]:
			_xrange[0]=var.player.level.size[0]-var.window_size[0]
			_xrange[1]=var.player.level.size[0]
			var.camera[0]=_xrange[0]
		
		if _yrange[1]>=var.player.level.size[1]-1:
			_yrange[0]=var.player.level.size[1]-var.window_size[1]
			_yrange[1]=var.player.level.size[1]
			var.camera[1]=_yrange[0]-1
		
	else:
		_xrange = [var.player.pos[0]-var.view_dist,var.player.pos[0]+var.view_dist]
		_yrange = [var.player.pos[1]-var.view_dist,var.player.pos[1]+var.view_dist]
		
		if _xrange[0]<0: _xrange[0]=0
		if _xrange[1]>var.window_size[0]: _xrange[1]=var.window_size[0]
		
		if _yrange[0]<0: _yrange[0]=0
		if _yrange[1]>var.window_size[1]: _yrange[1]=var.window_size[1]
	
	for x in xrange(_xrange[0],_xrange[1]):
		for y in xrange(_yrange[0],_yrange[1]):
			_tile = None
			
			if var.player.level.items[x][y]:
				_item = var.player.level.items[x][y][0]
				_tile = var.tile_map[str(_item['tile'])].copy()
				if _item['name']=='tree':
					_tile['limbs'] = _item['limbs']
				
				if _item.has_key('images'):
					_tile['icon'] = _item['images'][_item['image_index']]
			
			for life in var.life:
				if life.z == var.player.z and life.pos == [x,y]:
					_tile = life.icon
					_tile['id'] = life.id
			
			#if var.player.level.tmap[x][y]:
			#	var.player.level.tmap[x][y]-=1
			
			if var.player.level.vmap[x][y]:
				if not _tile:
					_tile = var.tile_map[str(var.player.level.map[x][y])]
					_tile['id'] = var.player.level.map[x][y]
				_bgcolor = var.tile_map[str(var.player.level.map[x][y])]['color'][1]
				
				if not _tile['color'][1]:
					if _tile['color'][0]=='white' and _bgcolor in ['white','sand','lightsand','brown']:
						draw_tile(_tile,(x,y),('black',_bgcolor))
					else:
						draw_tile(_tile,(x,y),(_tile['color'][0],_bgcolor))
				
				elif _tile['color'][1]=='blue':
					draw_tile(_tile,(x,y),(_tile['color'][0],'blue'))
				else:
					draw_tile(_tile,(x,y),_tile['color'])
				
				#if var.player.level.tmap[x][y]:
				#	var.view.tint(r=var.player.level.tmap[x][y],region=(x,y,1,1))
				
			elif var.player.level.fmap[x][y]:
				if not _tile: _tile = var.tile_map[str(var.player.level.map[x][y])]
				draw_tile(_tile,(x,y),('darkergray','black'))

			elif refresh and var.output=='pygame':
				var.view.putchar(' ',x=x,y=y,fgcolor='black',bgcolor='black')
	
	_char = '%s the %s %s' % (var.player.name,var.player.alignment,var.player.race)
	_char = '%s' % (var.player.name)
	_health = 'HP: (%s\%s)' % (var.player.hp,var.player.hp_max)
	_depth = 'Depth: %s' % (-var.player.z)
	_skill = 'Level %s (%s\%s)' % (var.player.skill_level,var.player.xp,\
		var.player.skill_level*var.skill_mod)
	_thirst = 'Thirst (%s\\100)' % (var.player.thirst)
	_hunger = 'Hunger (%s\\100)' % (var.player.hunger)
	
	if var.player.level.outside:
		_in_building = var.player.in_building()
		if _in_building: _depth += ' (%s)' % (_in_building['name'])
	
	if var.output=='pygame':
		var.log.putchars(_char,x=0,y=var.window_size[1]-6,fgcolor='white',bgcolor='black')
		var.log.putchars(_health,x=len(_char)+1,y=var.window_size[1]-6,fgcolor='green',bgcolor='black')
		var.log.putchars(_depth,x=len(_char)+len(_health)+2,y=var.window_size[1]-6,fgcolor='gray',bgcolor='black')
		var.log.putchars(_skill,x=len(_char)+len(_health)+len(_depth)+3,y=var.window_size[1]-6,fgcolor='white',bgcolor='black')
		var.log.putchars(_thirst,x=len(_char)+len(_health)+len(_depth)+len(_skill)+4,y=var.window_size[1]-6,fgcolor='blue',bgcolor='black')
		var.log.putchars(_hunger,x=len(_char)+len(_health)+len(_depth)+len(_skill)+len(_thirst)+5,y=var.window_size[1]-6,fgcolor='maroon',bgcolor='black')
		var.log.putchars('FPS: %s' % str(var.fps),x=var.window_size[0]-7,y=var.window_size[1]-6,fgcolor='white')
	else:
		libtcod.console_clear(var.log)
		libtcod.console_set_default_foreground(var.log, libtcod.white)
		libtcod.console_print(var.log, 0, 0,_char)
		libtcod.console_set_default_foreground(var.log, libtcod.green)
		libtcod.console_print(var.log, len(_char)+1,0,_health)
		libtcod.console_set_default_foreground(var.log, libtcod.grey)
		libtcod.console_print(var.log, len(_char)+len(_health)+2,0,_depth)
		libtcod.console_set_default_foreground(var.log, libtcod.white)
		libtcod.console_print(var.log, len(_char)+len(_health)+len(_depth)+3,0,_skill)
		libtcod.console_set_default_foreground(var.log, libtcod.blue)
		libtcod.console_print(var.log, len(_char)+len(_health)+len(_depth)+len(_skill)+4,0,_thirst)
		libtcod.console_set_default_foreground(var.log, libtcod.dark_red)
		libtcod.console_print(var.log,len(_char)+len(_health)+len(_depth)+len(_skill)+len(_thirst)+5,0,_hunger)
		libtcod.console_set_default_foreground(var.log, libtcod.white)
		libtcod.console_print(var.log,var.window_size[0]-7,0,'FPS: %s' % str(var.fps))
		
		#Draw health of person attacking
		if var.player.in_danger:
			_in_danger = '%s: %s\\%s' % (var.player.in_danger.name,
				var.player.in_danger.hp,
				var.player.in_danger.hp_max)
			libtcod.console_set_default_foreground(var.log, libtcod.red)
			libtcod.console_print(var.log,var.window_size[0]-len(_in_danger),1,_in_danger)
	
	#TODO: Resetting colors here might help.
	if var.in_menu:
		var.menu.putchars(var.menu_name,x=(var.window_size[0]/2)-len(var.menu_name)/2,y=(var.window_size[1]/2)-(len(var.in_menu)/2)-4,fgcolor='white',bgcolor='black')
		
		for item in var.in_menu:
			if var.menu_index == var.in_menu.index(item):
				_color = 'white'
			else:
				_color = 'gray'
			_tile = var.tile_map[str(item['item']['tile'])]
			_entry = '%s x%s (%sb)' % (item['item']['name'],item['count'],functions.get_item_price(item['item']))
			_center_x = (var.window_size[0]/2)-len(var.menu_name)/2
			_center_y = (var.window_size[1]/2)-(len(var.in_menu)/2)+var.in_menu.index(item)-3
			var.menu.putchars(_tile['icon'],x=_center_x-1,y=_center_y,fgcolor=_tile['color'][0],bgcolor=_tile['color'][1])
			var.menu.putchars(' '+_entry,x=_center_x,y=_center_y,fgcolor=_color,bgcolor='black')
	
	_i=0
	for entry in var.history:
		_fgcolor = 'altgray'
		
		if entry.count('gold'):
			_fgcolor = 'gold'
		elif entry.count('bronze'):
			_fgcolor = 'brown'
		
		if var.output=='pygame':
			var.log.putchars(entry,
				x=0,
				y=var.window_size[1]-5+(_i),
				fgcolor=_fgcolor,
				bgcolor='black')
		else:
			entry = entry.replace(' %s ' % var.player.name,' you ')
			
			if entry.startswith('You hit') or entry.startswith('You strike'):
				_r = 0
				_g = 250
				_b = 0
			elif entry.count(' you '):
				_r,_g,_b = (250,0,0)
			else:
				_r = 200
				_g = 200
				_b = 200
			
			libtcod.console_set_default_foreground(var.log, libtcod.Color(_r,_g,_b))
			libtcod.console_print(var.log,0,1+_i,entry)
		_i+=1
	
	if var.output=='pygame':
		if var.in_menu: var.menu.update()
		else:
			var.log.update()
			
			if var.player.level.outside:
				var.view.update_alt(var.dirty)
			else:
				var.view.update(_xrange=tuple(_xrange),_yrange=tuple(_yrange))
	else:
		libtcod.console_blit(var.log, 0, 0, var.window_size[0], 6, 0, 0, var.window_size[1]-6)
		
		if not var.camera == var.camera_last:
			on_scroll()
			var.camera_last = var.camera[:]
		
		libtcod.console_blit(var.splatter, 0, 0, var.window_size[0], var.window_size[1]-6, 0, 0, 0,0.4,0.7)
		libtcod.console_blit(var.view, 0, 0, var.window_size[0], var.window_size[1]-6, 0, 0, 0)
		libtcod.console_blit(var.tree, 0, 0, var.window_size[0], var.window_size[1]-6, 0, 0, 0,0.4,0.7)
		#var.console_buffer.blit(var.view)
		#print var.camera[0],var.camera[0]+var.window_size[0],
		#print _map[1][var.camera[0]:var.camera[0]+var.window_size[0],var.camera[1]:var.camera[0]+var.window_size[0]]
		libtcod.console_flush()
	
	if time.time()-var.fpstime>=1:
		var.fpstime=time.time()
		var.fps = var.temp_fps
		var.time += 1
		var.temp_fps = 0
	else:
		var.temp_fps += 1

def on_scroll():
	if not var.player.level.outside: return
	_map = var.player.level.color_map
	libtcod.console_fill_background(var.view,
		_map[0][var.camera[1]:var.camera[1]+var.window_size[1],var.camera[0]:var.camera[0]+var.window_size[0]],
		_map[1][var.camera[1]:var.camera[1]+var.window_size[1],var.camera[0]:var.camera[0]+var.window_size[0]],
		_map[2][var.camera[1]:var.camera[1]+var.window_size[1],var.camera[0]:var.camera[0]+var.window_size[0]])

def tick():
	_key = None
	for key in var.input:
		if key in ['up','down','left','right']:
			if var.input[key]:
				_key = key

	_atime = time.time()
	
	if time.time()-var.gametime>=1:
		if var.server:
			if not len(var.tick_history):
				var.tick_history.append(var.ticks)
			else:
				#logging.debug('Ticks this frame: %s' % str(var.ticks))
				var.tick_history.insert(0,var.ticks)
			
			var.ticks = 0
			if len(var.tick_history)>10: var.tick_history.pop()
		
		var.gametime = time.time()
	
	if var.timer>=20:
		if not var.in_menu:
			for level in var.world.levels:
				level['level'].tick()
		var.timer = 0
	else:
		var.timer+=1
	
	if var.in_menu:
		if var.menu_index<0: var.menu_index = len(var.in_menu)-1
		if var.menu_index>len(var.in_menu)-1: var.menu_index = 0
		
	else:
		if var.player.speed or var.server:
			var.player.walk(None)
					
			for life in var.life:
				life.tick()
				if life.has_event('passed_out'): continue				
				if life.player: continue
				life.walk(None)
				
		elif not var.player.in_danger:
			if _key: var.player.walk(_key)
			
			for life in var.life:
				life.tick()
				if life.has_event('passed_out'): continue
				if life.player: continue
				life.walk(None)
		elif var.player.in_danger:
			if _key:
				var.player.walk(_key)
				
				for life in var.life:
					life.tick()
					if life.has_event('passed_out'): continue
					if life.player: continue
					life.walk(None)
	
	if var.server:
		var.ticks += 1
		
		if var.ticks>=var.server_tick_rate:
			time.sleep(1)
		
		return
	
	if var.mouse_pos == (None,None):
		var.mouse_pos = (0,0)
	
	#if not var.player.speed:
	if var.player.level.outside:
		draw_screen(refresh=True)
	else:
		draw_screen(refresh=True)
	
	if var.output=='pygame': var.clock.tick(var.max_fps)

def get_input():
	if var.output=='pygame':
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key in [K_ESCAPE,K_q]:
				if var.in_menu:
					functions.destroy_menu(who=var.player)
				else:
					#var.world.save()
					pygame.quit()
					sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_UP:
					var.input['up'] = True
					var.menu_index-=1
				elif event.key == K_DOWN:
					var.input['down'] = True
					var.menu_index+=1
				elif event.key == K_LEFT:
					var.input['left'] = True
				elif event.key == K_RIGHT:
					var.input['right'] = True
				elif event.key == K_RETURN:
					if var.in_menu:
						functions.menu_select()
					else:
						var.player.enter()
						var.buffer = [[0] * var.world_size[1] for i in range(var.world_size[0])]
						region = (0,0,var.window_size[0]+1,var.window_size[1]+1)
						var.view.setbrightness(0, region=region)
						draw_screen(refresh=True)
				elif event.key == K_w:
					var.player.place_item(21,(0,-1))
				elif event.key == K_a:
					var.player.place_item(21,(-1,0))
				elif event.key == K_d:
					var.player.place_item(21,(1,0))
				elif event.key == K_s:
					var.player.place_item(21,(0,1))
				elif event.key == K_v:
					for pos in var.player.level.real_estate:
						var.view.tint(b=255,region=(pos[0],pos[1],1,1))
				elif event.key == K_b:
					if var.player.in_building(name='storage') and not var.in_menu:
						_building_owner = var.player.level.get_room('storage')['owner']
						
						if _building_owner and _building_owner.in_building(name='storage'):
							_menu = var.player.level.get_room_items('storage')
							if len(_menu):
								functions.build_menu(var.player.level.get_room_items('storage'),
									who=var.player,
									name='Shopping (Buy)',
									trading=True,
									callback=var.player.buy_item)
								_building_owner.say('What would you like today?')
							else:
								_building_owner.say('I have nothing to sell!')
				
				elif event.key == K_n:
					if var.player.in_building(name='storage') and not var.in_menu:
						_building_owner = var.player.level.get_room('storage')['owner']
						
						if _building_owner and _building_owner.in_building(name='storage'):
							functions.build_menu(var.player.items,
								who=var.player,
								name='Shopping (Sell)',
								trading=True,
								callback=var.player.sell_item,
								sell_to=_building_owner)
							_building_owner.say('What items do you have for me?')
							
				elif event.key == K_i:
					if len(var.player.items):
						functions.build_menu(var.player.items,
							name='Inventory',
							callback=var.player.equip_item)
				elif event.key == K_p:
					var.world.get_stats()
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
				elif event.key == K_6:
					var.player.teleport(-4)
				elif event.key == K_j:
					logging.debug('Taking screenshot...')
					pygame.image.save(var.window._windowsurface, 'screenshot.jpg')
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
					var.max_fps = 20
				elif event.key == K_x:
					var.max_fps = 60
				elif event.key == K_c:
					var.max_fps = 10
				elif event.key == K_v:
					for pos in var.player.level.real_estate:
						var.view.setbrightness(0, region=(pos[0],pos[1],1,1))
			elif event.type == MOUSEMOTION:
				var.mouse_pos = var.view.getcoordinatesatpixel(event.pos)
			elif event.type == MOUSEBUTTONDOWN:
				for life in var.life:
					if life.z == var.player.z:
						if [life.pos[0]-var.camera[0],life.pos[1]-var.camera[1]] == list(var.mouse_pos):
							print '='*8
							print life.name
							print 'Task: %s' % life.task
							print 'Path: %s' % life.path
							print 'Path dest: %s' % str(life.path_dest)
							#print 'Path type: %s' % life.path_type
							print 'Position: %s' % str(life.pos)
							print 'Traits: %s' % life.traits
							print 'Attracted to: %s' % life.attracted_to
							print 'Likes: %s' % life.likes
							print 'Dislikes: %s' % life.dislikes
							#print [entry for entry in life.get_top_love_interests()]
							for event in life.events:
								print event['what'],event['score']
							print '='*8
							life.build_history()
							#print 'Inventory: '
							#for item in life.items:
							#	print item
				
				for item in var.player.level.items[var.mouse_pos[0]+var.camera[0]][var.mouse_pos[1]+var.camera[1]]:
					if [item['pos'][0]-var.camera[0],item['pos'][1]-var.camera[1]] == list(var.mouse_pos):
						print item
	else:
		key = libtcod.console_check_for_keypress(flags=libtcod.KEY_PRESSED) 
		
		if key.vk == libtcod.KEY_UP:
			var.input['up']=True
		else:
			var.input['up']=False
		
		if key.vk == libtcod.KEY_DOWN:
			var.input['down']=True
		else:
			var.input['down']=False
		
		if key.vk == libtcod.KEY_LEFT:
			var.input['left']=True
		else:
			var.input['left']=False
		
		if key.vk == libtcod.KEY_RIGHT:
			var.input['right']=True
		else:
			var.input['right']=False
		
		if key.vk == libtcod.KEY_ENTER:
			if var.in_menu:
				functions.menu_select()
			else:
				var.player.enter()
				var.buffer = [[0] * var.world_size[1] for i in range(var.world_size[0])]
				region = (0,0,var.window_size[0]+1,var.window_size[1]+1)
				libtcod.console_clear(var.view)
				draw_screen(refresh=True)
		
		if key.c == ord('x'):
			var.max_fps=60
			libtcod.sys_set_fps(var.max_fps)
		
		if key.c == ord('z'):
			var.max_fps=20
			libtcod.sys_set_fps(var.max_fps)
		
		if key.c == ord('c'):
			var.max_fps=10
			libtcod.sys_set_fps(var.max_fps)
		
		if key.vk in [libtcod.KEY_ESCAPE] or key.c == ord('q'):
			return True
	
	tick()
	return False

#if not var.server: draw_screen()
if var.server or var.output=='pygame':
	while 1:
		if var.server:			
			try:
				tick()
			except KeyboardInterrupt:
				logging.info('Shutting down.')
				
				_total = 0
				for entry in var.tick_history:
					_total+=entry
				
				try:
					logging.info('Average FPS: %s' % str((_total/len(var.tick_history))))
				except:
					logging.error('Wasn\'t running long enough to find average FPS')
				var.world.save()
				sys.exit()
		else: get_input()
else:
	while not libtcod.console_is_window_closed():
		if get_input(): break