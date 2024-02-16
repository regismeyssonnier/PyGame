# coding=utf-8
import pygame
import time 
import random
import math
import datetime
import copy

dis_width = 1700
dis_height = 956
NBMAXTOUR = 10
SIMULATION_TURNS = 4
SOLUTION_COUNT = 6

PI = 3.1415926535897932384626433832795
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
		self.simulation = Simulation([], checkpoint, 25, 10)
		self.score = 0

	def sel_checkpoint(self, check):
		self.checkpoint = check

	def get_direction(self):
		return self.vdir

	def Move(self):
		

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

#new generation
class Vector2(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Sim(object):
	def __init__(self):
		self.pos = Vector2(0,0)
		self.speed = Vector2(0,0)
		self.angle = 0
		self.angletot = 0
		self.next_checkpoint = 1
		self.thrust = 200
		self.check_point = 1
		self.check_pass = 1
		self.direction = Vector2(1,1)

	def clone(self):
		new_sim = Sim()
		new_sim.pos.x = self.pos.x
		new_sim.pos.y = self.pos.y
		new_sim.speed.x = self.speed.x
		new_sim.speed.y = self.speed.y
		new_sim.angle = self.angle
		new_sim.angletot = self.angletot
		new_sim.next_checkpoint = self.next_checkpoint
		new_sim.thrust = self.thrust
		new_sim.check_point = self.check_point
		new_sim.check_pass = self.check_pass
		new_sim.direction.x = self.direction.x
		new_sim.direction.y = self.direction.y

		return new_sim

	def simulate(self):
		anglef = (self.angletot + self.angle + 360) % 360
		angle_rad = anglef * math.pi / 180.0
		direction = Vector2(math.cos(angle_rad) * float(self.thrust), math.sin(angle_rad) * float(self.thrust))
		self.speed = Vector2(self.speed.x + direction.x, self.speed.y + direction.y)
		self.pos.x += self.speed.x
		self.pos.y += self.speed.y

	def end_simulate(self):
		self.pos.x = int(self.pos.x)
		self.pos.y = int(self.pos.y)
		self.speed = Vector2(int(self.speed.x * 0.85), int(self.speed.y * 0.85))




class Solutionm:
	def __init__(self):
		self.moves1 = [Sim()] * 30  # Crée un tableau de taille 20 avec des valeurs None
		self.score = -2000000000

	def clone(self):
		new_solution = Solutionm()  # Crée une nouvelle instance de Solutionm
		new_solution.moves1 = [sim.clone() for sim in self.moves1]  # Copie le tableau moves1
		new_solution.score = self.score  # Copie la valeur de score
		return new_solution


class Simulation2(object):
	def __init__(self, nbs, d):
		self.NB_SOL = nbs
		self.DEPTH = d
		self.solution = []
		self.checkpoints = []
		self.podRadius = 400.0
		self.podRadiusSqr = self.podRadius * self.podRadius
		self.minImpulse = 120.0
		self.frictionFactor = 0.85
		self.MAXT = 5
		self.MINT = 0
		self.MAXA = 18
		self.MINA = -18
		self.state_chaser = 0
		self.state_chaser2 = 0

		for i in range(nbs):
			sol = Solutionm()
			for j in range(d):
				rng = random.Random()
				sm = Sim()
				angle = rng.randint(self.MINA, self.MAXA)
				sm.angle = min(max(angle, -18), 18)
				thrust = rng.randint(self.MINT, self.MAXT)
				sm.thrust = thrust#min(max(thrust, 0), 3)
				
				sol.moves1[j] = sm

			sol.score = -2000000000
			self.solution.append(sol)

		
	def Trier(self):
		self.solution.sort(key=lambda x: x.score, reverse=True)


	def mutate2(self, ind):
		dthrust = lambda: random.randint(self.MINT, self.MAXT)
		dangle = lambda: random.randint(self.MINA, self.MAXA)
		dcross = lambda: random.randint(0, 2)

		sol = self.solution[ind].clone()

		for i in range(self.DEPTH):
			num = dcross()
			if num == 0:
				sol.moves1[i].angle = dangle()
				sol.moves1[i].angle = max(-18, min(sol.moves1[i].angle, 18))
			
			elif num == 1:
				sol.moves1[i].thrust = dthrust()
				#sol.moves1[i].thrust = max(0, min(sol.moves1[i].thrust, 3))
			
			else:
				sol.moves1[i].angle = dangle()
				sol.moves1[i].angle = max(-18, min(sol.moves1[i].angle, 18))
		

				sol.moves1[i].thrust = dthrust()
				#sol.moves1[i].thrust = max(0, min(sol.moves1[i].thrust, 3))
			

		return sol


	def play(self, p, turn, time):
		start_time = datetime.datetime.now()
		maxt = -1

		def get_time():
			global maxt
			stop_time = datetime.datetime.now()
			duration = (stop_time - start_time).total_seconds() * 1000  # Convertir en millisecondes
			maxt = int(duration)
			return duration <= time

		dthrust = lambda: random.randint(self.MINT, self.MAXT)
		dangle = lambda: random.randint(self.MINA, self.MAXA)
		dsol = lambda: random.randint(0, self.NB_SOL - 1)
		dgene = lambda: random.uniform(0, 1.0)

		if turn > 0:
			for n in range(self.NB_SOL):
				for d in range(self.DEPTH - 1):
					self.solution[n].moves1[d] = self.solution[n].moves1[d + 1].clone()
					self.solution[n].score = -2000000000

				i = self.DEPTH - 1
				self.solution[n].moves1[i].angle = dangle()
				self.solution[n].moves1[i].angle = max(-18, min(self.solution[n].moves1[i].angle, 18))
		
				self.solution[n].moves1[i].thrust = dthrust()
				#self.solution[n].moves1[i].thrust = max(0, min(self.solution[n].moves1[i].thrust, 3))
			

		nb_turn = 0

		while get_time():
			score_chaser = 0

			for ind in range(self.NB_SOL):
				solret = self.mutate2(ind)

				pod1 = Sim()
				pod1.angletot = p.angletot;
				pod1.speed.x = p.speed.x;
				pod1.speed.y = p.speed.y;
				pod1.pos.x = p.pos.x
				pod1.pos.y = p.pos.y
				pod1.score = -2000000000;
				pod1.check_point = p.check_point;
				pod1.check_pass = p.check_pass;
				
				for i in range(self.DEPTH):
								
					pod1.angle = solret.moves1[i].angle
					pod1.thrust = solret.moves1[i].thrust
					#print(pod1.angle)
					#print(pod1.thrust)
					pod1.simulate()
					pod1.angletot = (int(pod1.angletot + pod1.angle + 360) % 360)
					pod1.end_simulate()

					p1dist = distance(pod1.pos, self.checkpoints[pod1.check_point])

					if p1dist <= 50:
						pod1.check_pass += 1
						pod1.check_point = (pod1.check_point + 1) % len(self.checkpoints)



				p1dist = distance(pod1.pos, self.checkpoints[pod1.check_point])
				score = 50000 * pod1.check_pass - p1dist
				solret.score = score + solret.moves1[0].thrust

				if solret.score > self.solution[self.NB_SOL - 1].score:
					self.solution[self.NB_SOL - 1] = solret.clone()
					self.Trier()

					#for i in range(self.NB_SOL):
					#	print(str(i) +  " " + str(self.solution[i].score))


				nb_turn += 1

		#print(nb_turn)
		#print(self.solution[0].score)


class SuperPod:

	def __init__(self, x, y, angle, checkpoint):

		self.simulation = Simulation2(3, 15)
		self.sim = Sim()
		self.sim.pos.x = x
		self.sim.pos.y = y
		self.sim.speed = Vector2(0,1)
		self.sim.angletot = angle
		self.simulation.checkpoints = checkpoint
		self.sim.check_pass = 1
		self.sim.check_point = 1

	def Move(self, turn, time):

		self.simulation.play(self.sim, turn, time)

		solm = self.simulation.solution[0]

		anglef = int(self.sim.angletot + solm.moves1[0].angle + 360) % 360
		angleRad = anglef * PI / 180.0
		thrust = solm.moves1[0].thrust
		#print(str(thrust) + " " + str(solm.moves1[0].angle))
		dir_x = math.cos(angleRad) * float(thrust)
		dir_y = math.sin(angleRad) * float(thrust)
		self.sim.direction.x = math.cos(angleRad) * 100
		self.sim.direction.y = math.sin(angleRad) * 100
		self.sim.speed.x += dir_x
		self.sim.speed.y += dir_y
		self.sim.pos.x = int(self.sim.pos.x + self.sim.speed.x)
		self.sim.pos.y = int(self.sim.pos.y + self.sim.speed.y)
		self.sim.speed = Vector2(int(self.sim.speed.x * 0.85), int(self.sim.speed.y * 0.85))

		self.sim.angletot = int(self.sim.angletot + solm.moves1[0].angle + 360) % 360
	



#end new generation


pygame.init()

blue = (0, 0, 255)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 102)
green = (0, 255, 0)
purple = (200, 0, 255)
cyan = (0, 120, 255)

