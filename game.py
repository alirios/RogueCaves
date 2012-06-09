import levelgen, functions, world, cache, life
import logging, random, time, var, sys, os

if '-server' in sys.argv:
	var.server = True
else:
	import pygcurse, pygame
	from pygame.locals import *
	pygame.font.init()
	var.server = False

__release__ = None
if not __release__: __version__ = time.strftime('%m.%d.%YA')
else: __version__ = 'Release %s' % __release__

logger = logging.getLogger()
if '-debug' in sys.argv: logger.setLevel(logging.DEBUG)
else: logger.setLevel(logging.INFO)
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

if var.server: logging.info('Rogue Caves Server - %s' % __version__)
else: logging.info('Rogue Caves - %s' % __version__)

#Setup stuff...
var.window_size = (99,33)
var.world_size = (99,33)
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
var.solid = [0,11,15]
var.blocking = [10]
var.items = [13,14]
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
var.items = {'11':{'name':'dirt','solid':True,'type':'solid','life':2,'tile':11},
			'13':{'name':'gold','solid':False,'type':'ore','tile':13,'price':15},
			'14':{'name':'coal','solid':False,'type':'ore','tile':14,'price':2},
			'17':{'name':'meat','solid':False,'type':'food','tile':17,'price':8},
			'18':{'name':'chest','solid':True,'type':'storage','items':[],'tile':18,'price':25},
			'19':{'name':'pickaxe','solid':False,'type':'weapon','damage':3,\
				'status':None,'rank':1,'sharp':True,'tile':19,'price':15},
			'20':{'name':'bronze','solid':False,'type':'ore','tile':20,'price':1},
			'21':{'name':'carrot (seed)','solid':False,'type':'seed','tile':21,'price':2,\
				'growth':0,'growth_max':2,'growth_time':0,'growth_time_max':2,'image_index':0,\
				'images':['i','I','Y'],'makes':22},
			'22':{'name':'carrot','solid':False,'type':'food','tile':22,'price':4,'cook_time':10,\
				'makes':25},
			'23':{'name':'hoe','solid':False,'type':'weapon','damage':1,\
				'status':None,'rank':1,'sharp':True,'tile':23,'price':9},
			'24':{'name':'stove','solid':False,'type':'stove','tile':24,'price':50,'cooking':None},
			'25':{'name':'steamed carrot','solid':False,'type':'cooked food','tile':25,'price':8},
			'26':{'name':'single bed','solid':False,'type':'bed','owner':None,'tile':26,'price':35}}
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
	'18':{'icon':'#','color':['brown','lightsand']},
	'19':{'icon':'/','color':['silver',None]},
	'20':{'icon':'b','color':['gray','brown']},
	'21':{'icon':'i','color':['sand',None]},
	'22':{'icon':'Y','color':['brown',None]},
	'23':{'icon':'L','color':['silver',None]},
	'24':{'icon':'#','color':['gray','darkergray']},
	'25':{'icon':'i','color':['brown',None]},
	'26':{'icon':'#','color':['white','red']}}

if not var.server:
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
	
	#Setup
	var.clock = pygame.time.Clock()
	var.buffer = [[0] * var.world_size[1] for i in range(var.world_size[0])]
	
	#Fonts...
	_font = pygame.font.Font('ProggyClean.ttf', 16)

	#Surfaces...
	var.window = pygcurse.PygcurseWindow(var.window_size[0],\
		var.window_size[1],\
		font=_font,\
		caption='RogueCaves')
	var.view = pygcurse.PygcurseSurface(var.window_size[0],\
		var.window_size[1]-6,\
		font=_font,\
		windowsurface=var.window._windowsurface)
	var.menu = pygcurse.PygcurseSurface(var.window_size[0],\
		var.window_size[1]-6,\
		font=_font,\
		windowsurface=var.window._windowsurface)
	var.log = pygcurse.PygcurseSurface(var.window_size[0],\
		var.window_size[1],\
		font=_font,\
		windowsurface=var.window._windowsurface)

	#Stuff...
	var.window.autoupdate = False
	var.view.autoupdate = False
	var.log.autoupdate = False

	#Log
	_title = 'Rogue Caves'
	var.view.putchars(_title,
		x=(var.window_size[0]/2)-(len(_title)/2),
		y=var.window_size[1]/2,
		fgcolor='white')
	var.view.putchars(__version__,
		x=(var.window_size[0]/2)-(len(__version__)/2),
		y=(var.window_size[1]/2)+1,
		fgcolor='gray')
	
	var.view.putchars('Generating world...',x=0,y=0)
	var.view.update()

#Load dictionary files
if not var.server:
	var.view.putchars('Loading dictionaries...',x=0,y=1)
	var.view.update()
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
var.world = world.World(size=(var.world_size[0],var.world_size[1]-6),depth=6)
if '-load' in sys.argv:
	var.world.load()
