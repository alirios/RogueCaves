import random, life, var

def log(text):
	if len(var.history)>=5:
		if var.output=='pygame':
			var.log.fill(fgcolor=(255,0,0),region=(0,var.window_size[1]-6,var.window_size[0],6))
		
		var.history.pop(0)
	
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

def get_item_name(item):
	if item['type']=='cup':
		if item.has_key('contains') and item['contains']:
			if item['volume'] == item['volume_max']:
				return '%s %s filled with %s' % (item['material'],item['name'],item['contains'])
			elif item['volume'] <= float(item['volume_max'])/2:
				return '%s %s filled halfway with %s' %\
					(item['material'],item['name'],item['contains'])
	else:
		return item['name']

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
	random.seed()
	if len(get_alife_with_gender('male')) > len(get_alife_with_gender('female')):
		_male = False
	else:
		_male = True
	
	_ret =  life.human(male=_male)
	_ret.z = 1
	_ret.level = var.world.get_level(_ret.z)
	
	#Now we generate some stats here based on traits which 
	#are randomly chosen, and determine the 'base' of each
	#ALife.
	_attractive_score = 0
	_high_attractions_score = 0
	_mid_attractions_score = 0
	_low_attractions_score = 0
	
	#"High" attractions are typically more superficial and have a higher
	#chance of changing.
	_high_attractions = ['looks','status','power','wealth','strength']
	
	#"Mid" attractions deal with the more concrete, unchanging values
	_mid_attractions = ['honest','charity','provider','skill']
	
	#"Low" attractions are the negative things
	_low_attractions = ['brash']
	
	_likes = ['dogs','pets','animals','food','cooked food','ale','cup','weapon']
	
	_rand_value = random.randint(0,10)
	if _rand_value>7:
		_ret.traits.append('athletic')
		_high_attractions_score+=2
		_mid_attractions_score+=1
		_attractive_score = 2
		_ret.speed_max = 1
		_ret.atk = 3
	elif _rand_value>4:
		_ret.traits.append('fit')
		_high_attractions_score+=1
		_mid_attractions_score+=2
		_low_attractions_score+=1
		_attractive_score = 4
		_ret.speed_max = 2
		_ret.atk = 2
	else:
		_ret.traits.append('slow')
		_mid_attractions_score+=1
		_low_attractions_score+=2
		_attractive_score = 6
		_ret.speed_max = 3
	
	_ret.speed = _ret.speed_max
	
	if random.randint(0,10)>_attractive_score:
		_ret.traits.append('attractive')
		_high_attractions_score+=1
	else:
		_mid_attractions_score+=1
	
	_ret.traits.append(random.choice(['brash','honest','shy']))
	_ret.traits.append(random.choice(['faithful']))
	
	_ret.attracted_to.extend(random.sample(_high_attractions,_high_attractions_score))
	_ret.attracted_to.extend(random.sample(_mid_attractions,_mid_attractions_score))
	#_ret.attracted_to.extend(random.sample(_low_attractions,_low_attractions_score))
	_ret.attracted_to.extend(random.sample(_low_attractions,1))
	
	#Now pick some things this ALife likes
	_ret.likes = random.sample(_likes,random.randint(2,4))
	
	for like in _ret.likes:
		_likes.remove(like)
	
	#and dislikes
	#_ret.dislikes = random.sample(_likes,random.randint(2,4))
	_ret.dislikes = ['ale']
	
	if job=='trade':
		if _male:
			_ret.icon['color'][0] = 'blue'
		else:
			_ret.icon['color'][0] = 'purple'
		_ret.skills = ['trade']
		_ret.pos = list(_ret.level.get_open_buildings_of_type('store')[0]['door'])
	elif job=='farmer':
		_ret.level = var.world.get_level(_ret.z)
		_building = _ret.level.get_open_buildings_with_items(['storage','stove'])[0]['name']
		_ret.claim_building(_building,'home')
		if _male:
			_ret.icon['color'][0] = 'red'
		else:
			_ret.icon['color'][0] = 'purple'
		for i in range(9):
			_ret.add_item_raw(21)
		_ret.skills = ['farm']
		_ret.pos = list(_ret.get_claimed('home',return_building=True)['door'])
	elif job=='barkeep':
		if _male:
			_ret.icon['color'][0] = 'blue'
		else:
			_ret.icon['color'][0] = 'purple'
		_ret.skills = ['barkeep']
		_ret.pos = list(_ret.level.get_open_buildings_of_type('store')[0]['door'])
	
	return _ret

def generate_dog():
	#obedient
	pass