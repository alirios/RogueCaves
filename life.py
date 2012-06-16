import pathfinding, functions, draw, var
import logging, random, time, copy, sys, re, os

class life:
	def __init__(self,player=False):
		self.player = player
		
		if not self.player:
			self.icon = {'icon':'@','color':['white',None]}
		
		self.id = functions.get_id()
		self.name = 'Default'
		self.hp = 10
		self.hp_max = 10
		self.speed = 0
		self.speed_max = 0
		self.pos = [0,0]
		self.last_pos = [0,0]
		self.z = 0
		self.xp = 0
		self.skill_level = 1
		self.seen = []
		self.path = None
		self.path_type = None
		self.path_dest = None
		self.mine_dest = None
		self.alignment = 0
		self.god = None
		self.owner = None
		
		self.atk = 1
		self.defe = 1
		self.dislike_at = 15
		
		self.weapon = None
		self.claims = []
		self.owned_land = []
		self.traits = []
		self.attracted_to = []
		self.likes = []
		self.dislikes = []
		self.history = []
		
		self.lowest = {'who':None,'score':0}
		self.highest = {'who':None,'score':0}
		self.task = {'what':None}
		self.task_delay = 0
		self.events = []
		self.limbs = {}
		
		self.thirst = 0
		self.thirst_timer_max = 100
		self.thirst_timer = self.thirst_timer_max
		self.thirsty_at = 50
		self.hunger = 0
		self.hunger_timer_max = 75
		self.hunger_timer = self.hunger_timer_max
		self.hungry_at = 75
		self.fatigue = 0
		self.fatigue_timer_max = 100
		self.fatigue_timer = self.fatigue_timer_max
		self.fatigued_at = 15
		self.items = []
		self.skills = []
		self.talents = []
		
		var.life.append(self)
	
	def save(self,keys={}):
		_keys = keys
		_keys['id'] = self.id
		_keys['name'] = self.name
		_keys['player'] = self.player
		_keys['icon'] = self.icon
		_keys['hp'] = self.hp
		_keys['hp_max'] = self.hp_max
		_keys['speed'] = self.speed
		_keys['speed_max'] = self.speed_max
		_keys['pos'] = self.pos
		_keys['last_pos'] = self.last_pos
		_keys['z'] = self.z
		_keys['xp'] = self.xp
		_keys['skill_level'] = self.skill_level
		_keys['race'] = self.race
		_keys['faction'] = self.faction
		_keys['task'] = copy.deepcopy(self.task)
		if _keys['task'] and _keys['task'].has_key('who') and _keys['task']['who']:
			_keys['task']['who'] = self.task['who'].id
		
		_keys['events'] = copy.deepcopy(self.events)
		for event in _keys['events']:
			if event['who']: event['who'] = event['who'].id
		
		_keys['claims'] = self.claims
		
		_keys['seen'] = []
		for seen in self.seen:
			_s = seen.copy()
			_s['who'] = _s['who'].id
			_keys['seen'].append(_s)
		
		_keys['path'] = self.path
		_keys['path_type'] = self.path_type
		_keys['path_dest'] = self.path_dest
		_keys['mine_dest'] = self.mine_dest
		_keys['alignment'] = self.alignment
		##TODO: Save god
		if self.owner:
			_keys['owner'] = self.owner.id
		else:
			_keys['owner'] = self.owner
		_keys['atk'] = self.atk
		_keys['defe'] = self.defe
		_keys['dislike_at'] = self.dislike_at
		##TODO: Save weapon
		_keys['task_delay'] = self.task_delay
		_keys['thirst'] = self.thirst
		_keys['thirst_timer'] = self.thirst_timer
		_keys['thirst_timer_max'] = self.thirst_timer_max
		_keys['thirsty_at'] = self.thirsty_at
		_keys['hunger'] = self.hunger
		_keys['hunger_timer'] = self.hunger_timer
		_keys['hunger_timer_max'] = self.hunger_timer_max
		_keys['hungry_at'] = self.hungry_at
		_keys['fatigue'] = self.fatigue
		_keys['fatigue_timer'] = self.fatigue_timer
		_keys['fatigue_timer_max'] = self.fatigue_timer_max
		_keys['fatigued_at'] = self.fatigued_at
		_keys['history'] = self.history
		
		_items = copy.deepcopy(self.items)
		for item in _items:
			#_keys['items'] = self.items
			if item.has_key('planted_by'):
				item['planted_by'] = item['planted_by'].id
			if item.has_key('from'):
				item['from'] = item['from'].id
		
		_keys['items'] = _items
		_keys['talents'] = self.talents
		_keys['traits'] = self.traits
		_keys['skills'] = self.skills
		_keys['likes'] = self.likes
		_keys['dislikes'] = self.dislikes
		_keys['limbs'] = self.limbs
		
		return _keys
	
	def load(self,keys):
		self.id = keys['id']
		self.name = keys['name']
		self.player = keys['player']
		
		if self.player:
			var.player = self
		
		self.icon = keys['icon']
		self.icon['icon'] = str(self.icon['icon'])
		self.hp = keys['hp']
		self.hp_max = keys['hp_max']
		self.speed = keys['speed']
		self.speed_max = keys['speed_max']
		self.pos = keys['pos']
		self.last_pos = keys['last_pos']
		self.z = keys['z']
		
		self.level = var.world.get_level(self.z)
		
		self.xp = keys['xp']
		self.skill_level = keys['skill_level']
		self.race = keys['race']
		self.faction = keys['faction']
		self.task = keys['task']
		
		self.events = keys['events']
		for event in self.events:
			if event['who']:
				event['who'] = functions.get_alife_by_id(event['who'])
		
		self.claims = keys['claims']
		for claim in self.claims:
			claim['where'] = str(claim['where'])
			claim['label'] = str(claim['label'])
		
		self.seen = keys['seen']
		self.path = keys['path']
		self.path_type = keys['path_type']
		self.path_dest = keys['path_dest']
		self.mine_dest = keys['mine_dest']
		self.alignment = keys['alignment']
		##TODO: Save god
		self.owner = keys['owner']
		self.atk = keys['atk']
		self.defe = keys['defe']
		self.dislike_at = keys['dislike_at']
		##TODO: Save weapon
		self.task_delay = keys['task_delay']
		self.thirst = keys['thirst']
		self.thirst_timer = keys['thirst_timer']
		self.thirst_timer_max = keys['thirst_timer_max']
		self.thirsty_at = keys['thirsty_at']
		self.hunger = keys['hunger']
		self.hunger_timer = keys['hunger_timer']
		self.hunger_timer_max = keys['hunger_timer_max']
		self.hungry_at = keys['hungry_at']
		self.fatigue = keys['fatigue']
		self.fatigue_timer = keys['fatigue_timer']
		self.fatigue_timer_max = keys['fatigue_timer_max']
		self.fatigued_at = keys['fatigued_at']
		self.history = keys['history'] 
		self.items = keys['items']
		self.talents = keys['talents']
		self.traits = keys['traits']
		self.skills = keys['skills']
		self.likes = keys['likes']
		self.dislikes = keys['dislikes']
		self.limbs = keys['limbs']
	
	def build_history(self):
		logging.debug('[ALife.%s.HistoryGen] Starting...' % (self.name))
		_history = copy.deepcopy(self.history)
		
		_out = open(os.path.join('data','history.txt'),'w')
		for entry in _history:
			if entry.has_key('to'):
				entry['to'] = functions.get_alife_by_id(entry['to']).name
			for word in entry['what'].split(' '):
				if word in ['with','from']: continue
				if entry.has_key(word):
					entry['what'] = entry['what'].replace(word,entry[word])
			
			if entry['from']==self.id:
				_out_string = self.name+' '
			else:
				_out_string = '%s saw %s ' % (self.name,functions.get_alife_by_id(entry['from']).name)
				entry['what'] = entry['what'].replace('ed ',' ')
			
			_out_string += entry['what']
			_out.write(_out_string+'\n')
		_out.close()
	
	def finalize(self):
		for seen in self.seen:
			seen['who'] = functions.get_alife_by_id(seen['who'])
		
		for item in self.items:
			if item.has_key('planted_by'):
				item['planted_by'] = functions.get_alife_by_id(item['planted_by'].id)
			if item.has_key('from'):
				item['from'] = functions.get_alife_by_id(item['from'].id)
		
		if self.task.has_key('what'):
			if self.task.has_key('who') and self.task['who']:
				self.task['who'] = functions.get_alife_by_id(self.task['who'])
			
			if self.task.has_key('where') and self.task['where']:
				self.task['where'] = str(self.task['where'])
		
		if self.owner:
			self.owner = functions.get_alife_by_id(self.owner)

	def add_event(self,what,score,who=None,where=None,items=[],delay=0):
		for event in self.events:
			if event['what'] == what and event['who'] == who:
				#logging.debug('[ALife.%s.Event] Updated %s: %s -> %s' %
				#	(self.name,event['what'],event['score'],score))
				if where: event['where'] = where
				event['items'] = items
				event['score'] = score
				return False
		
		#logging.debug('[ALife.%s.Event] Added: %s, score %s' % (self.name,what,score))
		self.events.append({'what':what,'score':score,'who':who,'where':where,'delay':delay,\
			'items':items})
		return True
	
	def get_event(self):
		_highest = {'what':None,'score':-1}
		for event in self.events:
			if event['score']>=_highest['score']:
				_highest['what'] = event['what']
				_highest['ret'] = event
				_highest['score'] = event['score']
		
		if _highest['what']:
			return _highest['ret']
		else:
			return _highest
	
	def remove_event(self,what):
		for event in self.events:
			if event['what'] == what:
				self.events.remove(event)
				return True
		
		return False
	
	def announce(self,**kargv):
		_broadcast = {'from':self.id}
		_broadcast.update(kargv)
		
		_in_building = self.in_building()
		if _in_building:
			_broadcast['where'] = _in_building['name']
		
		self.history.append(_broadcast)
		
		for who in var.life:
			if who == self: continue
			if self.z == who.z and self.can_see(who.pos):
				who.receive_announce(_broadcast)
	
	def receive_announce(self,what):
		self.history.append(what)
	
	def add_item(self,item):
		"""Helper function. Originally copied the item, added it to the items
		array, and returned itself. No longer copies."""
		#TODO: Should we copy the item?
		#_i = item.copy()
		item['owner_id'] = self.id
		item['pos'] = tuple(self.pos)
		self.items.append(item)
		
		return item
	
	def add_item_raw(self,item):
		"""Returns a raw (new) copy of an item from the global items array
		and adds it to the items array."""
		_i = var.items[str(item)].copy()
		_i['pos'] = tuple(self.pos)
		_i['owner_id'] = self.id
		self.items.append(_i)
		
		return _i
	
	def buy_item(self,item):
		"""Removes item from menu and adds it to the items array."""
		functions.remove_menu_item(item)
		self.level.remove_item_at(item['item'],item['item']['pos'])
		self.add_item(item['item'])

	def buy_item_from_shop_alife(self,items,where):
		"""Helper function for ALife. Buy 'item' from 'where'"""
		##TODO: We aren't adding the original object to the buyer's item array
		
		for item in items:
			for _item in self.level.get_all_items_in_building(where):
				if _item['tile'] == item or _item['type'] == item:
					if not self.level.remove_item_from_building(_item,where):
						print 'STOP'
						sys.exit()
					_i = self.add_item(_item)
					logging.debug('[ALife.%s] Bought %s from %s' %
						(self.name,_i['name'],where))
		
					self.announce(what='bought item from where',item=item)
					break
		
		return False
	
	def buy_item_type_from_alife(self,type,who):
		if self.get_relationship_with(who)<=self.dislike_at:
			who.remove_event('serve_item_to')
		else:
			who.add_event('serve_item_to',75,who=self,items=type)
	
	def serve_item_to(self,type,who):
		if type == 'drink' and 'barkeep' in self.skills:
			_give_cup = None
			_fill_cup = None
			_has_cups = self.get_items(type='cup')
			_stored_cups = self.level.get_all_items_in_building_of_type(self.get_claimed('work'),'cup')
			_stored_drinks =\
				self.level.get_all_items_in_building_of_type(self.get_claimed('work'),'container')
			
			if _has_cups:
				for cup in _has_cups:
					if cup['contains']:
						_give_cup = cup
						break
					else:
						_fill_cup = cup
						break
			elif _stored_cups:
				self.pick_up_item_at(_stored_cups[0]['pos'],'cup')
			
			if _give_cup:
				if not who == self:					
					self.go_to_and_do(who.pos,
						self.give_item_to,
						first=_give_cup,
						second=who)
				
				if self.pos == who.pos:
					self.remove_event('serve_item_to')
					self.announce(what='served item to',
						item=functions.get_item_name(_give_cup),
						to=who.id)
				
			elif _fill_cup and _stored_drinks:
				self.go_to_and_do(_stored_drinks[0]['pos'],
					self.fill_container,
					first=_fill_cup,
					second=_stored_drinks[0])
	
	def give_item_to(self,item,who):
		"""Gives item to ALife"""
		item['from'] = self
		who.add_item(item)
		self.items.remove(item)
		
		logging.debug('[ALife.%s] Gave %s to %s' %
			(self.name,functions.get_item_name(item),who.name))
		
		_person = self.get_relationship_with(who)
		
		_likes = who.does_like_item(item)
		_dislikes = who.does_dislike_item(item)
		
		self.say_phrase('give_item',item=item,other=who,action=True)
		
		if _person['score']>self.dislike_at:
			if _likes:
				if 'brash' in who.traits:
					who.say_phrase('receive_item_positive_brash',item=item,other=self)
					
					for like in _likes:
						if not like in _person['likes']:
							_person['likes'].append(like)
							logging.debug('[ALife.%s] Learned that %s likes %s.' %
								(self.name,who.name,like))
				
				elif 'shy' in who.traits:
					who.say_phrase('receive_item_positive_shy',item=item,other=self)
				else:
					who.say_phrase('receive_item_positive',item=item)
					
				logging.debug('[ALife.%s] Took the %s from %s gladly!' %
					(who.name,functions.get_item_name(item),self.name))
			elif _dislikes:
				if 'brash' in who.traits:
					who.say_phrase('receive_item_negative_brash',item=item)
					
					for dislike in _dislikes:
						if not dislike in _person['dislikes']:
							if not item['type'] in _person['dislikes']:
								_person['dislikes'].append(dislike)
								logging.debug('[ALife.%s] Learned that %s dislikes %s.' %
									(self.name,who.name,dislike))
					
				elif 'honest' in who.traits:
					who.say_phrase('receive_item_negative_honest',item=item)
					
					for dislike in _dislikes:
						if not dislike in _person['dislikes']:
							if not dislike in _person['dislikes']:
								_person['dislikes'].append(dislike)
								logging.debug('[ALife.%s] Learned that %s dislikes %s.' %
									(self.name,who.name,dislike))
					
				elif 'shy' in who.traits:
					who.say_phrase('receive_item_negative_shy',item=item)
				else:
					who.say_phrase('receive_item_negative_fake',item=item,other=self)
				
				logging.debug('[ALife.%s] Reluctantly took the %s from %s.' %
					(who.name,functions.get_item_name(item),self.name))
			else:
				who.say_phrase('thank_you',item=item,other=self)
		else:
			#if 'brash' in who.traits:
			#	who.
			logging.debug('[ALife.%s] Did not like the %s from %s.' %
				(who.name,functions.get_item_name(item),self.name))
			
			##TODO: Anger?
			#who.destroy_item(item)
			who.announce(what='threw item at person',
				person=self.id,
				item=functions.get_item_name(item),
				why='did not like item')
			who.throw_item(item,self.pos)
		
		logging.debug('[ALife.%s] Relationship with %s: %s' %
			(self.name,who.name,_person['score']))
		
		return			
	
	def sell_item(self,item,**kargv):
		"""Removes item from inventory and adds it to the items array."""
		functions.remove_menu_item(item)
		item['item']['traded'] = True
		
		for _item in self.items:
			if _item['name'] == item['item']['name']:
				self.items.remove(_item)
				break
		
		kargv['args']['sell_to'].add_item(item['item'])
	
	def sell_item_alife(self,item,who):
		"""Helper function for ALife. Sells 'item' to 'who'"""
		self.items.remove(item)
		item['traded'] = True
		
		for price in range(item['price']):
			self.add_item_raw(20)
		
		who.add_item(item)
		
		logging.debug('[ALife.%s] Sold %s to %s' %
			(self.name,item['name'],who.name))
	
	def destroy_item(self,item):
		_str = 'smashes the %s.' % functions.get_item_name(item)
		if item.has_key('material'):
			if item['material']=='clay': _str += ' Bits of clay fall everywhere!'
		#else:
		#	#self.say('smashes the %s!' % functions.get_item_name(item),action=True)
		
		if item.has_key('contains'): _str += ' %s stains the ground!' % item['contains']
		
		self.say(_str,action=True)
		self.items.remove(item)		
		logging.debug('[ALife.%s] Destroys the %s' % (self.name,functions.get_item_name(item)))
		self.announce(what='destroyed item',item=functions.get_item_name(item))
	
	def throw_item(self,item,at):
		self.items.remove(item)
		_str = 'throws the %s! ' % functions.get_item_name(item)
		logging.debug('[ALife.%s] Threw %s at %s' %
			(self.name,functions.get_item_name(item),at))
		
		for life in var.life:
			if not life.z==self.z or life==self: continue
			if tuple(item['pos']) == tuple(life.pos):
				_str += 'It hits %s! The %s falls to the ground.' % (life.name,item['name'])
				logging.debug('[ALife.%s] The %s hit %s' %
					(self.name,functions.get_item_name(item),life.name))
				self.announce(what='hit person with item',
					person=life.id,
					item=functions.get_item_name(item))
				#self.level.items[item['pos'][0]][item['pos'][1]].append(item)
				self.level.place_item(tuple(item['pos']),item)
				self.say(_str,action=True)
				return		
		
		_i = 0
		_last_pos = tuple(item['pos'])
		for pos in draw.draw_diag_line(self.pos,at):
			print 'travel'
			if self.level.map[pos[0]][pos[1]] in var.solid:
				#self.level.items[_last_pos[0]][_last_pos[1]].append(item)
				self.level.place_item(_last_pos,item)
				_str += 'It hits the wall and falls to the ground.'
				break
			
			if _i>=6:
				_str += 'It falls to the ground'
				self.level.place_item(tuple(item['pos']),item)
				break
			
			for life in var.life:
				if not life.z==self.z or life==self: continue
				if pos == tuple(life.pos):
					_str += 'It hits %s! The %s falls to the ground.' % (life.name,item['name'])
					logging.debug('[ALife.%s] The %s hit %s' %
						(self.name,functions.get_item_name(item),life.name))
					self.announce(what='hit person with item',
						person=life.id,
						item=functions.get_item_name(item))
					#self.level.items[pos[0]][pos[1]].append(item)
					self.level.place_item(tuple(pos),item)
					break
			
			_last_pos = pos
			_i+=1
	
	def push(self,who):
		self.announce(what='pushed person',person=who.id)
		_score = self.get_relationship_with(who)['score']
		logging.debug('[ALife.%s] Pushed %s (%s) %s' % (self.name,who.name,_score,self.lowest['score']))
		
		_open = self.level.get_open_space_around(who.pos,dist=1)
		if tuple(self.pos) in _open: _open.remove(tuple(self.pos))
		if tuple(who.pos) in _open: _open.remove(tuple(who.pos))
		
		if _open:
			who.pos = list(random.choice(_open))
	
	def equip_item(self,item):
		"""Helper function. Equips item 'item'"""
		if item.has_key('item'): item=item['item']
		
		if item['type'] == 'weapon':
			if self.weapon==item:
				functions.log('You\'re already holding the %s!' % (self.get_weapon_name()))
				return
			
			self.weapon = item
			if self.player: functions.log('You equip the %s.' % (self.get_weapon_name()))
			return
	
	def place_item(self,item,pos):
		if self.player: _pos = (self.pos[0]+pos[0],self.pos[1]+pos[1])
		else: _pos = pos
		if 0>_pos[0] or _pos[0]>=self.level.size[0]: return
		if 0>_pos[1] or _pos[1]>=self.level.size[1]: return
		if len(self.level.items[_pos[0]][_pos[1]]): return
		
		_items = self.get_items(tile=item)
		
		if len(_items): _item=_items[0]
		else: return False
		
		if _item['type'] == 'seed':
			if not self.level.map[_pos[0]][_pos[1]] in var.DIRT:
				if not var.server: var.buffer[_pos[0]][_pos[1]] = None
				self.level.map[_pos[0]][_pos[1]] = random.choice(var.DIRT)
				
				if self.weapon and self.weapon['name']=='hoe':
					self.weapon['status']='dirt'
					self.announce(what='tilled earth with hoe for item',
						item=var.items[str(item)]['name'],
						hoe=functions.get_item_name(self.weapon))
				else:
					self.announce(what='tilled earth for item',
						item=var.items[str(item)]['name'])
				
				self.announce(what='planted item',item=var.items[str(item)]['name'])
				
				return False
			_item['planted_by'] = self
			_item['pos'] = _pos
			self.level.items[_pos[0]][_pos[1]].append(_item)
			self.items.remove(_item)
		
		return True
	
	def flag_item(self,item,flag):
		item[flag] = True
		logging.debug('[ALife.%s] Flagged %s at %s with \'%s\'' %
			(self.name,item['name'],item['pos'],flag))
		
		return True
	
	def put_item_of_type(self,type,pos):
		"""Dumps a single item of 'type' in a container at 'pos'"""
		##TODO: Could probably merge this with the below function
		##TODO: Would calling self.level.items[pos[0]][pos[1]] be easier/safer?
		for _item in self.level.get_items(type='storage'):
			_found = False
			if tuple(_item['pos']) == tuple(pos):
				_found = True
				for item in self.items:
					if item['type'] == type:
						self.items.remove(item)
						item['pos'] = pos
						_item['items'].append(item)
						logging.debug('[ALife.%s] Put %s in chest at %s' %
							(self.name,item['name'],pos))
						break
				break
	
	def put_all_items_of_type(self,type,pos):
		"""Dumps items of 'type' into a container at 'pos'"""
		#TODO: Would calling self.level.items[pos[0]][pos[1]] be easier/safer?
		for _item in self.level.get_tems('storage'):
			_found = False
			if tuple(_item['pos']) == tuple(pos):
				_found = True
				for item in self.items:
					if item['type'] == type:
						self.items.remove(item)
						item['pos'] = pos
						_item['items'].append(item)
				
				break
	
	def put_all_items_tagged(self,tag,pos):
		"""Dumps items with flag 'tag' into a container located at 'pos'"""
		#TODO: Would calling self.level.items[pos[0]][pos[1]] be easier/safer?
		for _item in self.level.get_all_items_of_type('storage'):
			_found = False
			if tuple(_item['pos']) == tuple(pos):
				_found = True
				for item in self.items:
					if item.has_key(tag) and item[tag]:
						self.items.remove(item)
						_item['items'].append(item)
				
				break
	
	def get_items(self,**kargv):
		"""Returns items matching all values in kargv"""
		_ret = []
		
		for item in self.items:
			_match = kargv.keys()
			for key in kargv:
				if item.has_key(key) and item[key]==kargv[key]:
					_match.remove(key)
					
					if not _match:
						_ret.append(item)
						break
		
		return _ret
	
	def get_items_ext(self,**kargv):
		"""Returns items matching all values in kargv. Assumes each arg is a list"""
		_ret = []
		
		for item in self.items:
			_match = kargv.keys()
			for key in kargv:
				if item.has_key(key) and item[key] in kargv[key]:
					_match.remove(key)
					
					if not _match:
						_ret.append(item)
						break
		
		return _ret
	
	def get_all_items_tagged(self,tag):
		"""Returns items with flag 'tag'."""
		_ret = []
		
		for item in self.items:
			if item.has_key(tag) and item[tag]:
				_ret.append(item)
		
		return _ret
	
	def get_all_cookable_items(self,where):
		_ret = []
		_food = self.level.get_items_in_building(where,type='food')
		_food.extend(self.get_items(type='food'))
		
		_ret.extend(_food)
		
		return _ret
	
	def get_all_growing_crops(self):
		"""Returns all items still being grown by this ALife."""
		_ret = []
		
		for crop in self.level.get_all_items_tagged('planted_by',ignore_storage=True):
			if crop['type']=='seed' and crop['planted_by']==self:
				_ret.append(crop)
		
		return _ret
	
	def get_all_grown_crops(self):
		"""Returns all items grown by this ALife that have yet to been picked/traded."""
		_ret = []
		
		for crop in self.level.get_all_items_tagged('planted_by',ignore_storage=True):
			if crop['type']=='food' and crop['planted_by']==self and not crop.has_key('traded'):
				_ret.append(crop)
		
		return _ret
	
	def get_all_gifts_from(self,who):
		"""Returns all gifts received from 'who'"""
		_ret = []
		
		for item in self.items:
			if item.has_key('from') and item['from']==who:
				_ret.append(item)
		
		_building = self.get_claimed('home')
		if _building:
			for item in self.level.get_all_items_in_building(self.get_claimed('home')):
				if item.has_key('from') and item['from']==who:
					_ret.append(item)	
		
		return _ret
	
	def get_top_love_interests(self):
		"""Returns this ALife's top love interests"""
		_ret = []
		_t = []
		
		for item in self.seen:
			_temp = {'score':item['score'],'item':item}
			
			if not len(_t): _t.append(_temp);continue
			
			_highest = 0
			for _item in _t:
				if _item['item'] == item: continue
				if _temp['score'] > _item['score']:
					if _t.index(_item) > _highest: _highest = _t.index(_item)
			
			_t.insert(_highest,_temp)
		
		for item in _t:
			_who = item['item']['who']
			if not _who.gender == self.gender and self.race == _who.race:
				_ret.append({'who':_who,'score':item['score']})
		
		return _ret
	
	def get_all_relationships(self):
		"""Returns this ALife's relationships"""
		_ret = []
		_t = []
		
		for item in self.seen:
			_t.append({'score':item['score'],'item':item})
		
		for item in _t:
			_who = item['item']['who']
			if self.race == _who.race:
				_ret.append({'who':_who,'score':item['score']})
		
		return _ret
	
	def get_relationship_with(self,who):
		"""Returns this ALife's relationship with 'who'"""
		for person in self.seen:
			if person['who'] == who:
				return person
		
		return False
	
	def get_item_id(self,id):
		"""Returns item of id 'id'"""
		for item in self.items:
			if item['tile'] == id:
				return item
		
		return False
	
	def get_nearest_store(self,items=None):
		"""Returns nearest store to this ALife"""
		_lowest = {'name':None,'dist':9001}
		
		for building in self.level.get_all_buildings_of_type('store'):
			if not building['owner']: continue
			if not tuple(building['owner'].pos) in building['walking_space']: continue
			if items:
				_has_item = False
				for item in self.level.get_all_items_in_building(building['name']):
					if item['type'] in items: _has_item = True;break
			
				if not _has_item: continue
			else:
				_has_item = True
			
			_dist = functions.distance(self.pos,building['door'])
			
			if _dist < _lowest['dist']:
				_lowest['name'] = building['name']
				_lowest['dist'] = _dist
		
		if not _lowest['name']: return False
		return _lowest['name']
	
	def get_nearest_building_of_type(self,type,open=True):
		_lowest = {'name':None,'dist':9001}
		
		for building in self.level.get_all_buildings_of_type(type):
			if not building['owner']: continue
			if not tuple(building['owner'].pos) in building['walking_space'] and open: continue
			_dist = functions.distance(self.pos,building['door'])
			
			if _dist < _lowest['dist']:
				_lowest['name'] = building['name']
				_lowest['dist'] = _dist
		
		if not _lowest['name']: return False
		return _lowest['name']
	
	def get_money(self):
		"""Returns amount of money the ALife has."""
		_ret = 0
		
		for ore in self.get_items(type='ore'):
			_ret+=ore['price']
		
		return _ret
	
	def get_farm_speed(self):
		"""Returns speed this ALife can farm at."""
		if self.weapon and self.weapon['name']=='hoe': return self.weapon['speed']
		
		return 1#8
		
	def get_open_stoves(self,where):
		"""Returns all stoves in 'where' either done cooking or empty"""
		_ret = []
		_stoves = self.level.get_all_items_in_building_of_type(where,'stove')
		
		for stove in _stoves:
			if stove['cooking'] and stove['cooking']['type'] == 'cooked food':
				_ret.append(stove)
			elif not stove['cooking']: _ret.append(stove)
		
		return _ret

	def get_done_stoves(self,where):
		"""Returns all stoves in 'where' done cooking"""
		_ret = []
		_stoves = self.level.get_all_items_in_building_of_type(where,'stove')
		
		for stove in _stoves:
			if stove['cooking'] and stove['cooking']['type'] == 'cooked food':
				_ret.append(stove)
		
		return _ret
		
	def get_open_beds(self,where):
		"""Returns all empty beds in 'where'"""
		_ret = []
		_beds = self.level.get_all_items_in_building_of_type(where,'bed')
		
		for bed in _beds:
			if not bed['owner']:
				_ret.append(bed)
		
		return _ret
	
	def get_past_event(self,*kargv):
		"""Gets historic event that matches the keys/values in kargv"""
		_ret = []
		search = kargv[0]
		
		for event in self.history:
			_matches = []
			for key in search:
				if event.has_key(key):
					if event[key]==search[key]:
						_matches.append(key)
					else:
						_matches = []
						break
				else:
					_matches = []
					break
				
			if len(_matches)==len(search):
				_ret.append(event)
		
		return _ret
	
	def is_in_bed(self):
		"""Helper function. Is this ALife sleeping?"""
		_beds = self.level.get_all_items_of_type('bed')
		
		for bed in _beds:
			if bed['owner'] == self:
				return bed
		
		return False
	
	def does_like_item(self,item):
		"""Returns a list of things this ALife likes about 'item'"""
		_ret = []
		
		if item['type'] in self.likes: _ret.append(item['type'])
		if item.has_key('contains') and item['contains'] in self.likes:
			_ret.append(item['contains'])
		
		return _ret
	
	def does_dislike_item(self,item):
		"""Returns a list of things this ALife likes about 'item'"""
		_ret = []
		
		if item['type'] in self.dislikes: _ret.append(item['type'])
		if item.has_key('contains') and item['contains'] in self.dislikes:
			_ret.append(item['contains'])
		
		return _ret
	
	def on_enemy_spotted(self,who):
		pass
	
	def on_friendly_spotted(self,who):
		pass
	
	def on_wake(self):
		logging.debug('[ALife.%s] Woke up' % self.name)
	
	def on_sleep(self):
		logging.debug('[ALife.%s] Fell asleep' % self.name)
	
	def on_submission(self,who):
		logging.debug('[ALife.%s] Submission, scared of %s' % (self.name,who.name))
	
	def claim_real_estate(self,pos,size,label):
		"""Helper function. Registers land at 'pos' with 'size' as 'label'"""
		self.owned_land.append({'where':pos,'size':size,'label':label})
		self.level.claim_real_estate((pos[0],pos[1]),(size[0],size[1]))
		
		logging.debug('[ALife.%s.Land] Claimed %s,%s with size %s,%s as %s'
			% (self.name,pos[0],pos[1],size[0],size[1],label))
	
	def get_owned_land(self,label):
		for entry in self.owned_land:
			if entry['label'] == label:
				return entry
		
		return False
	
	def claim_work_at(self,type):
		if self.task.has_key('where'):
			_owner = self.level.get_room(self.task['where'])['owner']
			if _owner and not _owner == self:
				self.remove_event(self.task['what'])
				_building = self.level.get_open_buildings_of_type(type)[0]['name']
			else:
				_building = self.level.get_open_buildings_of_type(type)[0]['name']
		else:
			_building = self.level.get_open_buildings_of_type(type)[0]['name']
		
		return _building
	
	def claim_building(self,where,label):
		_temp = {'where':where,'label':label}
		_room = self.level.get_room(where)
		_room['owner'] = self
		
		if label == 'home':
			_room['name'] = '%s\'s house' % self.name
		#elif label == 'work':
		#	_room['name'] = '%s\'s shop' % self.name
		
		_temp['where'] = _room['name']
		
		self.claims.append(_temp)
		logging.debug('[ALife.%s.Land] Claimed %s as %s'
			% (self.name,where,label))
	
	def get_claimed(self,label,return_building=False):
		for claim in self.claims:
			if claim['label'] == label:
				if return_building: return self.level.get_room(claim['where'])
				return claim['where']
		
		return False
	
	def say(self,what,action=False):
		if not what: return False
		logging.debug('[ALife.%s.say] %s' %(self.name,what))
		
		"""Sends a string prefixed with the ALife's name to the log."""
		if self.z == var.player.z and self.can_see(var.player.pos):
			if action:
				if var.player.name in what:
					what = what.replace(var.player.name,'you')
				functions.log('%s %s' % (self.name,what))
			else: functions.log('%s: %s' % (self.name,what))
	
	def say_phrase(self,type,action=False,**kargv):
		"""Retrieves a phrase and formats it accordingly"""
		_phrase = functions.get_phrase(type)
		_tags = [tag.strip('<>') for tag in re.findall('<[\d\w\s.]*>',_phrase)]
		for tag in _tags:
			_split = tag.split('.')
			
			if _split[0]=='other':
				if _split[1]=='name': _phrase = _phrase.replace(tag,kargv['other'].name)
			elif _split[0]=='building':
				if _split[1]=='name': _phrase = _phrase.replace(tag,kargv['building']['name'])
			elif _split[0]=='self':
				if _split[1]=='gender':
					if self.gender=='male': _phrase = _phrase.replace(tag,'his')
					else: _phrase = _phrase.replace(tag,'her')
			elif _split[0]=='item':
				if _split[1]=='name':
					_phrase = _phrase.replace(tag,functions.get_item_name(kargv['item']))
				else:
					_phrase = _phrase.replace(tag,kargv['item'][_split[1]])
		
		_phrase = _phrase.replace('<','').replace('>','')
		self.say(_phrase,action=action)
	
	def attack(self,who):
		"""Performs attack on object 'who'"""
		if who.race in ['zombie']:
			if self.player: functions.log('You swing at the %s!' % (who.race))
			elif who.player: functions.log('The %s swings at you!' % (who.race))
		elif who.race in ['human']:
			if self.player: functions.log('You swing at %s!' % (who.name))
			elif who.player: functions.log('%s swings at you!' % (self.name))
			#else: functions.log('%s swings at %s!' % (self.name,who.name))
		else:
			if self.player: functions.log('You swing at %s!' % (who.name))
			elif who.player: functions.log('The %s swings at you!' % (self.race))
		
		self.hunger_timer -= 5
		self.xp += 1
		
		if self.weapon:
			_dam = random.randint(self.atk,self.weapon['damage']+self.atk)
			if _dam >= self.weapon['damage']:
				if self.player:
					functions.log('Your %s hits for maximum damage!' % self.weapon['name'])
				elif who.player:
					functions.log('%s hits you with a %s for maximum damage!' % 
						(self.name,self.get_weapon_name()))
				
				if self.weapon['sharp']:
					self.weapon['status'] = 'the blood of %s the %s' % (who.name,who.race)
					
					_pos = random.choice([(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),\
						(-1,1),(0,1),(1,1)])
					_x = who.pos[0]+_pos[0]
					_y = who.pos[1]+_pos[1]
					
					if not 0>_x and not _x>=self.level.size[0] and\
						not 0>_y and not _y>=self.level.size[1]:
						self.level.tmap[_x][_y] = random.randint(150,255)
						
			
			who.hp -= _dam
			logging.debug('[ALife.%s] Attacked %s for %s damage' % (self.name,who.name,self.atk))
			self.announce(what='attacked person',person=who.id,damage=_dam)
		else:
			_dam = self.atk
			
			if who.race == 'human':
				_hit_limb = random.choice(['left arm','right arm'])
				
				if who.limbs[_hit_limb]['skin']['bruised']<3:
					who.limbs[_hit_limb]['skin']['bruised']+=1
					#logging.debug('[ALife.%s] Hit %s in the %s' % (self.name,who.name,_hit_limb))
				elif who.limbs[_hit_limb]['skin']['bruised']==3:
					who.limbs[_hit_limb]['skin']['bruised']+=1
					_what = 'Hit %s in the %s, bruising the skin severely!' % (who.name,_hit_limb)
					logging.debug('[ALife.%s] %s' % (self.name,_what))
					_dam += 2
				elif who.limbs[_hit_limb]['muscle']['bruised']<3:
					print 'HEREERERE'
					who.limbs[_hit_limb]['muscle']['bruised']+=1
					#_what = 'Hit %s in the %s, bruising the muscle severely!' % (who.name,_hit_limb)
					#logging.debug('[ALife.%s] Hit %s in the %s' % (self.name,who.name,_hit_limb))
					_dam += 2
				elif who.limbs[_hit_limb]['muscle']['bruised']==3:
					who.limbs[_hit_limb]['muscle']['bruised']+=1
					_what = 'Hit %s in the %s, bruising the muscle severely!' % (who.name,_hit_limb)
					logging.debug('[ALife.%s] %s' % (self.name,_what))
					_dam += 4
				
			who.hp -= _dam
			logging.debug('[ALife.%s] Attacked %s for %s damage' % (self.name,who.name,_dam))
			self.announce(what='attacked person',person=who.id,damage=_dam)
		
		if who.hp<=0:
			if who.race in ['zombie']:
				if self.player: functions.log('You slay the %s!' % (who.race))
				elif who.player: functions.log('The %s slays you!' % (who.race))
			else:
				if self.player: functions.log('You slay %s the %s!' % (who.name,who.race))
				elif who.player: functions.log('The %s slays you!' % (self.race))
			
			self.xp += who.xp
			
			for item in who.items:
				if self.player: functions.log('Found %s!' % item['name'])
				self.add_item(item)
				
				if not self.weapon and item['type']=='weapon':
					self.equip_item(item)
			
			if self.god:
				self.god.on_kill(self,who)
			
			who.kill()
		
		if self.xp>=self.skill_level*var.skill_mod:
			self.xp-=self.skill_level*var.skill_mod
			self.skill_level+=1
			self.hp = self.hp_max
	
	def has_seen(self,who):
		"""Helper function. Searches 'seen' for object 'who'"""
		for seen in self.seen:
			if seen['who'] == who:
				return seen
		
		return False
	
	def in_building(self,pos=None,name=None):
		"""Returns the building the ALife is currently in
		
		if 'name', check to see if the current building is 'name'
		if 'pos', check to see if 'pos' is in 'name'
		"""
		
		if not pos: pos = tuple(self.pos)
		
		for room in self.level.rooms:
			if pos in room['walking_space']:
				if name:
					if room['name'] == name: return room
				else:
					return room
		
		return False
	
	def can_see(self,pos):
		"""Performs a series of checks to determine if the ALife can see 'pos'"""
		_seen = True
		_l = draw.draw_diag_line(self.pos,pos)
		
		_blocking = []
		#for life in var.life:
		#	if not life.z == self.z or self == life: continue
		#	_blocking.append((life.pos[0],life.pos[1]))
		
		if tuple(pos) in _blocking:
			_blocking.remove(tuple(pos))

		for _pos in _l:
			if self.level.map[_pos[0]][_pos[1]] in var.solid:
				_seen = False
				break
			
			if not _l.index(_pos)==len(_l)-1 and self.level.has_solid_item_at(_pos):
				_seen = False
				break
			
			if _pos in _blocking:
				_seen = False
				break
		
		return _seen
	
	def can_see_ext(self,pos):
		"""Legacy function. Uses A* to determine if the ALife can see 'pos'"""
		#TODO: Deprecated. Marked for removal in 2012A."""
		_seen = True
		_path = self.path = pathfinding.astar(start=self.pos,end=pos,\
			omap=self.level.map,size=self.level.size).path
		
		if _path:
			return True
		else:
			return False
	
	def can_traverse(self,pos):
		"""Checks to see if the ALife can travel to 'pos'"""
		_seen = True
		_l = draw.draw_diag_line(self.pos,pos)
		
		_blocking = []
		for life in var.life:
			if not life.z == self.z or self == life: continue
			_blocking.append((life.pos[0],life.pos[1]))
		
		if tuple(pos) in _blocking:
			_blocking.remove(tuple(pos))
		
		for _pos in _l:
			if self.level.map[_pos[0]][_pos[1]] in var.blocking:
				_seen = False
				break
			
			if not _l.index(_pos)==len(_l)-1 and self.level.has_solid_item_at(_pos):
				_seen = False
				break
			
			if _pos in _blocking:
				_seen = False
				break
		
		return _seen
	
	def place_tile(self,pos,tile):
		"""Places a tile of 'tile' at position 'pos'"""
		_pos = (self.pos[0]+pos[0],self.pos[1]+pos[1])
		if not self.level.map[_pos[0]][_pos[1]] in var.solid:
			self.level.map[_pos[0]][_pos[1]] = tile
			if _pos in self.level.walls:
				self.level.walls.remove(_pos)
			
			if not _pos in self.level.walking_space:
				self.level.walking_space.append(_pos)
	
	def tick(self):
		"""Performs a single tick, incrementing various counters."""
		self.hunger_timer -= 1
		self.thirst_timer -= 1
		self.fatigue_timer -= 1
		
		if self.hunger_timer <= 0:
			self.hunger_timer = self.hunger_timer_max
			self.hunger+=1
		
		if self.thirst_timer <= 0:
			self.thirst_timer = self.thirst_timer_max
			self.thirst+=1
		
		if self.fatigue_timer <= 0:
			self.fatigue_timer = self.fatigue_timer_max
			if self.is_in_bed():
				self.fatigue-=1
			else:
				self.fatigue+=1
		
		if self.pos == self.last_pos or self.z<1: return
		
		if self.race == 'human':
			for room in self.level.rooms:
				if room['owner'] == self: continue
				if not room['owner'] or \
					not tuple(room['owner'].pos) in room['walking_space']: continue
				if tuple(self.pos) in room['walking_space']:
					if not tuple(self.last_pos) in room['walking_space']:
						if room['owner'].get_relationship_with(self)>room['owner'].dislike_at: return
						room['owner'].say_phrase('enter_building',building=room,other=self)
				elif tuple(self.last_pos) in room['walking_space']:
					if not tuple(self.pos) in room['walking_space']:
						if room['owner'].get_relationship_with(self)>room['owner'].dislike_at: return
						room['owner'].say_phrase('leave_building',other=self)
	
	def fill_container(self,item,what):
		"""Fills 'item' with 'what'"""
		item['contains'] = what['contains']
		item['volume'] = item['volume_max']
		logging.debug('[ALife.%s] Filled the %s with %s' %
			(self.name,item['name'],what['contains']))
		self.announce(what='filled item with liquid',
			item=functions.get_item_name(item),
			liquid=what['contains'])
	
	def drink(self,what):
		##TODO: How much can they drink at one time?
		self.thirst -= 5
		what['volume'] -= 5
		
		if not what['contains']: return False
		
		logging.debug('[ALife.%s] Drank some %s from a %s' %
			(self.name,what['contains'],what['name']))
		
		#if what['contains'] in self.likes:
		if 'brash' in self.traits:
			self.say_phrase('drink_brash',action=True,item=what)
		elif 'shy' in self.traits:
			self.say_phrase('drink_shy',action=True,item=what)
		else:
			self.say_phrase('drink',action=True,item=what)
		
		if what['contains'] in self.dislikes:
			if 'brash' in self.traits:
				self.say_phrase('vomit_brash',action=True,item=what)
				self.announce(what='vomited',
					why='disliked contains in item',
					contains=what['contains'],
					item=functions.get_item_name(what))
				
				#If this item is from somebody, we can get mad at them!
				if what.has_key('from'):
					self.say_phrase('curse_brash',other=what['from'])
					self.announce(what='cursed',
						why='disliked contains in item from person',
						contains=what['contains'],
						item=functions.get_item_name(what),
						person=what['from'].id)
				
				if self.get_relationship_with(what['from'])['score']<=self.dislike_at:
					if self.can_see(what['from']['pos']):
						self.throw_item(what,what['from'].pos)
					else:
						self.destroy_item(what)
				
			else:
				self.say_phrase('vomit',action=True,item=what)
				self.announce(what='vomited',
					why='disliked contains in item',
					contains=what['contains'],
					item=functions.get_item_name(what))
			
			self.throw_item(what,what['from'].pos)
			#self.announce('what'='Threw item at'}
			
			self.thirst+=3
			self.hunger+=2
		#else:
		#	self.say_phrase('drink',action=True,item=what)
		
		if what['volume']<=0: what['contains'] = None
	
	def think(self):
		"""Tracks whether ALife on the current level have been seen for the
		first time, lost, or moved in the last tick."""
		for life in var.life:
			if life == self or not self.z == life.z: continue
			
			_temp = self.has_seen(life)
			
			if not self.z == life.z and _temp:
				if _temp and _temp['in_los']:
					_temp['in_los'] = False
			
			_l = draw.draw_diag_line(self.pos,life.pos)
			
			_seen = self.can_see(life.pos)
			
			if _seen:
				_seen = self.can_traverse(life.pos)
			
			if _seen and not life.z == self.z: _seen = False
			
			if _seen:
				if _temp:
					_temp['los'] = _l[:]
					_temp['in_los'] = True
					_temp['last_seen'] = life.pos[:]
				else:
					self.seen.append({'who':life,
						'los':_l,
						'in_los':True,
						'last_seen':life.pos[:],
						'likes':[],
						'dislikes':[],
						'score':0})
			else:
				if _temp and _temp['in_los']:
					_temp['in_los'] = False
		
		for seen in self.seen:
			if seen['in_los']:
				_score = self.judge(seen['who'])
				seen['score'] = _score
				
				if _score < 0 and _score <= self.lowest['score']:
					if seen['who'].hp<=0: continue
					self.lowest['who'] = seen['who']
					
					if _score < self.lowest['score']:
						self.on_enemy_spotted(self.lowest['who'])
					
					#print self.name,'is scared of',self.lowest['who'].name,_score
					self.lowest['score'] = _score
					self.lowest['last_seen'] = seen['last_seen'][:]
				elif self.lowest['who'] and self.lowest['who'] == seen['who']:
					self.lowest['score'] = _score
					#print self.name,'SET NEW SCORE',_score
				
				if _score >= 0:
					if _score >= self.highest['score']:
						self.highest['who'] = seen['who']
						
						if _score > self.highest['score']:
							self.on_friendly_spotted(self.highest['who'])
						
						self.highest['score'] = _score
						self.highest['last_seen'] = seen['last_seen'][:]
			
			else:
				if self.lowest['who'] == seen['who']:
					self.lowest['last_seen'] = seen['last_seen'][:]
				
				if self.highest['who'] == seen['who']:
					self.highest['last_seen'] = seen['last_seen'][:]
		
		if self.lowest['who']:
			#if self.judge(self)>=abs(self.judge(self.lowest['who'])):
			if self.add_event('attack',100,who=self.lowest['who']):
				if self.lowest['who'].player:
					self.lowest['who'].is_in_danger(self)
			#else:
			#	if self.add_event('flee',100,who=self.lowest['who']):
			#		self.remove_event('attack')
			#	self.task = 'flee'
			
			if self.get_relationship_with(self.lowest['who'])['score']>=0:
				#print self.name,'no longer scared of',self.lowest['who'].name
				self.lowest['who'] = None
				self.lowest['score'] = 0
				self.remove_event('attack')
		else:
			if self.task == 'attacking':
				self.task = None
				print 'SHOULD STOP ATTACKING NOW'
		
		_event = self.get_event()
		
		if _event and not self.task==_event:
			self.task = _event

	def think_finalize(self):
		if self.task['what'] == 'food':
			##TODO: Eventually sort this array by how good the food is
			_item = self.get_items(type='food')
			_item.extend(self.get_items(type='cooked food'))
			
			if _item:
				self.hunger = 0
				self.hunger_timer = self.hunger_timer_max
				self.items.remove(_item[0])
				self.remove_event(self.task['what'])
				self.task = None
				self.say('That was good!')
				logging.debug('[ALife.%s] Ate a %s.' % (self.name,_item[0]['name']))
			else:
				_items = []
				_wants = ['food','cooked food']
				
				for claim in self.claims:
					for item in self.level.get_all_items_in_building_of_type(claim['where'],_wants):
						_items.append(item)
				
				if _items:
					_item = functions.sort_item_array_by_distance(_items,self.pos)[0]
					self.pick_up_item_at(_item['pos'],_item['type'])
		elif self.task['what'] == 'mine':
			self.mine()
		elif self.task['what'] == 'deliver':
			if len(self.get_items(type='ore')):
				_pos = None
				_room = var.world.get_level(1).get_room('storage')
				_chest = None
				for pos in _room['walking_space']:
					for item in var.world.get_level(1).items[pos[0]][pos[1]]:
						if item['type']=='storage':
							for space in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
								if (pos[0]+space[0],pos[1]+space[1]) in _room['walking_space']:
									_pos = (pos[0]+space[0],pos[1]+space[1])
									_chest = item
									break
							break
				
				if tuple(self.pos) == _pos:
					self.put_all_items_of_type('ore',_chest['pos'])
					self.remove_event(self.task['what'])
					self.task = None
					self.mine_dest = None
				elif _pos:
					self.go_to(_pos,z=1)
		elif self.task['what'] == 'attack':
			if self.task['who'].hp>0:
				self.go_to(self.task['who'].pos,z=self.task['who'].z)
				
				if tuple(self.pos) == tuple(self.task['who'].pos):
					self.push(self.task['who'])
				
				_score = self.lowest['who'].get_relationship_with(self)
			
		elif self.task['what'] == 'run_shop':
			self.run_shop(self.task['where'])
		elif self.task['what'] == 'run_forge':
			self.run_forge(self.task['where'])
		elif self.task['what'] == 'run_bar':
			self.run_bar(self.task['where'])
		elif self.task['what'] == 'serve_item_to':
			self.serve_item_to(self.task['items'],self.task['who'])
		elif self.task['what'] == 'flee':
			if self.get_claimed('home'):
				self.go_to(self.level.get_items_in_building(self.get_claimed('home'),type='bed')[0]['pos'])
			#else:
			#	print self.name,'NOWHERE TO RUN'
			
			if self.get_relationship_with(self.task['who'])>0:
				self.task['who'] = None
		elif self.task['what'] == 'farm':
			self.farm(self.task['where'])
		elif self.task['what'] == 'cook':
			self.cook()
		elif self.task['what'] == 'rest':
			self.rest()
		elif self.task['what'] == 'stay_home':
			if self.get_claimed('home'):
				if self.fatigue>=15 and self.get_open_beds(self.get_claimed('home')):
					if not self.is_in_bed():
						self.rest(self.get_claimed('home'))
				elif self.fatigue>=10 and self.is_in_bed():
					pass
				else:
					if not self.task_delay:
						self.guard_building(self.get_claimed('home'))
						self.task_delay = self.task['delay']
					elif self.task_delay>0:
						self.task_delay-=1
			else:
				if self.z==1:
					if self.level.get_open_buildings_of_type('home'):
						_building = self.level.get_open_buildings_of_type('home')[0]['name']
						self.go_to_and_claim_building(_building,'home')
					else:
						print 'No h0mez'
		elif self.task['what'] in ['water','socialize']:
			self.socialize()
		elif self.task['what'] == 'sell':
			self.sell_items(self.task['items'])
		elif self.task['what'] == 'sell items of type':
			self.sell_items_of_type(self.task['items'])
		elif self.task['what'] == 'buy':
			#self.buy_items(self.task['items'])
			self.go_to_building_and_buy(self.task['items'],self.task['where'])
		elif self.task['what'] == 'follow':
			self.follow_person(self.task['who'])
		elif self.task['what'] == 'store_items':
			self.store_items(self.task['items'])
		elif self.task['what'] == 'find_love':
			self.build_relationship_with(self.task['who'])
		
		if self.path:
			if tuple(self.pos) == tuple(self.path[0]):
				self.path.pop(0)
			
			if self.path:
				_new_pos = [self.path[0][0],self.path[0][1]]
				return _new_pos
		
		return self.pos
	
	def walk(self,dir):
		"""Movement rules for all ALife. Tracks collisions along with the
		pickup of items like gold and ore."""
		self.last_pos = self.pos[:]
		_pos = self.pos[:]
		
		if self.speed>0:
			self.speed -= 1
			return
		else:
			self.speed = self.speed_max
		
		if self.player:
			if dir == 'up' and self.pos[1]-1>=0:
				_pos[1]-=1
				if _pos[1]-var.camera[1]<=(var.window_size[1]/2)-var.scroll_speed:
					var.camera[1]-=var.scroll_speed
					if var.camera[1]<0: var.camera[1]=0
			elif dir == 'down' and self.pos[1]+1<var.world.size[1]:
				_pos[1]+=1
				if _pos[1]-var.camera[1]>=(var.window_size[1]/2)+var.scroll_speed-2:
					var.camera[1]+=var.scroll_speed
				if var.camera[1]>=var.world_size[1]-1:
					var.camera[1]=var.world_size[1]-1
					print 'greater'
			elif dir == 'left' and self.pos[0]-1>=0:
				_pos[0]-=1
				if _pos[0]-var.camera[0]<=(var.window_size[0]/2)-var.scroll_speed:
					var.camera[0]-=var.scroll_speed		
				if var.camera[0]<0: var.camera[0]=0
			elif dir == 'right' and self.pos[0]+1<var.world.size[0]:
				_pos[0]+=1
				if _pos[0]-var.camera[0]>=(var.window_size[0]/2)+var.scroll_speed:
					var.camera[0]+=var.scroll_speed
		else:
			_pos = self.think()
			
			if (self.pos[0],self.pos[1]) in self.level.exits\
				and self.path_dest in self.level.exits:
				self.enter()
				self.path_dest = None
			elif (self.pos[0],self.pos[1]) in self.level.entrances\
				and self.path_dest in self.level.entrances:
				self.enter()
				self.path_dest = None
		
		_tile = self.level.map[_pos[0]][_pos[1]]
		if _tile in var.blocking or _tile in var.solid:	
			self.pos = self.pos[:]
			return
		
		_items = self.level.items[_pos[0]][_pos[1]]
		if _items:
			_i = 0
			for _tile in _items:
				if _tile['solid']:
					self.pos = self.pos[:]
					return
				elif _tile['tile'] == 11:
					if _tile['life']<=0:
						_chance = random.randint(0,100)
						if _chance <= 55:
							self.level.map[_pos[0]][_pos[1]] = 1
						elif 55<_chance<=75:
							self.level.add_item(20,_pos)
						elif 75<_chance<=95:
							self.level.add_item(14,_pos)
						else:
							self.level.add_item(13,_pos)
						
						self.level.items[_pos[0]][_pos[1]].pop(_i)
					else:
						if self.weapon:
							_tile['life']-=self.weapon['damage']
						else:
							_tile['life']-=1
					self.pos = self.pos[:]
					return
				elif _tile['tile'] in [13,14,20]:
					_item = self.level.items[_pos[0]][_pos[1]].pop(_i)
					self.add_item(_item)
					if self.player:
						functions.log('You picked up +1 %s.' % _tile['name'])
				elif _tile['type'] == 'food' and _tile.has_key('planted_by'):
					if _tile['planted_by'] == self:
						_item = self.level.items[_pos[0]][_pos[1]].pop(_i)
						self.add_item(_item)
						if self.player:
							functions.log('You picked up some %s.' % _tile['name'])
				
				_i+=1
		
		_found = False
		for life in var.life:
			if life == self or not self.z == life.z: continue
			
			if life.pos == _pos:
				if self.get_relationship_with(life) and self.get_relationship_with(life)['score']<=0:
					self.attack(life)
					_found = True
		
		if not _found:
			if not self.pos == _pos:
				self.hunger_timer -= 1
			
			self.pos = _pos[:]
		
		if self.mine_dest:
			if (self.pos[0],self.pos[1]) == (self.mine_dest[0],self.mine_dest[1]):
				self.mine_dest = None
		
		if self.path_dest:
			if (self.pos[0],self.pos[1]) == (self.path_dest[0],self.path_dest[1]):
				self.path_dest = None

	def find_path(self,pos):
		if self.can_see(pos) and self.can_traverse(pos):
			if self.path_dest and (pos[0],pos[1]) == tuple(self.path_dest):
				self.path_dest = None
				return
			self.path = draw.draw_diag_line(self.pos,pos)
			self.path_dest = (pos[0],pos[1])
			self.path_type = 'Line'
		else:
			if self.path_dest and (pos[0],pos[1]) == tuple(self.path_dest):
				#self.path_dest = None
				return
			
			self.path_type = 'A*'
			
			_cache_path = var.cache.get_path_from_cache(self.pos,pos,self.z)
			if _cache_path:
				self.path = _cache_path
				self.path_dest = (pos[0],pos[1])
				return
			
			_blocking = []
			
			for item in self.level.get_all_solid_items():
				_blocking.append((item['pos'][0],item['pos'][1]))
			
			#We have to TRUST that the ALife knows what it's doing here...
			#basically we're assuming that even though the destination
			#is in the _blocking array, we can still move there and mine it			
			if tuple(pos) in _blocking:
				_blocking.remove(tuple(pos))
			
			#for life in var.life:
			#	if not life.z == self.z or self == life: continue
			#	
			#	#_blocking.append((life.pos[0],life.pos[1]))
			
			if tuple(pos) in _blocking:
				_blocking.remove(tuple(pos))
			
			try:
				_a = time.time()
				self.path = pathfinding.astar(start=self.pos,end=pos,\
					omap=self.level.map,size=self.level.size,blocking=_blocking).path
				#print 'Pathing time',time.time()-_a
			except KeyboardInterrupt:
				logging.error('[ALife.%s.Pathing] Failed to travel from %s to %s' %
					(self.name,self.pos,pos))
				sys.exit()
			
			if not self.path:
				self.path_dest = None
			else:
				self.path_dest = (pos[0],pos[1])
				var.cache.add_path_to_cache(self.pos,pos,self.path,self.z)
	
	def follow(self,who):
		if self.pos == who.pos or (self.z == who.z and functions.distance(self.pos,who.pos)<=3):
			return
		
		if not self.z == who.z:
			#TODO: Pathing for traversing levels
			if self.z<who.z:
				self.find_path(self.level.entrances[0])
				print 'Going up!'
			else:
				self.find_path(self.level.exits[0])
				print 'Going down!',self.pos,self.level.exits[0]
			return
		
		self.find_path(who.pos)
	
	def go_to(self,pos,z=None):
		if z == None:
			z = self.z
		
		if tuple(self.pos) == tuple(pos) and z == self.z:
			return True
		
		if not self.z == z:
			if self.z<z:
				self.find_path(self.level.entrances[0])
			else:
				self.find_path(self.level.exits[0])
			return False
		
		self.find_path(pos)
		return False
	
	def go_to_and_do(self,pos,callback,**kargv):
		"""Go to location and call function 'callback' with argument 'kargv'"""
		_there = self.go_to(pos)
		
		if _there: return callback(kargv['first'],kargv['second'])
		
		return True
	
	def go_to_and_claim_building(self,where,label):
		"""Go to 'where' and claim as 'label'"""
		_room = self.level.get_room(where)
		#print _room
		
		if self.go_to(_room['door']):
			#if tuple(self.pos) in _room['walking_space'] and not _room['owner']:
			if _room['owner']:
				pass
			else:
				self.claim_building(where,label)
	
	def go_to_building_and_buy(self,items,building):
		"""Go to 'building' and buy 'item'"""
		_building_owner = self.level.get_room(building)['owner']
		if not self.in_building(pos=self.path_dest,name=building):
			_pos = random.choice(self.level.get_room(building)['walking_space'])
		else:
			if self.in_building(name=building):
				_pos = tuple(self.pos)
			else:
				_pos = self.path_dest
		
		return self.go_to_and_do(_pos,\
			self.buy_item_from_shop_alife,\
			first=items,\
			second=building)
	
	def go_to_building_and_sell(self,item,building):
		"""Go to 'building' and sell 'item'"""
		_building_owner = self.level.get_room(building)['owner']
		if not self.in_building(pos=self.path_dest,name=building):
			_pos = random.choice(self.level.get_room(building)['walking_space'])
		else:
			if self.in_building(name=building):
				_pos = tuple(self.pos)
			else:
				_pos = self.path_dest
		
		return self.go_to_and_do(_pos,\
			self.sell_item_alife,\
			first=item,\
			second=_building_owner)
	
	def pick_up_item_at(self,pos,want,count=1,tag='type'):
		"""Go to 'pos' and pick up item type 'want'"""
		if not want: want=item['type']
		
		if tuple(self.pos) == pos:
			for i in range(count):
				for item in self.level.items[pos[0]][pos[1]]:
					if item[tag] == want:
						#self.level.items[pos[0]][pos[1]].remove(item)
						#self.level.items_shortcut.remove(_item)
						self.level.remove_item(pos,item)
						self.add_item(item)
						break
					elif item['type'] == 'storage':
						_found = False
						for _item in item['items']:
							if _item[tag] == want:
								item['items'].remove(_item)
								self.level.items_shortcut.remove(_item)
								self.add_item(_item)
								logging.debug('[ALife.%s] Removed %s from storage at %s' %
									(self.name,_item['name'],pos))
								_found = True
								break
						
						if _found: break
		
		else:
			self.go_to(pos)
	
	def guard_building(self,where):
		_room = var.world.get_level(1).get_room(where)
		
		if not _room: return False
		
		if self.path_dest in _room['walking_space']:
			pass
		else:
			self.go_to(random.choice(_room['walking_space']))
	
	def follow_person(self,who):
		if functions.distance(self.pos,who.pos)>=6:
			if self.path_dest:
				self.go_to(random.choice(self.level.get_open_space_around(who.pos,dist=3)))
			else:
				self.go_to(random.choice(self.level.get_open_space_around(who.pos,dist=3)))
		else:
			if self.task_delay:
				self.task_delay -= 1
			else:
				self.go_to(random.choice(self.level.get_open_space_around(who.pos,dist=3)))
				self.task_delay = self.task['delay']
	
	def run_shop(self,where):
		if self.get_claimed('work'):
			_storage = self.level.get_all_items_in_building_of_type(where,'storage')
			_dump = self.get_all_items_tagged('traded')
			
			if _dump and _storage:
				self.go_to_and_do(_storage[0]['pos'],\
					self.put_all_items_tagged,\
					first='traded',
					second=_storage[0]['pos'])
			else:
				if not self.task_delay:
					self.guard_building(where)
					self.task_delay = self.task['delay']
				elif self.task_delay>0:
					self.task_delay-=1
		else:
			self.go_to_and_claim_building(where,'work')
	
	def run_forge(self,where):
		if self.get_claimed('work'):
			_storage = self.level.get_items_in_building(where,type='storage')
			_forge = self.level.get_items_in_building(where,name='forge',forging=None)
			_done_forges = self.level.get_items_in_building(where,name='forge',forge_time=-1)
			_in_storage = []
			_job = None
			
			if _done_forges:
				if self.go_to(_done_forges[0]['pos']):
					_i = self.add_item(_done_forges[0]['forging'])
					logging.debug('[ALife.%s] Removed %s from forge at %s' %
						(self.name,_i['name'],_done_forges[0]['pos']))
					self.announce(what='removed a freshly forged product from where',
						product=functions.get_item_name(_i))
					_i['forged'] = True
					_done_forges[0]['forging'] = None
					_done_forges[0]['forge_time'] = 0
			
			if self.level.get_room(where)['orders'] and _forge:
				for order in self.level.get_room(where)['orders']:
					_needs = var.items[order]['recipe'][:]
					for need in _needs:
						for item in self.level.get_items_in_building(where,name=need):
							_needs.remove(need)
							_in_storage.append(item)
							break
						for item in self.get_items(name=need):
							_needs.remove(need)
							break
					
					if not _needs:
						if not _in_storage:
							_needs = var.items[order]['recipe'][:]
							_job = order
							if self.go_to(_forge[0]['pos']):
								self.level.get_room(where)['orders'].remove(_job)
								_forge[0]['forging'] = _job
								_forge[0]['forge_time'] = len(_needs)*20
								logging.debug('[ALife.%s] Placed materials for %s in forge at %s' %
									(self.name,var.items[_job]['name'],_forge[0]['pos']))
								self.announce(what='put materials in forge at where to make a product',
									product=functions.get_item_name(var.items[_job]))
						else:
							_item = _in_storage[0]
							self.pick_up_item_at(_item['pos'],_item['name'],tag='name')
						
						break
			
			if not _job:
				if not self.task_delay:
					self.guard_building(where)
					self.task_delay = self.task['delay']
				elif self.task_delay>0:
					self.task_delay-=1
		else:
			self.go_to_and_claim_building(where,'work')
	
	def run_bar(self,where):
		if self.get_claimed('work'):
			if not self.task_delay:
				self.guard_building(where)
				self.task_delay = self.task['delay']
			elif self.task_delay>0:
				self.task_delay-=1
		else:
			self.go_to_and_claim_building(where,'work')
	
	def can_farm(self):
		"""Returns all open space left to farm."""
		_ret = []
		_land = self.get_owned_land('farm')
		if not _land: return True
		
		for x in range(_land['size'][0]):
			for y in range(_land['size'][1]):
				pos = (_land['where'][0]+x,_land['where'][1]+y)
				if not self.level.items[pos[0]][pos[1]]: _ret.append(pos)
		
		return _ret
	
	def farm(self,where):
		"""Instructs the ALife to farm a plot of land at 'where',
		'where' is expected to be (x,y,width,height)"""
		##TODO: Should we check for (x1,y1,x2,y2)?
		#Each iteration we will scan for what tiles in 'where' are already planted
		#Until the array returned is empty, we will travel to the nearest tile and
		#plant there.
		_land = self.get_owned_land('farm')
		
		if _land:#self.task['where']:
			where = (_land['where'][0],_land['where'][1],_land['size'][0],_land['size'][1])
		else:
			_res = self.level.get_real_estate(self.pos,(3,3))
			
			_lowest = {'entry':None,'dist':100}
			for entry in _res:
				_pos = self.get_claimed('home',return_building=True)['walking_space'][0]
				_dist = functions.distance(tuple(_pos),entry)
				if _dist<_lowest['dist']:
					_lowest['dist'] = _dist
					_lowest['entry'] = entry
			
			where = (_lowest['entry'][0],_lowest['entry'][1],3,3)
			self.task['where'] = where
			
			self.claim_real_estate((where[0],where[1]),(where[2],where[3]),'farm')
			
		_open = []
		for x in range(where[2]):
			for y in range(where[3]):
				_pos = (where[0]+x,where[1]+y)
				
				if not len(self.level.items[_pos[0]][_pos[1]]):
					_open.append(_pos)
		
		if not self.task_delay:
			self.task_delay = self.task['delay']
			_stored_seed = self.level.get_all_items_in_building_of_type(self.get_claimed('home'),'seed')
			
			if not _open or (not len(self.get_items(type='seed')) and not _stored_seed):
				self.task['delay'] = 5
				_get = self.get_all_grown_crops()
				
				if _get:
					self.pick_up_item_at(_get[0]['pos'],_get[0]['type'])
			elif _open and len(self.get_items(type='seed')):
				if not self.go_to_and_do(_open[0],self.place_item,first=21,second=_open[0]):
					self.task_delay = self.get_farm_speed()
				
				#return True
			elif _stored_seed:
				self.pick_up_item_at(_stored_seed[0]['pos'],'seed',count=len(_open))
		elif self.task_delay>0:
			self.task_delay-=1
	
	def cook(self):
		_stoves = self.level.get_all_items_in_building_of_type(self.get_claimed('home'),'stove')
		_has_food = self.get_items(type='food')
		
		if not _stoves: return False
		
		_stove = None
		for stove in _stoves:
			if stove['cooking']:
				if stove['cooking']['type'] == 'cooked food':
					if self.go_to(stove['pos']):
						self.add_item(stove['cooking'])
						logging.debug('[ALife.%s] Removed %s from stove at %s' %
							(self.name,stove['cooking']['name'],stove['pos']))
						stove['cooking'] = None
						
						return True
					return False
				else:
					continue
			_stove = stove
			break
		
		if not _stove: return False
		
		if len(_has_food):
			_food = _has_food[0]
		else:
			_get_food = self.level.get_all_items_in_building_of_type(self.get_claimed('home'),'food')
			
			if not _get_food: return False
			else: _get_food = _get_food[0]
			
			if self.go_to_and_do(_get_food['pos'],\
					self.flag_item,
					first=_get_food,
					second='cook'):
			
				self.pick_up_item_at(_get_food['pos'],'food')
				return False
			else:
				return False
		
		if self.go_to(_stove['pos']):
			self.items.remove(_food)
			_stove['cooking'] = _food
			logging.debug('[ALife.%s] Put %s in stove at %s' %
				(self.name,_food['name'],_stove['pos']))
			return True		
	
	def rest(self,where):
		##TODO: Double beds?
		_beds = self.get_open_beds(where)
		
		if self.go_to(_beds[0]['pos']):
			_beds[0]['owner'] = self
			self.on_sleep()
	
	def sell_items(self,what):
		##TODO: Sort these eventually...
		#_has_food = self.get_all_items_of_type(what)
		#_stored_food = self.level.get_all_items_in_building_of_type(self.get_claimed('home'),what)
		_in_storage = []
		for item in what:
			if not item in self.items: _in_storage.append(item)
		
		#if not self.get_nearest_store():
		#	return False
		if not _in_storage and what:
			self.go_to_building_and_sell(what[0],self.task['where'])
			
			if not what[0] in self.items:
				self.task['items'].remove(item)
			
		elif _in_storage:
			self.pick_up_item_at(_in_storage[0]['pos'],_in_storage[0]['type'])
	
	def sell_items_of_type(self,what):
		##TODO: Sort these eventually...
		#_has_food = self.get_all_items_of_type(what)
		_has_food = self.get_items_ext(type=what)
		_stored_food = self.level.get_all_items_in_building_of_type(self.get_claimed('home'),what)
		
		if not self.get_nearest_store():
			return False
		elif _has_food:
			self.go_to_building_and_sell(_has_food[0],self.get_nearest_store())
		elif _stored_food:
			self.pick_up_item_at(_stored_food[0]['pos'],_stored_food[0]['type'])
	
	def store_items(self,what):
		_home = self.get_claimed('home')
		_storage = self.level.get_all_items_in_building_of_type(_home,'storage')
		_has = self.get_items_ext(type=what)

		if len(_storage):	
			if _has:
				self.go_to_and_do(_storage[0]['pos'],
					self.put_item_of_type,
					first=_has[0]['type'],
					second=_storage[0]['pos'])
	
	def can_build_relationship_with(self,who):
		"""Sees if the ALife can develop a relationship with 'who'"""
		##TODO: Go and fetch items in home
		#_ret = self.get_all_items_of_type(['food','cooked food'])
		_ret = self.get_items(type='food')
		_ret.extend(self.get_items(type='cooked food'))
		
		for item in _ret:
			if item.has_key('from'): _ret.remove(item)
		
		return _ret
	
	def build_relationship_with(self,who):
		"""Makes ALife attempt to form relationship with 'who'"""
		#Decide what to give this person
		
		_likes = self.get_relationship_with(who)['likes']
		_in_storage = None
		_has = None
		
		if _likes:
			_in_storage = self.level.get_items_in_building_ext(self.get_claimed('home'),type=_likes)
			_has = self.get_items_ext(type=_likes)
		elif not _in_storage and not _has:
			_tlikes = ['food','cooked food']
			_in_storage = self.level.get_items_in_building_ext(self.get_claimed('home'),type=_tlikes)
			_has = self.get_items_ext(type=['food','cooked food'])
		else:
			_in_storage = self.level.get_items_in_building_ext(self.get_claimed('home'),type=_tlikes)
			_has = self.get_items_ext(type=['food','cooked food'])
		
		for item in _has:
			if item.has_key('from'): _has.remove(item)
		
		for item in _in_storage:
			if item.has_key('from'): _in_storage.remove(item)
		
		if _has:
			self.go_to_and_do(who.pos,\
				self.give_item_to,\
				first=_has[0],\
				second=who)
		elif _in_storage:
			self.pick_up_item_at(_in_storage[0]['pos'],_in_storage[0]['type'])
		else:
			#print self.can_build_relationship_with(who),'This happens in build_relationship_with'
			pass
	
	def socialize(self):
		"""ALife attends social functions to relieve stress"""
		_building = self.get_nearest_building_of_type('bar')
		if not _building: return
		
		_has_drink = self.get_items(type='cup')
		
		for drink in _has_drink:
			if not drink['volume'] or not drink['contains']: _has_drink.remove(drink)
		
		if not self.task_delay:
			self.guard_building(_building)
			self.task_delay = self.task['delay']
		elif self.task_delay>0:
			self.task_delay-=1
		
		if self.in_building(name=_building) and self.thirst>=5:
			if _has_drink:
				self.drink(_has_drink[0])
			else:
				_building_owner = self.level.get_room(_building)['owner']
				_relationship = self.get_relationship_with(_building_owner)
				if _relationship and _relationship['score']>self.dislike_at:
					self.buy_item_type_from_alife('drink',_building_owner)
				elif _relationship and _relationship['score']<=self.dislike_at:
					logging.debug('[ALife.%s] Refuses to drink' % (self.name))
	
	def enter(self):
		if self.level.map[self.pos[0]][self.pos[1]] == 3:
			self.z += 1
		elif self.level.map[self.pos[0]][self.pos[1]] == 4:
			self.z -= 1
		
		self.level = var.world.get_level(self.z)
		self.start_pos = None
	
	def teleport(self,z):
		self.z = z
		self.level = var.world.get_level(self.z)
		self.pos = list(self.level.walking_space[0])
	
	def kill(self):
		for life in var.life:
			_temp = life.has_seen(self)
			
			if _temp:
				life.seen.remove(_temp)
				
				if life.race == 'human':
					if life.lowest['who'] == self:
						life.lowest['who'] = None
						life.lowest['score'] = 0
					
					if life.highest['who'] == self:
						life.highest['who'] = None
						life.highest['score'] = 0
		
		for r in range(10+random.randint(0,3)):
			_x = self.pos[0]+random.randint(-2,2)#+pos[0]
			_y = self.pos[1]+random.randint(-2,2)#+pos[1]
			
			if 0>_x or _x>=self.level.size[0]: continue
			if 0>_y or _y>=self.level.size[1]: continue
			
			self.level.tmap[_x][_y] = 255
		
		self.level.tmap[self.pos[0]][self.pos[1]] = 255
		
		logging.debug('%s died!' % self.name)
		var.life.remove(self)

