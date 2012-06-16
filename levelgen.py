import functions, life, draw, var
import logging, copy, math, random, time
import numpy

class LevelGen:
	def __init__(self,size=(50,50),rooms=25,room_size=(5,7),diagtunnels=True,overlaprooms=False,outside=False):
		self.size 			= size
		self.map 			= []
		self.rooms 			= []
		self.max_rooms 		= rooms
		self.room_size 		= room_size
		self.diagtunnels 	= diagtunnels
		self.overlaprooms 	= overlaprooms
		self.outside 		= outside
		self.landmarks 		= []
		self.walking_space 	= []
		self.walls 			= []
		
		#Lights and maps...
		self.lights 		= []
		self.fmap 			= [[0] * self.size[1] for i in xrange(self.size[0])]
		self.real_estate	= []
		self.lmap 			= []
		self.tmap 			= []
		self.fov 			= []
		self.items 			= []
		
		#Python has no concept of 2d arrays, so we "fake" it here.
		for x in xrange(self.size[0]):
			_y = []
			_l = []
			_i = []
			_t = []
			
			for y in xrange(self.size[1]):
				_y.append(0)
				_l.append({'source':False,'color':(0,0,0),'brightness':0})
				_i.append([])
				_t.append(0)
				self.walls.append((x,y))
			
			self.map.append(_y)
			self.lmap.append(_l)
			self.tmap.append(_t)
			self.items.append(_i)
	
	def save(self):
		_keys = {}
		_keys['size'] = self.size
		_keys['map'] = self.map
		_keys['fmap'] = self.fmap
		_keys['tmap'] = self.tmap
		_keys['real_estate'] = self.real_estate
		_keys['z'] = self.z
		_keys['entrances'] = self.entrances
		_keys['exits'] = self.exits
		_keys['outside'] = self.outside
		
		_rooms = []
		for room in self.rooms:
			if room.has_key('owner') and room['owner']:
				_r = room.copy()
				_r['owner'] = _r['owner'].id
				_rooms.append(_r)
			else:
				_rooms.append(room)
		
		_keys['rooms'] = _rooms
		
		_items = copy.deepcopy(self.items)
		for y in xrange(self.size[1]):
			for x in xrange(self.size[0]):
				for item in _items[x][y]:
					if item.has_key('planted_by'):
						item['planted_by'] = item['planted_by'].id
					if item.has_key('from'):
						item['from'] = item['from'].id
					if item.has_key('owner') and item['owner']:
						item['owner'] = item['owner'].id
					
					if item['type'] == 'storage':
						for _item in item['items']:
							if _item.has_key('planted_by'):
								_item['planted_by'] = _item['planted_by'].id
							if _item.has_key('from'):
								_item['from'] = _item['from'].id
					if item['type'] == 'stove' and item['cooking'] and item['cooking'].has_key('planted_by'):
						item['cooking']['planted_by'] = item['cooking']['planted_by'].id
		
		_keys['items'] = _items
		
		return _keys
	
	def load(self,keys):
		self.size = keys['size']
		self.map = keys['map']
		self.fmap = keys['fmap']
		self.tmap = keys['tmap']
		self.real_estate = keys['real_estate']
		self.z = keys['z']
		self.entrances = keys['entrances']
		self.exits = keys['exits']
		self.outside = keys['outside']
		
		self.rooms = keys['rooms']
		self.items = keys['items']
	
	def finalize(self):
		"""Cleans up after load()"""
		for room in self.rooms:
			room['name'] = str(room['name'])
			
			if room.has_key('owner') and room['owner']:
				room['owner'] = functions.get_alife_by_id(room['owner'])
		
		for y in xrange(self.size[1]):
			for x in xrange(self.size[0]):
				for item in self.items[x][y]:
					if item.has_key('planted_by'):
						item['planted_by'] = functions.get_alife_by_id(item['planted_by'])
					if item.has_key('from'):
						item['from'] = functions.get_alife_by_id(item['from'])
					if item.has_key('owner') and item['owner']:
						item['owner'] = functions.get_alife_by_id(item['owner'])
					
					if item['type'] == 'storage':
						for _item in item['items']:
							if _item.has_key('planted_by'):
								_item['planted_by'] = functions.get_alife_by_id(_item['planted_by'])
							if _item.has_key('from'):
								_item['from'] = functions.get_alife_by_id(_item['from'])
					if item['type'] == 'stove' and item['cooking'] and item['cooking'].has_key('planted_by'):
						item['cooking']['planted_by'] = functions.get_alife_by_id(item['cooking']['planted_by'])
	
	def build_color_map(self):
		self.color_map = []
		r = numpy.zeros((self.size[1],self.size[0]))
		g = numpy.zeros((self.size[1],self.size[0]))
		b = numpy.zeros((self.size[1],self.size[0]))
		
		for x in xrange(0,self.size[0]):	
			for y in xrange(0,self.size[1]):
				_fgcolor = var.color_codes[var.tile_map[str(self.map[x][y])]['color'][0]]
				_bgcolor = var.color_codes[var.tile_map[str(self.map[x][y])]['color'][1]]
				#r[x,y] = _fgcolor[0]
				#g[x,y] = _fgcolor[1]
				#b[x,y] = _fgcolor[2]
				r[y,x] = _bgcolor[0]
				g[y,x] = _bgcolor[1]
				b[y,x] = _bgcolor[2]
		
		self.color_map.append(r)
		self.color_map.append(g)
		self.color_map.append(b)
	
	def add_light(self,pos,color,life,brightness):
		self.lights.append(pos)
		
		self.lmap[pos[0]][pos[1]]['source'] 	= True
		self.lmap[pos[0]][pos[1]]['color'] 		= color
		self.lmap[pos[0]][pos[1]]['life'] 		= life
		self.lmap[pos[0]][pos[1]]['brightness'] = brightness
		self.lmap[pos[0]][pos[1]]['children'] 	= []
	
	def add_item(self,item,pos,no_place=False):
		_item = var.items[str(item)].copy()
		
		#if item in [18]: _item['items'] = []
		if _item.has_key('items'): _item['items'] = []
		
		_item['pos'] = pos
		
		if not no_place: self.items[pos[0]][pos[1]].append(_item)
		
		return _item
	
	def get_item(self,pos):
		return self.items[pos[0]][pos[1]]
	
	def get_all_items_of_tile(self,tile):
		_ret = []
		for y in xrange(self.size[1]):
			for x in xrange(self.size[0]):
				for item in self.items[x][y]:
					if item['type'] == 'storage':
						for _item in item['items']:
							if _item['tile'] == tile:
								_ret.append(_item)					
		
					if item['tile'] == tile:
						_ret.append(item)
		
		return _ret		
	
	def get_items(self,**kargv):
		_ret = []
		
		for y in xrange(self.size[1]):
			for x in xrange(self.size[0]):
				for item in self.items[x][y]:
					_match = kargv.keys()
					for key in kargv:
						if item.has_key(key) and item[key]==kargv[key]:
							_match.remove(key)
							
							if not _match:
								_ret.append(item)
								break
		
		return _ret
	
	def get_items_ext(self,**kargv):
		_ret = []
		
		for y in xrange(self.size[1]):
			for x in xrange(self.size[0]):
				for item in self.items[x][y]:
					_match = kargv.keys()
					for key in kargv:
						if item.has_key(key) and item[key] in kargv[key]:
							_match.remove(key)
							
							if not _match:
								_ret.append(item)
								break
		
		return _ret
	
	def get_items_in_building(self,building,**kargv):
		_ret = []
		
		for room in self.rooms:
			if room['name'].lower() == building.lower():
				for pos in room['walking_space']:
					for item in self.items[pos[0]][pos[1]]:
						if item['type'] == 'storage':
							for _item in item['items']:
								_match = kargv.keys()
								for key in kargv:
									if _item.has_key(key) and _item[key]==kargv[key]:
										_match.remove(key)
										
										if not _match:
											_ret.append(_item)
											break
						_match = kargv.keys()
						for key in kargv:
							if item.has_key(key) and item[key]==kargv[key]:
								_match.remove(key)
								
								if not _match:
									_ret.append(item)
									break
		
		return _ret
	
	def get_items_in_building_ext(self,building,**kargv):
		_ret = []
		
		for room in self.rooms:
			if room['name'].lower() == building.lower():
				for pos in room['walking_space']:
					for item in self.items[pos[0]][pos[1]]:
						if item['type'] == 'storage':
							for _item in item['items']:
								_match = kargv.keys()
								for key in kargv:
									if _item.has_key(key) and _item[key] in kargv[key]:
										_match.remove(key)
										
										if not _match:
											_ret.append(_item)
											break
						_match = kargv.keys()
						for key in kargv:
							if item.has_key(key) and item[key]==kargv[key]:
								_match.remove(key)
								
								if not _match:
									_ret.append(item)
									break
		
		return _ret
	
	def get_all_items_of_type(self,type,check_storage=True):
		if isinstance(type,list): _list = True
		else: _list = False
		
		_ret = []
		for y in xrange(self.size[1]):
			for x in xrange(self.size[0]):
				for item in self.items[x][y]:
					if item['type'] == 'storage' and check_storage:
						for _item in item['items']:
							if _list:
								if _item['type'] in type:
									_ret.append(_item)
							else:
								if _item['type'] == type:
									_ret.append(_item)
					if _list:
						if item['type'] in type:
							_ret.append(item)
					else:
						if item['type'] == type:
							_ret.append(item)
		
		return _ret
	
	def get_all_items_tagged(self,tag,ignore_storage=False):
		"""Returns items with flag 'tag'."""
		_ret = []
		
		for y in xrange(self.size[1]):
			for x in xrange(self.size[0]):
				for item in self.items[x][y]:
					if item['type'] == 'storage' and not ignore_storage:
						for _item in item['items']:
							if _item.has_key(tag) and _item[tag]:
								_ret.append(_item)
					if item.has_key(tag) and item[tag]:
						_ret.append(item)
		
		return _ret
	
	def get_all_items_in_building(self,building):
		"""Returns all items in 'building'"""
		_ret = []
		
		for room in self.rooms:
			if room['name'].lower() == building.lower():
				for pos in room['walking_space']:
					for item in self.items[pos[0]][pos[1]]:
						if item['type'] == 'storage':
							for _item in item['items']:
								_ret.append(_item)
						_ret.append(item)
		
		return _ret
	
	def get_all_items_in_building_tagged(self,building,tag):
		"""Returns all items in 'building' with 'tag'"""
		_ret = []
		
		for room in self.rooms:
			if room['name'].lower() == building.lower():
				for pos in room['walking_space']:
					for item in self.items[pos[0]][pos[1]]:
						if item['type'] == 'storage':
							for _item in item['items']:
								if _item.has_key(tag) and _item[tag]:
									_ret.append(_item)
						else:
							if item.has_key(tag) and item[tag]:
								_ret.append(item)
		
		return _ret
	
	def get_all_items_in_building_of_type(self,building,type):
		"""Returns all items in 'building' of 'type'"""
		_ret = []
		if isinstance(type,list): _list = True
		else: _list = False
		
		for room in self.rooms:
			if room['name'].lower() == building.lower():
				for pos in room['walking_space']:
					for item in self.items[pos[0]][pos[1]]:
						if item['type'] == 'storage':
							for _item in item['items']:
								if _list:
									if _item['type'] in type:
										_ret.append(_item)
								else:
									if _item['type'] == type:
										_ret.append(_item)
						if _list:
							if item['type'] in type:
								_ret.append(item)
						else:
							if item['type'] == type:
								_ret.append(item)
		
		return _ret
	
	def remove_item_from_building(self,item,building):
		"""Removes 'item' from 'building'"""
		for room in self.rooms:
			if room['name'].lower() == building.lower():
				for pos in room['walking_space']:
					for _item in self.items[pos[0]][pos[1]]:
						if _item['type'] == 'storage':
							for __item in _item['items']:
								if __item == item:
									_item['items'].remove(__item)
									return True
						if _item == item:
							self.items[pos[0]][pos[1]].remove(_item)
							return True
		
		return False
	
	def get_all_solid_items(self):
		_ret = []
		for y in xrange(self.size[1]):
			for x in xrange(self.size[0]):
				for item in self.items[x][y]:
					if item['solid']:
						_ret.append(item)
		
		return _ret
	
	def get_open_buildings_of_type(self,type):
		_ret = []
		
		for room in self.rooms:
			if room['owner']: continue
			if room['type'] == type: _ret.append(room)
		
		return _ret
	
	def get_open_buildings_with_items(self,items):
		_ret = []
		
		for room in self.rooms:
			if room['owner']: continue
			
			_needs = items[:]
			for pos in room['walking_space']:
				for item in self.items[pos[0]][pos[1]]:
					if item['type'] in _needs:
						_needs.remove(item['type'])
			
			if not _needs: _ret.append(room)
		
		return _ret
	
	def get_all_buildings_of_type(self,type):
		_ret = []
		
		for room in self.rooms:
			if room['type'].lower() == type.lower():
				_ret.append(room)
		
		return _ret
	
	def get_open_space_around(self,pos,dist=5):
		"""Returns all open spaces around 'pos' in xrange 'dist'"""
		_ret = []
		
		for x1 in xrange(-dist,dist+1):
			x = pos[0]+x1
			if x<0 or x>=self.size[0]: continue
			for y1 in xrange(-dist,dist+1):
				y = pos[1]+y1
				if y<0 or y>=self.size[1]: continue
				
				if self.map[x][y] in var.solid: continue
				_ret.append((x,y))
		
		return _ret
	
	def get_real_estate(self,size):
		_ret = []
		for x1 in xrange(self.size[0]):
			if not x1: continue
			#if x1==self.size[0]: continue
			for y1 in xrange(self.size[1]):
				if not y1: continue
				#if y1>=self.size[1]: continue
				_break = False
				for x2 in xrange(size[0]):
					if x1+x2>=self.size[0]: _break=True;break
					for y2 in xrange(size[1]):
						if y1+y2>=self.size[1]-1: _break=True;break
						if (x1+x2,y1+y2) in self.real_estate:
							_break = True
							break
					
					if _break: break
				
				if _break: break
				else: _ret.append((x1,y1))
		
		return _ret
	
	def claim_real_estate(self,pos,size):
		for x1 in xrange(size[0]):
			for y1 in xrange(size[1]):
				self.real_estate.append((pos[0]+x1,pos[1]+y1))
	
	def has_item_type_at(self,type,pos):
		for item in self.items[pos[0]][pos[1]]:
			if item['type'] == type:
				return True
		
		return False
	
	def has_solid_item_at(self,pos):
		for item in self.items[pos[0]][pos[1]]:
			if item['solid']:
				return True
		
		return False
	
	def remove_item_at(self,item,pos):
		for y in xrange(self.size[1]):
			for x in xrange(self.size[0]):
				for _item in self.items[x][y]:
					if _item['type'] == 'storage':
						for __item in _item['items']:
							if __item == item:
								_item['items'].remove(item)
					if _item == item:
						self.items[x][y].remove(item)						
	
	def get_room(self,name):
		for room in self.rooms:
			if room['name'].lower() == name.lower():
				return room
		
		return False
	
	def get_room_items(self,name):
		_ret = []
		
		for room in self.rooms:
			if room['name'].lower() == name.lower():
				for pos in room['walking_space']:
					for item in self.items[pos[0]][pos[1]]:
						if item['type'] == 'storage':
							for _item in item['items']:
								_ret.append(_item)		
						else:
							_ret.append(item)
		
		return _ret
	
	def dofov(self,pos,x,y,dist,efov=False):
		#This next bit comes from http://roguebasin.roguelikedevelopment.org/index.php/Eligloscode
		#I translated it to Python. You are welcome to use this code instead of writing your own :)
		i = 0
		ox = 0
		oy = 0
		ox = pos[0]+0.5
		oy = pos[1]+0.5
		while i<dist:
			i+=1
			if int(ox) >= self.size[0] or int(oy) >= self.size[1]: continue
			if int(ox) < 0 or int(oy) < 0: continue
			self.fmap[int(ox)][int(oy)]=1
			self.vmap[int(ox)][int(oy)]=1
			if self.map[int(ox)][int(oy)] in var.solid or\
				self.has_item_type_at('solid',(int(ox),int(oy))): return
			ox+=x;
			oy+=y;
		
	def light(self,pos):
		self.vmap = [[self.outside] * self.size[1] for i in xrange(self.size[0])]
		
		if self.outside: return
		
		x = 0
		y = 0
		i = 0
		self.fov = []
		while i<360:
			x=math.cos(i*0.01745);
			y=math.sin(i*0.01745);
			self.dofov(pos,x,y,10);
			i+=1
	
	def tick(self):
		for item in self.get_all_items_of_type(['seed','stove','forge'],check_storage=False):
			if item['type'] == 'seed':
				if item.has_key('planted_by') and item['growth']==item['growth_max']:
					self.items[item['pos'][0]][item['pos'][1]].remove(item)
					_i = self.add_item(item['makes'],item['pos'])
					_i['planted_by'] = item['planted_by']
				
				if item['growth_time']>=item['growth_time_max']:
					item['growth']+=1
					item['image_index']+=1
					item['growth_time']=0
				else: item['growth_time']+=1
			elif item['type'] == 'stove':
				if item['cooking'] and item['cooking']['type']=='food':
					if item['cooking']['type']=='food' and\
						item['cooking']['cook_time']: item['cooking']['cook_time']-=1
					else:
						item['cooking'] = self.add_item(item['cooking']['makes'],item['pos'],no_place=True)
			elif item['type'] == 'forge':
				if item['forging']:
					if item['forge_time']>0: item['forge_time']-=1
					elif not item['forge_time']:
						item['forging'] = self.add_item(item['forging'],item['pos'],no_place=True)
						item['forge_time'] = -1
	
	def tick_lights(self):
		for _l in self.lights:
			light = self.lmap[_l[0]][_l[1]]

			if self.lmap[_l[0]][_l[1]]['life']<=0:
				self.lmap[_l[0]][_l[1]]['source'] = False
				self.lmap[_l[0]][_l[1]]['color'] = (0,0,0)
				self.lmap[_l[0]][_l[1]]['brightness'] = 0
				self.lights.remove(_l)
				continue
			
			self.lmap[_l[0]][_l[1]]['life']-=1
			
			if light['source']:
				light['children'] = []
				
				for _pos in draw.draw_circle(_l,light['brightness']):
					if not (_pos) in light['children']: 
						light['children'].append(_pos)
	
	def decompose(self,times,edgesonly=True,count=4,tile=-1,to=1,all=False):
		for i in xrange(times):
			_map = copy.deepcopy(self.map)
			
			for y in xrange(self.size[1]-1):
				for x in xrange(self.size[0]-1):
					if (x,y) in self.landmarks: continue
					
					if self.map[x][y] and edgesonly: continue
					
					_count = 0
					for pos in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
						_x = x+pos[0]
						_y = y+pos[1]
						
						if 0>_x<self.size[0]-1: continue
						if 0>_y<self.size[1]-1: continue
						#print _x,_y
						
						if tile==-1:
							if self.map[_x][_y]:
								_count+=1
						elif tile>=0:
							if self.map[_x][_y]==tile:
								_count+=1
						elif all:
							_count+=1
					
					if _count>=count:
						_map[x][y]=to
		
			self.map = _map
	
	def decompose_ext(self,times,all=False,find=-1,to=-1,count=3):
		for i in xrange(times):
			_map = copy.deepcopy(self.map)
			
			for x in xrange(self.size[0]):
				for y in xrange(self.size[1]):
					if (x,y) in self.landmarks: continue
					
					if self.map[x][y]==find and not all: continue
					
					_count = 0
					for pos in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
						_x = x+pos[0]
						_y = y+pos[1]
						
						if 0>_x or _x>self.size[0]-1: continue
						if 0>_y or _y>self.size[1]-1: continue
						
						if self.map[_x][_y] == find:
							_count+=1			
					
					if _count>=count:
						_map[x][y]=to
		
			self.map = _map

	def walk(self,walkers=7,intensity=(25,45),types=[],where=[]):
		#Okay, this is a bit tricky...
		#I did this kind of levelgen for a previous
		#game and it looked okay...
		#We'll see how it works here.
		_walkers = []
		_dirs = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
		_ret = []
		
		for i in xrange(walkers):
			_pos = random.choice(where)
			_tile = random.choice(types)
			_walkers.append([_pos[0],_pos[1],_dirs[:],_tile])
		
		for i in xrange(random.randint(intensity[0],intensity[1])):
			for walker in _walkers:
				_pos=random.choice(walker[2])
				walker[2].remove(_pos)
				
				for i2 in xrange(random.randint(3,4)):
					
					if not len(walker[2]):
						walker[2] = _dirs[:]
					
					_x = walker[0]+_pos[0]
					_y = walker[1]+_pos[1]
					
					if (_x,_y) in self.landmarks: continue
					if 1>_x or _x>self.size[0]-2: continue
					if 1>_y or _y>self.size[1]-2: continue
					
					walker[0] = _x
					walker[1] = _y
					
					for pos in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
						if (_x+pos[0],_y+pos[1]) in self.landmarks: continue
						if 1>_x+pos[0] or _x+pos[0]>=self.size[0]-2: continue
						if 1>_y+pos[1] or _y+pos[1]>=self.size[1]-2: continue
						
						self.map[_x+pos[0]][_y+pos[1]] = walker[3]
						_ret.append((_x+pos[0],_y+pos[1]))
						
						if walker[3] in var.blocking:
							if (_x+pos[0],_y+pos[1]) in self.walking_space:
								self.walking_space.remove((_x+pos[0],_y+pos[1]))
						
					self.map[_x][_y] = walker[3]
					_ret.append((_x,_y))
			
		return _ret
	
	def generate_cave(self, entrances=[(4,4)],exits=[]):
		#We'll be generating the level in the following
		#way:
		#  Place a small room around the entrance
		#  Randomly place rooms
		#     Mark chosen spot as a "landmark"
		#  Connect landmarks via tunnels
		
		#Our map is currently all 0s
		#In the end, we will have a mix of numbers
		
		#0 - wall
		#1 - floor
		#2 - tunnel
		#3 - door
		
		self.entrances = entrances
		self.exits = exits
		
		#First, let's place our entrances+exits.
		_places = entrances[:]
		_places.extend(exits)
		for pos in _places:
			#We'll make a 3x3 area around it
			for x in xrange(-1,2):
				#One thing I suggest is making lines
				#as compact as possible.
				#For example, we'll be writing "entrance[0]+x"
				#and "entrance[1]+y" a lot in the next three lines
				#this can give us the impression that the line
				#is complicated when it's just simple addition...
				#Also doing more complex math OVER AND OVER
				#will slow things down a lot, so it's better
				#to just do it once and assign it to a variable
				#Addition is by no means complicated, but it
				#makes things more readable.
				
				#As a rule of thumb, I always put an underscore
				#before the variables I plan to throw away...
				_x = pos[0]+x
				
				for y in xrange(-1,2):
					#We need to check to see if we're drawing
					#inside the map first...
					#By the way, a '\' in Python
					#just lets us drop down a line in case
					#a line gets too lengthy...
					#Very handy!
					
					#Another temp variable...
					_y = pos[1]+y
					
					if 0<_x<self.size[0]\
						and 0<_y<self.size[1]:
							self.map[_x][_y] = 1
							if not (_x,_y) in self.walking_space:
								self.walking_space.append((_x,_y))
							if (_x,_y) in self.walls:
								self.walls.remove((_x,_y))
					
					#What we just did was "carve" out the room
					#Imagine these as rooms in a cave or something,
					#like the dungeons in Oblivion...
					#We also add the open space we create to a
					#"walking_space" list.
					#We'll use this later, but just know that
					#it marks places you could potentially walk
					#(it does more than just that, though!)
		
			#Now, here's where tunneling comes into play
			#First, we keep track of all the major "landmarks"
			#on our map.
			#These are things like doors, exits, and the center
			#of rooms.
			#We'll use these as guidelines for our tunnels...
			#Since we already have an entrance, add it to
			#the list...
			self.landmarks.append(pos)
		
		#We'll want to place our rooms next
		for i in xrange(self.max_rooms):
			#To prevent our rooms from being too far apart,
			#we want to randomly select a position and compare
			#it to our landmark list...
			_found = False
			_room_size = (random.randint(self.room_size[0],self.room_size[1]),\
				random.randint(self.room_size[0],self.room_size[1]))
			
			#Here, we keep looking through the list of walls on the map
			#Technically, every wall on the map could potentially be the
			#cornerstone for a room, so we should check them all until we
			#find one.
			#NOTE:
			#As you can see, we're using a while loop and checking the
			#array "self.walls"
			#If a position is randomly chosen from this array and it turns
			#out to not be a good place to put the room, then we should
			#remove it from the array so it doesn't get checked again.
			
			#Here, I make a copy of the array...
			_walls = self.walls[:]
			#We'll be using this throughout the while loop, which
			#will hopefully speed things up...
			
			while not _found:
				_found = True
				
				#This array holds all the positions for every tile
				#in the room.
				_room = []
				
				#Randomly select a position from our array of walls
				_pos = random.choice(_walls)
				
				#Remove the position from the array so it isn't checked
				#again.
				_walls.pop(_walls.index(_pos))
				
				#Check to make sure the room will fit in this spot
				if _pos[0]-(_room_size[0]/2)<=0 or _pos[0]+(_room_size[0]/2)>=self.size[0]: _found=False;continue
				if _pos[1]-(_room_size[1]/2)<=0 or _pos[1]+(_room_size[1]/2)>=self.size[1]: _found=False;continue
				
				#Start checking to see if the room "fits"
				for x in xrange(-_room_size[0]/2,_room_size[0]/2):					
					_x = _pos[0]+x
					
					for y in xrange(-_room_size[1]/2,_room_size[1]/2):
						_y = _pos[1]+y
						
						#ALRIGHT, IS YOUR BODY READY?
						#This is the last check we do to make sure the room
						#is okay. If we want to overlap rooms, then the next
						#line will always be true and the room can begin
						#being placed.
						#IF a floor tile is detected, then the loop breaks
						#and we restart the whole process.
	
						if not self.map[_x][_y] in [0,2] and not self.overlaprooms:
							_found = False
							break
						else:
							#We're okay. Add the floor tiles to the array
							#_room
							_room.append((_x,_y))
					
					if not _found: break
				
				#We made it.
				#Make sure the room is of proper size and begin placing.
				if _found and len(_room)>=9:
					__room = {'name':'cave_room','walls':[],'open_walls':[],'walking_space':_room,\
						'door':None,'type':None}
					
					#Find some open walls
					
					#For every floor tile in the room...
					for pos in _room:
						#change the spot on the map to a floor tile
						#and add this position to the "walking_space"
						#array.
						
						self.map[pos[0]][pos[1]] = 1
						self.walking_space.append(pos)
						
						#Remove the position from the REAL self.walls
						#array-- NOT the copy we made earlier
						if pos in self.walls:
							self.walls.remove(pos)
							
					#Add it to our rooms array
					self.rooms.append(__room)
					
					#Instead of finding the center, just find a random
					#spot in the array. This makes the tunnels look a
					#bit more natural.
					self.landmarks.append(random.choice(_room))
				else:
					_found = False
		
		#Hang in there...
		#This is the last big part.
		
		#Now we're going to loop through all the landmarks we just
		#placed and connect them in the best way possible...
		#The following array tracks which landmarks have already been
		#connected.
		_done = []
		
		for l1 in self.landmarks:
			#This is concept I use a lot in my code
			#It finds the nearest landmark to the one we're connecting.
			_lowest = {'where':None,'dist':9000}
			
			for l2 in self.landmarks:
				#We can't connect to ourselves!
				if l1 == l2 or l2 in _done: continue
				
				#Find the distance between the two landmarks.
				_dist = abs(l2[0]-l1[0])+abs(l2[1]-l1[1])
				
				#If it's closer than the current one, then set _lowest
				#to represent that.
				if _dist<_lowest['dist']:
					_lowest['dist'] = _dist
					_lowest['where'] = l2
			
			#If we couldn't connect it, then break (this is usually true
			#for the last room)
			if not _lowest['where']: break
			
			#If we allow diagonal tunnels, then randomly
			#choose between straight and diagonal here.
			if random.randint(0,1) and self.diagtunnels:
				_diag = True
				_line = draw.draw_diag_line(l1,_lowest['where'])
			else:
				_diag = False
				_line = draw.draw_line(l1,_lowest['where'])
			
			#Now, for every position in the line, "tunnel" the map
			for pos in _line:
				if not self.map[pos[0]][pos[1]]:
					#Diagonal tunnels require more space because the player
					#can't move like this...
					#   ####
					#   ##..
					#   #@##
					#   #.##
					if _diag:
						for _pos in [(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),(-1,1),(0,1),(1,1)]:
							__pos = (pos[0]+_pos[0],pos[1]+_pos[1])
							
							if __pos[0]<=0 or __pos[0]>=self.size[0]: continue
							if __pos[1]<=0 or __pos[1]>=self.size[1]: continue
							
							self.map[__pos[0]][__pos[1]] = 2
							
							if not __pos in self.walking_space:
								self.walking_space.append(__pos)
							
							if __pos in self.walls:
								self.walls.remove(__pos)
					else:
						#Else, change the map to a tunnel tile!
						if pos[0]<0 or pos[0]>=self.size[0]: continue
						if pos[1]<0 or pos[1]>=self.size[1]: continue
						self.map[pos[0]][pos[1]] = 2
						
						#Add it to the walking_space array if it isn't there already...
						if not pos in self.walking_space:
							self.walking_space.append(pos)
						
						#Remove the spot from the walls array also...
						if pos in self.walls:
							self.walls.remove(pos)
			
			#http://www.youtube.com/watch?feature=player_detailpage&v=7C7WCRoqFVs#t=103s
			_done.append(l1)
		
		#Place our exits
		for pos in entrances:
			self.map[pos[0]][pos[1]] = 3
		
		for pos in exits:
			self.map[pos[0]][pos[1]] = 4
	
	def generate_cave_rooms(self):
		if not len(self.rooms): return
		
		for room in random.sample(self.rooms,abs(self.z)*3):
			for pos in room['walking_space']:
				_x = room['walking_space'][0][0]-pos[0]
				_y = room['walking_space'][0][1]-pos[1]
				_x1 = room['walking_space'][len(room['walking_space'])-1][0]-pos[0]
				_y1 = room['walking_space'][len(room['walking_space'])-1][1]-pos[1]
				
				if not _x or not _y or not _x1 or not _y1:
					self.map[pos[0]][pos[1]] = 15
					room['walls'].append(pos)
				else:
					self.map[pos[0]][pos[1]] = 16
			
			for wall in room['walls']:
				_open = False
				_floor = False
				for _pos in [(0,-1),(1,0),(-1,0),(0,1)]:
					_x = wall[0]+_pos[0]
					_y = wall[1]+_pos[1]
					
					if self.map[_x][_y] == 1:
						_open = True
					
					if self.map[_x][_y] == 16:
						_floor = True
				
				if _open and _floor:
					room['open_walls'].append(wall)
			
			if room['open_walls']:
				for _pos in room['open_walls']:
					self.map[_pos[0]][_pos[1]] = 16
					if _pos in self.walking_space:
						self.walking_space.remove(_pos)
	
	def generate_forest(self,exits=[]):
		self.exits = exits
		self.entrances = [] #ALife needs this
		
		for x in xrange(self.size[0]):
			for y in xrange(self.size[1]):
				if not self.map[x][y]:
					self.map[x][y] = random.choice(var.GRASS)
				self.walking_space.append((x,y))
		
		#self.walk(where=self.walking_space,types=[6,7])
		
		#self.decompose_ext(3,find=8,to=8)
		#self.decompose_ext(3,find=8,to=7)
		#self.decompose_ext(1,find=7,to=7,count=1)
		#self.decompose_ext(3,find=6,to=6)
		#self.decompose_ext(3,find=7,to=7)
		
		_town = town()
		_town.generate()
		_room_size = (6,6)
		
		for _room_type in ['home','home','home','home','home','home','home','home','home',
			'store','store','bar','store','store','store','forge']:
			_room = []
			_zone = _town.get_random_zone()
			_pos = (50+(_zone['pos'][0])*_room_size[0],50+(_zone['pos'][1])*_room_size[1])
		
			for x in xrange(0,_room_size[0]):
				_x = _pos[0]+x
				for y in xrange(0,_room_size[1]):
					_y = _pos[1]+y
					_room.append((_x,_y))
			
			_room_walls = []
			_room_floor = []
			for pos in _room:
				self.real_estate.append((pos[0],pos[1]))
				if _pos[0]-pos[0]==0 or pos[0]==_pos[0]+_room_size[0]-1\
					or _pos[1]-pos[1]==0 or pos[1]==_pos[1]+_room_size[1]-1:
					self.map[pos[0]][pos[1]] = 15
					_room_walls.append(pos)
				else:
					self.map[pos[0]][pos[1]] = 16
					_room_floor.append(pos)
				
				if pos in self.walls:
					self.walls.remove(pos)
			
			__walls = _room_walls[:]
			_doors = []
			__pos = list(_pos)
			if _zone['open'][0]==1:
				__pos[0]+=((_zone['open'][0]*_room_size[0])-1)
				__pos[1]+=((_zone['open'][1]*_room_size[1])+random.randint(2,3))
			elif _zone['open'][0]==-1:
				__pos[1]+=((_zone['open'][1]*_room_size[1])+random.randint(2,3))
			if _zone['open'][1]==1:
				__pos[1]+=((_zone['open'][1]*_room_size[1])-1)
				__pos[0]+=((_zone['open'][0]*_room_size[0])+random.randint(2,3))
			elif _zone['open'][1]==-1:
				__pos[0]+=((_zone['open'][0]*_room_size[0])+random.randint(2,3))
			
			for ___pos in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
				____pos = (__pos[0]+___pos[0],__pos[1]+___pos[1])
				if not ____pos in self.real_estate:
					self.real_estate.append(____pos)
			
			_room_walls.remove(tuple(__pos))
			
			self.map[__pos[0]][__pos[1]] = 16
			__room = {'name':_room_type,'walls':_room_walls,'walking_space':_room_floor,\
				'door':__pos[:],'type':_room_type,'owner':None}
			
			self.rooms.append(__room)
			self.generate_building(__room)
			
			self.landmarks.append(random.choice(_room))
		
		#for road in _town.get_all_zones_of_type('road'):
		#	_pos = (1+(road['pos'][0])*_room_size[0],1+(road['pos'][1])*_room_size[1])
		#	for x in xrange(0,_room_size[0]):
		#		_x = _pos[0]+x
		#		for y in xrange(0,_room_size[1]):
		#			_y = _pos[1]+y
		#			try:
		#				#if road['orientation']=='hor':
		#				#	if y==0 or y==_room_size[1]-1: continue
		#				#else:
		#				#	if x==0 or x==_room_size[0]-1: continue
		#				self.map[_x][_y]=29
		#			except:
		#				pass
		
		for t in xrange(40):
			_tree = self.add_item(32,
				(random.randint(10,self.size[0]-10),
				random.randint(10,self.size[1]-10)))
			_tree['limbs'] = self.generate_tree()
		
		for pos in exits:
			self.map[pos[0]][pos[1]] = 4
			self.claim_real_estate(pos,(1,1))
	
	def generate_building(self,room):
		if room['type'] == 'home':
			_needs = [26,24,18]
		elif room['type'] == 'store':
			_needs = [18,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21]
		elif room['type'] == 'bar':
			_needs = [28,18,27,27,27]
		elif room['type'] == 'forge':
			_needs = [30,18,31]
			room['orders'] = ['23']
		
		room['name'] += str(functions.get_id())
		
		#We like putting things in corners...
		_possible = []
		for pos in room['walking_space']:
			_count = 0
			for _pos in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,-1),(-1,1),(1,1)]:
				x = pos[0]+_pos[0]
				y = pos[1]+_pos[1]
				
				if self.map[x][y] in var.solid:
					_count+=1

			if _count==5:
				_possible.append(pos)
		
		for need in _needs:
			_stored = False
			for _storage in self.get_all_items_in_building_of_type(room['name'],'storage'):
				_storage['items'].append(self.add_item(need,_pos,no_place=True))
				_stored = True
				break
			
			if _possible and not _stored:
				_pos = _possible.pop()
				_i = self.add_item(need,_pos)
				
				if need == 28:
					_i['contains'] = 'ale'
	
	def generate_tree(self):
		_limbs = []
		for x in xrange(-6,7):
			_y = []
			
			for y in xrange(-6,7):
				_y.append(0)
			
			_limbs.append(_y)
		
		for pos in draw.draw_circle((0,0),random.choice([5,7,9,11,13])):
			_limbs[pos[0]][pos[1]]=1	
		
		return _limbs

