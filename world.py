import levelgen, life as alife, functions, var
import logging, random, time, json, os

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
		
		logging.debug('[LevelGen] Starting')
		for level in self.levels:
			_ltime = time.time()
			
			#Place our first cave...
			if level['z']==1:
				_entrances=[(random.randint(4,self.size[0]-4),random.randint(4,self.size[1]-4))]
				_exits=[(random.randint(4,self.size[0]-4),random.randint(4,self.size[1]-4))] 
			else:
				_entrances=_exits[:]
				_exits=[(random.randint(4,self.size[0]-4),random.randint(4,self.size[1]-4))] 
			
			#logging.debug('DEPTH: %s' % str(level['z']))
			if level['type']=='cave':
				level['level'] = levelgen.LevelGen(rooms=abs(level['z']*5),size=self.size,diagtunnels=random.randint(0,1),outside=False)
				level['level'].z = level['z']
				_ctime = time.time()
				level['level'].generate_cave(entrances=_entrances,exits=_exits)
				#logging.debug('\tCaveGen took: %s' % (time.time()-_ctime))
				
				_dtime = time.time()
				level['level'].decompose(self.depth-abs(level['z']),edgesonly=False)
				#logging.debug('\tDecompose setting %s took %s' % (self.depth-abs(level['z']),time.time()-_ctime))
				
				_wtime = time.time()
				_w = level['level'].walk(where=level['level'].walls,walkers=-level['z'],types=[10,11],intensity=(10,12))
				#logging.debug('\tWalkers: %s, took %s' % (-level['z'],time.time()-_wtime))
				
				_rtime = time.time()
				level['level'].generate_cave_rooms()
				#logging.debug('\tRooms: %s, took %s' % (len(level['level'].rooms),time.time()-_rtime))
				
				for pos in _w:
					if level['level'].map[pos[0]][pos[1]] == 11:
						level['level'].map[pos[0]][pos[1]] = 1
						level['level'].add_item(11,pos)
				
			else:
				level['level'] = levelgen.LevelGen(rooms=abs(level['z']*10),size=self.size,diagtunnels=False,outside=True)
				level['level'].generate_forest(exits=_exits)
				level['level'].z = level['z']
			#logging.debug('\tTotal: %s' % (time.time()-_ltime))
		
		logging.debug('[LevelGen] Took: %s' % (time.time()-_stime))
		logging.debug('[World.ALife] Creating ALife...')
		
		for r in range(2): functions.generate_human('trade')
		for r in range(1): functions.generate_human('farmer')
		for r in range(1): functions.generate_human('barkeep')
	
	def save(self):
		logging.debug('[World.save] Gathering ALife strings...')
		_alife = []
		for life in var.life:
			_alife.append(life.save())
		
		logging.debug('[World.save] Gathering level strings...')
		_levels = []
		for level in self.levels:
			_levels.append(level['level'].save())
		
		logging.debug('[World.save] Offloading strings to disk...')
		
		_save_file = open(os.path.join('data','test01.sav'),'w')
		#_save_file.write(str(_alife))
		_save_file.write(json.dumps({'alife':_alife})+'\n')
		#_save_file.write(str(_levels))
		_save_file.write(json.dumps({'levels':_levels})+'\n')
		_save_file.close()
		
		logging.debug('[World.save] Done!')
	
	def load(self):
		logging.debug('[World.load] Reading save file...')
		_load_file = open(os.path.join('data','test01.sav'),'r')
		
		logging.debug('[World.load] Gathering ALife strings...')
		_alife = json.loads(_load_file.readline())
		logging.debug('[World.load] Gathering level strings...')
		_levels = json.loads(_load_file.readline())
		
		for level in _levels['levels']:
			_level = levelgen.LevelGen()
			_level.load(level)
			
			for entry in self.levels:
				if entry['z'] == level['z']:
					entry['level'] = _level
		
		for life in _alife['alife']:
			if life['race'] == 'human':
				_alife = alife.human()
			elif life['race'] == 'dog':
				_alife = alife.dog()
			else:
				logging.error('[World.load] Can\'t load: %s' % life['race'])
			
			for entry in life:
				if isinstance(life[entry],unicode):
					life[entry] = str(life[entry])
			
			_alife.load(life)
		
		logging.debug('[World.load] Finalizing ALife...')
		for life in var.life:
			life.finalize()
		
		for entry in self.levels:
			entry['level'].finalize()
		
		_load_file.close()
		
	def get_stats(self):
		logging.debug('[World.Stats] Gathering stats...')
		_cache = var.cache.get_stats()
		logging.debug('[World.Stats.Cache_Size] %s' % _cache['size'])
		self.save()