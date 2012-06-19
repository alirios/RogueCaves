import functions
import logging
import random

def damage_limb(attacker,defender,limb,weapon=None):
	_dam = 0
	_limb_damage = 1+(attacker.atk/5)
	_msg = ''
	_in_pain = False
	
	if weapon and weapon['sharp']:
		if attacker.player:
			_msg += 'You strike %s in the %s' % (defender.name,limb)
		elif defender.player:
			_msg += '%s strikes you in the %s' % (attacker.name,limb)
		else:
			if attacker.race=='human':
				_msg += '%s strikes %s in the %s' % (attacker.name,defender.name,limb)
			else:
				_msg += '%s bites %s in the %s' % (attacker.name,defender.name,limb)
		
		if limb.count('arm') or limb.count('leg'):
			if defender.limbs[limb]['skin']['cut']<3:
				defender.limbs[limb]['skin']['cut']+=_limb_damage
				
				_messages = [', leaving a bruise.',
					', bruising it.',
					', bruising the skin.',
					'.']
				_msg += random.choice(_messages)
				
				logging.debug('[ALife.%s] Hit %s in the %s (%s)' %
					(attacker.name,defender.name,limb,_limb_damage))
			elif defender.limbs[limb]['skin']['cut']==3:
				defender.limbs[limb]['skin']['cut']+=_limb_damage
				
				_messages = [', bruising it severely.',
					', leaving a heavy bruise!',
					', bruising the skin severely!',
					'.']
				_msg += random.choice(_messages)
				
				_in_pain = 1
				_dam += 2
				
				_what = 'Hit %s in the %s, bruising the skin severely!' % (defender.name,limb)
				logging.debug('[ALife.%s] %s' % (attacker.name,_what))
			elif defender.limbs[limb]['muscle']['cut']<3:
				defender.limbs[limb]['muscle']['cut']+=_limb_damage
				
				_messages = [', bruising the muscle itself.',
					', weakening the muscle.',
					', causing the muscle to bruise.']
				_msg += random.choice(_messages)
				
				_dam += 2
			elif defender.limbs[limb]['muscle']['cut']==3:
				defender.limbs[limb]['muscle']['cut']+=_limb_damage
				
				_messages = [', rendering it immobile!',
					', making it useless.',
					', causing it to go limp.']
				_msg += random.choice(_messages)
				
				_dam += 4
				_in_pain = 2
				
				_what = 'Hit %s in the %s, bruising the muscle severely!' % (defender.name,limb)
				logging.debug('[ALife.%s] %s' % (attacker.name,_what))
		elif limb.count('chest'):
			pass
	else:
		if attacker.player:
			_msg += 'You hit %s in the %s' % (defender.name,limb)
		elif defender.player:
			_msg += '%s hits you in the %s' % (attacker.name,limb)
		else:
			if attacker.race=='human':
				_msg += '%s hits %s in the %s' % (attacker.name,defender.name,limb)
		
		if limb.count('arm') or limb.count('leg'):
			if defender.limbs[limb]['skin']['bruised']<3:
				defender.limbs[limb]['skin']['bruised']+=_limb_damage
				
				_messages = [', leaving a bruise.',
					', bruising it.',
					', bruising the skin.',
					'.']
				_msg += random.choice(_messages)
				
				logging.debug('[ALife.%s] Hit %s in the %s (%s)' %
					(attacker.name,defender.name,limb,_limb_damage))
			elif defender.limbs[limb]['skin']['bruised']==3:
				defender.limbs[limb]['skin']['bruised']+=_limb_damage
				
				_messages = [', bruising it severely.',
					', leaving a heavy bruise!',
					', bruising the skin severely!',
					'.']
				_msg += random.choice(_messages)
				
				_in_pain = 1
				_dam += 2
				
				_what = 'Hit %s in the %s, bruising the skin severely!' % (defender.name,limb)
				logging.debug('[ALife.%s] %s' % (attacker.name,_what))
			elif defender.limbs[limb]['muscle']['bruised']<3:
				defender.limbs[limb]['muscle']['bruised']+=_limb_damage
				
				_messages = [', bruising the muscle itself.',
					', weakening the muscle.',
					', causing the muscle to bruise.']
				_msg += random.choice(_messages)
				
				_dam += 2
			elif defender.limbs[limb]['muscle']['bruised']==3:
				defender.limbs[limb]['muscle']['bruised']+=_limb_damage
				
				_messages = [', rendering it immobile!',
					', making it useless.',
					', causing it to go limp.']
				_msg += random.choice(_messages)
				
				_dam += 4
				_in_pain = 2
				
				_what = 'Hit %s in the %s, bruising the muscle severely!' % (defender.name,limb)
				logging.debug('[ALife.%s] %s' % (attacker.name,_what))
		elif limb.count('chest'):
			pass
	
	functions.log(_msg)
	
	if _in_pain==1:
		if defender.player:
			if random.randint(0,1):
				functions.log('You wince in pain.')
			else:
				functions.log('You grasp your %s.' % limb)
		else:
			if random.randint(0,1):
				defender.say('winces in pain.',action=True)
			else:
				defender.say('grasps their %s.' % limb,action=True)	
	elif _in_pain==2:
		if defender.player:
			if random.randint(0,1):
				functions.log('You cry out in pain.')
			else:
				functions.log('You grasp your immobile %s.' % limb)
		else:
			if random.randint(0,1):
				defender.say('cries out in pain.',action=True)
			else:
				defender.say('grasps their immobile %s.' % limb,action=True)	
	
	return _dam	