color = [red, white, yellow, green, purple, black, purple, cyan]


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
		pygame.draw.rect(dis, color[2], [c.x-25, c.y-25, 50, 50])



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
	pod = SuperPod(X, Y, 0, checkpoint)
	direction = Point(checkpoint[pod.sim.check_point].x, checkpoint[pod.sim.check_point].y)
	
	pod2 = Pod(X, Y, 0, checkpoint)
	pod2.sel_checkpoint(checkpoint)
	direction2 = Point(checkpoint[pod2.nextCheckpoint].x, checkpoint[pod2.nextCheckpoint].y)
	
	"""
	NBPOD = 10
	directionp=[]
	pods=[]
	for i in range(NBPOD):
		p = Pod(X, Y, 0, checkpoint)
		p.sel_checkpoint(checkpoint)
		pods.append(p)
		d = Point(checkpoint[pods[i].nextCheckpoint].x, checkpoint[pods[i].nextCheckpoint].y)
		directionp.append(d)
	"""

	#sim = Simulation2()
	#sim.InitCheckpointsFromInput(3, 5, checkpoint)
	#solver = Solver(sim)
	
	turn = 0
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

		dt = det(direction, checkpoint[pod.sim.check_point])

		ang = angle_vec(direction, checkpoint[pod.sim.check_point], pod.sim.pos)
		if(dt < 0):
			ang = -ang
		#if(ang > 18):
		#	ang = 18
		#if ang < -18:
	#		ang = -18

		#angle = (angle+ang)%360
		pod.Move(turn, 45)
		#pod2.Move()

		#for i in range(NBPOD):
		#	pods[i].Move()

		#print("angle " + str(ang) + ", thrust " + str(thrust) + ", check " + str(pod.nextCheckpoint))
		
		#direction = Point(math.cos(ang*3.14159/180.0) * 10000.0, math.sin(ang*3.14159/180.0) * 10000.0)
		#direction = checkpoint[pod.sim.check_point]
		pygame.draw.line(dis, purple, [pod.sim.pos.x,pod.sim.pos.y], [pod.sim.pos.x+pod.sim.direction.x, pod.sim.pos.y+pod.sim.direction.y])
		#direction2 = checkpoint[pod2.nextCheckpoint]
		#pygame.draw.line(dis, purple, [pod2.pos.x,pod2.pos.y], [direction2.x, direction2.y])


		#for i in range(NBPOD):
		#	directionp[i] = checkpoint[pods[i].nextCheckpoint]
		#	pygame.draw.line(dis, purple, [pods[i].pos.x,pods[i].pos.y], [directionp[i].x, directionp[i].y])


		d = distance(pod.sim.pos, checkpoint[pod.sim.check_point])
		#print("distance " + str(d))
		if(d <= 50):
			pod.sim.check_point = (pod.sim.check_point + 1) % len(checkpoint)
			pod.sim.check_pass += 1

		d = distance(pod2.pos, checkpoint[pod2.nextCheckpoint])
		#print("distance " + str(d))

		"""
		if(d <= 50):
			pod2.nextCheckpoint = (pod2.nextCheckpoint + 1) % len(checkpoint)
			pod2.checkpass += 1

		for i in range(NBPOD):
			d = distance(pods[i].pos, checkpoint[pods[i].nextCheckpoint])
			#print("distance " + str(d))
			if(d <= 50):
				pods[i].nextCheckpoint = (pods[i].nextCheckpoint + 1) % len(checkpoint)
				pods[i].checkpass += 1
		"""
			
		#p = ConvertSolutionToOutput(solver.Solve([pod, Pod(0,0,0,[])], 0.95), [pod, Pod(0,0,0,[])])
							  
		pygame.draw.rect(dis, color[0], [pod.sim.pos.x, pod.sim.pos.y, 50, 50])
		#print ("x " + str(pod.pos.x) + " y " + str(pod.pos.y))

		#pygame.draw.rect(dis, purple, [pod2.pos.x, pod2.pos.y, 50, 50])

		#for i in range(NBPOD):
		#	pygame.draw.rect(dis, color[i%len(color)], [pods[i].pos.x, pods[i].pos.y, 50, 50])



		draw_checkpoint(checkpoint)
		#pygame.draw.line(dis, yellow, [pod.pos.x,pod.pos.y], [pod.pos.x+pod.get_direction().x*400.0, pod.pos.y+pod.get_direction().y*400.0])
		#pygame.draw.line(dis, yellow, [pod2.pos.x,pod2.pos.y], [pod2.pos.x+pod2.get_direction().x*400.0, pod2.pos.y+pod2.get_direction().y*400.0])

		
		#for i in range(NBPOD):
		#	pygame.draw.line(dis, yellow, [pods[i].pos.x,pods[i].pos.y], [pods[i].pos.x+pods[i].get_direction().x*400.0, pods[i].pos.y+pods[i].get_direction().y*400.0])


		#for i in range(NBMAXTOUR):
		#	pygame.draw.rect(dis, green, [pod.simulation.retp[i].pos.x, pod.simulation.retp[i].pos.y, 5, 5])
		
		#for i in range(NBMAXTOUR):
		#	pygame.draw.rect(dis, green, [pod2.simulation.retp[i].pos.x, pod2.simulation.retp[i].pos.y, 5, 5])
		
		#for p in range(NBPOD):
		#	for i in range(NBMAXTOUR):
		#		pygame.draw.rect(dis, green, [pods[p].simulation.retp[i].pos.x, pods[p].simulation.retp[i].pos.y, 5, 5])
		
		pygame.display.update()

		turn+=1

		#clock.tick(interval_tour)

	
	pygame.quit()
	quit()
	


gameLoop()