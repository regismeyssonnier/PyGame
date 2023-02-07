import math

def distance(p1, p2):
	return math.sqrt((p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y))

def normalize(p1):
	l = math.sqrt(p1.x*p1.x + p1.y*p1.y)
	return Point(p1.x / l, p1.y / l)

def normalize3(p1):
	l = math.sqrt(p1.x*p1.x + p1.y*p1.y + p1.z*p1.z)
	return Point3(p1.x / l, p1.y / l, p1.z / l)

def norme(p):
	return math.sqrt(p.x * p.x + p.y * p.y)

def norme3(p):
	return math.sqrt(p.x * p.x + p.y * p.y + p.z * p.z)

def det(p1, p2):
	return p1.x * p2.y - p1.y * p2.x 

def cross3(p1, p2):
	return Point3(p1.y * p2.z - p1.z * p2.y, p1.z * p2.x - p1.x * p2.z, p1.x * p2.y - p1.y * p2.x)

def dot3(p1, p2):
	return p1.x * p2.x + p1.y * p2.y + p1.z * p2.z

def angle_vec(p1, p2, pm):
	u = Point(p1.x - pm.x, p1.y - pm.y)
	v = Point(p2.x - pm.x, p2.y - pm.y)
	nu = norme(u);
	nv = norme(v)

	uvpsc = u.x * v.x + u.y * v.y
	#print("--costh " + str(nu*nv))
	if(nu*nv == 0):costh = 0
	else:costh = uvpsc / (nu * nv)
	#print("costh " + str(costh))
	if(costh < -1.0):costh = -1.0
	if(costh > 1.0):costh = 1.0
	return math.acos(costh) * 180.0 / 3.1415926535897932384626433832795


def angle_vec3(p1, p2, pm):
	u = Point3(p1.x - pm.x, p1.y - pm.y, p1.z - pm.z)
	v = Point3(p2.x - pm.x, p2.y - pm.y, p2.z - pm.z)
	nu = norme3(u);
	nv = norme3(v)

	uvpsc = u.x * v.x + u.y * v.y + u.z * v.z
	#print("--costh " + str(nu*nv))
	if(nu*nv == 0):costh = 0
	else:costh = uvpsc / (nu * nv)
	#print("costh " + str(costh))
	if(costh < -1.0):costh = -1.0
	if(costh > 1.0):costh = 1.0
	return math.acos(costh) * 180.0 / 3.1415926535897932384626433832795


class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Point3:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

