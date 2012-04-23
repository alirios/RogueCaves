import levelgen
import logging, random, time

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
			
			logging.debug('DEPTH: %s' % str(level['z']))
			if level['type']=='cave':
				level['level'] = levelgen.LevelGen(rooms=abs(level['z']*5),size=self.size,diagtunnels=random.randint(0,1),outside=False)
				level['level'].z = level['z']
				_ctime = time.time()
				level['level'].generate_cave(entrances=_entrances,exits=_exits)
				logging.debug('\tCaveGen took: %s' % (time.time()-_ctime))
				
				_dtime = time.time()
				level['level'].decompose(self.depth-abs(level['z']),edgesonly=False)
				logging.debug('\tDecompose setting %s took %s' % (self.depth-abs(level['z']),time.time()-_ctime))
				
				_wtime = time.time()
				_w = level['level'].walk(where=level['level'].walls,walkers=-level['z'],types=[10,11],intensity=(10,12))
				logging.debug('\tWalkers: %s, took %s' % (-level['z'],time.time()-_wtime))
				
				_rtime = time.time()
				level['level'].generate_cave_rooms()
				logging.debug('\tRooms: %s, took %s' % (len(level['level'].rooms),time.time()-_rtime))
				
				for pos in _w:
					if level['level'].map[pos[0]][pos[1]] == 11:
						level['level'].map[pos[0]][pos[1]] = 1
						level['level'].add_item(11,pos)
				
			else:
				level['level'] = levelgen.LevelGen(rooms=abs(level['z']*10),size=self.size,diagtunnels=False,outside=True)
				level['level'].generate_forest(entrances=_entrances,exits=_exits)
			logging.debug('\tTotal: %s' % (time.time()-_ltime))
		
		logging.debug('Worldgen took: %s' % (time.time()-_stime))
		