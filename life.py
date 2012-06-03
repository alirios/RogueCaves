import pathfinding, functions, draw, var
import logging, random, copy

class life:
	def __init__(self,player=False):
		self.player = player
		
		if self.player:
			self.icon = {'icon':'@','color':['white',None]}
		
		self.id = functions.get_id()
		self.name = 'Default'
		self.hp = 10
		self.hp_max = 10
		self.speed = 0
		self.speed_max = 0
		self.pos = [0,0]
		self.last_pos = [0,0]
		self.z = 0
		self.xp = 0
		self.skill_level = 1
		self.seen = []
		self.path = None
		self.path_type = None
		self.path_dest = None
		self.mine_dest = None
		self.alignment = 0
		self.god = None
		
		self.atk = 1
		self.defe = 1
		
		self.weapon = None
		self.owned_land = []
		
		self.thirst = 0
		self.thirst_timer_max = 100
		self.thirst_timer = self.thirst_timer_max
		self.thirsty_at = 50
		self.hunger = 0
		self.hunger_timer_max = 75
		self.hunger_timer = self.hunger_timer_max
		self.hungry_at = 75
		self.fatigue = 0
		self.fatigue_timer_max = 100
		self.fatigue_timer = self.fatigue_timer_max
		self.fatigued_at = 15
		self.items = []
		self.skills = []
		
		var.life.append(self)
	
	def save(self):
		_keys = {}
		_keys['id'] = self.id
		_keys['name'] = self.name
		_keys['player'] = self.player
		_keys['icon'] = self.icon
		_keys['hp'] = self.hp
		_keys['hp_max'] = self.hp_max
		_keys['speed'] = self.speed
		_keys['speed_max'] = self.speed_max
		_keys['pos'] = self.pos
		_keys['last_pos'] = self.last_pos
		_keys['z'] = self.z
		_keys['xp'] = self.xp
		_keys['skill_level'] = self.skill_level
		_keys['race'] = self.race
		_keys['faction'] = self.faction
		_keys['task'] = self.task
		_keys['events'] = self.events
		_keys['claims'] = self.claims
		
		_keys['seen'] = []
		for seen in self.seen:
			_s = seen.copy()
			_s['who'] = _s['who'].id
			_keys['seen'].append(_s)
		
		_keys['path'] = self.path
		_keys['path_type'] = self.path_type
		_keys['path_dest'] = self.path_dest
		_keys['mine_dest'] = self.mine_dest
		_keys['alignment'] = self.alignment
		##TODO: Save god
		_keys['atk'] = self.atk
		_keys['defe'] = self.defe
		##TODO: Save weapon
		_keys['task_delay'] = self.task_delay
		_keys['thirst'] = self.thirst
		_keys['thirst_timer'] = self.thirst_timer
		_keys['thirst_timer_max'] = self.thirst_timer_max
		_keys['thirsty_at'] = self.thirsty_at
		_keys['hunger'] = self.hunger
		_keys['hunger_timer'] = self.hunger_timer
		_keys['hunger_timer_max'] = self.hunger_timer_max
		_keys['hungry_at'] = self.hungry_at
		_keys['fatigue'] = self.fatigue
		_keys['fatigue_timer'] = self.fatigue_timer
		_keys['fatigue_timer_max'] = self.fatigue_timer_max
		_keys['fatigued_at'] = self.fatigued_at
		_keys['in_danger'] = self.in_danger
		
		_items = copy.deepcopy(self.items)
		for item in _items:
			#_keys['items'] = self.items
			if item.has_key('planted_by'):
				item['planted_by'] = item['planted_by'].id
		
		_keys['items'] = _items
		_keys['skills'] = self.skills
		
		return _keys
	
	def load(self,keys):
		self.id = keys['id']
		self.name = keys['name']
		self.player = keys['player']
		
		if self.player:
			var.player = self
		
		self.icon = keys['icon']
		self.icon['icon'] = str(self.icon['icon'])
		self.hp = keys['hp']
		self.hp_max = keys['hp_max']
		self.speed = keys['speed']
		self.speed_max = keys['speed_max']
		self.pos = keys['pos']
		self.last_pos = keys['last_pos']
		self.z = keys['z']
		
		self.level = var.world.get_level(self.z)
		
		self.xp = keys['xp']
		self.skill_level = keys['skill_level']
		self.race = keys['race']
		self.faction = keys['faction']
		self.task = keys['task']
		self.events = keys['events']
		self.claims = keys['claims']
		self.seen = keys['seen']
		self.path = keys['path']
		self.path_type = keys['path_type']
		self.path_dest = keys['path_dest']
		self.mine_dest = keys['mine_dest']
		self.alignment = keys['alignment']
		##TODO: Save god
		self.atk = keys['atk']
		self.defe = keys['defe']
		##TODO: Save weapon
		self.task_delay = keys['task_delay']
		self.thirst = keys['thirst']
		self.thirst_timer = keys['thirst_timer']
		self.thirst_timer_max = keys['thirst_timer_max']
		self.thirsty_at = keys['thirsty_at']
		self.hunger = keys['hunger']
		self.hunger_timer = keys['hunger_timer']
		self.hunger_timer_max = keys['hunger_timer_max']
		self.hungry_at = keys['hungry_at']
		self.in_danger = keys['in_danger']
		self.items = keys['items']
		self.skills = keys['skills']
	
	def finalize(self):
		for seen in self.seen:
			seen['who'] = functions.get_alife_by_id(seen['who'])
	
	def add_item(self,item):
		"""Helper function. Originally copied the item, added it to the items
		array, and returned itself. No longer copies."""
		#TODO: Should we copy the item?
		#_i = item.copy()
		item['owner_id'] = self.id
		item['pos'] = tuple(self.pos)
		self.items.append(item)
		
		return item
	
	def add_item_raw(self,item):
		"""Returns a raw (new) copy of an item from the global items array
		and adds it to the items array."""
		_i = var.items[str(item)].copy()
		_i['pos'] = tuple(self.pos)
		_i['owner_id'] = self.id
		self.items.append(_i)
		
		return _i
	
	def buy_item(self,item):
		"""Removes item from menu and adds it to the items array."""
		functions.remove_menu_item(item)
		self.level.remove_item_at(item['item'],item['item']['pos'])
		self.add_item(item['item'])

	def buy_item_from_shop_alife(self,item,where):
		"""Helper function for ALife. Buy 'item' from 'where'"""
		##TODO: We aren't adding the original object to the buyer's item array

		for _item in self.level.get_all_items_in_building(where):
			if _item['tile'] == item:
				self.level.remove_item_from_building(_item,where)
				_i = self.add_item_raw(item)
				logging.debug('[ALife.%s] Bought %s from %s' %
					(self.name,_i['name'],where))
				return True
		
		return False
	
	def sell_item(self,item,**kargv):
		"""Removes item from inventory and adds it to the items array."""
		functions.remove_menu_item(item)
		item['item']['traded'] = True
		
		for _item in self.items:
			if _item['name'] == item['item']['name']:
				self.items.remove(_item)
				break
		
		kargv['args']['sell_to'].add_item(item['item'])
	
	def sell_item_alife(self,item,who):
		"""Helper function for ALife. Sells 'item' to 'who'"""
		self.items.remove(item)
		item['traded'] = True
		
		for price in range(item['price']):
			self.add_item_raw(20)
		
		who.add_item(item)
		
		logging.debug('[ALife.%s] Sold %s to %s' %
			(self.name,item['name'],who.name))
	
	def equip_item(self,item):
		"""Helper function. Equips item 'item'"""
		if item.has_key('item'): item=item['item']
		
		if item['type'] == 'weapon':
			if self.weapon==item:
				functions.log('You\'re already holding the %s!' % (self.get_weapon_name()))
				return
			
			self.weapon = item
			if self.player: functions.log('You equip the %s.' % (self.get_weapon_name()))
			return
	
	def place_item(self,item,pos):
		if self.player: _pos = (self.pos[0]+pos[0],self.pos[1]+pos[1])
		else: _pos = pos
		if 0>_pos[0] or _pos[0]>=self.level.size[0]: return
		if 0>_pos[1] or _pos[1]>=self.level.size[1]: return
		if len(self.level.items[_pos[0]][_pos[1]]): return
		
		_items = self.get_all_items_of_id(item)
		
		if len(_items): _item=_items[0]
		else: return False
		
		if _item['type'] == 'seed':
			_item['planted_by'] = self
			_item['pos'] = _pos
			self.level.items[_pos[0]][_pos[1]].append(_item)
			self.items.remove(_item)
	
	def flag_item(self,item,flag):
		item[flag] = True
		logging.debug('[ALife.%s] Flagged %s at %s with \'%s\'' %
			(self.name,item['name'],item['pos'],flag))
		
		return True
	
	def put_item_of_type(self,type,pos):
		"""Dumps a single item of 'type' in a container at 'pos'"""
		##TODO: Could probably merge this with the below function
		##TODO: Would calling self.level.items[pos[0]][pos[1]] be easier/safer?
		for _item in self.level.get_all_items_of_type('storage'):
			_found = False
			if tuple(_item['pos']) == tuple(pos):
				_found = True
				for item in self.items:
					if item['type'] == type:
						self.items.remove(item)
						item['pos'] = pos
						_item['items'].append(item)
						logging.debug('[ALife.%s] Put %s in chest at %s' %
							(self.name,item['name'],pos))
						break
				break
	
	def put_all_items_of_type(self,type,pos):
		"""Dumps items of 'type' into a container at 'pos'"""
		#TODO: Would calling self.level.items[pos[0]][pos[1]] be easier/safer?
		for _item in self.level.get_all_items_of_type('storage'):
			_found = False
			if tuple(_item['pos']) == tuple(pos):
				_found = True
				for item in self.items:
					if item['type'] == type:
						self.items.remove(item)
						item['pos'] = pos
						_item['items'].append(item)
				
				break
	
	def put_all_items_tagged(self,tag,pos):
		"""Dumps items with flag 'tag' into a container located at 'pos'"""
		#TODO: Would calling self.level.items[pos[0]][pos[1]] be easier/safer?
		for _item in self.level.get_all_items_of_type('storage'):
			_found = False
			if tuple(_item['pos']) == tuple(pos):
				_found = True
				for item in self.items:
					if item.has_key(tag) and item[tag]:
						self.items.remove(item)
						_item['items'].append(item)
				
				break
	
	def get_item_name(self,name):
		"""Helper function. Returns item with name 'name'"""
		for item in self.items:
			if item['name'] == name:
				return item
		
		return False
	
	def get_all_items_of_id(self,id):
		"""Returns items of id 'id'"""
		_ret = []
		
		for item in self.items:
			if item['tile'] == id:
				_ret.append(item)
		
		return _ret
	
	def get_all_items_of_type(self,type):
		"""Returns items of type 'type'"""
		_ret = []
		if isinstance(type,list): _list = True
		else: _list = False
		
		for item in self.items:
			if _list:
				if item['type'] in type:
					_ret.append(item)
			else:
				if item['type'] == type:
					_ret.append(item)
		
		return _ret
	
	def get_all_items_tagged(self,tag):
		"""Returns items with flag 'tag'."""
		_ret = []
		
		for item in self.items:
			if item.has_key(tag) and item[tag]:
				_ret.append(item)
		
		return _ret
	
	def get_all_cookable_items(self,where):
		_ret = []
		_food = self.level.get_all_items_in_building_of_type(where,'food')
		_food.extend(self.get_all_items_of_type('food'))
		
		_ret.extend(_food)
		
		return _ret
	
	def get_all_growing_crops(self):
		"""Returns all items still being grown by this ALife."""
		_ret = []
		
		for crop in self.level.get_all_items_tagged('planted_by',ignore_storage=True):
			if crop['type']=='seed' and crop['planted_by']==self:
				_ret.append(crop)
		
		return _ret
	
	def get_all_grown_crops(self):
		"""Returns all items grown by this ALife that have yet to been picked/traded."""
		_ret = []
		
		for crop in self.level.get_all_items_tagged('planted_by',ignore_storage=True):
			if crop['type']=='food' and crop['planted_by']==self and not crop.has_key('traded'):
				_ret.append(crop)
		
		return _ret
	
	def get_item_id(self,id):
		"""Returns item of id 'id'"""
		for item in self.items:
			if item['tile'] == id:
				return item
		
		return False
	
	def get_money(self):
		"""Returns amount of money the ALife has."""
		_ret = 0
		
		for ore in self.get_all_items_of_type('ore'):
			_ret+=ore['price']
		
		return _ret
	
	def get_owned_land(self,label):
		for entry in self.owned_land:
			if entry['label'] == label:
				return entry
		
		return False
	
	def get_open_stoves(self,where):
		"""Returns all stoves in 'where' either done cooking or empty"""
		_ret = []
		_stoves = self.level.get_all_items_in_building_of_type(where,'stove')
		
		for stove in _stoves:
			if stove['cooking'] and stove['cooking']['type'] == 'cooked food':
				_ret.append(stove)
			elif not stove['cooking']: _ret.append(stove)
		
		return _ret				
	
	def claim_real_estate(self,pos,size,label):
		"""Helper function. Registers land at 'pos' with 'size' as 'label'"""
		self.owned_land.append({'where':pos,'size':size,'label':label})
		self.level.claim_real_estate((pos[0],pos[1]),(size[0],size[1]))
		
		logging.debug('[ALife.%s.Land] Claimed %s,%s with size %s,%s as %s'
			% (self.name,pos[0],pos[1],size[0],size[1],label))
	
	def claim_building(self,where,label):
		self.claims.append({'where':where,'label':label})
		self.level.get_room(where)['owner'] = self
		
		logging.debug('[ALife.%s.Land] Claimed %s as %s'
			% (self.name,where,label))
	
	def get_claimed(self,label):
		for claim in self.claims:
			if claim['label'] == label:
				return claim['where']
		
		return False
	
	def say(self,what):
		"""Sends a string prefixed with the ALife's name to the log."""
		if self.z == var.player.z and self.can_see(var.player.pos):
			functions.log('%s: %s' % (self.name,what))
	
	def attack(self,who):
		"""Performs attack on object 'who'"""
		if who.race in ['zombie']:
			if self.player: functions.log('You swing at the %s!' % (who.race))
			elif who.player: functions.log('The %s swings at you!' % (who.race))
		elif who.race in ['human']:
			if self.player: functions.log('You swing at %s!' % (who.name))
			elif who.player: functions.log('%s swings at you!' % (self.name))
		else:
			if self.player: functions.log('You swing at %s!' % (who.name))
			elif who.player: functions.log('The %s swings at you!' % (self.race))
		
		self.hunger_timer -= 5
		self.xp += 1
		
		if self.weapon:
			_dam = random.randint(self.atk,self.weapon['damage']+self.atk)
			if _dam >= self.weapon['damage']:
				if self.player:
					functions.log('Your %s hits for maximum damage!' % self.weapon['name'])
				elif who.player:
					functions.log('%s hits you with a %s for maximum damage!' % 
						(self.name,self.get_weapon_name()))
				
				if self.weapon['sharp']:
					self.weapon['status'] = 'the blood of %s the %s' % (who.name,who.race)
					
					_pos = random.choice([(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),\
						(-1,1),(0,1),(1,1)])
					_x = who.pos[0]+_pos[0]
					_y = who.pos[1]+_pos[1]
					
					if not 0>_x and not _x>=self.level.size[0] and\
						not 0>_y and not _y>=self.level.size[1]:
						self.level.tmap[_x][_y] = random.randint(150,255)
						
			
			who.hp -= _dam
		else:
			who.hp -= self.atk
		
		if who.hp<=0:
			if who.race in ['zombie']:
				if self.player: functions.log('You slay the %s!' % (who.race))
				elif who.player: functions.log('The %s slays you!' % (who.race))
			else:
				if self.player: functions.log('You slay %s the %s!' % (who.name,who.race))
				elif who.player: functions.log('The %s slays you!' % (self.race))
			
			self.xp += who.xp
			
			for item in who.items:
				if self.player: functions.log('Found %s!' % item['name'])
				self.add_item(item)
				
				if not self.weapon and item['type']=='weapon':
					self.equip_item(item)
			
			if self.god:
				self.god.on_kill(self,who)
			
			who.kill()
		
		if self.xp>=self.skill_level*var.skill_mod:
			self.xp-=self.skill_level*var.skill_mod
			self.skill_level+=1
			self.hp = self.hp_max
	
	def has_seen(self,who):
		"""Helper function. Searches 'seen' for object 'who'"""
		for seen in self.seen:
			if seen['who'] == who:
				return seen
		
		return False
	
	def in_building(self,pos=None,name=None):
		"""Returns the building the ALife is currently in
		
		if 'name', check to see if the current building is 'name'
		if 'pos', check to see if 'pos' is in 'name'
		"""
		
		if not pos: pos = tuple(self.pos)
		
		for room in self.level.rooms:
			if pos in room['walking_space']:
				if name:
					if room['name'] == name: return room
				else:
					return room
		
		return False
	
	def can_see(self,pos):
		"""Performs a series of checks to determine if the ALife can see 'pos'"""
		_seen = True
		_l = draw.draw_diag_line(self.pos,pos)
		
		_blocking = []
		#for life in var.life:
		#	if not life.z == self.z or self == life: continue
		#	_blocking.append((life.pos[0],life.pos[1]))
		
		if tuple(pos) in _blocking:
			_blocking.remove(tuple(pos))

		for _pos in _l:
			if self.level.map[_pos[0]][_pos[1]] in var.solid:
				_seen = False
				break
			
			if not _l.index(_pos)==len(_l)-1 and self.level.has_solid_item_at(_pos):
				_seen = False
				break
			
			if _pos in _blocking:
				_seen = False
				break
		
		return _seen
	
	def can_see_ext(self,pos):
		"""Legacy function. Uses A* to determine if the ALife can see 'pos'"""
		#TODO: Deprecated. Marked for removal in 2012A."""
		_seen = True
		_path = self.path = pathfinding.astar(start=self.pos,end=pos,\
			omap=self.level.map,size=self.level.size).path
		
		if _path:
			return True
		else:
			return False
	
	def can_traverse(self,pos):
		"""Checks to see if the ALife can travel to 'pos'"""
		_seen = True
		_l = draw.draw_diag_line(self.pos,pos)
		
		_blocking = []
		for life in var.life:
			if not life.z == self.z or self == life: continue
			_blocking.append((life.pos[0],life.pos[1]))
		
		if tuple(pos) in _blocking:
			_blocking.remove(tuple(pos))
		
		for _pos in _l:
			if self.level.map[_pos[0]][_pos[1]] in var.blocking:
				_seen = False
				break
			
			if not _l.index(_pos)==len(_l)-1 and self.level.has_solid_item_at(_pos):
				_seen = False
				break
			
			if _pos in _blocking:
				_seen = False
				break
		
		return _seen
	
	def place_tile(self,pos,tile):
		"""Places a tile of 'tile' at position 'pos'"""
		_pos = (self.pos[0]+pos[0],self.pos[1]+pos[1])
		if not self.level.map[_pos[0]][_pos[1]] in var.solid:
			self.level.map[_pos[0]][_pos[1]] = tile
			if _pos in self.level.walls:
				self.level.walls.remove(_pos)
			
			if not _pos in self.level.walking_space:
				self.level.walking_space.append(_pos)
	
	def tick(self):
		"""Performs a single tick, incrementing various counters."""
		self.hunger_timer -= 1
		self.thirst_timer -= 1
		self.fatigue_timer -= 1
		
		if self.hunger_timer <= 0:
			self.hunger_timer = self.hunger_timer_max
			self.hunger+=1
		
		if self.thirst_timer <= 0:
			self.thirst_timer = self.thirst_timer_max
			self.thirst+=1
		
		if self.fatigue_timer <= 0:
			self.fatigue_timer = self.fatigue_timer_max
			self.fatigue+=1
		
		if self.pos == self.last_pos or self.z<1: return
		
		for room in self.level.rooms:
			if room['owner'] == self: continue
			if not room['owner'] or \
				not tuple(room['owner'].pos) in room['walking_space']: continue
			if tuple(self.pos) in room['walking_space']:
				if not tuple(self.last_pos) in room['walking_space']:
					room['owner'].say('Welcome to \'%s\'!' % room['name'])
			elif tuple(self.last_pos) in room['walking_space']:
				if not tuple(self.pos) in room['walking_space']:
					room['owner'].say('Thanks for stopping by!')
	
	def think(self):
		"""Tracks whether ALife on the current level have been seen for the
		first time, lost, or moved in the last tick."""
		for life in var.life:
			if life == self or not self.z == life.z: continue
			
			_temp = self.has_seen(life)
			
			if not self.z == life.z and _temp:
				if _temp and _temp['in_los']:
					_temp['in_los'] = False
			
			_l = draw.draw_diag_line(self.pos,life.pos)
			
			_seen = self.can_see(life.pos)#True
			
			if _seen:
				_seen = self.can_traverse(life.pos)
			
			if _seen and not life.z == self.z: _seen = False
			
			if _seen:
				if _temp:
					_temp['los'] = _l[:]
					_temp['in_los'] = True
					_temp['last_seen'] = life.pos[:]
				else:
					self.seen.append({'who':life,'los':_l,'in_los':True,'last_seen':life.pos[:]})
			else:
				if _temp and _temp['in_los']:
					#print _temp['who'].name,'lost'
					_temp['in_los'] = False
		
		return self.pos
	
	def walk(self,dir):
		"""Movement rules for all ALife. Tracks collisions along with the
		pickup of items like gold and ore."""
		self.last_pos = self.pos[:]
		_pos = self.pos[:]
		
		if self.speed>0:
			self.speed -= 1
			return
		else:
			self.speed = self.speed_max
		
		if self.player:
			if dir == 'up' and self.pos[1]-1>=0:
				_pos[1]-=1
			elif dir == 'down' and self.pos[1]+1<var.world.size[1]:
				_pos[1]+=1
			elif dir == 'left' and self.pos[0]-1>=0:
				_pos[0]-=1
			elif dir == 'right' and self.pos[0]+1<var.world.size[0]:
				_pos[0]+=1
		else:
			_pos = self.think()
			
			if (self.pos[0],self.pos[1]) in self.level.exits\
				and self.path_dest in self.level.exits:
				self.enter()
				self.path_dest = None
			elif (self.pos[0],self.pos[1]) in self.level.entrances\
				and self.path_dest in self.level.entrances:
				self.enter()
				self.path_dest = None
		
		_tile = self.level.map[_pos[0]][_pos[1]]
		if _tile in var.blocking or _tile in var.solid:			
			self.pos = self.pos[:]
			return
		
		_items = self.level.items[_pos[0]][_pos[1]]
		if _items:
			_i = 0
			for _tile in _items:
				if _tile['tile'] == 11:
					if _tile['life']<=0:
						_chance = random.randint(0,100)
						if _chance <= 55:
							self.level.map[_pos[0]][_pos[1]] = 1
						elif 55<_chance<=75:
							self.level.add_item(20,_pos)
						elif 75<_chance<=95:
							self.level.add_item(14,_pos)
						else:
							self.level.add_item(13,_pos)
						
						self.level.items[_pos[0]][_pos[1]].pop(_i)
					else:
						if self.weapon:
							_tile['life']-=self.weapon['damage']
						else:
							_tile['life']-=1
					self.pos = self.pos[:]
					return
				elif _tile['tile'] in [13,14,20]:
					_item = self.level.items[_pos[0]][_pos[1]].pop(_i)
					self.add_item(_item)
					if self.player:
						functions.log('You picked up +1 %s.' % _tile['name'])
				elif _tile['type'] == 'food' and _tile.has_key('planted_by'):
					if _tile['planted_by'] == self:
						_item = self.level.items[_pos[0]][_pos[1]].pop(_i)
						self.add_item(_item)
						if self.player:
							functions.log('You picked up some %s.' % _tile['name'])
				
				_i+=1
		
		_found = False
		for life in var.life:
			if life == self or not self.z == life.z: continue
			
			if self.faction == life.faction:
				pass
				##TODO: Should I do this?
				#if life.pos == _pos:
				#	if self.player:
				#		functions.log('%s is in the way.' % life.name)
				#	_found = True
			elif life.pos == _pos:
				self.attack(life)
				_found = True
		
		if not _found:
			if not self.pos == _pos:
				self.hunger_timer -= 1
			
			self.pos = _pos[:]
		
		if self.mine_dest:
			if (self.pos[0],self.pos[1]) == (self.mine_dest[0],self.mine_dest[1]):
				self.mine_dest = None
		
		if self.path_dest:
			if (self.pos[0],self.pos[1]) == (self.path_dest[0],self.path_dest[1]):
				self.path_dest = None

	def find_path(self,pos):
		if self.can_see(pos) and self.can_traverse(pos):
			if self.path_dest and (pos[0],pos[1]) == tuple(self.path_dest):
				self.path_dest = None
				return
			self.path = draw.draw_diag_line(self.pos,pos)
			self.path_dest = (pos[0],pos[1])
			self.path_type = 'Line'
		else:
			if self.path_dest and (pos[0],pos[1]) == tuple(self.path_dest):
				#self.path_dest = None
				return
			
			self.path_type = 'A*'
			
			_cache_path = var.cache.get_path_from_cache(self.pos,pos,self.z)
			if _cache_path:
				self.path = _cache_path
				self.path_dest = (pos[0],pos[1])
				return
			
			_blocking = []
			
			for item in self.level.get_all_solid_items():
				_blocking.append((item['pos'][0],item['pos'][1]))
			
			#We have to TRUST that the ALife knows what it's doing here...
			#basically we're assuming that even though the destination
			#is in the _blocking array, we can still move there and mine it			
			if tuple(pos) in _blocking:
				_blocking.remove(tuple(pos))
			
			#for life in var.life:
			#	if not life.z == self.z or self == life: continue
			#	
			#	#_blocking.append((life.pos[0],life.pos[1]))
			
			if tuple(pos) in _blocking:
				_blocking.remove(tuple(pos))
			
			self.path = pathfinding.astar(start=self.pos,end=pos,\
				omap=self.level.map,size=self.level.size,blocking=_blocking).path
			
			if not self.path:
				self.path_dest = None
			else:
				self.path_dest = (pos[0],pos[1])
				var.cache.add_path_to_cache(self.pos,pos,self.path,self.z)
	
	def follow(self,who):
		if self.pos == who.pos or (self.z == who.z and functions.distance(self.pos,who.pos)<=3):
			return
		
		if not self.z == who.z:
			#TODO: Pathing for traversing levels
			if self.z<who.z:
				self.find_path(self.level.entrances[0])
				print 'Going up!'
			else:
				self.find_path(self.level.exits[0])
				print 'Going down!',self.pos,self.level.exits[0]
			return
		
		self.find_path(who.pos)
	
	def go_to(self,pos,z=None):
		if z == None:
			z = self.z
		
		if tuple(self.pos) == pos and z == self.z:
			return True
		
		if not self.z == z:
			if self.z<z:
				self.find_path(self.level.entrances[0])
			else:
				self.find_path(self.level.exits[0])
			return False
		
		self.find_path(pos)
		return False
	
	def go_to_and_do(self,pos,callback,**kargv):
		"""Go to location and call function 'callback' with argument 'kargv'"""
		_there = self.go_to(pos)
		
		if _there: return callback(kargv['first'],kargv['second'])
		
		return True
	
	def go_to_building_and_buy(self,item,building):
		"""Go to 'building' and buy 'item'"""
		_building_owner = self.level.get_room(building)['owner']
		if not self.in_building(pos=self.path_dest,name=building):
			_pos = random.choice(self.level.get_room(building)['walking_space'])
		else:
			if self.in_building(name=building):
				_pos = tuple(self.pos)
			else:
				_pos = self.path_dest
		
		return self.go_to_and_do(_pos,\
			self.buy_item_from_shop_alife,\
			first=item,\
			second=building)
	
	def go_to_building_and_sell(self,item,building):
		"""Go to 'building' and sell 'item'"""
		_building_owner = self.level.get_room(building)['owner']
		if not self.in_building(pos=self.path_dest,name=building):
			_pos = random.choice(self.level.get_room(building)['walking_space'])
		else:
			if self.in_building(name=building):
				_pos = tuple(self.pos)
			else:
				_pos = self.path_dest
		
		return self.go_to_and_do(_pos,\
			self.sell_item_alife,\
			first=item,\
			second=_building_owner)
	
	def pick_up_item_at(self,pos,want):
		"""Go to 'pos' and pick up item type 'want'"""
		if not want: want=item['type']
		
		if tuple(self.pos) == pos:
			for item in self.level.items[pos[0]][pos[1]]:
				if item['type'] == want:
					self.level.items[pos[0]][pos[1]].remove(item)
					self.add_item(item)
					break
				elif item['type'] == 'storage':
					_found = False
					for _item in item['items']:
						if _item['type'] == want:
							item['items'].remove(_item)
							self.add_item(_item)
							logging.debug('[ALife.%s] %s removed from storage at %s' %
								(self.name,_item['type'],pos))
							_found = True
							break
					
					if _found: break
		
		else:
			self.go_to(pos)
	
	def guard_building(self,where):
		_room = var.world.get_level(1).get_room(where)
		
		if not _room: return False
		
		if self.path_dest in _room['walking_space']:
			pass
		else:
			self.go_to(random.choice(_room['walking_space']))
	
	def run_shop(self,where):
		if self.get_claimed('work'):
			_storage = self.level.get_all_items_in_building_of_type('storage','storage')
			_dump = self.get_all_items_tagged('traded')
			
			if _dump and _storage:
				self.go_to_and_do(_storage[0]['pos'],\
					self.put_all_items_tagged,\
					first='traded',
					second=_storage[0]['pos'])
				#self.put_all_items_of_tag('traded')
			else:
				if not self.task_delay:
					self.guard_building(where)
					self.task_delay = self.task['delay']
				elif self.task_delay>0:
					self.task_delay-=1
		else:
			_room = var.world.get_level(1).get_room(where)
			self.guard_building(where)
			#Ownership
			if tuple(self.pos) in _room['walking_space'] and not _room['owner']:
				self.claim_building(where,'work')
				functions.log('%s has claimed \'%s\'!' % (self.name,where))
	
	def farm(self,where):
		"""Instructs the ALife to farm a plot of land at 'where',
		'where' is expected to be (x,y,width,height)"""
		##TODO: Should we check for (x1,y1,x2,y2)?
		#Each iteration we will scan for what tiles in 'where' are already planted
		#Until the array returned is empty, we will travel to the nearest tile and
		#plant there.
		_land = self.get_owned_land('farm')
		
		if _land:#self.task['where']:
			where = (_land['where'][0],_land['where'][1],_land['size'][0],_land['size'][1])
		else:
			_res = self.level.get_real_estate((3,3))
			
			_lowest = {'entry':None,'dist':100}
			for entry in _res:
				_pos = self.level.get_room(self.get_claimed('home'))['walking_space'][0]
				_dist = functions.distance(tuple(_pos),entry)
				if _dist<_lowest['dist']:
					_lowest['dist'] = _dist
					_lowest['entry'] = entry
			
			where = (_lowest['entry'][0],_lowest['entry'][1],3,3)
			self.task['where'] = where
			
			self.claim_real_estate((where[0],where[1]),(where[2],where[3]),'farm')
			
		_open = []
		
		for x in range(where[2]):
			for y in range(where[3]):
				_pos = (where[0]+x,where[1]+y)
				
				if not len(self.level.items[_pos[0]][_pos[1]]):
					_open.append(_pos)
		
		if not self.task_delay:
			self.task_delay = self.task['delay']
			if not _open or not len(self.get_all_items_of_type('seed')):
				self.task['delay'] = 5
				_crops_to_sell = self.get_all_items_tagged('planted_by')
				_get = self.get_all_grown_crops()
				_sell = []
				
				for crop in _crops_to_sell:
					if crop['type']=='food' and crop['planted_by']==self and not crop.has_key('cook'):
						_sell.append(crop)
				
				if _get:
					self.pick_up_item_at(_get[0]['pos'],_get[0]['type'])
				elif _sell:
					##TODO: _sell is a bit misleading
					#_sell actually refers to items that are harvested.
					#they can be sold, but first the ALife must consider
					#whether it needs them or not to feed themselves/others
					#We do that check now.
					_food = self.get_all_cookable_items(self.get_claimed('home'))
					
					#if len(_food)>=2:
					#	self.go_to_building_and_sell(_sell[0],'storage')
					#else:
					_home = self.get_claimed('home')
					_storage = self.level.get_all_items_in_building_of_type(_home,'storage')
					
					if len(_storage):				
						self.go_to_and_do(_storage[0]['pos'],\
							self.put_item_of_type,\
							first=_sell[0]['type'],\
							second=_storage[0]['pos'])
						
				else:
					if self.get_money() and\
						len(self.level.get_all_items_in_building_of_type('storage','seed')):
						self.go_to_building_and_buy(21,'storage')
			else:
				self.go_to_and_do(_open[0],self.place_item,first=21,second=_open[0])
				return True
		elif self.task_delay>0:
			self.task_delay-=1
	
	def cook(self):
		_stoves = self.level.get_all_items_in_building_of_type(self.get_claimed('home'),'stove')
		_has_food = self.get_all_items_of_type('food')
		
		if not _stoves: return False
		
		_stove = None
		for stove in _stoves:
			if stove['cooking']:
				if stove['cooking']['type'] == 'cooked food':
					if self.go_to(stove['pos']):
						self.add_item(stove['cooking'])
						logging.debug('[ALife.%s] Removed %s from stove at %s' %
							(self.name,stove['cooking']['name'],stove['pos']))
						stove['cooking'] = None
						
						return True
					return False
				else:
					continue
			_stove = stove
			break
		
		if not _stove: return False
		
		if len(_has_food):
			_food = _has_food[0]
		else:
			_get_food = self.level.get_all_items_in_building_of_type(self.get_claimed('home'),'food')
			
			if not _get_food: return False
			else: _get_food = _get_food[0]
			
			if self.go_to_and_do(_get_food['pos'],\
					self.flag_item,
					first=_get_food,
					second='cook'):
			
				self.pick_up_item_at(_get_food['pos'],'food')
				return False
			else:
				return False
		
		if self.go_to(_stove['pos']):
			self.items.remove(_food)
			_stove['cooking'] = _food
			logging.debug('[ALife.%s] Put %s in stove at %s' %
				(self.name,_food['name'],_stove['pos']))
			return True		
	
	def rest(self):
		_beds = self.level.get_all_items_in_building_of_type(self.get_claimed('home'),'bed')
		
		print _beds
	
	def enter(self):
		if self.level.map[self.pos[0]][self.pos[1]] == 3:
			self.z += 1
		elif self.level.map[self.pos[0]][self.pos[1]] == 4:
			self.z -= 1
		
		self.level = var.world.get_level(self.z)
		self.start_pos = None
	
	def teleport(self,z):
		self.z = z
		self.level = var.world.get_level(self.z)
		self.pos = list(self.level.walking_space[0])
	
	def kill(self):
		for life in var.life:
			_temp = life.has_seen(self)
			
			if _temp:
				life.seen.remove(_temp)
				
				if life.race == 'human':
					if life.lowest['who'] == self:
						life.lowest['who'] = None
						life.lowest['score'] = 0
					
					if life.highest['who'] == self:
						life.highest['who'] = None
						life.highest['score'] = 0
		
		for r in range(10+random.randint(0,3)):
			_x = self.pos[0]+random.randint(-2,2)#+pos[0]
			_y = self.pos[1]+random.randint(-2,2)#+pos[1]
			
			if 0>_x or _x>=self.level.size[0]: continue
			if 0>_y or _y>=self.level.size[1]: continue
			
			self.level.tmap[_x][_y] = 255
		
		self.level.tmap[self.pos[0]][self.pos[1]] = 255
		
		logging.debug('%s died!' % self.name)
		var.life.remove(self)