class human(life):
	def __init__(self,player=False,male=True):
		life.__init__(self,player=player)
		
		self.icon = {'icon':'@','color':['white',None]}
		
		self.race = 'human'
		if male:
			self.gender = 'male'
			self.name = functions.get_name_by_gender('male')
		else:
			self.gender = 'female'
			self.name = functions.get_name_by_gender('female')
		
		self.hp = 20
		self.hp_max = 20
		
		#self.thirsty_at = -1
		self.married = None
		self.in_danger = False
		self.faction = 'good'
		self.trading = False
		
		self.limbs = {'left arm':{'skin':{'cut':5,'bruised':0,'bleeding':0},
				'muscle':{'cut':0,'bruised':0,'bleeding':0},
				'bone':{'chipped':0}},
			'right arm':{'skin':{'cut':0,'bruised':0,'bleeding':0},
				'muscle':{'cut':0,'bruised':0,'bleeding':0},
				'bone':{'chipped':0}},
			'left leg':{'skin':{'cut':0,'bruised':0,'bleeding':0},
				'muscle':{'cut':0,'bruised':0,'bleeding':0},
				'bone':{'chipped':0}},
			'right leg':{'skin':{'cut':0,'bruised':0,'bleeding':0},
				'muscle':{'cut':0,'bruised':0,'bleeding':0},
				'bone':{'chipped':0}}}
	
	def save(self):
		_keys = {}
		_keys['in_danger'] = self.in_danger
		
		return life.save(self,keys=_keys)
	
	def load(self,keys):
		if keys.has_key('in_danger'):
			self.in_danger = keys['in_danger']
		
		return life.load(self,keys)
	
	def on_wake(self):
		life.on_wake(self)
		self.say('yawns.',action=True)
	
	def on_sleep(self):
		life.on_sleep(self)
		self.say('Zzz')
	
	def on_submission(self,who):
		life.on_submission(self,who)
		self.say('scampers off.',action=True)
	
	def is_in_danger(self,who):
		self.in_danger = True
		if self.player:
			if who.weapon:
				functions.log('%s the %s charges towards you with a %s!' % \
					(who.name,who.race,who.get_weapon_name()))
			else:
				functions.log('%s the %s runs towards you!' % \
					(who.name,who.race))
	
	def get_weapon_name(self):
		_name = ''
		
		if self.weapon['rank']>1:
			if self.weapon['rank']==2:
				_name+='shining '
		
		_name+='%s' % self.weapon['name']
		
		if self.weapon['status']:
			_name+=' covered in %s' % self.weapon['status']
			
		return _name
	
	def mine(self):
		if self.mine_dest and self.path_dest == self.mine_dest: return
		
		_lowest = {'score':1000,'pos':None}
		for item in self.level.get_all_items_of_tile(11):
			if not self.can_see(item['pos']): continue
			
			_dist = functions.distance(self.pos,item['pos'])
			
			if _dist<_lowest['score']:
				_lowest['score'] = _dist
				_lowest['pos'] = item['pos']
		
		if _lowest['pos']:
			self.go_to(_lowest['pos'])
			self.mine_dest = _lowest['pos']
		else:
			_pos = var.world.get_level(self.z-1).entrances[0]
			
			self.go_to(_pos,z=self.z-1)
	
	def judge(self,who):
		#Don't waste time if they're dead
		if not who.hp: return 0
		
		#This is so much easier...
		_score = 0
		
		if self.faction == who.faction:
			#Alright, so here goes...
			#To score this in a way that makes sense, the best thing to do is
			#maintain a certain amount of realism and practicality.
			#There are a lot of variables that would be easy to toss in, but
			#we'll stick to the basics for now.
			
			#Health plays a very, very small part in postive (same faction)
			#judgement.
			_score+=(who.hp/2)
			
			#We're assuming everyone is straight and has no attraction to the
			#same gender. Add a small bonus here for now. Eventually we'll
			#find a way to calculate how attractive someone is based on stats
			#and replace the fixed value
			if not self.gender == who.gender:
				_score+=5
		
			#Some people are more attracted to power. Power (for now) is the
			#max damage a weapon can potentially do.
			if 'power' in self.attracted_to:
				if who.weapon: _score += who.weapon['damage']
			
			#Money can also be "attractive." Figure that in...
			if 'wealth' in self.attracted_to:
				##TODO: We should probably search for "apparent" money here
				##based on the prices on the armor being worn, etc
				_score+=(who.get_money()/4)
			
			#Strength is also a positive influence for some.
			if 'strength' in self.attracted_to:
				_score+=who.atk*2
			elif self.gender == 'female':
				#Females are naturally attracted to strength. Regardless of
				#whether 'strength' is in attracted_to, they will get a small
				#bonus from it.
				_score+=who.atk
			
			if 'looks' in self.attracted_to:
				if 'attractive' in who.traits: _score+=10
				elif 'athletic' in who.traits: _score+=7
				elif 'fit' in who.traits: _score+=5
				else: _score -= 5
								
			#Status is also something to consider. A person with a lot of
			#real estate is more likely to be higher up the ladder than others
			if 'status' in self.attracted_to:
				_score+=len(who.claims)*5
				_score+=len(who.owned_land)*3
			
			if 'brash' in self.attracted_to:
				_score+=5
			
			if 'honest' in self.attracted_to:
				_score+=5
			
			if 'shy' in self.attracted_to:
				_score+=5

			#Consider gifts from this person.			
			if 'charity' in self.attracted_to:
				for item in self.get_all_gifts_from(who):
					_score+=(item['price']/2)
			else:
				for item in self.get_all_gifts_from(who):
					_score+=(item['price']/4)
			
			if 'provider' in self.attracted_to:
				if 'farm' in who.skills:
					_score+=5
			
			if 'skill' in self.attracted_to:
				_score+=(len(who.skills))*2
			
			_neg = 0
			for match in self.get_past_event({'from':self.id,'person':who.id,'what':'cursed'}):
				_neg-=10
			
			for match in self.get_past_event({'from':who.id,'person':self.id,'what':'cursed'}):
				_neg-=10
			
			_what = 'threw item at person'
			for match in self.get_past_event({'from':who.id,'person':self.id,'what':_what}):
				_neg-=10
				#Threw item at me
			
			_what = 'threw item at person'
			for match in self.get_past_event({'from':self.id,'person':who.id,'what':_what}):
				_neg-=20
				#I threw an item at them
			
			_what = 'hit person with item'
			for match in self.get_past_event({'from':who.id,'person':self.id,'what':_what}):
				_neg-=20
			#	#print 'I was hit by someone',_score
			
			#_what = 'hit person with item'
			#for match in self.get_past_event({'from':self.id,'person':who.id,'what':_what}):
			#	_score-=25
			#	#print 'I hit someone', _score
			
			#for match in self.get_past_event({'from':who.id,'person':self.id,'what':'pushed person'}):
			#	_score+=5
			
			#for match in self.get_past_event({'from':self.id,'person':who.id,'what':'pushed person'}):
			#	_score+=5
			
			_events = self.get_past_event({'from':self.id,'person':who.id,'what':'attacked person'})
			for match in _events:
				if self.hp>=5:
					_neg-=(match['damage']*2)
					#print self.name,'Adding the damage in'
				#else:
				#	_neg+=(match['damage']*2)
				#	print self.name,'Subtracting the damage in'
				#print 'I punched this dude, now I feel better',_score
			
			_events = self.get_past_event({'from':who.id,'person':self.id,'what':'attacked person'})
			for match in _events:
				if self.hp>=5:
					_neg-=match['damage']
					#print self.name,'Adding the damage in'
				#else:
				#	_neg+=match['damage']
				#	print self.name,'Subtracting the damage in'
				#print 'This dude punched me, better look out',_score
			
			for match in self.get_past_event({'from':who.id,'what':'vomited'}):
				if 'vomit' in self.dislikes: _score-=6
				elif 'vomit' in self.likes: _score+=3
				else: _score-=3
				
			#Submission
			if self.hp>=5 and who.hp>=5:
				_score+=_neg
			else:
				_score = 10
			
			#If the ALife is married to this person, give them a huge bonus
			##TODO: Could marriage be a negative thing?
			if self.married == who:
				if 'faithful' in self.traits:
					_score+=30
				elif 'unfaithful' in self.traits:
					pass #do nothing, no bonus
				else:
					_score+=20
			
		else:
			_score += who.hp+who.atk+who.defe
			if who.weapon: _score+=who.weapon['damage']*2
			_score *= -1
		
		return _score
	
	def think(self):
		life.think(self)
		
		#Take care of needs here
		if self.hunger >= self.hungry_at and not self.hungry_at == -1:
			self.add_event('food',self.hunger)
		
		if self.thirst >= self.thirsty_at and not self.thirsty_at == -1:
			self.add_event('water',self.thirst)
		
		_farm_score = 0
		_cook_score = 0
		_sell_score = 0
		_buy_score = 0
		_store_items_score = 0
		
		#Consider skills
		if 'farm' in self.skills:
			#_farm_score-=(len(self.get_all_items_of_type(['food','cooked_food']))*2)
			
			_stored = len(self.level.get_all_items_in_building_of_type(self.get_claimed('home'),'seed'))
			_has = len(self.get_items(type='seed'))
			
			##TODO: Calculate how much food this ALife needs
			if self.can_farm() and not self.task['what']=='farm':
				_farm_score+=(_stored*10)
				_farm_score+=(_has*10)
			elif self.can_farm() and self.task['what']=='farm' and (_stored or _has):
				_farm_score = 75
			
			if self.get_all_grown_crops():
				_farm_score = 75			
				
			#Cooking
			if self.get_open_stoves(self.get_claimed('home')):
				_cook_score+=len(self.get_all_cookable_items(self.get_claimed('home')))*15
				_cook_score+=len(self.get_done_stoves(self.get_claimed('home')))*15
			
			##TODO: Find out how much money is needed to buy more seed
			_sell_score = len(self.get_items(type='food'))*10
			_sell_score += len(self.get_items(type='cooked food'))*10
			_sell_score += len(self.level.get_items_in_building(self.get_claimed('home'),type='food'))
			_sell_score +=\
				len(self.level.get_items_in_building(self.get_claimed('home'),type='cooked food'))
			_sell_what = ['food','cooked food']
			_sell_score -= self.get_money()*2
			if not self.get_nearest_store(): _sell_score = -1
			
			_farm = self.get_owned_land('farm')
			_store = self.get_nearest_store(items=['seed'])
			if _store and _farm:# and self.get_money():
				_farm_size = _farm['size'][0]*_farm['size'][1]
				_seeds = len(self.level.get_all_items_in_building_of_type(self.get_claimed('home'),'seed'))
				_seeds += len(self.get_items(type='seed'))
				
				_open_can_seed = _farm_size-_seeds
				
				if self.task['what']=='buy' and _open_can_seed>0:
					_buy_score = 75
				else:
					_buy_score = int((_open_can_seed/float(_farm_size))*100)/2
			
			_buy_what = ['seed']
			
			#Store away extra food
			_store_items_score +=\
				len(self.get_items_ext(type=['seed','food','cooked food']))*3
			_store_what = ['seed','food','cooked food']
			
			self.add_event('farm',_farm_score-self.fatigue,delay=5)
			self.add_event('cook',_cook_score-self.fatigue,delay=5)
			self.add_event('sell items of type',_sell_score-self.fatigue,items=_sell_what,delay=5)
			self.add_event('buy',_buy_score-self.fatigue,items=_buy_what,where=_store,delay=5)
			self.add_event('store_items',_store_items_score-self.fatigue,items=_store_what,delay=5)
		elif 'trade' in self.skills:
			_trade_score = 25
			
			if self.get_claimed('work'):
				self.add_event('run_shop',_trade_score,where=self.get_claimed('work'),delay=20)
			else:
				_building = self.claim_work_at('store')
				self.add_event('run_shop',_trade_score-self.fatigue,where=_building,delay=20)
		elif 'blacksmith' in self.skills:
			_smith_score = 25
			
			if self.get_claimed('work'):
				_items = self.level.get_all_items_in_building_tagged(self.get_claimed('work'),'forged')
				_items.extend(self.get_all_items_tagged('forged'))
				self.add_event('run_forge',_smith_score,where=self.get_claimed('work'),delay=20)
			else:
				_items = []
				_building = self.claim_work_at('forge')
				self.add_event('run_forge',_smith_score-self.fatigue,where=_building,delay=20)
			
			if _items and self.get_nearest_store():
				self.add_event('sell',50,items=_items,where=self.get_nearest_store(),delay=5)
			else:
				self.add_event('sell',0,items=_items,where=self.get_nearest_store(),delay=5)
		elif 'barkeep' in self.skills:
			_barkeep_score = 25
			
			if self.get_claimed('work'):
				self.add_event('run_bar',_barkeep_score,where=self.get_claimed('work'),delay=20)
			else:
				if self.task.has_key('where'):
					_owner = self.level.get_room(self.task['where'])['owner']
					if _owner and not _owner == self:
						self.remove_event('run_bar')
						_building = self.level.get_open_buildings_of_type('bar')[0]['name']
					else:
						_building = self.level.get_open_buildings_of_type('bar')[0]['name']
				else:
					_building = self.level.get_open_buildings_of_type('bar')[0]['name']
				self.add_event('run_bar',_barkeep_score-self.fatigue,where=_building,delay=20)
		
		_love_score = -(_farm_score+_cook_score+_sell_score+_store_items_score)/2
		if _love_score>0: _love_score=0
		_love_score -= self.fatigue
		
		if self.get_top_love_interests() and not self.married:
			_likes = self.get_top_love_interests()[0]
			_love_score += _likes['score']
			
			_can_build = self.can_build_relationship_with(_likes['who'])
			if _can_build:
				_love_score += len(_can_build)
			else:
				_love_score = 0
			
			self.add_event('find_love',_love_score,who=_likes['who'],delay=20)
		
		_in_bed = self.is_in_bed()
		if _in_bed:
			self.add_event('stay_home',self.fatigue*2,delay=15)
			
			if not tuple(self.pos) == tuple(_in_bed['pos']):
				_in_bed['owner'] = None
				self.on_wake()		
		else:
			self.add_event('stay_home',self.fatigue*.8,delay=15)
		
		_bar = self.get_nearest_building_of_type('bar')
		if _bar:
			_has_relationship = self.get_relationship_with(self.level.get_room(_bar)['owner'])
			if not _has_relationship or _has_relationship['score']>self.dislike_at:
				self.add_event('socialize',self.fatigue,delay=20)
				#self.add_event('socialize',90,delay=20)
			else:
				#print 'Refusing to socialize'
				#print _has_relationship
				self.add_event('socialize',0,delay=20)
		
		return life.think_finalize(self)
	
	def kill(self):
		life.kill(self)
		
		if not self.player and self.task['who'] and self.task['who'].player:
			self.task['who'].in_danger = False

