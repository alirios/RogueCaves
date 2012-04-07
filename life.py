import pathfinding, functions, draw, var
import random

class life:
	def __init__(self,player=False):
		self.player = player
		
		if self.player:
			self.icon = {'icon':'@','color':['white',None]}
		
		self.name = 'Default'
		self.hp = 10
		self.hp_max = 10
		self.speed = 0
		self.speed_max = 0
		self.pos = [0,0]
		self.z = 0
		self.xp = 0
		self.skill_level = 1
		self.seen = []
		self.path = None
		self.start_pos = None
		self.path_dest = None
		self.mine_dest = None
		self.alignment = 'neutral'
		
		self.atk = 1
		self.defe = 1
		
		self.thirst = 0
		self.thirst_timer = var.thirst_timer_max
		self.hunger = 0
		self.hunger_timer = var.hunger_timer_max
		self.items = []
		self.gold = 0
		self.coal = 0
		
		var.life.append(self)
	
	def add_item(self,item):
		self.items.append({'name':var.items[str(item)],'tile':item})
	
	def get_item_name(self,name):
		for item in self.items:
			if item['name'] == name:
				return item
		
		return False
	
	def get_item_id(self,id):
		for item in self.items:
			if item['tile'] == id:
				return item
		
		return False
	
	def say(self,what):
		if self.z == var.player.z and self.can_see(var.player.pos):
			functions.log('%s: %s' % (self.name,what))
	
	def attack(self,who):
		if who.race in ['zombie']:
			if self.player: functions.log('You swing at the %s!' % (who.race))
			elif who.player: functions.log('The %s swings at you!' % (who.race))
		else:
			if self.player: functions.log('You swing at %s!' % (who.name))
			elif who.player: functions.log('The %s swings at you!' % (self.race))
			#functions.log('You swing at %s!' % (who.name))
		
		self.hunger_timer -= 5
		self.xp += 1
		who.hp -= 1
		
		if who.hp<=0:
			if who.race in ['zombie']:
				if self.player: functions.log('You slay the %s!' % (who.race))
				elif who.player: functions.log('The %s slays you!' % (who.race))
			else:
				if self.player: functions.log('You slay %s!' % (who.name))
				elif who.player: functions.log('The %s slays you!' % (self.race))
			
			self.xp += who.xp
			
			if who.gold:
				self.gold += who.gold
				if self.player: functions.log('Found +%s gold!' % who.gold)
			
			if who.coal:
				self.coal += who.coal
				if self.player: functions.log('Found +%s coal!' % who.coal)
			
			who.kill()
		
		if self.xp>=self.skill_level*var.skill_mod:
			self.xp-=self.skill_level*var.skill_mod
			self.skill_level+=1
			self.hp = self.hp_max
	
	def has_seen(self,who):
		for seen in self.seen:
			if seen['who'] == who:
				return seen
		
		return False
	
	def can_see(self,pos):
		_seen = True
		_l = draw.draw_diag_line(self.pos,pos)
		
		for pos in _l:
			if self.level.map[pos[0]][pos[1]] in var.solid:
				_seen = False
				break
			
			if not _l.index(pos)==len(_l)-1 and self.level.has_solid_item_at(pos):
				_seen = False
				break
		
		return _seen
	
	def can_see_ext(self,pos):
		_seen = True
		_path = self.path = pathfinding.astar(start=self.pos,end=pos,\
			omap=self.level.map,size=self.level.size).path
		
		if _path:
			return True
		else:
			return False
	
	def can_traverse(self,pos):
		_seen = True
		_l = draw.draw_diag_line(self.pos,pos)
		
		for pos in _l:
			if self.level.map[pos[0]][pos[1]] in var.blocking:
				_seen = False
				break
			
			if not _l.index(pos)==len(_l)-1 and self.level.has_solid_item_at(pos):
				_seen = False
				break
		
		return _seen
	
	def place(self,pos,tile):
		_pos = (self.pos[0]+pos[0],self.pos[1]+pos[1])
		if not self.level.map[_pos[0]][_pos[1]] in var.solid:
			self.level.map[_pos[0]][_pos[1]] = tile
			if _pos in self.level.walls:
				self.level.walls.remove(_pos)
			
			if not _pos in self.level.walking_space:
				self.level.walking_space.append(_pos)
	
	def tick(self):
		self.hunger_timer -= 1
		self.thirst_timer -= 1
		
		if self.hunger_timer <= 0:
			self.hunger_timer = 100
			self.hunger+=1
		
		if self.thirst_timer <= 0:
			self.thirst_timer = 75
			self.thirst+=1
	
	def think(self):		
		for life in var.life:
			if life == self or not self.z == life.z: continue
			
			_temp = self.has_seen(life)
			
			if not self.z == life.z and _temp:
				if _temp and _temp['in_los']:
					#print _temp['who'].name,'lost'
					_temp['in_los'] = False
			
			_l = draw.draw_diag_line(self.pos,life.pos)
			
			_seen = self.can_see(life.pos)#True
			
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
	
	def walk(self,dir):
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
			if _tile == 11:
				_chance = random.randint(0,100)
				
				if _chance <= 75:
					self.level.map[_pos[0]][_pos[1]] = 1
				elif 75<_chance<=95:
					self.level.add_item(14,_pos)
				else:
					self.level.add_item(13,_pos)
			
			self.pos = self.pos[:]
			return
		
		_items = self.level.items[_pos[0]][_pos[1]]
		if _items:
			_i = 0
			for _tile in _items:
				if _tile['tile'] == 11:
					if _tile['life']<=0:
						_chance = random.randint(0,100)
						if _chance <= 75:
							self.level.map[_pos[0]][_pos[1]] = 1
						elif 75<_chance<=95:
							self.level.add_item(14,_pos)
						else:
							self.level.add_item(13,_pos)
						
						self.level.items[_pos[0]][_pos[1]].pop(_i)
					else:
						_tile['life']-=1
					self.pos = self.pos[:]
					return
				elif _tile['tile'] == 13:
					self.gold += 1
					self.level.items[_pos[0]][_pos[1]].pop(_i)
					if self.player:
						functions.log('You picked up +1 gold.')
				elif _tile['tile'] == 14:
					self.coal += 1
					self.level.items[_pos[0]][_pos[1]].pop(_i)
					if self.player:
						functions.log('You picked up +1 coal.')
				elif _tile['tile'] == 17:
					self.add_item(17)
					self.level.items[_pos[0]][_pos[1]].pop(_i)
					if self.player:
						functions.log('You picked up some food.')
				
				_i+=1
		
		_found = False
		for life in var.life:
			if life == self or not self.z == life.z: continue
			
			if self.race == life.race:
				if life.pos == _pos:
					if self.player:
						functions.log('%s is in the way.' % life.name)
					_found = True
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

	def find_path(self,pos):
		if self.can_see(pos) and self.can_traverse(pos):
			if (pos[0],pos[1]) == self.path_dest: return
			self.path = draw.draw_diag_line(self.pos,pos)
			self.path_dest = (pos[0],pos[1])
		else:
			if (pos[0],pos[1]) == self.path_dest: return
			if tuple(self.pos) == self.start_pos: print 'dont have to recalculate';return
			_blocking = []
			
			for item in self.level.get_all_solid_items():
				_blocking.append((item['pos'][0],item['pos'][1]))
			
			self.path = pathfinding.astar(start=self.pos,end=pos,\
				omap=self.level.map,size=self.level.size,blocking=_blocking).path
			self.start_pos = (pos[0],pos[1])
			self.path_dest = (pos[0],pos[1])
	
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
		
		if self.pos == pos:
			return
		
		if not self.z == z:
			if self.z<z:
				self.find_path(self.level.entrances[0])
			else:
				self.find_path(self.level.exits[0])
			return
		
		self.find_path(pos)
		
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
				print 'Removed dead entity'
				
				if life.race == 'human':
					if life.lowest['who'] == self:
						life.lowest['who'] = None
						life.lowest['score'] = 0
					
					if life.highest['who'] == self:
						life.highest['who'] = None
						life.highest['score'] = 0
		
		var.life.remove(self)

