# coding=utf-8
import pygame
import time 
import random
import math

dis_width = 1700
dis_height = 956
NBMAXTOUR = 20
#-------------------------------CLASS
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

def distance(p1, p2):
	return math.sqrt((p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y))

def norme(p):
	return math.sqrt(p.x * p.x + p.y * p.y)

def det(p1, p2):
	return p1.x * p2.y - p1.y * p2.x 

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

class Checkpoint:

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.radius = 50

class Simulation:

	def __init__(self, pod, checkpoint, init_game, pct):
		self.pod = pod
		self.checkpoint = checkpoint
		self.game = []
		self.init_game = init_game
		self.pct = pct
		self.turn = []
		self.score = 0
		self.retp = []
		self.ret = []
		self.nb_coup = 0
		self.nb_touch = 0
		for i in range(init_game):
			self.game.append([random.uniform(-18.0, 18.0), random.randint(0, 3)])


	def Simulate(self, epodb, dft):
		vt = []
		ncheck = 0
		self.ret = []
		self.retp = []
		epod2 = Pod(epodb.pos.x, epodb.pos.y, epodb.angle, epodb.checkpoint)
		epod2.nextCheckpoint = epodb.nextCheckpoint
		epod2.v.x = epodb.v.x
		epod2.v.y = epodb.v.y
		ncheck = epodb.nextCheckpoint
		last_check = ncheck
		self.score = 0
		
		for x in range(NBMAXTOUR):
			
			for i in range(self.init_game):
				#a = self.game[i][0]
				epod = Pod(epod2.pos.x, epod2.pos.y, epod2.angle, epod2.checkpoint)
				epod.nextCheckpoint = epod2.nextCheckpoint
				epod.v.x = epod2.v.x
				epod.v.y = epod2.v.y
			
				ar = epod.angle
				thrust = self.game[i][1]

				#dir = Point(10000.0, 10000.0)
				#vd = Point(math.cos(a*3.14159/180.0) * float(dir.x), math.sin(a*3.14159/180.0) * float(dir.y))
		
				#va = Point(math.cos(ar*3.14159/180.0) * float(10000.0), math.sin(ar*3.14159/180.0) * float(10000.0))
		
				#vb = Point(self.checkpoint[epod.nextCheckpoint].x - epod.pos.x,self.checkpoint[epod.nextCheckpoint].y - epod.pos.y)
			
				#angva = self.game[i][0]  *(dft * 5.0 / 100.0) + ar
				angva = self.game[i][0] + ar

				vv = Point(math.cos(angva*3.14159/180.0) * float(thrust), math.sin(angva*3.14159/180.0) * float(thrust))
				epod.v.x += vv.x
				epod.v.y += vv.y
				epod.pos.x = round(epod.pos.x + epod.v.x)
				epod.pos.y = round(epod.pos.y + epod.v.y)
				epod.v.x = epod.v.x * 0.85
				epod.v.y = epod.v.y * 0.85
				epod.v.x = int(epod.v.x)
				epod.v.y = int(epod.v.y)
				epod.angle = angva
				vt.append(epod)

				




			vd = []
			for i in range(self.init_game):
				dist = distance(vt[i].pos, self.checkpoint[ncheck])
				
				vd.append([distance(vt[i].pos, self.checkpoint[ncheck]), i])

			vd.sort()

			isg = int(float(self.init_game * self.pct / 100.0))

			rd = random.randint(0, isg-1)
			epod2 = Pod(vt[vd[rd][1]].pos.x, vt[vd[rd][1]].pos.y, vt[vd[rd][1]].angle, vt[vd[rd][1]].checkpoint)
			epod2.nextCheckpoint = vt[vd[rd][1]].nextCheckpoint
			epod2.v.x = vt[vd[rd][1]].v.x
			epod2.v.y = vt[vd[rd][1]].v.y

			if distance(epod2.pos, self.checkpoint[ncheck]) <= 50:
				ncheck = (ncheck+1)%len(self.checkpoint)
			

			ind = vd[rd][1]
			self.retp.append(epod2)
			self.ret.append(ind)
			vt = []
		
		touch = True
		checkpass = 0
		self.nb_touch = -1
		for i in range(NBMAXTOUR):
			dist = distance(self.retp[i].pos, self.checkpoint[last_check])
			if dist <= 50:
				checkpass += 1
				if(touch):
					self.nb_touch = i
					touch = False

			self.score += checkpass * 30000 - dist

		#print("isg " + str(ind))

		return self.ret[0]


