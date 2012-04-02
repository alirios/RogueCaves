import functions, draw, var

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
		self.alignment = 'neutral'
		
		var.life.append(self)
	
	def attack(self,who):
		if who.race in ['zombie']:
			if self.player: functions.log('You swing at the %s!' % (who.race))
			elif who.player: functions.log('The %s swings at you!' % (who.race))
		else:
			if self.player: functions.log('You swing at %s!' % (who.name))
			elif who.player: functions.log('The %s swings at you!' % (self.race))
			#functions.log('You swing at %s!' % (who.name))
		
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
			who.kill()
		
		if self.xp>=self.skill_level*var.skill_mod:
			self.xp-=self.skill_level*var.skill_mod
			self.skill_level+=1
			self.hp = self.hp_max
	
	def think(self):
		self.seen = []
		
		for life in var.life:
			if life == self or not self.z == life.z: continue
			
			_l = draw.draw_diag_line(self.pos,life.pos)
			
			_seen = True
			for pos in _l:
				if not self.level.map[pos[0]][pos[1]]:
					_seen = False
					break
			
			if _seen:
				self.seen.append({'who':life,'dist':len(_l),'los':_l})
		
		if not self.seen: return self.pos
		
		self.focus = self.seen[0]
		self.focus['los'].pop(0)
		return [self.focus['los'][0][0],self.focus['los'][0][1]]
	
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
				self.level.map[_pos[0]][_pos[1]] = 1
			
			_pos = self.pos[:]
		
		_found = False
		for life in var.life:
			if life == self or not self.z == life.z: continue
			
			if life.pos == _pos:
				self.attack(life)
				_found = True
		
		if not _found:
			self.pos = _pos[:]
		
	def enter(self):
		if self.level.map[self.pos[0]][self.pos[1]] == 3:
			self.z += 1
			functions.log('You go up.')
		elif self.level.map[self.pos[0]][self.pos[1]] == 4:
			self.z -= 1
			functions.log('You go down.')
		
		self.level = var.world.get_level(self.z)
	
	def kill(self):
		var.life.remove(self)

class human(life):
	def __init__(self,player=False):
		self.icon = {'icon':'H','color':['white',None]}
		
		life.__init__(self,player=player)
		
		self.race = 'human'
		
		self.hp = 20
		self.hp_max = 20

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