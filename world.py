import levelgen
import random, time

class World:
	def __init__(self,height=1,depth=5,size=(50,50)):
		self.levels = []
		
		self.depth = depth
		self.height = height
		self.size = size
		
		for i in range(1,self.height+1):
			self.levels.append({'z':i,'level':None,'type':'forest'})
		
		for i in range(self.depth):
			self.levels.append({'z':-i,'level':None,'type':'cave'})
	
	def get_level(self,z):
		for level in self.levels:
			if level['z'] == z:
				return level['level']
		
		return False
	
	def generate(self):
		_stime = time.time()
		_exits = None
		
		for level in self.levels:
			_ltime = time.time()
			level['level'] = levelgen.LevelGen(rooms=abs(level['z']*10),size=self.size,diagtunnels=False)
			
			#_entrances=[(random.randint(4,self.size[0]-4),random.randint(4,self.size[1]-4))]
			
			#Place our first cave...
			if level['z']==1:
				_entrances=[(random.randint(4,self.size[0]-4),random.randint(4,self.size[1]-4))]
				_exits=[(random.randint(4,self.size[0]-4),random.randint(4,self.size[1]-4))] 
			else:
				_entrances=_exits[:]
				_exits=[(random.randint(4,self.size[0]-4),random.randint(4,self.size[1]-4))] 
				
				#_exits = _entrances
			#if not level['z']:
			#	_entrances=[(random.randint(4,self.size[0]-4),random.randint(4,self.size[1]-4))]
			#	_exits=[(random.randint(4,self.size[0]-4),random.randint(4,self.size[1]-4))] 
			#else:
			#	_
			#	_exits=[(random.randint(4,self.size[0]-4),random.randint(4,self.size[1]-4))] 
			
			if level['type']=='cave':
				level['level'].generate_cave(entrances=_entrances,exits=_exits)
				level['level'].decompose(self.depth-abs(level['z']),edgesonly=False)
			else:
				level['level'].generate_forest(entrances=_entrances,exits=_exits)
			print 'DEPTH: %s, generated in:' % (str(level['z'])),time.time()-_ltime
		
		print 'Worldgen took:',time.time()-_stime
			