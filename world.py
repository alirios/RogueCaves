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
			
			#Place our first cave...
			if level['z']==1:
				_entrances=[(random.randint(4,self.size[0]-4),random.randint(4,self.size[1]-4))]
				_exits=[(random.randint(4,self.size[0]-4),random.randint(4,self.size[1]-4))] 
			else:
				_entrances=_exits[:]
				_exits=[(random.randint(4,self.size[0]-4),random.randint(4,self.size[1]-4))] 
			
			print 'DEPTH: %s...' % str(level['z'])
			if level['type']=='cave':
				level['level'] = levelgen.LevelGen(rooms=abs(level['z']*5),size=self.size,diagtunnels=random.randint(0,1),outside=False)

				_ctime = time.time()
				level['level'].generate_cave(entrances=_entrances,exits=_exits)
				print '\tCaveGen took',time.time()-_ctime
				
				_dtime = time.time()
				level['level'].decompose(self.depth-abs(level['z']),edgesonly=False)
				print '\tDecompose setting %s took' % (self.depth-abs(level['z'])),time.time()-_ctime
				
				_wtime = time.time()
				level['level'].walk(where=level['level'].walls,walkers=-level['z'],types=[10,11],intensity=(10,12))
				print '\tWalkers: %s, took %s' % (-level['z'],time.time()-_wtime)
			else:
				level['level'] = levelgen.LevelGen(rooms=abs(level['z']*10),size=self.size,diagtunnels=False,outside=True)
				level['level'].generate_forest(entrances=_entrances,exits=_exits)
			print '\tTotal:',time.time()-_ltime
		
		print 'Worldgen took:',time.time()-_stime
			