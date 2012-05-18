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
		for _item in _t:
			if _item['item'] == item: continue
			if _temp['dist'] < _item['dist']:
				if _t.index(_item) < _lowest: _lowest = _t.index(_item)
		
		_t.insert(_lowest,_temp)
	
	for item in _t:
		_ret.append(item['item'])
	
	return _ret

def item_list_to_menu(list):
	_ret = []
	
	for item in list:
		_found = False
		for entry in _ret:
			if entry['item']['name'] == item['name']:
				entry['count']+=1
				_found = True
				break
			
		if not _found:
			_ret.append({'item':item,'count':1})
				
	return _ret