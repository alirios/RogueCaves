import var

def log(text):
	if len(var.history)>=5: var.history.pop(0)
	
	var.history.append(text)

def distance(pos1,pos2):
	return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

def sort_item_array_by_distance(items,pos):
	_ret = []
	_t = []
	
	for item in items:
		_dist = distance(item['pos'],pos)
		_temp = {'dist':_dist,'item':item}
		
		if not len(_t): _t.append(_temp);continue
		
		_lowest = 9001
		#_highest = -1
		for _item in _t:
			if _item['item'] == item: continue
			if _temp['dist'] < _item['dist']:
				if _t.index(_item) < _lowest: _lowest = _t.index(_item)
			#if _temp['dist'] > _item['dist']: _highest = _t.index(_item)
		
		_t.insert(_lowest,_temp)
	
	for item in _t:
		_ret.append(item['item'])
	
	return _ret