class crazy_miner(human):
	def __init__(self):
		human.__init__(self)
		
		self.hungry_at = -1
		self.thirsty_at = -1
		
		self.race = 'human'
		self.faction = 'evil'
	
	def on_enemy_spotted(self,who):
		self.say('I see yah, you crazy bastard!')

class dog(life):
	def __init__(self,male=True):
		life.__init__(self)
		
		self.race = 'dog'
		self.faction = 'good'
		
		if male:
			self.gender = 'male'
			self.name = functions.get_dog_name_by_gender('male')
		else:
			self.gender = 'female'
			self.name = functions.get_dog_name_by_gender('female')
		
		self.icon['icon'] = 'd'
		self.icon['color'][0] = 'brown'
	
	def on_enemy_spotted(self,who):
		life.on_enemy_spotted(self,who)
		self.say_phrase('dog_angry',other=who,action=True)
	
	def on_friendly_spotted(self,who):
		life.on_friendly_spotted(self,who)
		
		if self.owner == who:
			self.say_phrase('dog_happy_owner',other=who,action=True)
	
	def judge(self,who):
		_score = 0
		
		if self.faction == who.faction:
			if self.gender == who.gender: _score+=5
				
			if 'Animal Husbandry' in who.talents: _score+=15
			if self.owner == who: _score+=50
			
			_score-=(self.fatigue*2)
			
			if _score<0: _score = 1
				
		else:
			if who.weapon: _score+=who.weapon['damage']*2
			_score *= -1
		
		return _score
	
	def think(self):
		life.think(self)
		
		if self.highest['who']:
			self.add_event('follow',50,who=self.highest['who'],delay=15)

		return life.think_finalize(self)

