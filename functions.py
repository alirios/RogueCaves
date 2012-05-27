import random, var

def log(text):
	if len(var.history)>=5: var.history.pop(0)
	
	var.history.append(text)

def distance(pos1,pos2):
	return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

def get_name_by_gender(gender):
	if gender == 'male':
		return 'derp'
	else:
		return random.choice(var.names_female).strip()

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

def get_id():
	var.id-=1
	return var.id

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

def build_menu(list,who=None,name='Menu',trading=False,callback=None,**kargv):
	if trading: who.trading = True
	var.menu_index = 0
	var.in_menu = item_list_to_menu(list)
	var.menu_name = name
	var.menu_callback = callback
	var.callback_args = kargv

def destroy_menu(who=None):
	if who: who.trading = False
	var.menu_index = 0
	var.in_menu = None
	var.menu_name = ''
	var.menu_callback = None
	var.callback_args = None

def menu_select():
	if var.callback_args:
		var.menu_callback(var.in_menu[var.menu_index],args=var.callback_args)
	else:
		var.menu_callback(var.in_menu[var.menu_index])
	
def remove_menu_item(item):
	if item['count']==1:
		var.in_menu.remove(item)
	else: item['count']-=1

def get_item_price(item):
	"""Returns the price of an item.
	
	Shops are only allowed to hold a certain amount of goods (100 of any item.)
	After this limit is reached, another shop must open to store the overflow.
	As the supply of an item decreases, the price increases, and the seller
	will recieve a bonus for selling this type of item while its supply is
	low.
	
	Formula: base_price + (100-supply)
	
	But until all of this gets implemented, we'll just return the base price
	"""
	return item['price']