import logging

class cache:
	def __init__(self):
		self.path_cache = []
	
	def add_path_to_cache(self,start,end,path,z):
		logging.debug('[Cache.new_path] %s,%s to %s,%s, z=%s' %
			(start[0],start[1],end[0],end[1],z))
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
				logging.debug('[Cache.old_path] Returning: %s,%s to %s,%s, z=%s' %
					((start[0],start[1],end[0],end[1],z)))
				return __path['path']
			elif __path['end'] == tuple(start) and __path['start'] == tuple(end)\
				and __path['z']==z:
				logging.debug('[Cache.old_path.reverse] Returning: %s,%s to %s,%s, z=%s' %
					((start[0],start[1],end[0],end[1],z)))
				_temp = __path['path'][:]
				_temp.reverse()
				return _temp				
		
		return False