class zombie(life):
	def __init__(self,player=False):
		self.icon = {'icon':'Z','color':['lightgreen',None]}
		
		life.__init__(self,player=player)
		
		self.race = 'zombie'
		
		self.hp = 3
		self.hp_max = 3
		self.speed = 5
		self.speed_max = 5
		self.xp = 0
	
	def think(self):
		life.think(self)
		
		if not self.seen: return self.pos
		
		#Find closest
		_lowest = {'who':None,'lowest':9000,'los':None}
		for seen in self.seen:
			if seen['who'].faction == self.faction: continue
			
			if len(seen['los'])<=_lowest['lowest']:
				_lowest['who'] = seen['who']
				_lowest['lowest'] = len(seen['los'])
				_lowest['los'] = seen['los']
		
		if _lowest['who']:
			self.focus = _lowest
		else:
			return self.pos
		
		if self.focus['los']:
			self.focus['los'].pop(0)
		
		if not self.focus['los']:
			return self.pos
		
		return [self.focus['los'][0][0],self.focus['los'][0][1]]

class god:
	def __init__(self):
		self.alignment = 'neutral'
		self.name = 'Default'
		self.purpose = 'Nothing'
		self.accepts = []
		self.denies = []
		
		self.followers = []
		
		self.kills = []
	
	def get_name(self):
		return '%s, the god of %s' % (self.name,self.purpose)

	def on_kill(self,by,who):
		if by.player:
			if who.race in self.accepts:
				if by.alignment<10:
					by.alignment+=1
					
				self.kills.append({'by':by.name,'who':who.name,'accept':True})
				functions.log('%s accepts your kill.' % self.get_name())
			
			elif who.race in self.denies:
				if by.alignment>-10:
					by.alignment-=1
				
				self.kills.append({'by':by.name,'who':who.name,'accept':False})
				functions.log('%s denies your kill.' % self.get_name())
			
			if by.alignment>=1:
				functions.log('You feel that %s is happy with your actions lately.' % self.get_name())
			elif by.alignment<=-1:
				functions.log('You feel that %s is not happy with your actions lately!' % self.get_name())