class town:
	def __init__(self,size=(78,36)):
		self.size = size
		self.zone_size = 6
		self.map = []
		self.zones = []
		
		#Instead of creating a map that is "real" size,
		#	(that is, every x,y coord in self.size),
		#	we instead make "zones", which are simply
		#	chunks out of the landscape of size zone_size^2.
		for x in xrange(self.size[0]/self.zone_size):
			_y = []
			
			for y in xrange(self.size[1]/self.zone_size):
				_y.append({'pos':(x,y),'zone':None,'facing_road':None})
			
			self.zones.append(_y)
	
	def generate(self):
		#Here things get a bit complicated... sorta.
		#We can make the process of generating a town
		#	a lot easier by using the power of MATH to
		#	calculate the available space and return
		#	buildings of a proper size.
		
		#PASS 1: Layout
		#It's good to have a blueprint before we start
		#	putting down buildings, so do some guessing
		#	as to what we want.
		#LAYOUT FLAGS:
		#	orientation: the way a town is built (hor,ver)
		#	road_size: the number of plots a road takes (DEF: 1)
		#	zone_type: the type of zone that is placed here (res,com)
		_flags = {}
		_flags['orientation'] = random.choice(['hor','ver'])
		_flags['road_size'] = 1
		_flags['zone_type'] = 'res'
		_at_chunk = [0,0]
		_chunk = [0,0]
		_chunk_size = (2+(_flags['road_size']))
		_chunk[0]=_chunk_size
		_chunk[1]=_chunk_size
		
		for i in xrange(8):
			for _x in xrange(_chunk[0]):
				x = _at_chunk[0]+_x
				for _y in xrange(_chunk[1]):
					y = _at_chunk[1]+_y
					
					if _flags['orientation']=='ver':
						if _x==0 or _x==_chunk_size-1:
							self.zones[x][y]['zone'] = _flags['zone_type']
						else:
							self.zones[x][y]['zone'] = 'road'
					else:
						if _y==0 or _y==_chunk_size-1:
							self.zones[x][y]['zone'] = _flags['zone_type']
						else:
							self.zones[x][y]['zone'] = 'road'
					
					self.zones[x][y]['orientation'] = _flags['orientation']
			
			if y == (self.size[1]/self.zone_size)-1:
				_at_chunk[1] = 0
				_at_chunk[0] += _chunk_size
			else:
				_at_chunk[1] = _chunk[1]
			
			_flags['orientation'] = random.choice(['hor','ver'])
		
		#Now connect the zones.
		_zones = copy.deepcopy(self.zones)
		for x in xrange(self.size[0]/self.zone_size):
			for y in xrange(self.size[1]/self.zone_size):
				if self.zones[x][y]['zone']=='road': continue
				_count = 0
				for __pos in [(-1,0),(1,0),(0,-1),(0,1)]:
					_pos = (x+__pos[0],y+__pos[1])
					if _pos[0]<0 or _pos[0]>=(self.size[0]/self.zone_size): continue
					if _pos[1]<0 or _pos[1]>=(self.size[1]/self.zone_size): continue
					
					if self.zones[_pos[0]][_pos[1]]['zone']:
						if self.zones[_pos[0]][_pos[1]]['zone']=='road':
							_zones[x][y]['facing_road'] = __pos
						else:
							_count+=1
				
				if x==0: continue
				if y==0 or y==(self.size[1]/self.zone_size)-1: continue
				if _count==2:
					_zones[x][y]['zone'] = 'road'
		
		self.zones = _zones
	
	def get_zone(self,remove=True):
		for y in xrange(self.size[1]/self.zone_size):
			for x in xrange(self.size[0]/self.zone_size):
				if self.zones[x][y]['zone']=='res':
					if remove: self.zones[x][y]['zone'] = None
					return {'pos':(x,y),'open':self.zones[x][y]['facing_road']}
	
	def get_random_zone(self,remove=True):
		_zones = []
		
		for y in xrange(self.size[1]/self.zone_size):
			for x in xrange(self.size[0]/self.zone_size):
				if self.zones[x][y]['zone']=='res':
					_zones.append({'pos':(x,y),'open':self.zones[x][y]['facing_road']})
		
		_ret = random.choice(_zones)
		self.zones[_ret['pos'][0]][_ret['pos'][1]]['zone'] = None
		return _ret
	
	def get_all_zones_of_type(self,type):
		_ret = []
		
		for y in xrange(self.size[1]/self.zone_size):
			for x in xrange(self.size[0]/self.zone_size):
				if self.zones[x][y]['zone']==type:
					_ret.append({'pos':(x,y),'orientation':self.zones[x][y]['orientation']})
		
		return _ret
	
	def out(self):
		for y in xrange(self.size[1]/self.zone_size):
			for x in xrange(self.size[0]/self.zone_size):
				if self.zones[x][y]['zone']: print self.zones[x][y]['zone'][1],
				else: print '.',
			print