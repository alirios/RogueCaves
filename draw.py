def draw_line(pos1,pos2,diag=False,includeend=False):
	if diag:
		_l = draw_line_diag(pos1,pos2)
		return _l.path
	else:
		d = max(abs(pos1[0]-pos1[0]), abs(pos1[1]-pos2[1]));
		path1 = []
		
		for i in range(d):
			path1.append((pos1[0] + (pos1[0]-pos1[0]) * i/d, pos1[1] + (pos2[1]-pos1[1]) * i/d))
		
		d = max(abs(pos1[0]-pos2[0]), abs(pos2[1]-pos2[1]));
		path2 = []
		
		for i in range(d):
			path2.append((pos1[0] + (pos2[0]-pos1[0]) * i/d, pos2[1]))
		
		path2.append(pos2)
		path1.extend(path2)
		
		if includeend:
			path1.append(pos2)

		return path1

def draw_circle(at,size):
	Circle = 0
	width=size
	height=size
	CenterX=(width/2)
	CenterY=(height/2)
	circle = []

	for i in range(height):
		for j in range(width+1):
			Circle = (((i-CenterY)*(i-CenterY))/((float(height)/2)*(float(height)/2)))+((((j-CenterX)*(j-CenterX))/((float(width)/2)*(float(width)/2))));
			if Circle>0 and Circle<1.1:
				circle.append((at[0]+(j-(width/2)),at[1]+(i-(height/2))))
	
	return circle