class Pod:
	def __init__(self, x, y, angle, checkpoint):
		self.pos = Point(x, y)
		self.last_v = Point(1, 1)
		self.v = Point(1, 1)
		self.angle = angle
		self.nextCheckpoint = 0
		self.vdir = Point(0.0, 0.0)
		self.time = 0;
		self.last_time = 0;
		self.checkpoint = checkpoint
		self.checkpass = 0
		self.start = True
		self.playret = False
		self.lock = False
		self.simulation = Simulation([], checkpoint, 50, 10)

	def sel_checkpoint(self, check):
		self.checkpoint = check

	def get_direction(self):
		return self.vdir

	def Move(self, thrust, angle):
		a = angle
		ar = (self.angle ) % 360
		thrust = 2.0

		self.last_time = self.time
		self.time = pygame.time.get_ticks();
		diff_t = self.time - self.last_time

		"""dir = Point(10000.0, 10000.0)
			vd = Point(math.cos(a*3.14159/180.0) * float(dir.x), math.sin(a*3.14159/180.0) * float(dir.y))
			va = Point(math.cos(ar*3.14159/180.0) * float(10000.0), math.sin(ar*3.14159/180.0) * float(10000.0))
		
			vb = Point(self.checkpoint[self.nextCheckpoint].x - self.pos.x,self.checkpoint[self.nextCheckpoint].y - self.pos.y)
			angva = angle_vec(va, self.checkpoint[self.nextCheckpoint], self.pos)
			angva = angva  *(diff_t * 18 / 100)
		
			dt = det(va, vb)
			mass = 1.0
			if(angva > 18):
				angva = 18
			
			if(dt < 0):
				angva = -angva
			#mass = -mass

			angva = angva  *(diff_t * 0.85 / 100.0)"""

		#self.pos.x = self.pos.x * 16000 / dis_width
		#self.pos.y = self.pos.y * 9000 / dis_height
		pd = Pod(self.pos.x, self.pos.y , self.angle, self.checkpoint)
		pd.nextCheckpoint = self.nextCheckpoint;
		pd.v.x = self.v.x
		pd.v.y = self.v.y


		if self.simulation.nb_touch != -1 and self.simulation.nb_touch <= NBMAXTOUR/2 and self.lock == False:
			print("unlock" + str(self.simulation.nb_touch))
			self.playret = True
			self.lock = True
		
		if  self.playret == False or self.start:
			an = self.simulation.Simulate(pd, diff_t)
			self.simulation.nb_coup = 0
			self.start = False
		elif self.lock and self.playret:
			print("play sim")
			an = self.simulation.ret[self.simulation.nb_coup]

		

		if self.playret:
			self.simulation.nb_coup += 1

		if(self.simulation.nb_coup == NBMAXTOUR):
			self.simulation.nb_coup = 0
			self.simulation.nb_touch = -1
			self.lock = False
			self.playret = False


		#print("ang game " + str(self.simulation.game[an][0]))
		angva = (self.simulation.game[an][0] + self.angle)%360
		thrust = self.simulation.game[an][1] 

		#print("thrust " + str(thrust))
		#direction = Point(math.cos(a*3.14159/180.0) * 10000.0, math.sin(a*3.14159/180.0) * 10000.0)
		#ang = angle_vec()
		
		vv = Point(math.cos(angva*3.14159/180.0) * float(thrust), math.sin(angva*3.14159/180.0) * float(thrust))
		#ec = Point((mass*vv.x*vv.x) / 2.0, (mass*vv.y*vv.y) / 2.0)
	
		self.v.x += vv.x 
		self.v.y += vv.y
		self.vdir.x = vv.x * dis_width / 16000
		self.vdir.y = vv.y * dis_height / 9000
		vx = Point(self.pos.x, self.pos.y)
		
		#lpos = Point(self.pos.x, self.pos.y)
		#dir = Point(10000.0, 10000.0)
		#vd = Point(math.cos(a*3.14159/180.0) * float(dir.x), math.sin(a*3.14159/180.0) * float(dir.y))
		dd = Point(0.0, 0.0)
		dd.x = self.v.x
		dd.y = self.v.y
		ang = a*3.14159/180.0
		ddr = Point(0.0, 0.0)
		ddr.x = dd.x * math.cos(ang) + dd.y * -math.sin(ang)
		ddr.y = dd.x * math.sin(ang) + dd.y * math.cos(ang)
		ddr.x += self.pos.x
		ddr.y += self.pos.y
		#print(str(ddr.x) + " v " + str(ddr.y))
		self.pos.x = round(self.pos.x + self.v.x)
		self.pos.y = round(self.pos.y + self.v.y)
		self.v.x = self.v.x * 0.85
		self.v.y = self.v.y * 0.85
		self.v.x = int(self.v.x)
		self.v.y = int(self.v.y)
		self.angle = angva

		#self.pos.x = self.pos.x * dis_width / 16000
		#self.pos.y = self.pos.y * dis_height / 9000