class human(life):
	def __init__(self,player=False,male=True):
		self.icon = {'icon':'H','color':['white',None]}
		
		life.__init__(self,player=player)
		
		self.race = 'human'
		if male:
			self.gender = 'male'
			self.name = functions.get_name_by_gender('male')
			self.attracted_to = ['looks']
		else:
			self.gender = 'female'
			self.name = functions.get_name_by_gender('female')
			self.attracted_to = ['power']
		
		self.hp = 20
		self.hp_max = 20
		
		self.thirsty_at = -1
		self.married = None
		self.worth = None
		self.mode = {'task':None,'who':None}
		self.task = None
		self.task_delay = 0
		self.in_danger = False
		self.faction = 'good'
		self.trading = False
		self.claims = []
		
		self.lowest = {'who':None,'score':0}
		self.highest = {'who':None,'score':0}
		
		self.events = []
	
	def on_enemy_spotted(self):
		pass
	
	def is_in_danger(self,who):
		self.in_danger = True
		if self.player:
			if who.weapon:
				functions.log('%s the %s charges towards you with a %s!' % \
					(who.name,who.race,who.get_weapon_name()))
			else:
				functions.log('%s the %s runs towards you!' % \
					(who.name,who.race))
	
	def get_weapon_name(self):
		_name = ''
		
		if self.weapon['rank']>1:
			if self.weapon['rank']==2:
				_name+='shining '
		
		_name+='%s' % self.weapon['name']
		
		if self.weapon['status']:
			_name+=' covered in %s' % self.weapon['status']
			
		return _name
	
	def add_event(self,what,score,who=None,where=None,delay=0):
		for event in self.events:
			if event['what'] == what and event['who'] == who:
				#logging.debug('[ALife.%s.Event] Updated %s: %s -> %s' %
				#	(self.name,event['what'],event['score'],score))
				event['score'] = score
				return False
		
		logging.debug('[ALife.%s.Event] Added: %s, score %s' % (self.name,what,score))
		self.events.append({'what':what,'score':score,'who':who,'where':where,'delay':delay})
		return True
	
	def get_event(self):
		_highest = {'what':None,'score':-1}
		for event in self.events:
			if event['score']>=_highest['score']:
				_highest['what'] = event['what']
				_highest['ret'] = event
				_highest['score'] = event['score']
		
		if _highest['what']:
			return _highest['ret']
		else:
			return _highest
	
	def remove_event(self,what):
		for event in self.events:
			if event['what'] == what:
				self.events.remove(event)
				return True
		
		return False
	
	def mine(self):
		if self.mine_dest and self.path_dest == self.mine_dest: return
		
		_lowest = {'score':1000,'pos':None}
		for item in self.level.get_all_items_of_tile(11):
			if not self.can_see(item['pos']): continue
			
			_dist = functions.distance(self.pos,item['pos'])
			
			if _dist<_lowest['score']:
				_lowest['score'] = _dist
				_lowest['pos'] = item['pos']
		
		if _lowest['pos']:
			self.go_to(_lowest['pos'])
			self.mine_dest = _lowest['pos']
		else:
			_pos = var.world.get_level(self.z-1).entrances[0]
			
			self.go_to(_pos,z=self.z-1)

	def judge(self,who):
		#This is so much easier...
		_score = 0
		_score = (who.hp+who.atk+who.defe)
		
		if self.faction == who.faction:
			if not self.gender == who.gender:
				_score+=5
		
				if ['power'] in self.attracted_to:
					if who.weapon: _score += who.weapon['damage']*2
				if ['wealth'] in self.attracted_to:
					##TODO: We should probably search for "apparent" money here
					#based on the prices on the armor being worn, etc
					_score+=(who.get_money()/4)
				if ['strength'] in self.attracted_to:
					_score+=who.atk*2
				
		else:
			if who.weapon: _score+=who.weapon['damage']*2
			_score *= -1
		
		return _score
	
	def think(self):
		life.think(self)
		
		#ACT HUMANLY!
		for seen in self.seen:
			if seen['in_los']:
				_score = self.judge(seen['who'])
				
				if _score < 0 and _score <= self.lowest['score']:
					self.lowest['score'] = _score
					self.lowest['who'] = seen['who']
					self.lowest['last_seen'] = seen['last_seen'][:]
				
				if _score >= 0 and _score >= self.highest['score']:
					self.highest['score'] = _score
					self.highest['who'] = seen['who']
					self.highest['last_seen'] = seen['last_seen'][:]
			
			else:
				if self.lowest['who'] == seen['who']:
					self.lowest['last_seen'] = seen['last_seen'][:]
				
				if self.highest['who'] == seen['who']:
					self.highest['last_seen'] = seen['last_seen'][:]
		
		if self.lowest['who']:
			if self.judge(self)>=abs(self.judge(self.lowest['who'])):
				if self.add_event('attack',100,who=self.lowest['who']):
					self.on_enemy_spotted()
					if self.lowest['who'].player:
						self.lowest['who'].is_in_danger(self)
			else:
				if self.add_event('flee',100,who=self.lowest['who']):
					self.remove_event('attack')
				self.task = 'flee'
		else:
			if self.task == 'attacking':
				self.task = None
		
		if self.highest['who']:
			if not self.married:
				pass
		
		# and not self.task in ['attacking','flee']:
		#elif self.highest['who'] and self.married == self.highest['who']:
		#	#TODO: This one will happen too much...
		#	self.follow(self.highest['who'])
		#	self.task = 'following'
		#else:
		_event = self.get_event()
		
		if _event and not self.task==_event:
			self.task = _event
		
		if self.task['what'] == 'food':
			##TODO: Eventually sort this array by how good the food is
			_item = self.get_all_items_of_type(['food','cooked food'])
			
			if _item:
				self.hunger = 0
				self.hunger_timer = self.hunger_timer_max
				self.items.remove(_item[0])
				self.remove_event(self.task['what'])
				self.task = None
				self.say('That was good!')
			else:
				_items = []
				
				for claim in self.claims:
					for item in self.level.get_all_items_in_building_of_type(claim['where'],'food'):
						_items.append(item)
				
				if _items:
					_item = functions.sort_item_array_by_distance(_items,self.pos)[0]
					self.pick_up_item_at(_item['pos'],'food')
				
		elif self.task['what'] == 'mine':
			self.mine()
		elif self.task['what'] == 'deliver':
			if len(self.get_all_items_of_type('ore')):
				_pos = None
				_room = var.world.get_level(1).get_room('storage')
				_chest = None
				for pos in _room['walking_space']:
					for item in var.world.get_level(1).items[pos[0]][pos[1]]:
						if item['type']=='storage':
							for space in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
								if (pos[0]+space[0],pos[1]+space[1]) in _room['walking_space']:
									_pos = (pos[0]+space[0],pos[1]+space[1])
									_chest = item
									break
							break
				
				if tuple(self.pos) == _pos:
					self.put_all_items_of_type('ore',_chest['pos'])
					self.remove_event(self.task['what'])
					self.task = None
					self.mine_dest = None
				elif _pos:
					self.go_to(_pos,z=1)
		elif self.task['what'] == 'attack':
			if self.task['who'].hp>0:
				self.go_to(self.task['who'].pos,z=self.task['who'].z)
			else:
				if self.remove_event(self.task['what']):
					self.task = None
					self.say('Got em.')
					self.lowest = {'who':None,'score':0}
		elif self.task['what'] == 'run_shop':
			self.run_shop(self.task['where'])
		elif self.task['what'] == 'flee':
			print 'Running away'
		elif self.task['what'] == 'farm':
			self.farm(self.task['where'])
		elif self.task['what'] == 'cook':
			self.cook()
		elif self.task['what'] == 'rest':
			self.rest()
		elif self.task['what'] == 'stay_home':
			if not self.task_delay:
				self.guard_building(self.get_claimed('home'))
				self.task_delay = self.task['delay']
			elif self.task_delay>0:
				self.task_delay-=1
		elif self.task['what'] == 'trade':
			self.trade_items
		
		
		#Take care of needs here
		if self.hunger >= self.hungry_at and not self.hungry_at == -1:
			self.add_event('food',self.hunger)
			print self.hungry_at
		
		if self.thirst >= self.thirsty_at and not self.thirsty_at == -1:
			self.add_event('water',self.thirst)
		
		if 'farm' in self.skills:
			_farm_score = 0
			_cook_score = 0
			_sell_score = 0
			_farm_score-=len(self.get_all_items_of_type(['food','cooked_food'])*2)
			
			##TODO: Calculate how much food this ALife needs for himself and family
			#if len(_food)<10:
			_farm_score+=len(self.get_all_items_of_type('seed'))*15
			
			if self.get_open_stoves(self.get_claimed('home')):
				_cook_score+=len(self.get_all_cookable_items(self.get_claimed('home')))*15
			_farm_score+=len(self.get_all_grown_crops())*20
			#_farm_score+=len(self.get_all_growing_crops())*5
			
			##TODO: Find out how much money is needed to buy more seed
			_trade_score += len(self.get_all_items_of_type(['food','cooked food']))*15
			_trade_what = ['food','cooked food']
			_sell_score -= self.get_money()*2
			
			print _farm_score,_cook_score,_trade_score
			
			self.add_event('farm',_farm_score,delay=5)
			self.add_event('cook',_cook_score,delay=5)
			self.add_event('stay_home',self.fatigue,delay=15)
			self.add_event('trade',_sell,delay=5)
		
		#if self.fatigue >= self.fatigued_at and not self.fatigued_at == -1:
		#	self.add_event('rest',self.fatigue*2)
		
		#self.add_event('deliver',(len(self.get_all_items_of_type('ore'))*50))
		
		if self.path:
			if tuple(self.pos) == tuple(self.path[0]):
				self.path.pop(0)
			
			if self.path:
				_new_pos = [self.path[0][0],self.path[0][1]]
				return _new_pos
		
		return self.pos
	
	def kill(self):
		life.kill(self)
		
		if not self.player and self.task['who'].player:
			self.task['who'].in_danger = False

