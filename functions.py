import var

def log(text):
	if len(var.history)>=5: var.history.pop(0)
	
	var.history.append(text)