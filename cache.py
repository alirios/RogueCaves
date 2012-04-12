import logging

class cache:
	def __init__(self):
		self.path_cache = []
	
	def add_path_to_cache(self,start,end,path,z):
		for __path in self.path_cache:
			if __path['start'] == tuple(start) and __path['end'] == tuple(end)\
				and __path['z']==z:
				logging.debug('Path already exists in cache.')
				return
		
		if path:
			_path = {'start':tuple(start),'end':tuple(end),'path':path[:],'z':z}
		else:
			_path = {'start':tuple(start),'end':tuple(end),'path':path,'z':z}
		self.path_cache.append(_path)
	
	def get_path_from_cache(self,start,end,z):
		for __path in self.path_cache:
			if __path['start'] == tuple(start) and __path['end'] == tuple(end)\
				and __path['z']==z:
				logging.debug('Reusing old path.')
				return __path['path']
		
		return False