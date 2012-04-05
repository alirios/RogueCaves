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
		self.path_dest = ()
		self.alignment = 'neutral'
		
		self.atk = 1
		self.defe = 1
		
		self.thirst = 0
		self.thirst_timer = 75
		self.hunger = 0
		self.hunger_timer = 100
		self.gold = 0
		self.coal = 0
		
		var.life.append(self)
	
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
				functions.log('Found +%s gold!' % who.gold)
			
			if who.coal:
				self.coal += who.coal
				functions.log('Found +%s coal!' % who.coal)
			
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
		for pos in draw.draw_diag_line(self.pos,pos):
			if self.level.map[pos[0]][pos[1]] in var.solid:
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
					print _temp['who'].name,'lost'
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
					print _temp['who'].name,'lost'
					_temp['in_los'] = False
	
	def walk(self,dir):
		_pos = self.pos[:]
		
		if self.speed>0:
			self.speed -= 1
			return
		else:
			self.speed = self.speed_max
		
		if self.player:
			if dir == 'up':
				_pos[1]-=1
			elif dir == 'down' and self.pos[1]+1<var.world.size[1]:
				#if not self.level.map[self.pos[0]][self.pos[1]+1] in var.blocking:
				_pos[1]+=1
			elif dir == 'left':
				_pos[0]-=1
			elif dir == 'right' and self.pos[0]+1<var.world.size[0]:
				#if not self.level.map[self.pos[0]+1][self.pos[1]] in var.blocking:
				_pos[0]+=1
		else:
			_pos = self.think()
		
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
			for _tile in _items:
				if _tile == 13:
					self.gold += 1
					if self.player:
						functions.log('You picked up +1 gold.')
				elif _tile == 14:
					self.coal += 1
					if self.player:
						functions.log('You picked up +1 coal.')
				
				self.level.items[_pos[0]][_pos[1]].remove(_tile)
		
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

	def find_path(self,pos):
		if self.can_see(pos):
			if not (pos[0],pos[1]) == self.path_dest:
				self.path = draw.draw_diag_line(self.pos,pos)
				
				self.path_dest = (pos[0],pos[1])
		else:
			if not (pos[0],pos[1]) == self.path_dest:
				self.path = pathfinding.astar(start=self.pos,end=pos,\
					omap=self.level.map,size=self.level.size).path
				
				self.path_dest = (pos[0],pos[1])
	
	def follow(self,who):
		if self.pos == who.pos or functions.distance(self.pos,who.pos)<=3:
			return
		
		self.find_path(who.pos)
		
	def enter(self):
		if self.level.map[self.pos[0]][self.pos[1]] == 3:
			self.z += 1
			functions.log('You go up.')
		elif self.level.map[self.pos[0]][self.pos[1]] == 4:
			self.z -= 1
			functions.log('You go down.')
		
		self.level = var.world.get_level(self.z)
	
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
		
		self.married = None
		self.worth = None
		self.mode = {'task':None,'who':None}
		self.task = None
		
		self.lowest = {'who':None,'score':0}
		self.highest = {'who':None,'score':0}
		
		self.events = []
	
	def add_event(self,what,score):
		for event in self.events:
			if event['what'] == what:
				event['score'] = score
				return
		
		self.events.append({'what':what,'score':score})
	
	def get_event(self):
		_highest = {'what':None,'score':-1}
		for event in self.events:
			if event['score']>=_highest['score']:
				_highest['what'] = event['what']
				_highest['score'] = event['score']
		
		return _highest['what']
	
	def judge(self,who):
		#This is so much easier...
		_score = 0
		
		_score = (who.hp+who.atk+who.defe)
		
		if not self.race == who.race:
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
		
		if not self.mode['task']:
			if self.lowest['who']:
				if self.judge(self)>=abs(self.lowest['score']):
					self.path = draw.draw_diag_line(self.pos,self.lowest['who'].pos)
					#if len(self.path)>1: self.path.pop(0)
					self.task = 'attacking'
				else:
					self.task = 'flee'
			elif self.highest['who'] and self.married == self.highest['who']:
				#This one will happen too much...
				self.follow(self.highest['who'])
				self.task = 'following'
			else:
				_event = self.get_event()
				
				if _event and not self.task==_event:
					self.say('I need to get %s' % (_event))
					self.task = _event
				
				if self.task == 'food':
					self.follow(var.player)
				
		else:
			if self.mode['task'] == 'follow':
				self.follow(self.mode['who'])
				self.task = 'following'
		
		#Take care of daily schedules here
		if self.hunger >= 1:
			self.add_event('food',self.hunger)
		
		if self.thirst >= 50:
			self.add_event('water',self.thirst)
		
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