#---------------------------END CLASS


pygame.init()

blue = (0, 0, 255)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 102)
green = (0, 255, 0)
purple = (200, 0, 255)
cyan = (0, 120, 255)

color = [red, white, yellow, green, purple]


dis=pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Pod')


clock = pygame.time.Clock()
interval_tour = 100;

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

#var importante


def Your_score(score):
	value = score_font.render("Votre score : " + str(score), True, yellow)
	dis.blit(value, [0, 0]) 

def draw_checkpoint(check):
	for c in check:
		pygame.draw.rect(dis, color[2], [c.x, c.y, 50, 50])



def gameLoop():

	X = 100
	Y = 300
	x1_change = 0
	y1_change = 0
	deplacement_x = 20
	deplacement_y = 20
	game_over = False
	angle = 0
	thrust = 2
	angle_act = 0
	touched = False

	
	
	checkpoint = [Checkpoint(200, 300), Checkpoint(1000, 150), Checkpoint(1500, 600), Checkpoint(1000, 400), Checkpoint(750, 700)]
	pod = Pod(X, Y, 0, checkpoint)
	pod.sel_checkpoint(checkpoint)
	direction = Point(checkpoint[pod.nextCheckpoint].x, checkpoint[pod.nextCheckpoint].y)

	while not game_over:
		
		for event in pygame.event.get():
			#print(event)
			if event.type == pygame.QUIT:
				game_over = True
			if event.type == pygame.KEYDOWN:				
				if event.key == pygame.K_KP4:
					x1_change = -deplacement_x
					y1_change = 0
	
				elif event.key == pygame.K_KP6:
					x1_change = deplacement_x
					y1_change = 0
	
				elif event.key == pygame.K_KP8:
					y1_change = -deplacement_y
					x1_change = 0
	
				elif event.key == pygame.K_KP5:
					y1_change = deplacement_y
					x1_change = 0
				elif event.key == pygame.K_a:
					touched = True
					angle += 1
					if angle > 18:
						angle = 18
				elif event.key == pygame.K_q:
					touched = True
					angle -= 1;
					if angle < -18:
						angle = -18
				elif event.key == pygame.K_z:
					thrust += 1
				elif event.key == pygame.K_s:
					thrust -= 1
					if(thrust < 1):
						thrust = 1

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a:
					touched = False
					
				elif event.key == pygame.K_q:
					touched = False
					

		X = X + x1_change
		Y = Y + y1_change 		
		dis.fill(blue)
		
		#direction = Point(checkpoint[pod.nextCheckpoint].x, checkpoint[pod.nextCheckpoint].y)

		dt = det(direction, checkpoint[pod.nextCheckpoint])

		ang = angle_vec(direction, checkpoint[pod.nextCheckpoint], pod.pos)
		if(dt < 0):
			ang = -ang
		#if(ang > 18):
		#	ang = 18
		#if ang < -18:
	#		ang = -18

		#angle = (angle+ang)%360
		pod.Move(thrust, ang);
		#print("angle " + str(ang) + ", thrust " + str(thrust) + ", check " + str(pod.nextCheckpoint))
		
		#direction = Point(math.cos(ang*3.14159/180.0) * 10000.0, math.sin(ang*3.14159/180.0) * 10000.0)
		direction = checkpoint[pod.nextCheckpoint]
		pygame.draw.line(dis, purple, [pod.pos.x,pod.pos.y], [direction.x, direction.y])
		
		d = distance(pod.pos, checkpoint[pod.nextCheckpoint])
		#print("distance " + str(d))
		if(d <= 50):
			pod.nextCheckpoint = (pod.nextCheckpoint + 1) % len(checkpoint)
			pod.checkpass += 1

				
		pygame.draw.rect(dis, color[0], [pod.pos.x, pod.pos.y, 50, 50])
		print ("x " + str(pod.pos.x) + " y " + str(pod.pos.y))

		draw_checkpoint(checkpoint)
		pygame.draw.line(dis, yellow, [pod.pos.x,pod.pos.y], [pod.pos.x+pod.get_direction().x*400.0, pod.pos.y+pod.get_direction().y*400.0])


		for i in range(NBMAXTOUR):
			pygame.draw.rect(dis, green, [pod.simulation.retp[i].pos.x, pod.simulation.retp[i].pos.y, 5, 5])
					
		pygame.display.update()

		clock.tick_busy_loop(interval_tour)

	
	pygame.quit()
	quit()
	


gameLoop()