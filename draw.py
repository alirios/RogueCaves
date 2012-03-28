class line_diag:
	def __init__(self, start, end):
		self.path = []
		if start == end: return None
		
		self.start = list(start)
		self.end = list(end)
		
		self.steep = abs(self.end[1]-self.start[1]) > abs(self.end[0]-self.start[0])
		
		if self.steep:
			self.start = self.swap(self.start[0],self.start[1])
			self.end = self.swap(self.end[0],self.end[1])
		
		if self.start[0] > self.end[0]:
			self.start[0],self.end[0] = self.swap(self.start[0],self.end[0])		
			self.start[1],self.end[1] = self.swap(self.start[1],self.end[1])
		
		dx = self.end[0] - self.start[0]
		dy = abs(self.end[1] - self.start[1])
		error = 0
		
		try:
			derr = dy/float(dx)
		except:
			return None
		
		ystep = 0
		y = self.start[1]
		
		if self.start[1] < self.end[1]: ystep = 1
		else: ystep = -1
		
		for x in range(self.start[0],self.end[0]+1):
			if self.steep:
				self.path.append((y,x))
			else:
				self.path.append((x,y))
			
			error += derr
			
			if error >= 0.5:
				y += ystep
				error -= 1.0
		
		if not self.path[0] == (start[0],start[1]):
			self.path.reverse()
	
	def swap(self,n1,n2):
		return [n2,n1]

def draw_diag_line(start,end):
	_l = line_diag(start,end)
	
	return _l.path

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