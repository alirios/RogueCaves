import draw, copy, math
import random, time

class LevelGen:
	def __init__(self,size=(60,40)):
		self.size = size
		
		self.map = []
		self.rooms = []
		self.max_rooms = 13
		self.landmarks = []
		self.walking_space = []
		self.walls = []
		
		#Lighting...
		self.fmap = []
		self.lmap = []
		
		#Python has no concept of 2d arrays, so we "fake" it here.
		for x in range(self.size[0]):
			_y = []
			
			for y in range(self.size[1]):
				_y.append(0)
				self.walls.append((x,y))
			
			self.map.append(_y)
		
		for x in range(0,self.size[0]):
			self.fmap.append([0] * self.size[1])
		
	def dofov(self,pos,x,y):
		#I translated it to Python. You are welcome to use this code instead of writing your own :)
		i = 0
		ox = 0
		oy = 0
		ox = pos[0]+0.5
		oy = pos[1]+0.5
		while i<16:
			i+=1
			if int(ox) >= self.size[0] or int(oy) >= self.size[1]: continue
			self.fmap[int(ox)][int(oy)]=1
			self.lmap[int(ox)][int(oy)]=1
			if self.map[int(ox)][int(oy)] == 0: return
			ox+=x;
			oy+=y;
		
	def light(self,pos):
		self.lmap = []
		for x in range(0,self.size[0]):
			self.lmap.append([0] * self.size[1])
		
		x = 0
		y = 0
		i = 0
		while i<360:
			x=math.cos(i*0.01745);
			y=math.sin(i*0.01745);
			self.dofov(pos,x,y);
			i+=1
	
	def decompose(self,times):
		for i in range(times):
			_map = copy.deepcopy(self.map)
			
			for y in range(self.size[1]-1):
				for x in range(self.size[0]-1):
					_count = 0
					for pos in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
						_x = x+pos[0]
						_y = y+pos[1]
						
						if 0>_x<self.size[0]-1: continue
						if 0>_y<self.size[1]-1: continue
						#print _x,_y
						if self.map[_x][_y]:
							_count+=1
					
					if _count>=4:
						_map[x][y]=1
		
			self.map = _map
	
	def generate(self, entrance=(4,4)):
		#We'll be generating the level "in-line",
		#which means the entire level in generated in
		#order. (Room, tunnel, room, tunnel.)
		#THEN we'll be randomly connecting rooms with 
		#tunnels for some added complexity.
		
		#Our map is current all 0s
		#In the end, we will have a mix of numbers
		
		#0 - wall
		#1 - floor
		#2 - tunnel
		#3 - door
		
		#First, let's place our entrance.
		#We'll make it a 3x3 area around it
		for x in range(-1,2):
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
			_x = entrance[0]+x
			
			for y in range(-1,2):
				
				#We need to check to see if we're drawing
				#inside the map first...
				#By the way, a '\' in Python
				#just lets us drop down a line incase
				#a line gets too lengthy...
				#Very handy!
				
				#Another temp variable...
				_y = entrance[1]+y
				
				if 0<_x<self.size[0]\
					and 0<_y<self.size[1]:
						self.map[_x][_y] = 1
						self.walking_space.append((_x,_y))
						self.walls.remove((_x,_y))
				
				#What we just did was "carve" out the room
				#Imagine these as rooms in a cave or something,
				#like the dungeons in Oblivion...
				#We also add the open space we create to a
				#"walking_space" list.
				#We'll use this later, but just know that
				#it marks places you could potentially walk
				#(it does more than just that, though!)
		
		#Place our door
		self.map[entrance[0]][entrance[1]] = 3
		
		#Now, here's where tunneling comes into play
		#First, we keep track of all the major "landmarks"
		#on our map.
		#These are things like door, exits, and the center
		#of rooms.
		#We'll use these as guidelines for our tunnels...
		#Since we already have an entrance, add it to
		#the list...
		self.landmarks.append(entrance)
		
		#We'll want to place our rooms next
		for i in range(self.max_rooms):
			#To prevent our rooms from being too far apart,
			#we want to randomly select a position and compare
			#it to our landmark list...
			_found = False
			_room_size = (random.randint(3,8),random.randint(3,8))
			
			while not _found:
				_found = True
				_room = []
				_pos = random.choice(self.walls)
				
				for x in range(-_room_size[0]/2,_room_size[0]/2):
					_x = _pos[0]+x
					
					#Save us some time by checking to see if we're
					#outside the map...
					if 1>_x or _x>=self.size[0]-1: _found = False;break
					
					for y in range(-_room_size[1]/2,_room_size[1]/2):
						_y = _pos[1]+y
						
						if 1<_y<self.size[1]-2:
							if not self.map[_x][_y] in [0,2]:
								_found = False
								break
							else:
								_room.append((_x,_y))
					
					if not _found: break
				
				if _found and len(_room)>=9:
					for pos in _room:
						self.map[pos[0]][pos[1]] = 1
						self.walking_space.append(pos)
						
						if pos in self.walls:
							self.walls.remove(pos)
						
					_center = random.randint(0,len(_room[0]))
					self.landmarks.append((_room[_center]))
				else:
					_found = False
			
		_done = []
		for l1 in self.landmarks:
			_lowest = {'where':None,'dist':9000}
			for l2 in self.landmarks:
				if l1 == l2 or l2 in _done: continue
				
				_dist = abs(l2[0]-l1[0])+abs(l2[1]-l1[1])
				
				if _dist<_lowest['dist']:
					_lowest['dist'] = _dist
					_lowest['where'] = l2
			
			if not _lowest['where']: break
			
			_line = draw.draw_line(l1,_lowest['where'])
			
			for pos in _line:
				if not self.map[pos[0]][pos[1]]:
					self.map[pos[0]][pos[1]] = 2
					if not pos in self.walking_space:
						self.walking_space.append(pos)
					
					if pos in self.walls:
						self.walls.remove(pos)
				
			_done.append(l1)
			#_done.append(l2)
				
	def out(self):
		for y in range(self.size[1]):
			for x in range(self.size[0]):
				_tile = self.map[x][y]
				if not _tile: print ' ',
				else: print _tile,
			
			print

#l = LevelGen()
#l.generate()
#l.out()