class human(life):
	def __init__(self,player=False):
		self.icon = {'icon':'H','color':['white',None]}
		
		life.__init__(self,player=player)
		
		self.race = 'human'
		self.gender = 'male'
		
		self.hp = 20
		self.hp_max = 20
		
		self.hungry_at = 50
		self.thirsty_at = 50
		self.married = None
		self.worth = None
		self.mode = {'task':None,'who':None}
		self.task = None
		
		self.lowest = {'who':None,'score':0}
		self.highest = {'who':None,'score':0}
		
		self.events = []
	
	def add_event(self,what,score,who=None):
		for event in self.events:
			if event['what'] == what:
				event['score'] = score
				return
		
		self.events.append({'what':what,'score':score,'who':who})
	
	def get_event(self):
		_highest = {'what':None,'score':-1}
		for event in self.events:
			if event['score']>=_highest['score']:
				_highest['what'] = event['what']
				_highest['score'] = event['score']
				_highest['who'] = event['who']
		
		return _highest
	
	def remove_event(self,what):
		for event in self.events:
			if event['what'] == what:
				print 'Removed!'
				self.events.remove(event)
				return True
		
		print 'Warning: Event %s not found!' % what
		return False
	
	def judge(self,who):
		#This is so much easier...
		_score = 0
		
		_score = (who.hp+who.atk+who.defe)
		
		if not self.race == who.race:
			_score *= -1
		
		return _score
	
	def mine(self):
		if self.mine_dest: return
		#Okay, find the nearest dirt...
		_lowest = {'score':1000,'pos':None}
		for item in self.level.get_all_items(11):
			if not self.can_see(item['pos']): continue
			
			_dist = functions.distance(self.pos,item['pos'])
			
			if _dist<_lowest['score']:
				_lowest['score'] = _dist
				_lowest['pos'] = item['pos']
		
		if _lowest['pos']:
			self.go_to(_lowest['pos'])
			self.mine_dest = _lowest['pos']
		else:
			self.follow(var.player)
	
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
			if self.judge(self)>=abs(self.lowest['score']):
				#self.go_to(self.lowest['who'].pos)
				#self.task = 'attacking'
				self.add_event('attack',100,who=self.lowest['who'])
			else:
				self.task = 'flee'
		else:
			if self.task == 'attacking':
				print 'Task reset'
				self.task = None
		
		if not self.mode['task']:# and not self.task in ['attacking','flee']:
			#elif self.highest['who'] and self.married == self.highest['who']:
			#	#TODO: This one will happen too much...
			#	self.follow(self.highest['who'])
			#	self.task = 'following'
			#else:
			_event = self.get_event()
			
			if _event and not self.task==_event:
				self.say('%s' % (_event['what']))
				self.task = _event
			
			if self.task['what'] == 'food':
				_item = self.get_item_id(17)
				
				if _item:
					self.hunger = 0
					self.hunger_timer = var.hunger_timer_max
					self.items.remove(_item)
					self.remove_event(self.task['what'])
					self.task = None
					self.say('That was good!')
				else:
					_pos = None
					_room = var.world.get_level(1).get_room('home')
					for pos in _room['walking_space']:
						for item in var.world.get_level(1).items[pos[0]][pos[1]]:
							if item['type']=='food':
								_pos = pos
								break
					
					if _pos:
						self.go_to(_pos,z=1)
			elif self.task['what'] == 'mine':
				self.mine()
			elif self.task['what'] == 'deliver':
				if self.coal+self.gold:
					_pos = None
					_room = var.world.get_level(1).get_room('storage')
					for pos in _room['walking_space']:
						for item in var.world.get_level(1).items[pos[0]][pos[1]]:
							if item['type']=='storage':
								for space in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
									if (pos[0]+space[0],pos[1]+space[1]) in _room['walking_space']:
										_pos = (pos[0]+space[0],pos[1]+space[1])
										break
								break
					
					if tuple(self.pos) == _pos:
						self.coal = 0
						self.gold = 0
						self.remove_event(self.task['what'])
						self.task = None
						self.say('Delivered!')
						print 'Made it!'
					elif _pos:
						self.go_to(_pos,z=1)
			elif self.task['what'] == 'attack':
				if self.task['who'].hp>0:
					self.go_to(self.task['who'].pos)
				else:
					self.remove_event(self.task['what'])
					self.task = None
					self.say('Got em.')
				
		#else:
		#	if not self.task in ['attacking','flee']:
		#		if self.mode['task'] == 'follow':
		#			self.follow(self.mode['who'])
		#			self.task = 'following'
		#		elif self.mode['task'] == 'mine':
		#			self.mine()
		
		#Take care of daily schedules here
		if self.hunger >= self.hungry_at:
			self.add_event('food',self.hunger)
		
		if self.thirst >= self.thirsty_at:
			self.add_event('water',self.thirst)
		
		self.add_event('deliver',(self.coal+self.gold)*50)
		
		if self.path:
			if len(self.path)>1: self.path.pop(0)
			return [self.path[0][0],self.path[0][1]]
		
		return self.pos

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
			if seen['who'].race == self.race: continue
			
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