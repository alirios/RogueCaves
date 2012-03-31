import draw, copy, math
import random, time

class LevelGen:
	def __init__(self,size=(80,80),rooms=25,room_size=(3,6),diagtunnels=True,overlaprooms=False):
		self.size = size
		
		self.map = []
		self.rooms = []
		self.max_rooms = rooms
		self.room_size = room_size
		self.diagtunnels = diagtunnels
		self.overlaprooms = overlaprooms
		self.landmarks = []
		self.walking_space = []
		self.walls = []
		
		#Lights and maps...
		self.lights = []
		self.fmap = [[0] * self.size[1] for i in range(self.size[0])]
		self.lmap = []
		self.fov = []
		
		#Python has no concept of 2d arrays, so we "fake" it here.
		for x in range(self.size[0]):
			_y = []
			_l = []
			
			for y in range(self.size[1]):
				_y.append(0)
				_l.append({'source':False,'color':(0,0,0),'brightness':0})
				self.walls.append((x,y))
			
			self.map.append(_y)
			self.lmap.append(_l)
		
	def add_light(self,pos,color,life,brightness):
		self.lights.append(pos)
		
		self.lmap[pos[0]][pos[1]]['source'] = True
		self.lmap[pos[0]][pos[1]]['color'] = color
		self.lmap[pos[0]][pos[1]]['life'] = life
		self.lmap[pos[0]][pos[1]]['brightness'] = brightness
		self.lmap[pos[0]][pos[1]]['children'] =[]
	
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
			self.fmap[int(ox)][int(oy)]=1
			self.vmap[int(ox)][int(oy)]=1
			if self.map[int(ox)][int(oy)] == 0: return
			ox+=x;
			oy+=y;
		
	def light(self,pos):
		self.vmap = [[0] * self.size[1] for i in range(self.size[0])]
		
		x = 0
		y = 0
		i = 0
		self.fov = []
		while i<360:
			x=math.cos(i*0.01745);
			y=math.sin(i*0.01745);
			self.dofov(pos,x,y,10);
			i+=1
	
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
	
	def decompose(self,times,edgesonly=True):
		for i in range(times):
			_map = copy.deepcopy(self.map)
			
			for y in range(self.size[1]-1):
				for x in range(self.size[0]-1):
					if self.map[x][y] and edgesonly: continue
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
		
		#First, let's place our entrance.
		#We'll make a 3x3 area around it
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
				#just lets us drop down a line in case
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
		#These are things like doors, exits, and the center
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
				if _pos[0]-(_room_size[0]/2)<0 or _pos[0]+(_room_size[0]/2)>self.size[0]: continue
				if _pos[1]-(_room_size[1]/2)<0 or _pos[1]+(_room_size[1]/2)>self.size[1]: continue
				
				#Start checking to see if the room "fits"
				for x in range(-_room_size[0]/2,_room_size[0]/2):					
					_x = _pos[0]+x
					
					for y in range(-_room_size[1]/2,_room_size[1]/2):
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
							
							if __pos[0]<0 or __pos[0]>=self.size[0]: continue
							if __pos[1]<0 or __pos[1]>=self.size[1]: continue
							
							self.map[__pos[0]][__pos[1]] = 2
							
							if not __pos in self.walking_space:
								self.walking_space.append(__pos)
							
							if __pos in self.walls:
								self.walls.remove(__pos)
					else:
						#Else, change the map to a tunnel tile!
						self.map[pos[0]][pos[1]] = 2
						
						#Add it to the walking_space array if it isn't there already...
						if not pos in self.walking_space:
							self.walking_space.append(pos)
						
						#Remove the spot from the walls array also...
						if pos in self.walls:
							self.walls.remove(pos)
			
			#http://www.youtube.com/watch?feature=player_detailpage&v=7C7WCRoqFVs#t=103s
			_done.append(l1)
				
	def out(self):
		for y in range(self.size[1]):
			for x in range(self.size[0]):
				_tile = self.map[x][y]
				if not _tile: print ' ',
				else: print _tile,
			
			print