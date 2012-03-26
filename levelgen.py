class LevelGen:
	def __init__(self,size=(30,30)):
		self.size = size
		
		self.map = []
		self.rooms = []
		self.max_rooms = 3
		
		#Python has no concept of 2d arrays, so we "fake" it here.
		for x in range(self.size[0]):
			_y = []
			
			for y in range(self.size[1]):
				_y.append(0)
			
			self.map.append(_y)
		
	def generate(self, entrance=(4,4)):
		#Some level generators place rooms randomly
		#then connect them with tunnels.
		#This works, but I feel the end result
		#is usually very boring.
		#We'll be generating the level "in-line",
		#which means the entire level in generated in
		#order. (Room, tunnel, room, tunnel.)
		
		#Our map is current all 0s
		#In the end, we will have a mix of numbers
		
		#0 - wall
		#1 - floor
		#2 - door
		
		#First, let's place our entrance.
		#We'll make it a 3x3 area around it
		for x in range(-1,2):
			for y in range(-1,2):
				
				#We need to check to see if we're drawing
				#inside the map first...
				#By the way, a '\' in Python
				#just lets us drop down a line incase
				#a line gets too lengthy...
				#Very handy!
				
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
				#before the variables I plan to throwaway...
				
				_x = entrance[0]+x
				_y = entrance[1]+y
				
				if 0<_x<self.size[0]\
					and 0<_y<self.size[1]:
						self.map[_x][_y] = 1
		
		#Place our door
		self.map[entrance[0]][entrance[1]] = 2
		
		#Now, here's where tunneling comes in
		
		for i in range(self.max_rooms):
			pass
						
			
	
	def out(self):
		for y in range(self.size[0]):
			for x in range(self.size[1]):
				print self.map[x][y],
			
			print

_m = LevelGen()
_m.generate()
_m.out()