else:
	var.world.generate()
	
	#Gods
	if not var.server:
		var.view.putchars('Gods...',x=0,y=2)
		var.view.update()

	var.ivan = life.god()
	var.ivan.name = 'Ivan'
	var.ivan.purpose = 'death'
	var.ivan.alignment = 'evil'
	var.ivan.accepts = ['human']

	#People
	if not var.server:
		var.view.putchars('People...',x=0,y=3)
		var.view.update()

	var.player = life.human(player=True)
	var.player.name = 'flags'
	var.player.z = 1
	var.player.speed = 1
	var.player.speed_max = 1
	var.player.level = var.world.get_level(var.player.z)
	var.player.pos = list(var.player.level.get_open_buildings_of_type('store')[0]['door'])
	var.player.god = var.ivan
	var.player.talents.append('Animal Husbandry')

	for i in range(9):
		var.player.add_item_raw(21)

	#for i in range(1,var.world.depth):
	#	test = life.crazy_miner()
	#	test.name = 'Chester'
	#	test.z = -i
	#	test.speed = 3
	#	test.speed_max = 3
	#	test.level = var.world.get_level(test.z)
	#	test.pos = random.choice(test.level.walking_space)
	#	_i = test.add_item_raw(19)
	#	test.equip_item(_i)

	#for i in range(2):
	#	test = life.human(male=False)
	#	test.z = 1
	#	test.speed = 3
	#	test.speed_max = 3
	#	test.level = var.world.get_level(test.z)
	#	test.icon['color'][0] = 'blue'
	#	test.skills = ['trade']
	#	test.pos = list(test.level.get_open_buildings_of_type('store')[0]['door'])
	
	for i in range(1):
		test = life.dog(male=random.randint(0,1))
		test.z = 1
		test.speed = 1
		test.speed_max = 1
		test.level = var.world.get_level(test.z)
		test.pos = test.level.get_open_space_around((2,2))[0]
		test.owner = var.player
		
	#for i in range(1):
	#	test = life.human()
	#	test.z = 1
	#	test.speed = 1
	#	test.speed_max = 1
	#	test.level = var.world.get_level(test.z)
	#	_building = test.level.get_open_buildings_with_items(['storage','stove'])[0]['name']
	#	test.claim_building(_building,'home')
	#	test.icon['color'][0] = 'red'
	#	for i in range(9):
	#		test.add_item_raw(21)
	#	test.skills = ['farm']
	#	test.pos = list(test.get_claimed('home',return_building=True)['door'])

var.temp_fps = 0
var.gametime = time.time()
var.fpstime = time.time()
var.dirty = []

def draw_tile(tile,pos,color):
	if tile.has_key('id'):
		if var.buffer[pos[0]][pos[1]] == tile['id'] and var.player.level.outside: return
		else:
			#print var.buffer[pos[0]][pos[1]],tile['id']
			var.buffer[pos[0]][pos[1]] = tile['id']
	
	var.dirty.append(pos)
	
	if isinstance(tile['icon'],unicode):
		tile['icon'] = str(tile['icon'])
	
	var.view.putchar(tile['icon'],x=pos[0],y=pos[1],fgcolor=color[0],bgcolor=color[1])

