import var

class life:
	def __init__(self,player=False):
		self.player = player
		
		if self.player:
			self.icon = {'icon':'@','color':'white'}
		
		self.name = 'Default'
		self.hp = 10
		self.pos = [0,0]
		
		var.life.append(self)
	
	def walk(self,dir):
		if dir == 'up' and self.level.map[self.pos[0]][self.pos[1]-1]:
			self.pos[1]-=1
		elif dir == 'down' and self.level.map[self.pos[0]][self.pos[1]+1]:
			self.pos[1]+=1
		elif dir == 'left' and self.level.map[self.pos[0]-1][self.pos[1]]:
			self.pos[0]-=1
		elif dir == 'right' and self.level.map[self.pos[0]+1][self.pos[1]]:
			self.pos[0]+=1

class human(life):
	def __init__(self,player=False):
		self.icon = {'icon':'H','color':'grey'}
		
		life.__init__(self,player=player)
		
		self.hp = 15