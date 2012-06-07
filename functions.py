import random, life, var

def log(text):
	if len(var.history)>=5: var.history.pop(0)
	
	var.history.append(text)

def distance(pos1,pos2):
	return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

def get_id():
	var.id-=1
	return var.id

def get_name_by_gender(gender):
	if gender == 'male':
		return random.choice(var.names_male).strip()
	else:
		return random.choice(var.names_female).strip()

def get_dog_name_by_gender(gender):
	if gender == 'male':
		return random.choice(var.names_male_dogs).strip()
	else:
		return random.choice(var.names_female_dogs).strip()

def get_alife_with_gender(gender):
	return [life for life in var.life if life.gender==gender]

def get_alife_by_id(id):
	for life in var.life:
		if life.id == id: return life
	
	print 'OH MAN NO ALIFE WITH ID %s' % id
	return False

def get_phrase(type):
	_ret = [phrase['text'] for phrase in var.phrases if phrase['type']==type]
	
	return random.choice(_ret)

def sort_array_by_distance(items,pos):
	_ret = []
	_t = []
	
	for item in items:
		_dist = distance(item,pos)
		_temp = {'dist':_dist,'item':item}
		
		if not len(_t): _t.append(_temp);continue
		
		_lowest = 9001
		for _item in _t:
			if _item == item: continue
			if _temp['dist'] < _item['dist']:
				if _t.index(_item) < _lowest: _lowest = _t.index(_item)
		
		_t.insert(_lowest,_temp)
	
	for item in _t:
		_ret.append(item)
	
	return _ret

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

def generate_human(job):
	if len(get_alife_with_gender('male')) > len(get_alife_with_gender('female')):
		_gender = False
	else:
		_gender = True
	
	_ret =  life.human(male=_gender)
	_ret.z = 1
	_ret.level = var.world.get_level(_ret.z)
	
	#Now we generate some stats here based on traits which 
	#are randomly chosen, and determine the 'base' of each
	#ALife.
	_traits = []
	
	if random.randint(0,10)>7:
		_traits.append('athletic')
		_ret.speed_max = 1
		_ret.atk = 3
	elif random.randint(0,10)>4:
		_traits.append('fit')
		_ret.speed_max = 2
		_ret.atk = 2
	else:
		_traits.append('slow')
		_ret.speed_max = 3
	
	_ret.speed = _ret.speed_max
	
	#Determine their chance of being attractive here...
	_attractive_score = 0
	if 'athletic' in _traits: _attractive_score = 2
	elif 'fit' in _traits: _attractive_score = 4
	else: _attractive_score = 6
	
	if random.randint(0,10)>_attractive_score: _traits.append('attractive')
	
	#Here we get to stereotype!
	if 'attractive' in _traits:
		_ret.attracted_to.append('looks')
	
	_ret.traits = _traits[:]
	
	if job=='trade':
		_ret.icon['color'][0] = 'blue'
		_ret.skills = ['trade']
		_ret.pos = list(_ret.level.get_open_buildings_of_type('store')[0]['door'])
	elif job=='farmer':
		_ret.level = var.world.get_level(_ret.z)
		_building = _ret.level.get_open_buildings_with_items(['storage','stove'])[0]['name']
		_ret.claim_building(_building,'home')
		_ret.icon['color'][0] = 'red'
		for i in range(9):
			_ret.add_item_raw(21)
		_ret.skills = ['farm']
		_ret.pos = list(_ret.get_claimed('home',return_building=True)['door'])
	
	return _ret