def draw_screen(refresh=False):	
	region = (0,0,var.window_size[0]+1,var.window_size[1]+1)
	_starttime = time.time()
	#var.view.fill('black','black',region=region)
	if not var.player.level.outside:
		var.view.setbrightness(0, region=region)
	
	var.player.level.light(var.player.pos)
	#_m.tick_lights()
	var.dirty = []
	
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
				_item = var.player.level.items[x][y][0]
				_tile = tile_map[str(_item['tile'])].copy()
				
				if _item.has_key('images'):
					_tile['icon'] = _item['images'][_item['image_index']]
			
			for life in var.life:
				if life.z == var.player.z and life.pos == [x,y]:
					_tile = life.icon
					_tile['id'] = life.id
			
			if var.player.level.tmap[x][y]:
				var.player.level.tmap[x][y]-=1
			
			if var.player.level.vmap[x][y]:
				if not _tile:
					_tile = tile_map[str(var.player.level.map[x][y])]
					_tile['id'] = var.player.level.map[x][y]
				_bgcolor = tile_map[str(var.player.level.map[x][y])]['color'][1]
				
				if not _tile['color'][1]:
					if _tile['color'][0]=='white' and _bgcolor in ['white','sand','lightsand','brown']:
						draw_tile(_tile,(x,y),('black',_bgcolor))
					else:
						draw_tile(_tile,(x,y),(_tile['color'][0],_bgcolor))
				
				elif _tile['color'][1]=='blue':
					draw_tile(_tile,(x,y),(_tile['color'][0],pygame.Color(0, 0, random.randint(150,200))))
				else:
					draw_tile(_tile,(x,y),_tile['color'])
				
				if var.player.level.tmap[x][y]:
					var.view.tint(r=var.player.level.tmap[x][y],region=(x,y,1,1))
				
				#_dist = functions.distance(var.player.pos,var.mouse_pos)
				#if (x,y)==var.mouse_pos:
				#	if _dist<=5:
				#		var.view.lighten(50,(x,y,1,1))
				#	else:
				#		var.view.darken(50,(x,y,1,1))

			elif var.player.level.fmap[x][y]:
				if not _tile: _tile = tile_map[str(var.player.level.map[x][y])]
				
				var.view.putchar(_tile['icon'],\
					x=x,\
					y=y,\
					fgcolor=_tile['color'][0],\
					bgcolor='altgray')
				var.view.darken(100,(x,y,1,1))
			elif refresh:
				var.view.putchar(' ',x=x,y=y,fgcolor='black',bgcolor='black')
	
	var.log.fill(fgcolor=(255,0,0),region=(0,var.window_size[1]-6,var.window_size[0],6))
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
	
	var.log.putchars(_char,x=0,y=var.window_size[1]-6,fgcolor='white',bgcolor='black')
	var.log.putchars(_health,x=len(_char)+1,y=var.window_size[1]-6,fgcolor='green',bgcolor='black')
	var.log.putchars(_depth,x=len(_char)+len(_health)+2,y=var.window_size[1]-6,fgcolor='gray',bgcolor='black')
	var.log.putchars(_skill,x=len(_char)+len(_health)+len(_depth)+3,y=var.window_size[1]-6,fgcolor='white',bgcolor='black')
	var.log.putchars(_thirst,x=len(_char)+len(_health)+len(_depth)+len(_skill)+4,y=var.window_size[1]-6,fgcolor='blue',bgcolor='black')
	var.log.putchars(_hunger,x=len(_char)+len(_health)+len(_depth)+len(_skill)+len(_thirst)+5,y=var.window_size[1]-6,fgcolor='maroon',bgcolor='black')
	var.log.putchars('FPS: %s' % str(var.fps),x=var.window_size[0]-7,y=var.window_size[1]-6,fgcolor='white')
	
	#TODO: Resetting colors here might help.
	if var.in_menu:
		var.menu.putchars(var.menu_name,x=(var.window_size[0]/2)-len(var.menu_name)/2,y=(var.window_size[1]/2)-(len(var.in_menu)/2)-4,fgcolor='white',bgcolor='black')
		
		for item in var.in_menu:
			if var.menu_index == var.in_menu.index(item):
				_color = 'white'
			else:
				_color = 'gray'
			_tile = tile_map[str(item['item']['tile'])]
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
		
		var.log.putchars(entry,\
			x=0,\
			y=var.\
			window_size[1]-5+(_i),\
			fgcolor=_fgcolor,\
			bgcolor='black')
		_i+=1
	
	if var.in_menu: var.menu.update()
	else:
		var.log.update()
		#var.view.update(_xrange=tuple(_xrange),_yrange=tuple(_yrange))
		var.view.update_alt(var.dirty)
	
	if time.time()-var.fpstime>=1:
		var.fpstime=time.time()
		var.fps = var.temp_fps
		var.time += 1
		var.temp_fps = 0
	else:
		var.temp_fps += 1

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
				if life.player: continue
				life.walk(None)
		elif not var.player.in_danger:
			if _key: var.player.walk(_key)
			
			for life in var.life:
				life.tick()
				if life.player: continue
				life.walk(None)
		elif var.player.in_danger:
			if _key:
				var.player.walk(_key)
				
				for life in var.life:
					life.tick()
					if life.player: continue
					life.walk(None)
	
	if var.server:
		var.ticks += 1
		
		if var.ticks>=var.server_tick_rate:
			time.sleep(1)
		
		return
	
	if var.mouse_pos == (None,None):
		var.mouse_pos = (0,0)
	if var.player.level.outside:
		draw_screen(refresh=True)
	else:
		draw_screen()
	var.clock.tick(var.max_fps)

def get_input():
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
				var.max_fps = 1
			elif event.key == K_v:
				for pos in var.player.level.real_estate:
					var.view.setbrightness(0, region=(pos[0],pos[1],1,1))
		elif event.type == MOUSEMOTION:
			var.mouse_pos = var.view.getcoordinatesatpixel(event.pos)
		elif event.type == MOUSEBUTTONDOWN:
			for life in var.life:
				if life.z == var.player.z:
					if life.pos == list(var.mouse_pos):
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
						#print 'Inventory: '
						#for item in life.items:
						#	print item
			
			for item in var.player.level.items[var.mouse_pos[0]][var.mouse_pos[1]]:
				if item['pos'] == var.mouse_pos:
					print item
	
	tick()

if not var.server: draw_screen()

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