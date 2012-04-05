import var

def log(text):
	if len(var.history)>=5: var.history.pop(0)
	
	var.history.append(text)

def distance(pos1,pos2):
	return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])