class crazy_miner(human):
	def __init__(self):
		human.__init__(self)
		
		self.hungry_at = -1
		self.thirsty_at = -1
		
		self.race = 'human'
		self.faction = 'evil'
	
	def on_enemy_spotted(self):
		human.on_enemy_spotted(self)
		self.say('I see yah, you crazy bastard!')

class zombie(life):
	def __init__(self,player=False):
		self.icon = {'icon':'Z','color':['lightgreen',None]}
		
		life.__init__(self,player=player)
		
		self.race = 'zombie'
		
		self.hp = 3
		self.hp_max = 3
		self.speed = 5
		self.speed_max = 5
		self.xp = 0
	
	def think(self):
		life.think(self)
		
		if not self.seen: return self.pos
		
		#Find closest
		_lowest = {'who':None,'lowest':9000,'los':None}
		for seen in self.seen:
			if seen['who'].faction == self.faction: continue
			
			if len(seen['los'])<=_lowest['lowest']:
				_lowest['who'] = seen['who']
				_lowest['lowest'] = len(seen['los'])
				_lowest['los'] = seen['los']
		
		if _lowest['who']:
			self.focus = _lowest
		else:
			return self.pos
		
		if self.focus['los']:
			self.focus['los'].pop(0)
		
		if not self.focus['los']:
			return self.pos
		
		return [self.focus['los'][0][0],self.focus['los'][0][1]]

class god:
	def __init__(self):
		self.alignment = 'neutral'
		self.name = 'Default'
		self.purpose = 'Nothing'
		self.accepts = []
		self.denies = []
		
		self.followers = []
		
		self.kills = []
	
	def get_name(self):
		return '%s, the god of %s' % (self.name,self.purpose)

	def on_kill(self,by,who):
		if by.player:
			if who.race in self.accepts:
				if by.alignment<10:
					by.alignment+=1
					
				self.kills.append({'by':by.name,'who':who.name,'accept':True})
				functions.log('%s accepts your kill.' % self.get_name())
			
			elif who.race in self.denies:
				if by.alignment>-10:
					by.alignment-=1
				
				self.kills.append({'by':by.name,'who':who.name,'accept':False})
				functions.log('%s denies your kill.' % self.get_name())
			
			if by.alignment>=1:
				functions.log('You feel that %s is happy with your actions lately.' % self.get_name())
			elif by.alignment<=-1:
				functions.log('You feel that %s is not happy with your actions lately!' % self.get_name())