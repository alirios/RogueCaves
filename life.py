import draw, var

class life:
	def __init__(self,player=False):
		self.player = player
		
		if self.player:
			self.icon = {'icon':'@','color':'white'}
		
		self.name = 'Default'
		self.hp = 10
		self.pos = [0,0]
		self.seen = []
		self.alignment = 'neutral'
		
		var.life.append(self)
	
	def think(self):
		self.seen = []
		
		for life in var.life:
			if life == self: continue
			
			_l = draw.draw_diag_line(self.pos,life.pos)
			
			_seen = True
			for pos in _l:
				if not self.level.map[pos[0]][pos[1]]:
					_seen = False
					break
			
			if _seen:
				self.seen.append({'who':life,'dist':len(_l)})
				print 'Sees you!'
	
	def walk(self,dir):
		if self.player:
			if dir == 'up' and self.level.map[self.pos[0]][self.pos[1]-1]:
				self.pos[1]-=1
			elif dir == 'down' and self.pos[1]+1<var.window_size[1]-6:
				if self.level.map[self.pos[0]][self.pos[1]+1]:
					self.pos[1]+=1
			elif dir == 'left' and self.level.map[self.pos[0]-1][self.pos[1]]:
				self.pos[0]-=1
			elif dir == 'right' and self.level.map[self.pos[0]+1][self.pos[1]]:
				self.pos[0]+=1
		else:
			self.think()

class human(life):
	def __init__(self,player=False):
		self.icon = {'icon':'H','color':'white'}
		
		life.__init__(self,player=player)
		
		self.race = 'human'
		
		self.hp = 15