def attack(attacker,defender):
	if defender.race in ['zombie']:
		if attacker.player:
			_atk_msg = 'You swing at the %s.' % (defender.race)
		elif defender.player:
			_atk_msg = 'The %s swings at you.' % (defender.race)
	elif defender.race in ['human']:
		if attacker.player:
			_atk_msg = 'You swing at %s.' % (defender.name)
		elif defender.player:
			_atk_msg = '%s swings at you.' % (attacker.name)
	elif defender.race in ['dog']:
		if attacker.player:
			_atk_msg = 'You swing at %s.' % (defender.name)
		elif defender.player:
			_atk_msg = '%s lunges at you.' % (attacker.name)
		else:
			if attacker.race=='human':
				functions.log('%s swings at %s' % (attacker.name,defender.name))
			elif attacker.race=='dog':
				functions.log('%s bites %s' % (attacker.name,defender.name))
	else:
		if attacker.player:
			_atk_msg = 'You swing at %s.' % (defender.name)
		elif defender.player:
			_atk_msg = 'The %s swings at you.' % (attacker.race)
	
	attacker.hunger_timer -= 5
	attacker.xp += 1
	
	if attacker.weapon:
		_dam = random.randint(attacker.get_base_damage(),attacker.get_max_damage())
		if _dam >= attacker.weapon['damage']:
			if attacker.player:
				functions.log('Your %s hits for maximum damage!' % attacker.weapon['name'])
			elif defender.player:
				functions.log('%s hits you with a %s for maximum damage!' % 
					(attacker.name,attacker.weapon['name']))
			
			if attacker.weapon['sharp']:
				attacker.weapon['status'] = 'the blood of %s the %s' % (defender.name,defender.race)
				
				_pos = random.choice([(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),\
					(-1,1),(0,1),(1,1)])
				_x = defender.pos[0]+_pos[0]
				_y = defender.pos[1]+_pos[1]
				
				if not 0>_x and not _x>=attacker.level.size[0] and\
					not 0>_y and not _y>=attacker.level.size[1]:
					attacker.level.tmap[_x][_y] = random.randint(150,255)
		
		defender.hp -= _dam
		logging.debug('[ALife.%s] Attacked %s for %s damage' % (attacker.name,defender.name,attacker.atk))
		attacker.announce(what='attacked person',person=defender.id,damage=_dam)
	else:
		_dam = attacker.get_base_damage()
		
		if defender.race in ['human','zombie']:
			_hit_limb = random.choice(['left arm','right arm'])
		else:
			_hit_limb = random.choice(defender.limbs.keys())
	
		_dam += damage_limb(attacker,defender,_hit_limb)
			
		defender.hp -= _dam
		logging.debug('[ALife.%s] Attacked %s for %s damage' % (attacker.name,defender.name,_dam))
		attacker.announce(what='attacked person',person=defender.id,damage=_dam)
		
		##TODO: Missing
		#functions.log(_atk_msg)
	
	if defender.hp<=0:
		if defender.race in ['zombie']:
			if attacker.player: functions.log('You slay the %s!' % (defender.race))
			elif defender.player: functions.log('The %s slays you!' % (defender.race))
		else:
			if attacker.player: functions.log('You slay %s the %s!' % (defender.name,defender.race))
			elif defender.player: functions.log('The %s slays you!' % (attacker.race))
		
		attacker.xp += defender.xp
		
		for item in defender.items:
			if attacker.player: functions.log('Found %s!' % item['name'])
			attacker.add_item(item)
			
			if not attacker.weapon and item['type']=='weapon':
				attacker.equip_item(item)
		
		if attacker.god:
			attacker.god.on_kill(attacker,defender)
		
		defender.kill()
	
	if attacker.xp>=attacker.skill_level:
		attacker.xp-=attacker.skill_level
		attacker.skill_level+=1
		attacker.hp = attacker.hp_max