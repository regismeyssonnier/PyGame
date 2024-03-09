# coding: utf-8
import pygame
import time 
import random
import math
import datetime
import copy
import numpy as np
import random

dis_width = 1700
dis_height = 956
NBMAXTOUR = 10
SIMULATION_TURNS = 4
SOLUTION_COUNT = 6
#DX = 9.4117647058823529411764705882353
#DY = 9.4142259414225941422594142259414
DX = 1.0
DY = 1.0
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



class NeuralNetwork:

	def __init__(self, dimension, LR):
		self.network  =[]
		self.network_w = []
		self.network_b = []
		self.etiquette = []
		self.LR = LR
		self.LRB = LR

		

		# Initialisation des param?tres d'Adam
		self.beta1 = 0.9
		self.beta2 = 0.999
		self.epsilon = 1e-8
		self.epoch = 0 

		i = 0
		for dim in dimension:
			self.network.append([0.0]*dim)

			if i > 0:
				self.network_b.append(np.random.uniform(low=-0.5, high=0.5, size=(dim)))

			if i < len(dimension)-1:
				self.network_w.append(np.random.uniform(low=-0.5, high=0.5, size=(dim, dimension[i+1])))


			i+=1


		self.m_w = [[[0.0] * len(k) for k in j] for j in self.network_w]
		self.v_w = [[[0.0] * len(k) for k in j] for j in self.network_w]
		self.m_b = [[0.0] * len(k) for k in self.network_b]
		self.v_b = [[0.0] * len(k) for k in self.network_b]

		self.cost = [0.0] * dimension[-1]

		#print(self.network_w)

	def sigmoid(self, x):
		x = np.clip(x, -700, 700)  # Ajustez la plage selon vos besoins
		return 1 / (1 + np.exp(-x))
		

	def derive(self, x):
		return x * (1 - x)

	def Relu(self, x):
		return np.maximum(0, x)

	def dRELU(self, x):
		return np.greater(x, 0)

	def SetEtiquette(self, et):
		self.etiquette = et;

	def SetInput(self, inp):
		self.network[0] = inp

	def normalizeInput(self):
		# Calculate mean
		mean = sum(self.network[0]) / len(self.network[0])

		# Calculate standard deviation
		stddev = math.sqrt(sum((val - mean) ** 2 for val in self.network[0]) / len(self.network[0]))

		# Normalize input data
		for i in range(len(self.network[0])):
			self.network[0][i] = (self.network[0][i] - mean) / stddev

			  
	def ForwardNN(self):

		for i in range(0, len(self.network)-2):
			for j in  range(0, len(self.network[i+1])):
				h = 0.0
				for k in range(0, len(self.network[i])):
					h += self.network[i][k] * self.network_w[i][k][j]

				h += self.network_b[i][j];
				self.network[i+1][j] = self.Relu(h);


		ind = len(self.network)-2
		for j in range(len(self.network[ind+1])):
			h = 0.0
			for k in range(len(self.network[ind])):
				h += self.network[ind][k] * self.network_w[ind][k][j]
			h += self.network_b[ind][j];
			self.network[ind + 1][j] = self.sigmoid(h);

		
		for i in range(len(self.network[-1])):
			self.cost[i] += self.network[-1][i] - self.etiquette[i]

	def PredictNN(self):

		for i in range(0, len(self.network)-2):
			for j in  range(0, len(self.network[i+1])):
				h = 0.0
				for k in range(0, len(self.network[i])):
					h += self.network[i][k] * self.network_w[i][k][j]

				h += self.network_b[i][j];
				self.network[i+1][j] = self.Relu(h);


		ind = len(self.network)-2
		for j in range(len(self.network[ind+1])):
			h = 0.0
			for k in range(len(self.network[ind])):
				h += self.network[ind][k] * self.network_w[ind][k][j]
			h += self.network_b[ind][j];
			self.network[ind + 1][j] = self.sigmoid(h);


	def BackwardNN(self):
	   
		result = [ [] for _ in range(len(self.network)-1) ]
		
		for i in range(len(self.network[-1])):
			result[-1].append(self.cost[i] * self.derive(self.network[-1][i]))
			self.network_b[-1][i] -= self.LR * result[-1][i]


		for i in range(len(result) - 2, -1, -1):
			#print(i)
			for j in range(len(self.network[i + 1])):
				result[i].append(0.0)
				for k in range(len(self.network[i + 2])):
					result[i][j] += self.network_w[i + 1][j][k] * result[i + 1][k] * self.dRELU(self.network[i + 1][j])
				self.network_b[i][j] -= self.LR * result[i][j]

		#print(result)

		for i in range(len(self.network) - 2, -1, -1):
			for j in range(len(self.network[i])):
				for k in range(len(self.network[i + 1])):
					self.network_w[i][j][k] -= self.LR * self.network[i][j] * result[i][k]

		self.cost = [0.0] * len(self.network[-1])

	def BackwardNNA(self):
	   
		result = [ [] for _ in range(len(self.network)-1) ]
		
		for i in range(len(self.network[-1])):
			result[-1].append(self.cost[i] * self.derive(self.network[-1][i]))
			self.network_b[-1][i] -= self.LR * result[-1][i]


		for i in range(len(result) - 2, -1, -1):
			#print(i)
			for j in range(len(self.network[i + 1])):
				result[i].append(0.0)
				for k in range(len(self.network[i + 2])):
					result[i][j] += self.network_w[i + 1][j][k] * result[i + 1][k] * self.dRELU(self.network[i + 1][j])
				self.network_b[i][j] -= self.LR * result[i][j]

		
		# Mise ? jour des poids avec l'optimiseur Adam
		for i in range(len(self.network) - 2, -1, -1):
			for j in range(len(self.network[i])):
				for k in range(len(self.network[i + 1])):
					# Calcul des gradients pour les poids
					gradient_w = self.network[i][j] * result[i][k]

					# Mise ? jour d'Adam
					self.m_w[i][j][k] = self.beta1 * self.m_w[i][j][k] + (1 - self.beta1) * gradient_w
					self.v_w[i][j][k] = self.beta2 * self.v_w[i][j][k] + (1 - self.beta2) * (gradient_w ** 2)

					m_hat_w = self.m_w[i][j][k] / (1 - self.beta1 ** (self.epoch + 1))
					v_hat_w = self.v_w[i][j][k] / (1 - self.beta2 ** (self.epoch + 1))

					self.network_w[i][j][k] -= self.LR * m_hat_w / (np.sqrt(v_hat_w) + self.epsilon)

		# Mise ? jour des biais avec l'optimiseur Adam
		for i in range(len(self.network) - 2, -1, -1):
			for j in range(len(self.network[i+1])):
				# Calcul des gradients pour les biais
				gradient_b = result[i][j]

				# Mise ? jour d'Adam
				self.m_b[i][j] = self.beta1 * self.m_b[i][j] + (1 - self.beta1) * gradient_b
				self.v_b[i][j] = self.beta2 * self.v_b[i][j] + (1 - self.beta2) * (gradient_b ** 2)

				m_hat_b = self.m_b[i][j] / (1 - self.beta1 ** (self.epoch + 1))
				v_hat_b = self.v_b[i][j] / (1 - self.beta2 ** (self.epoch + 1))

				self.network_b[i][j] -= self.LR * m_hat_b / (np.sqrt(v_hat_b) + self.epsilon)



		self.cost = [0.0] * len(self.network[-1])

		self.epoch += 1

	def TrainingNN(self, inp, target, nbi, nb):
	 
		indexes = list(range(nbi))

		for i in range(nb):
			random.shuffle(indexes)

			for jj in range(nbi):
				j = indexes[jj]
				self.SetInput(inp[j])
				self.SetEtiquette(target[j])
				self.ForwardNN()
				self.BackwardNN()

				if (i + 1) % 1000 == 0:
					cost_ = [0.0] * len(self.network[-1])

					for k in range(nbi):
						self.SetInput(inp[k])
						self.SetEtiquette(target[k])
						self.ForwardNN()

						for l in range(len(self.network[-1])):
							cost_[l] += (self.network[-1][l] - target[k][l]) ** 2

					for l in range(len(self.network[-1])):
						cost_[l] = cost_[l] / len(self.network[-1])

					for l in range(len(self.network[-1])):
						print("output {}: {}".format(l, self.network[-1][l]))

					for l in range(len(self.network[-1])):
						print("error {}: {}".format(l, cost_[l]))


	def Save_NN(self, name):
		f = open("Test/" + name, "w")

		for i in range(len(self.network_w)):
			for j in range(len(self.network_w[i])):
				for k in range(len(self.network_w[i][j])):
					f.write(str(self.network_w[i][j][k])+'\n')

		for i in range(len(self.network_b)):
			for j in range(len(self.network_b[i])):
				f.write(str(self.network_b[i][j])+'\n')

		f.close()

	def Load_NN(self, name):
		f = open("Test/" + name, "r")

		for i in range(len(self.network_w)):
			for j in range(len(self.network_w[i])):
				for k in range(len(self.network_w[i][j])):
					self.network_w[i][j][k] = float(f.readline())


		for i in range(len(self.network_b)):
			for j in range(len(self.network_b[i])):
				self.network_b[i][j] = float(f.readline())

		f.close()

	def Adapt_LR(self, good, nb):

		self.LR = (self.LRB / nb) * ((nb+0.0001) - good)

	def InitByDumpNN(self, nw, nb):
		self.network_w = nw
		self.network_b = nb
			

	def DisplayOutputNN(self):
		print(self.network_w)
		print(self.network_b)
		print("output:")
		for i in range(len(self.network[-1])):
			print("{} {}".format(i, self.network[-1][i]))


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
		self.thrust = 5.0
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
		self.moves1 = [Sim()] * 40  # Crée un tableau de taille 20 avec des valeurs None
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
		self.MAXT = 5.0
		self.MAXTF = 5.0
		self.MINT = 0
		self.MAXA = 18
		self.MINA = -18
		self.state_chaser = 0
		self.state_chaser2 = 0
		self.reward = [0]*37

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

		self.reward = [0]*37

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
					pod1.thrust = 4#solret.moves1[i].thrust
					solret.moves1[i].thrust = 4
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
				score = (2000 * pod1.check_pass - p1dist) + 4
				self.reward[int(solret.moves1[0].angle) + 18] = score / 50000.0
				solret.score = score 

				if solret.score > self.solution[self.NB_SOL - 1].score:
					self.solution[self.NB_SOL - 1] = solret.clone()
					self.Trier()

					#for i in range(self.NB_SOL):
					#	print(str(i) +  " " + str(self.solution[i].score))


				nb_turn += 1

		#print(nb_turn)
		#print(self.solution[0].score)

	def playRL(self, p, turn, time):
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
				
		nb_turn = 0
				
		score_chaser = 0

		self.solution[0].score = -2000000000

		while get_time():
			pass

			
		

		
				
		index = 0;
		for ang in range(-18, 19):

			solret = Solutionm()

			pod1 = Sim()
			pod1.angletot = p.angletot;
			pod1.speed.x = p.speed.x;
			pod1.speed.y = p.speed.y;
			pod1.pos.x = p.pos.x
			pod1.pos.y = p.pos.y
			pod1.score = -2000000000;
			pod1.check_point = p.check_point;
			pod1.check_pass = p.check_pass;
			
			solret.moves1[0].angle = ang
			solret.moves1[0].thrust = dthrust()
			pod1.angle = ang
			pod1.thrust = 1
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
			score = 2000 * pod1.check_pass - p1dist
			solret.score = score + solret.moves1[0].thrust
				
			if solret.score > self.solution[0].score:
				self.solution[0]  =solret


			nb_turn += 1



class SuperPod:

	def __init__(self, x, y, angle, checkpoint):

		self.simulation = Simulation2(3, 7)
		self.sim = Sim()
		self.sim.pos.x = x
		self.sim.pos.y = y
		self.sim.speed = Vector2(0,1)
		self.sim.angletot = angle
		self.simulation.checkpoints = checkpoint
		self.sim.check_pass = 1
		self.sim.check_point = 1
		self.sim.thrust = self.simulation.MAXT
		self.sim.angle = 0;
		self.nn = NeuralNetwork([7, 37, 37], 0.1)
		self.nn.InitByDumpNN([[[-0.102,-0.181,-0.360,0.106,-0.500,1.274,-0.157,-0.161,-0.227,0.019,2.804,-0.104,0.008,0.025,0.096,-0.218,-0.054,-0.247,0.131,1.539,0.061,0.088,-1.087,-1.482,0.064,-0.075,0.526,-0.080,0.049,-0.058,-0.172,-0.427,-0.277,0.144,-0.042,0.011,1.855],[0.449,-0.405,-0.141,0.414,0.092,2.993,-0.194,-0.073,0.103,0.057,0.374,0.224,0.244,0.239,-0.093,-0.137,0.060,-0.144,2.668,-2.991,0.314,-0.208,-2.448,1.103,-0.046,0.273,-0.566,-0.077,-1.392,0.094,-0.040,0.257,2.092,0.066,-0.007,0.024,0.228],[-0.067,-0.287,0.074,-0.179,-0.171,-0.458,0.252,-0.495,-0.263,-0.136,-1.649,-0.591,-0.018,-0.224,0.058,0.295,-0.022,-0.126,0.541,-1.655,0.304,-0.343,-0.985,0.591,0.110,0.157,0.014,0.200,-0.602,-0.134,-0.055,0.207,-1.414,-0.391,-0.221,0.006,-0.558],[-0.327,0.143,-0.499,-0.141,0.396,-0.851,0.002,-0.189,0.042,-0.268,-1.780,-0.277,-0.365,-0.163,-0.278,-0.536,0.141,-0.150,0.026,1.054,-0.262,0.098,1.252,1.344,0.039,-0.483,-5.863,-0.617,2.114,-0.062,0.499,-0.139,0.579,-0.016,0.094,0.064,-1.658],[0.300,0.342,0.025,0.177,0.085,-0.250,0.161,0.172,-0.045,-0.085,0.256,0.010,0.405,0.242,0.193,-0.092,-0.012,0.070,-0.959,0.312,0.182,0.459,0.795,0.206,0.404,-0.038,0.070,0.101,-0.046,-0.249,0.107,0.037,0.062,-0.054,0.059,0.164,0.066],[0.464,-0.466,0.140,-0.089,-0.097,-0.021,-0.050,0.047,0.037,-0.035,-0.211,-0.053,-0.270,0.054,-0.000,-0.222,0.084,-0.071,0.096,-0.124,-0.063,0.061,-0.771,-0.466,0.210,0.022,0.714,-0.221,1.900,0.129,0.072,-0.215,-0.299,-0.104,0.130,-0.092,-0.984],[0.112,-0.230,-0.306,-0.258,-0.749,0.429,0.112,0.163,-0.192,-0.422,0.204,1.728,0.068,-0.027,-0.116,-0.234,-0.279,0.056,-1.298,0.094,-0.004,-0.273,-0.018,-2.277,-0.063,-0.683,-0.248,0.076,-1.392,-0.235,-0.062,-0.306,-0.343,-0.286,-0.105,0.231,0.335]],
[[-0.446,0.217,0.104,-0.237,0.021,-0.344,-0.595,-0.067,-0.114,-0.738,-0.516,-0.397,0.160,-0.278,-0.348,0.063,0.258,-0.220,-0.355,-0.157,-0.069,-0.036,-0.078,-0.069,-0.165,0.011,0.191,-0.066,0.130,-0.074,-0.345,-0.292,0.075,0.106,0.313,0.043,-0.047],[-0.083,-0.122,0.291,-0.312,0.054,-0.161,-0.150,-0.422,-0.805,0.291,-0.104,0.202,0.034,0.099,0.075,-0.176,0.291,-0.099,-0.102,0.006,-0.126,-0.031,-0.118,0.192,0.046,0.161,0.038,-0.748,0.189,-0.097,-1.493,-1.084,-0.281,-0.094,-0.485,-0.456,-0.267],[-0.195,-0.055,0.090,0.073,0.275,-0.003,0.257,0.281,0.051,0.039,0.062,-0.249,0.113,-0.332,-0.096,0.265,-0.018,0.146,-0.110,-0.290,0.450,0.027,-0.052,0.241,0.172,-0.030,-0.398,-0.010,0.229,-0.181,0.234,-0.260,-0.162,0.100,0.062,-0.113,0.445],[-0.270,0.110,-0.405,-0.817,-0.123,-0.028,-0.329,-0.089,-0.321,-0.126,-0.058,-0.129,-0.019,0.114,-0.302,-0.301,0.056,0.253,0.377,0.136,0.232,0.221,-0.058,-0.212,0.146,-0.285,-0.062,0.057,0.293,-0.096,-0.534,-0.006,0.149,0.068,-0.143,0.204,0.417],[-0.522,-0.230,-0.198,-0.897,0.261,-0.787,-1.184,-0.388,-0.459,-0.164,-0.084,-0.219,0.243,-0.280,-0.430,-0.137,-0.110,-0.786,-0.881,0.022,-0.769,-0.150,-0.362,-0.066,-0.231,-0.003,-0.591,-0.376,-0.324,-0.030,-1.129,-0.423,0.008,0.101,-0.653,0.134,-0.279],[-14.481,-15.679,-19.789,-13.200,-18.610,-19.121,-6.370,-17.832,-1.328,-9.076,-8.185,-18.828,-16.705,-12.257,-19.297,-1.006,-24.726,-10.828,-0.315,-16.270,-15.573,-1.372,-8.826,-1.470,-1.290,-0.681,-10.926,0.108,-1.221,-0.744,0.050,0.262,-1.254,-1.996,-0.522,-0.753,-1.061],[-0.030,-0.354,-0.087,0.061,-0.256,-0.477,0.065,0.001,-0.074,-0.168,0.044,-0.157,-0.087,-0.146,0.204,0.106,0.184,0.043,-0.259,-0.003,0.216,-0.317,-0.121,0.110,-0.207,-0.069,-0.103,0.109,-0.031,-0.353,-0.023,0.061,-0.258,0.081,0.282,-0.119,-0.291],[0.138,-0.088,-0.059,-0.152,0.099,0.047,-0.183,-0.059,0.013,0.201,-0.180,0.127,-0.061,-0.214,0.058,-0.055,0.569,-0.116,0.090,-0.067,0.030,-0.220,0.130,0.239,0.157,-0.084,0.249,-0.031,-0.334,0.350,-0.086,-0.318,-0.015,0.037,-0.040,-0.023,0.136],[-0.434,0.192,-0.151,0.048,0.285,-0.406,-0.608,0.025,-0.550,-0.082,-0.158,0.374,-0.028,-0.607,-0.255,-0.538,-0.038,-0.330,-0.810,0.184,-0.158,0.248,-0.139,-0.186,0.106,-0.404,-0.033,0.078,-0.048,-0.194,0.010,-0.704,-0.017,0.276,0.138,0.103,-0.083],[-0.183,0.223,-0.048,0.484,-0.265,0.176,0.446,0.270,-0.200,0.163,0.224,-0.386,0.086,-0.237,0.385,-0.254,0.014,0.139,-0.184,-0.278,-0.058,0.326,0.009,0.078,0.234,0.230,0.384,0.113,0.071,-0.341,-0.075,0.050,0.019,0.293,-0.274,0.253,0.053],[-3.113,-17.138,-23.278,-19.299,-24.270,0.521,-26.303,-2.961,-1.028,-20.213,-24.635,-1.168,-28.165,-27.364,0.738,-0.844,0.838,-24.870,-1.506,1.037,-17.325,-25.667,-1.672,-0.756,-24.807,-0.810,-20.868,-3.410,-0.989,-1.688,-17.788,-2.250,-1.441,-0.449,-22.419,-1.362,-1.341],[-20.948,-28.977,-9.334,-20.767,-4.359,-28.548,-24.855,-24.461,-0.026,-16.702,-23.340,-31.472,-32.263,-31.023,-27.649,-12.391,-18.664,-8.423,-21.294,-32.086,0.039,-1.141,-1.904,-1.499,-1.166,-2.141,-0.045,-1.427,-1.155,-0.932,-0.935,-2.045,-0.684,-0.142,-0.589,-0.270,-0.675],[0.034,-0.124,0.123,-0.074,-0.193,0.450,-0.064,0.408,-0.047,0.012,0.099,-0.019,0.220,0.025,0.340,-0.042,-0.178,0.231,-0.477,-0.041,-0.239,-0.093,-0.115,-0.327,-0.323,0.185,0.018,-0.106,-0.015,-0.325,0.216,-0.065,-0.146,-0.195,-0.559,-0.114,-0.229],[0.341,0.366,-0.094,-0.324,-0.080,0.316,0.282,-0.179,0.010,0.042,0.234,0.059,-0.253,-0.060,-0.085,-0.052,-0.196,0.100,-0.144,0.432,-0.015,-0.062,-0.018,-0.177,-0.216,0.216,0.114,-0.454,0.199,0.105,-0.170,-0.090,0.270,0.113,0.201,0.314,-0.488],[-0.165,-0.299,0.033,-0.152,0.113,-0.002,0.136,0.069,-0.345,0.136,-0.044,-0.008,-0.139,-0.031,0.020,-0.260,-0.119,-0.196,-0.073,0.265,0.077,-0.066,0.059,-0.532,-0.142,0.275,-0.386,-0.222,-0.170,-0.040,0.104,-0.176,0.001,0.205,-0.207,-0.123,0.210],[-0.158,0.135,-0.064,0.271,0.233,-0.013,0.201,0.038,-0.209,0.115,0.253,-0.139,0.109,-0.098,-0.085,0.446,0.322,-0.216,-0.186,0.192,-0.223,0.131,0.154,0.206,0.419,-0.236,-0.011,-0.435,0.641,0.006,0.203,0.023,-0.040,-0.004,0.086,-0.071,0.573],[-0.140,0.294,0.126,0.064,0.068,-0.372,-0.282,0.084,0.147,0.291,-0.077,0.135,-0.281,-0.572,0.068,0.437,-0.007,-0.168,0.031,-0.108,0.133,0.375,-0.306,0.130,-0.208,-0.100,0.026,0.049,0.359,0.214,-0.026,-0.244,-0.481,0.005,-0.290,-0.182,-0.074],[-0.007,0.077,-0.305,-0.226,0.087,-0.235,0.256,-0.188,0.291,-0.235,0.002,-0.197,-0.206,0.244,-0.129,0.788,-0.058,-0.134,0.067,0.304,-0.060,0.382,0.048,0.182,0.022,0.151,0.188,0.138,-0.022,-0.210,-0.101,0.186,-0.056,-0.188,-0.012,0.431,0.345],[-18.083,-3.552,-2.284,-6.601,-1.809,-5.033,-3.502,-2.566,-6.777,-18.050,-2.162,-3.850,-0.566,-0.843,-3.869,-2.206,-1.603,-1.542,-1.165,-1.971,-1.726,-2.355,-0.573,-0.697,-2.162,-0.951,0.961,-1.191,0.129,-0.280,-0.381,0.527,0.347,-1.242,-0.922,-0.721,-0.729],[-22.697,-1.005,-25.721,-0.148,-1.563,-2.979,-34.929,-0.493,-2.621,-1.903,-0.476,-27.148,-1.492,-1.075,-0.374,-32.894,-6.184,-1.855,-2.195,-1.887,-1.101,-3.240,-34.026,-2.768,-2.211,-3.550,-5.696,-4.520,-1.313,-3.584,-35.169,-8.443,-40.793,-2.382,-18.070,-36.945,-2.880],[-0.268,-0.076,0.066,0.130,0.317,-0.173,0.172,-0.070,-0.066,-0.092,-0.236,0.032,-0.333,-0.038,0.123,-0.162,-0.001,-0.364,-0.163,-0.057,0.008,0.256,-0.148,0.406,0.341,0.201,-0.094,-0.067,-0.191,-0.134,0.067,-0.082,-0.148,-0.042,-0.182,-0.034,-0.278],[0.066,-0.093,0.080,-0.110,0.101,0.177,0.059,-0.002,-0.130,0.060,0.474,-0.100,-0.221,0.157,0.548,-0.140,0.132,0.292,-0.345,0.055,0.014,0.022,0.126,-0.099,-0.019,0.088,0.037,-0.207,-0.022,0.099,0.004,0.098,0.209,-0.088,0.096,0.140,-0.235],[-28.562,-37.003,-32.750,-32.530,-2.556,-2.343,-34.223,-5.746,-5.537,-36.544,-11.532,-0.372,-1.986,-28.321,-4.269,-3.268,-1.090,-4.888,-5.218,-2.150,-4.526,-2.644,-0.517,-3.687,-3.304,-0.628,0.582,-1.549,-2.629,-1.253,-3.868,-5.910,-32.228,-1.874,-28.391,-0.741,-1.560],[-1.369,-0.192,-0.225,-1.224,-0.051,-2.412,-46.031,-0.409,-0.316,-29.757,-1.159,-0.249,-1.699,-2.274,-1.482,-3.068,-1.111,-4.151,-8.833,-1.454,-3.166,-1.574,-2.094,-2.906,-2.318,-1.983,-4.848,-19.966,-2.102,-2.487,-38.210,-2.861,-3.244,-1.545,-1.466,-1.327,-23.623],[-0.174,0.294,0.434,-0.291,-0.374,-0.249,0.004,0.077,-0.253,-0.629,-0.126,-0.320,0.175,0.245,-0.097,0.186,-0.301,0.360,0.067,-0.452,0.366,0.177,-0.303,-0.041,-0.024,0.154,0.295,0.219,-0.114,-0.064,-0.035,0.326,-0.161,0.024,0.064,0.378,-0.306],[-0.395,-0.394,0.177,-0.117,-0.188,-0.091,-0.243,-0.371,-0.559,-0.078,-0.078,-0.173,0.022,0.217,-0.357,0.011,-0.303,-0.067,-0.096,-0.877,0.207,-0.473,0.189,0.001,-0.097,-0.021,0.190,0.174,0.003,-0.029,0.037,0.241,-0.597,-0.515,0.175,-0.311,-0.507],[-1.709,-19.308,-30.436,-0.845,-0.540,-1.499,-15.896,-1.033,-0.501,-19.007,-21.905,-0.414,-25.685,-0.988,-1.451,-1.428,-2.467,-27.745,-2.144,-2.480,-1.590,-2.032,-2.854,-2.027,-0.737,-2.247,-1.271,-0.599,-14.045,-1.777,-20.355,-0.732,-4.008,-2.122,-15.332,-22.181,-1.328],[0.278,0.092,-0.019,-0.197,-0.004,-0.072,-0.047,-0.107,-0.230,0.170,0.140,0.001,0.243,0.291,-0.347,0.168,-0.031,-0.011,-0.047,0.177,-0.435,0.128,0.092,0.082,-0.334,-0.186,-0.020,-0.226,-0.212,-0.361,-0.500,-1.328,0.155,-0.505,-0.404,-0.147,-0.318],[-0.765,-1.860,-4.261,-1.597,-13.726,-1.174,-46.524,-1.751,-3.163,-28.898,-35.060,-6.353,-29.247,-2.683,-3.081,-0.686,-1.978,-1.756,-0.989,-2.261,-1.277,-0.950,-0.191,-1.786,-1.357,-23.454,-1.178,-1.863,-1.149,-1.543,-2.132,0.188,-1.495,-1.214,-3.038,-0.711,-0.452],[-0.127,-0.399,-0.146,-0.217,0.065,0.119,-0.054,-0.075,-0.470,-0.350,-0.245,-0.264,-0.450,-0.275,-0.341,-0.319,-0.079,-0.387,-0.254,-0.464,-0.073,-0.109,-0.212,-0.468,-0.060,-0.241,0.005,-0.129,0.180,-0.167,0.318,-0.135,-0.037,-0.215,-0.115,-0.316,0.016],[-0.437,-0.126,-0.452,0.173,0.440,-0.469,-1.027,0.251,-0.525,-0.057,-0.559,-0.592,-0.297,-0.348,0.168,-0.264,0.329,-0.052,-0.781,0.034,0.025,-0.027,-0.229,-0.221,-0.185,-0.253,-0.159,0.001,-0.005,-0.089,0.020,-0.205,-0.935,0.143,0.271,-0.385,-0.024],[-0.280,-0.304,-0.266,-0.366,0.365,-0.494,-0.599,0.116,-0.701,-0.741,-1.237,-0.785,-0.005,-0.307,-0.215,0.063,0.411,0.114,-0.769,-0.472,0.043,-0.229,-0.041,-0.461,-0.413,0.117,0.159,-0.580,-0.081,-0.332,-0.074,-0.840,-0.565,-0.545,0.246,-0.703,-0.247],[-3.933,-8.816,-9.420,-5.870,1.398,-6.280,-7.474,-9.965,-8.602,-4.182,-12.430,-6.640,-8.964,-9.765,-7.799,-13.535,-13.484,-9.277,-9.265,-10.868,-12.734,-0.660,-15.337,-1.664,-0.483,-14.911,-16.608,-1.019,-1.328,-1.763,-1.660,-18.232,-1.695,-0.573,-1.156,-1.003,-0.760],[0.068,-0.255,0.312,0.239,0.031,-0.259,-0.097,0.126,-0.044,0.074,0.027,0.086,0.147,-0.102,0.111,0.067,-0.279,-0.186,0.196,-0.009,-0.132,-0.180,0.141,-0.432,-0.354,0.344,0.180,-0.042,-0.016,-0.246,-0.224,-0.027,0.002,0.034,-0.197,0.120,0.071],[-0.104,-0.019,0.294,0.011,0.077,0.583,0.169,-0.153,-0.453,-0.079,0.231,0.281,-0.346,-0.157,-0.095,0.145,-0.135,0.259,-0.209,0.207,-0.001,-0.210,0.171,0.269,-0.111,-0.156,0.294,-0.078,0.012,-0.183,-0.343,0.164,0.161,-0.264,-0.223,-0.061,0.172],[0.062,0.361,-0.237,-0.286,0.176,-0.193,-0.041,-0.274,0.154,-0.061,-0.038,-0.263,-0.006,0.412,0.095,-0.196,0.059,-0.129,0.062,0.308,0.001,-0.153,0.052,0.182,-0.390,-0.091,0.257,-0.074,-0.188,-0.220,-0.232,-0.128,-0.164,0.004,-0.253,-0.097,0.086],[-0.797,-1.492,-0.603,-3.436,-1.448,-1.475,-1.677,-1.838,-0.660,-1.255,-0.573,-1.383,-2.160,-1.779,-24.525,-1.358,-2.319,-2.675,-0.824,-32.326,-2.279,-3.104,-1.477,-1.790,-1.847,-2.758,-38.141,-3.573,-1.813,-3.231,-26.143,-0.925,-1.375,-4.600,-1.314,-2.202,-1.596]]],
[[0.105,-0.113,-0.234,-0.101,-0.294,-0.698,-0.395,-0.283,-0.476,-0.284,0.049,-0.746,0.163,0.081,0.141,-0.453,-0.045,-0.309,-0.593,-1.144,-0.373,-0.083,-0.439,-0.507,-0.185,-0.124,-0.154,-0.243,-0.993,-0.584,-0.500,-0.330,-0.295,-0.464,-0.463,-0.201,-0.598],
[0.217,-0.550,-0.789,-0.099,-0.647,-0.310,-0.901,-0.748,-1.115,0.204,-0.656,-1.140,-0.849,-0.579,-0.470,-0.588,-0.217,-0.365,0.079,0.024,0.128,0.251,-0.726,-0.349,-0.364,-0.525,-0.853,-0.804,-0.816,-0.532,-0.934,-1.629,-1.193,-0.593,-0.634,-1.112,-0.780]])

			
			
		"""[[[0.599,0.096,-0.112,-0.373,-0.041,-0.206,-0.375,0.164,-0.209,-0.034,-0.136,-0.128,0.340,-0.430,0.051,-0.832,0.223,-0.068,1.566,1.610,0.752,-0.144,-0.151,1.558,-0.692,1.765,-0.300,-0.063,2.079,-0.046,0.152,0.137,-0.260,-1.424,-0.243,0.042,-0.336],[-0.768,-0.005,0.171,0.087,-1.879,0.208,0.285,1.645,-0.254,0.313,0.542,-0.070,-2.044,-1.823,0.253,2.278,0.295,-0.198,1.381,1.267,2.480,-0.005,1.531,1.095,-1.301,0.065,-0.176,-0.009,1.284,0.042,0.229,-0.641,1.571,-0.845,0.156,0.110,2.247],[-0.114,0.157,0.144,0.014,-0.249,0.037,0.016,-0.227,-0.126,-0.091,-0.349,-0.173,-1.398,-1.290,-0.163,-0.323,-0.176,-0.175,-1.962,-1.473,-1.259,0.311,0.839,0.116,-0.657,-1.634,0.020,-0.136,-2.201,-0.102,0.224,-0.116,0.632,0.850,-0.276,0.342,0.333],[-4.921,-0.217,-0.117,0.460,1.497,-0.468,-0.336,-0.564,0.030,-0.277,-0.254,0.117,0.939,0.790,-0.016,1.635,-0.050,0.148,-1.056,0.149,-0.089,-0.446,-0.917,-0.720,1.313,-0.902,-0.062,0.043,-0.675,0.003,0.041,-0.191,-1.947,-0.572,-0.246,-0.455,-1.473],[0.121,0.195,-0.159,0.463,0.294,-0.031,-0.100,0.220,0.111,0.081,0.241,-0.067,0.538,-0.033,0.133,0.380,0.513,0.044,-0.007,0.465,-0.314,0.051,-0.282,0.321,0.691,0.577,0.268,0.341,0.368,0.136,0.135,0.165,0.304,0.303,-0.167,0.031,-0.655],[1.215,0.152,0.133,0.029,1.169,-0.111,0.143,-0.854,-0.086,-0.010,0.363,0.089,1.746,0.672,0.201,-0.408,0.080,-0.156,0.934,-0.895,-0.309,0.027,0.574,-0.746,-0.969,0.685,0.591,-0.095,-0.486,-0.077,0.023,-0.047,-0.875,1.147,0.183,0.046,0.170],[-0.185,0.524,-0.216,-0.052,-1.770,0.065,-0.263,-0.322,-0.234,-0.093,-0.027,-0.101,-1.037,1.018,-0.186,-1.622,0.126,0.074,-0.554,0.061,-0.069,-0.124,-0.661,-0.687,-0.096,0.027,-0.268,-0.187,-0.033,-0.002,-0.234,-0.217,0.629,-0.701,-0.297,0.085,0.952]],
[[-1.010,-6.432,-19.271,-0.267,0.363,-0.243,-8.048,-0.503,0.167,-11.866,-16.479,0.241,-17.254,0.506,-0.399,-1.006,-1.255,-19.225,-1.173,-1.050,-0.723,-1.558,-1.564,-1.205,0.142,-1.987,-0.883,0.603,-5.583,-1.336,-8.862,-0.015,-2.668,-2.108,-6.438,-10.808,-0.306],[-0.054,-0.081,-0.090,0.005,-0.095,-0.061,-0.188,-0.090,-0.207,-0.212,0.359,-0.159,-0.647,0.115,0.321,-0.342,-0.013,-0.036,-0.018,-0.417,-0.185,-0.362,-0.167,-0.245,0.014,-0.249,0.139,0.107,-0.112,0.054,-0.185,-0.089,-0.122,-0.593,-0.106,-0.090,-0.165],[-0.104,0.159,0.042,0.374,-0.075,-0.008,-0.082,-0.207,-0.093,0.279,-0.049,-0.128,-0.255,0.324,0.131,-0.021,0.182,-0.330,-0.252,-0.408,0.003,-0.249,-0.002,0.131,-0.097,-0.203,-0.475,-0.267,0.285,0.086,0.312,-0.071,0.654,-0.156,-0.077,-0.097,-0.060],[0.406,-0.178,-0.155,-0.294,0.084,-0.093,-0.431,-0.149,-0.066,-0.267,-0.324,-0.165,-0.142,0.060,0.133,0.121,0.081,-0.305,-0.033,-0.121,-0.497,-0.273,-0.044,-0.213,-0.440,-0.273,-0.097,-0.267,-0.078,-0.130,-0.044,-0.351,0.148,0.052,0.088,-0.150,-0.055],[0.136,-1.416,-0.987,-2.057,-5.392,-0.704,-25.481,-0.597,-1.675,-15.550,-4.354,-2.703,-5.281,-0.939,-2.646,-0.319,-1.184,-0.544,0.382,-1.120,-0.557,0.103,1.097,-1.673,0.124,-5.889,-0.831,-1.760,-0.778,-1.218,-1.616,1.468,-0.693,-1.541,-3.581,-0.248,-0.237],[0.456,-0.166,-0.104,-0.289,-0.230,0.059,-0.093,-0.350,0.040,-0.128,0.368,-0.199,0.131,0.038,-0.101,-0.480,0.138,0.340,0.200,-0.443,-0.036,-0.065,-0.141,0.118,0.086,-0.466,0.076,0.172,-0.011,-0.163,0.296,-0.034,-0.256,-0.321,0.269,-0.036,-0.266],[0.231,-0.189,0.066,0.279,0.395,-0.275,-0.091,-0.291,0.027,0.066,0.119,0.097,-0.650,-0.149,-0.146,0.727,-0.275,-0.296,0.047,-0.155,0.505,0.100,-0.050,-0.101,0.248,0.001,0.364,-0.098,-0.430,0.006,-0.096,0.080,-0.267,-0.167,0.102,0.182,-0.038],[-1.620,-0.721,-1.838,-1.403,-2.630,-0.854,-5.821,-1.979,-1.655,-4.087,-1.070,-0.874,-1.759,-0.936,-1.153,-1.087,-2.223,-1.891,-0.655,-0.762,-1.393,-1.345,-0.982,-3.687,-1.525,-2.495,-0.379,-0.406,-0.199,-4.065,-1.022,-1.320,-3.730,-1.704,0.178,-1.459,0.662],[-0.210,0.044,-0.350,-0.109,-0.269,-0.046,-0.300,0.029,-0.094,-0.075,-0.403,0.606,-0.151,-0.398,0.223,0.102,-0.071,-0.236,0.037,-0.689,-0.119,0.094,-0.252,-0.170,-0.084,-0.072,0.322,0.299,-0.219,-0.098,-0.049,-0.218,-0.237,-0.341,-0.208,-0.054,-0.194],[-0.297,-0.360,-0.222,0.239,-0.025,0.127,-0.268,-0.289,-0.151,-0.476,-0.281,-0.226,-0.022,-0.468,-0.356,-0.274,0.033,0.023,-0.061,-0.210,-0.125,-0.135,-0.431,-0.064,-0.244,-0.058,-0.185,0.297,-0.157,-0.390,0.072,-0.163,-0.261,0.076,-0.491,0.160,-0.226],[-0.704,-1.665,-0.347,-0.659,-2.427,0.240,-0.594,-1.256,-1.429,-0.162,-0.406,-0.045,-0.241,-1.298,0.318,-0.088,-0.280,-1.032,0.079,-0.216,-0.086,-0.038,0.158,0.082,0.142,0.085,-1.215,-0.196,-0.075,-0.153,-0.310,0.025,-0.054,-0.118,0.043,-0.060,-0.069],[-0.275,-0.216,-0.401,-0.133,0.280,-0.203,-0.006,-0.264,-0.043,0.171,0.210,0.353,-0.143,-0.309,0.129,0.106,0.291,-0.089,0.118,-0.254,-0.125,-0.069,0.032,0.245,0.015,0.138,-0.061,0.029,0.104,0.005,0.033,-0.366,0.005,-0.154,-0.094,-0.242,0.313],[0.134,-15.308,-12.144,-2.549,-11.384,-1.413,-5.006,-13.073,-2.987,-3.200,-6.856,-12.282,-7.189,-14.285,-0.614,1.115,-2.425,-9.510,-0.728,-1.109,-1.486,-1.570,-0.212,-1.811,-2.671,-6.404,-0.244,-0.132,-0.425,-2.292,-14.601,-5.155,-2.267,1.070,-15.031,-12.096,0.388],[-4.808,-2.580,-11.863,1.002,-11.165,-0.566,-14.462,-0.337,-13.606,-14.981,-13.227,-14.566,0.128,-19.812,0.149,-3.332,-1.272,-1.481,-3.510,-1.524,-0.972,-1.662,-21.412,0.092,-2.884,0.188,-0.960,-2.128,-0.486,-0.421,-2.952,-2.811,-3.306,-0.710,-1.782,-0.999,-0.537],[0.066,0.116,-0.438,-0.444,-0.356,-0.262,-0.904,-0.252,-0.245,-0.233,0.038,-0.282,-0.288,-0.155,-0.335,-0.136,0.019,0.013,-0.191,-0.067,-0.131,-0.011,-0.066,0.051,-0.014,-0.135,0.113,0.186,-0.121,0.237,-0.271,-0.255,-0.261,-0.039,-0.070,0.080,-0.162],[-10.403,-0.609,1.453,-15.335,1.209,-18.467,-6.203,-1.269,-12.695,-8.058,0.648,-2.098,-0.607,0.385,-0.973,-14.417,0.406,-11.919,-14.001,-0.384,-1.771,-0.907,-0.575,-1.992,-0.589,-6.458,-3.148,-1.135,-0.723,-1.828,-1.551,-2.872,-1.091,-0.499,-0.927,-0.846,-0.545],[0.078,0.059,-0.384,-0.172,-0.681,-0.466,-0.515,-0.047,0.149,-0.632,-0.373,-0.208,-0.275,-0.288,-0.623,-0.987,-0.609,0.128,-0.309,0.016,-0.155,0.549,-0.396,-0.314,0.306,-0.126,-0.379,0.224,-0.161,0.179,0.208,-0.525,0.043,-0.049,-0.034,0.222,0.358],[-0.306,-0.360,-0.552,-0.196,-0.011,-0.320,-0.208,-0.049,-0.245,-0.185,-0.351,-0.584,-0.217,-0.152,-0.266,-0.303,-0.204,-0.024,-0.340,0.027,0.253,-0.550,-0.187,-0.118,-0.234,0.081,0.047,-0.307,-0.141,-0.323,-0.070,-0.259,-0.014,-0.221,-0.456,-0.087,-0.037],[-7.832,-6.068,-2.328,-10.130,-9.230,0.989,-1.365,-10.823,-7.515,-1.381,-2.989,-8.999,-2.511,-9.375,-0.011,-0.514,1.365,-3.086,-0.119,0.966,-12.078,-11.463,-10.573,-0.397,-11.124,-0.608,-11.755,-5.415,-0.893,-1.216,-7.639,-1.029,-0.637,-0.044,-9.514,-0.995,-0.911],[-3.690,-3.034,-5.138,-5.848,-6.247,-4.758,-4.762,-3.989,-0.440,-4.232,-9.235,-7.974,-7.005,-4.603,-3.687,-1.090,-6.519,-6.366,0.232,-4.360,-7.054,-13.099,-1.816,0.576,-7.817,-0.812,-5.135,-0.350,-0.407,-0.897,-7.745,-8.651,-2.277,-1.579,-1.157,-0.316,-0.823],[-14.890,-16.247,-4.817,-15.147,-0.785,-15.205,-11.048,-18.625,-1.821,-12.501,-11.964,-16.078,-14.991,-13.619,-16.396,-2.020,-11.688,-17.734,-2.103,-17.901,-10.357,-0.332,-11.478,-1.790,-0.161,-1.825,-3.270,-0.391,-1.244,-0.532,0.541,0.415,-0.543,-0.506,-0.287,-0.317,-0.671],[-0.296,-0.444,-0.123,0.007,0.060,0.146,-0.325,0.225,-0.437,-0.369,-0.142,-0.265,-0.318,0.034,-0.246,-0.557,-0.179,-0.168,-0.654,-0.252,-0.224,-0.096,-0.364,-0.347,-0.028,-0.002,0.191,0.317,-0.134,-0.025,-0.541,-0.279,-0.246,-0.410,-0.266,-0.767,0.020],[-2.410,-0.613,-3.379,-1.847,-1.357,-1.659,-9.466,-1.322,-0.464,-15.604,-1.213,-0.905,-0.158,-0.608,-2.190,-0.867,-1.637,-1.196,-1.748,-1.911,-1.235,-0.730,-0.760,-0.757,-1.356,-0.161,0.017,-0.157,-0.038,-0.106,-1.105,-0.095,-0.207,-1.030,0.004,-0.076,-1.578],[-0.167,-0.743,0.181,-1.779,-1.350,-0.121,-1.047,-1.140,-0.361,-0.581,-0.167,-1.023,-2.074,-1.454,-3.757,-0.645,-1.216,-1.199,-0.005,-10.323,-1.124,-1.434,-1.159,-0.734,-0.378,-1.644,-15.090,-1.924,-1.304,-1.306,-20.165,0.230,-0.242,-1.086,0.675,-0.623,-0.869],[-3.354,-5.010,-5.615,-5.229,-0.276,-1.293,-20.866,-1.393,-0.441,-2.836,-1.638,-0.146,-0.797,-1.126,-0.651,-1.425,-1.475,-0.598,-2.532,0.136,-0.901,-0.633,-0.836,-1.567,-0.176,-0.223,0.524,-0.938,-0.943,-0.812,-2.845,-3.428,-1.687,-0.152,-1.398,-1.678,-0.908],[-7.475,-6.872,-5.718,-6.580,-3.982,1.155,-1.483,-4.404,0.559,-1.440,-2.605,-3.352,-6.086,-4.068,-1.906,0.372,-1.766,-3.375,-0.571,-0.083,-5.486,-3.827,-8.052,-0.532,-4.403,-0.588,-5.192,-4.740,-0.832,-1.520,-2.784,-0.652,-0.604,-0.099,-4.212,-3.369,-0.852],[0.175,0.205,-0.061,0.013,-0.252,0.079,-2.123,-0.500,0.146,-2.270,-0.813,0.116,-0.291,-0.216,-0.033,0.371,-0.230,-0.092,-0.683,-0.332,-0.058,0.107,0.227,-0.260,-0.045,-0.448,-0.330,-0.178,-0.393,-0.529,-1.712,-0.085,-0.153,-0.530,-0.468,-0.725,-0.201],[-0.220,-0.251,-0.269,-0.268,-0.675,0.227,-0.415,-0.627,-0.593,0.167,0.190,-0.182,0.015,-0.056,-0.141,-0.047,-0.157,0.301,-0.023,0.258,0.177,0.063,0.013,0.350,-0.075,-0.074,-0.363,0.032,-0.004,0.350,0.086,0.008,-0.278,0.233,0.004,-0.531,0.188],[-1.764,-2.030,-3.982,-3.863,-6.184,-7.217,-8.013,-3.002,2.150,-0.577,-3.659,-9.259,-0.547,-2.136,-1.256,-7.674,-3.503,-1.603,-6.573,-10.509,-1.863,-7.820,-4.791,-0.791,-8.564,0.231,-4.706,0.337,-0.038,-1.030,-7.213,-0.436,-1.314,-6.333,-0.469,-0.583,-0.709],[-0.055,-0.142,-0.432,-0.229,0.852,0.032,-0.427,0.095,-0.476,-0.204,0.046,-0.253,-0.307,0.050,-0.228,-0.129,0.145,0.226,0.060,0.159,0.228,0.023,-0.029,0.261,0.111,-0.090,0.310,-0.067,0.002,-0.045,-0.110,-0.405,-0.104,-0.019,-0.087,-0.216,-0.190],[-0.212,0.036,0.259,-0.054,0.224,0.165,-0.062,0.072,0.048,0.042,0.023,0.220,0.112,0.361,-0.012,-0.082,0.059,0.131,-0.099,0.021,0.061,-0.441,-0.148,-0.060,0.035,0.184,-0.096,0.172,0.103,-0.038,-0.151,-0.002,0.178,0.028,0.013,0.001,0.180],[0.334,-0.135,0.189,0.057,-0.271,-0.340,-0.754,0.019,-0.680,0.155,-0.055,-0.514,-0.229,-0.257,-0.111,0.137,0.094,-0.494,-0.060,-0.374,0.276,0.286,0.047,-0.056,-0.077,-0.181,-0.118,-0.187,0.032,-0.022,-0.469,-0.441,-0.427,0.166,-0.692,-0.344,-0.122],[-1.614,-2.026,-2.423,-6.303,0.261,-1.441,-0.211,-1.801,0.976,-3.083,-0.314,-0.393,0.788,0.019,-0.490,0.347,-0.740,-0.979,-0.300,0.109,-1.055,-0.448,0.101,-1.063,-1.650,-0.533,0.266,-0.784,-0.703,-2.677,-0.853,-1.551,-0.437,-7.287,-3.117,-3.689,-0.010],[-0.401,-0.616,-0.824,-0.711,-0.365,-1.125,-17.675,-0.532,0.874,-12.109,-1.549,-0.574,-0.532,-2.970,-1.052,-1.400,-1.037,-1.262,-2.278,-0.720,-1.735,-0.613,-1.422,-1.183,-1.016,-1.025,-2.330,-7.431,-1.710,-2.386,-5.026,-1.770,-1.206,-1.187,-0.714,-1.335,-4.067],[-0.104,-0.213,-0.505,-0.195,-0.049,-0.611,-1.592,0.215,-0.073,-0.302,-0.160,-1.553,-0.546,-0.349,-0.684,-0.267,-0.015,-0.439,0.000,-0.256,-0.201,-0.037,-0.309,-0.040,-0.300,-0.749,-0.231,-0.085,-0.261,-0.509,0.366,0.352,-0.517,-0.133,0.055,-0.503,-0.237],[0.153,-0.270,0.111,0.049,-0.578,-0.707,-0.107,-0.169,0.230,-1.000,-0.355,-0.678,0.145,-0.141,-0.098,0.249,0.084,-0.708,-0.044,-0.360,0.053,0.049,0.426,-0.116,-0.116,-0.293,-0.002,0.547,-0.121,-0.311,-0.333,0.054,-0.523,-0.348,-0.152,-0.361,-0.385],[-14.223,-10.773,-5.441,-3.039,-2.496,-4.831,-4.550,-0.615,-4.139,-22.743,-3.139,-3.220,-6.193,-3.229,-2.897,-0.675,-1.866,-0.168,-0.432,-2.014,-1.139,-0.898,-0.897,-0.171,-0.786,-0.699,1.475,-0.658,-0.460,0.076,-0.389,-0.625,0.767,-0.171,-0.041,-0.334,-0.427]]],
[[-0.532,-0.231,-0.429,-0.137,-0.059,-0.156,-0.444,-0.468,0.089,-0.289,-0.217,-0.287,-0.011,-0.861,0.061,0.244,0.047,-0.498,0.110,-0.224,0.179,-0.217,0.112,0.004,-0.227,-0.020,0.110,0.257,-0.094,-0.056,-0.437,0.073,0.106,-0.205,-0.230,-0.536,-0.840],
[-0.022,0.044,-0.003,0.260,-0.378,-0.338,-0.451,-0.353,-1.893,0.341,-0.298,-1.006,-0.501,-0.136,-0.291,-0.742,0.153,-0.306,0.351,0.094,0.435,0.135,-0.344,-0.060,-0.324,-0.426,-0.693,-0.627,-0.198,-0.033,-0.402,-0.798,-1.016,-0.369,-0.559,-0.480,-0.550]])
		"""
			
			
		"""[[[-0.018,-0.185,-0.106,-0.156,-0.061,-0.048,0.049,0.282,-0.173,-0.171,0.125,-0.169,-0.089,-0.327,-0.302,-0.121,-0.123,-0.064,0.085,0.060,-0.236,-0.013,-0.021,0.172,0.112,-0.193,0.143,-0.121,-0.059,-0.048,-0.169,-0.165,-0.179,-0.219,-0.022,0.003,0.099],[-0.157,0.276,0.470,0.248,-0.200,-0.114,0.199,0.373,0.109,0.261,0.225,0.353,-0.267,-0.078,-0.221,-0.015,-0.027,-0.318,0.052,0.011,-0.146,-0.181,0.072,-0.024,0.153,0.214,0.244,0.039,0.013,0.251,-0.310,-0.059,-0.250,-0.148,0.135,0.190,0.189],[-0.006,0.116,0.165,0.167,-0.080,-0.175,-0.095,-0.288,0.355,0.070,0.347,-0.107,-0.218,-0.040,-0.235,0.245,-0.130,0.076,-0.397,0.285,-0.175,-0.176,-0.206,-0.011,0.224,0.130,0.037,0.360,-0.049,-0.062,-0.263,-0.300,-0.267,-0.155,0.117,-0.127,-0.087],[-0.234,-0.152,0.043,-0.307,-0.238,-0.043,0.054,-0.207,-0.434,-0.311,0.070,-0.098,-0.026,0.023,-0.169,-0.593,-0.098,-0.133,-0.012,0.029,0.205,0.145,-0.428,-0.306,-0.296,-0.196,-0.148,-0.032,-0.047,-0.093,-0.193,0.367,-0.012,0.080,-0.213,0.295,-0.029],[-0.050,-0.075,0.435,-0.157,0.276,-0.176,-0.115,0.122,0.077,0.082,0.194,0.204,-0.216,0.256,0.017,0.430,0.042,0.109,0.176,-0.000,-0.057,0.062,0.117,0.307,0.199,0.201,-0.024,0.392,-0.123,0.179,0.187,0.262,0.006,0.163,0.241,0.029,0.035],[0.020,0.117,-0.211,-0.150,0.088,-0.095,-0.027,0.211,-0.111,-0.193,0.156,-0.046,0.035,-0.109,0.104,-0.250,0.081,-0.245,0.108,0.011,0.051,0.195,0.039,0.151,0.096,-0.140,-0.090,-0.017,0.159,-0.347,0.180,0.733,0.213,-0.244,-0.256,-0.126,0.030],[-0.257,-0.041,0.146,0.037,0.257,0.159,-0.074,0.289,-0.378,-0.054,-0.031,-0.392,-0.006,-0.122,-0.372,-0.168,-0.228,-0.256,-0.102,-0.107,-0.273,-0.253,-0.104,0.257,-0.147,-0.273,-0.077,-0.131,-0.061,-0.249,-0.210,0.055,0.137,-0.425,0.253,-0.563,0.345]],
[[-0.069,-0.051,-0.133,0.015,-0.008,0.068,-0.052,-0.058,-0.008,-0.165,-0.192,0.013,-0.173,0.137,-0.055,0.067,-0.182,-0.209,-0.147,-0.113,-0.107,0.018,0.179,-0.119,0.102,-0.129,-0.036,0.292,-0.127,-0.041,-0.067,0.170,-0.027,-0.247,-0.101,-0.099,0.004],[-0.172,-0.050,-0.126,-0.077,0.062,-0.192,-0.107,0.123,0.115,-0.208,-0.059,-0.024,-0.075,-0.227,-0.085,-0.056,-0.041,-0.019,-0.321,-0.150,-0.176,0.190,-0.151,-0.104,0.053,0.058,0.056,-0.177,0.075,-0.014,-0.148,-0.028,0.041,0.095,0.314,0.121,-0.265],[-0.093,0.272,0.199,-0.079,-0.005,0.085,0.137,-0.140,0.190,-0.006,-0.218,-0.023,0.164,0.083,-0.043,-0.182,0.334,0.049,0.199,0.123,0.039,0.399,-0.260,-0.007,0.217,0.093,-0.112,-0.214,-0.078,-0.194,-0.009,0.055,-0.162,0.350,0.062,-0.117,-0.132],[-0.222,0.127,-0.110,-0.097,-0.123,0.175,0.153,-0.146,0.130,0.174,0.040,0.040,0.010,0.071,0.083,-0.323,-0.025,0.121,0.153,-0.187,0.295,0.117,0.266,0.044,0.235,0.340,0.134,-0.152,-0.133,0.066,-0.001,-0.162,0.046,0.237,-0.229,-0.140,0.314],[0.145,0.026,0.246,0.020,0.110,0.380,0.064,-0.173,0.167,0.164,0.151,0.090,-0.124,-0.040,0.299,-0.194,0.411,-0.093,0.352,0.420,-0.119,0.216,0.365,-0.090,-0.071,-0.287,-0.598,-0.235,-0.306,-0.448,0.032,0.292,0.134,-0.293,0.316,-0.185,-0.182],[-0.229,0.066,-0.210,0.270,-0.233,-0.135,-0.048,-0.036,0.065,-0.040,-0.076,-0.060,-0.108,-0.207,0.063,-0.092,-0.296,-0.121,-0.234,-0.088,-0.227,-0.317,-0.107,0.173,-0.183,-0.072,-0.006,0.001,0.041,-0.036,0.261,0.089,0.306,0.032,-0.031,0.382,0.217],[-0.027,-0.086,-0.014,-0.181,0.074,-0.047,-0.019,-0.025,-0.085,-0.050,-0.057,-0.016,-0.079,-0.070,-0.109,-0.144,-0.024,-0.041,-0.152,-0.091,-0.135,0.031,-0.027,-0.098,-0.009,0.011,-0.138,0.050,0.049,0.289,0.107,0.082,-0.061,0.301,0.110,0.519,0.320],[0.001,0.047,-0.012,0.047,-0.075,-0.096,-0.034,0.008,-0.043,-0.053,-0.092,-0.026,0.003,-0.020,-0.019,-0.113,-0.041,-0.000,-0.217,-0.003,0.009,-0.048,-0.004,0.201,-0.107,0.085,-0.067,-0.089,0.381,-0.257,-0.216,0.048,0.060,-0.408,-0.174,0.084,0.118],[-0.087,-0.035,-0.166,0.265,0.150,0.011,-0.087,-0.363,0.047,0.189,-0.101,-0.153,0.039,0.140,-0.028,-0.009,0.066,0.063,0.074,0.086,-0.152,0.115,0.079,-0.061,-0.036,-0.075,0.038,0.020,-0.127,0.067,-0.024,0.103,-0.277,-0.108,-0.189,-0.110,-0.053],[-0.257,-0.121,-0.226,-0.141,-0.032,-0.295,-0.015,-0.146,-0.072,-0.199,-0.239,-0.072,0.037,-0.057,0.036,0.193,-0.015,-0.095,0.148,0.025,-0.133,-0.037,-0.011,-0.276,-0.084,-0.005,0.207,0.077,-0.099,-0.423,-0.163,-0.178,0.082,-0.108,-0.253,0.059,0.269],[-0.138,-0.313,-0.132,0.108,-0.220,-0.054,0.496,0.211,-0.231,0.406,-0.255,-0.032,-0.328,0.057,0.194,0.157,-0.115,-0.176,-0.069,0.295,0.131,-0.183,0.196,0.275,0.173,0.008,-0.084,-0.286,0.033,0.085,-0.110,0.103,-0.229,-0.099,0.109,-0.377,0.164],[0.154,0.144,0.036,0.404,0.209,0.441,-0.356,0.269,-0.053,0.012,-0.201,0.115,0.018,0.006,-0.438,0.201,-0.128,0.175,-0.324,-0.306,0.199,-0.095,-0.150,-0.468,0.062,-0.009,-0.018,-0.382,0.346,0.217,0.075,0.401,0.004,-0.025,-0.236,0.219,0.367],[-0.274,-0.333,0.053,0.168,-0.001,0.234,0.232,-0.133,-0.204,-0.018,0.088,-0.131,-0.070,0.286,0.070,0.295,0.052,0.070,0.010,0.322,0.314,0.216,0.153,0.093,0.311,-0.004,0.235,0.265,0.308,0.368,0.156,0.102,0.155,-0.344,0.014,-0.043,0.061],[0.061,-0.071,0.395,-0.131,0.406,0.271,-0.020,-0.060,-0.012,-0.045,-0.098,0.051,-0.103,-0.026,0.205,-0.056,0.021,-0.022,-0.183,0.205,-0.052,-0.001,0.154,-0.284,0.248,-0.167,0.044,0.206,-0.159,-0.064,-0.009,-0.648,0.118,-0.387,-0.211,0.149,0.206],[-0.056,-0.215,-0.198,0.267,-0.134,0.080,0.009,-0.063,0.127,-0.072,-0.302,-0.205,-0.047,-0.035,-0.202,0.219,0.051,-0.335,-0.087,-0.042,-0.243,0.275,0.375,-0.284,0.011,-0.373,-0.260,-0.068,-0.128,-0.148,-0.122,-0.058,-0.133,-0.094,-0.260,-0.115,0.128],[-0.171,0.140,0.067,0.017,0.051,0.382,-0.279,0.046,-0.348,-0.015,0.193,0.171,-0.463,-0.092,-0.117,0.374,0.163,-0.302,0.103,0.028,-0.075,-0.355,0.035,0.199,-0.090,0.342,-0.108,-0.014,0.125,-0.146,0.211,-0.161,0.010,0.006,-0.094,-0.005,0.030],[-0.097,0.229,-0.244,-0.145,0.316,0.018,-0.163,-0.118,0.241,0.184,0.175,0.218,-0.082,0.383,-0.368,-0.163,-0.363,-0.306,0.190,0.148,0.039,0.285,0.206,0.078,0.037,0.072,-0.249,0.003,0.135,0.136,-0.035,0.318,0.473,0.303,0.164,-0.177,-0.454],[-0.075,-0.056,-0.033,-0.141,-0.243,0.166,-0.018,-0.173,-0.087,0.251,0.302,-0.173,-0.183,0.060,0.083,-0.138,-0.070,0.129,0.146,-0.094,0.047,-0.003,-0.185,-0.062,-0.149,0.114,-0.361,-0.184,-0.263,-0.022,-0.133,-0.109,-0.109,-0.023,0.049,-0.146,0.184],[0.209,-0.060,-0.107,-0.407,-0.005,-0.065,-0.600,0.072,0.066,-0.044,0.119,-0.263,-0.410,-0.221,-0.007,0.088,0.020,0.143,-0.016,-0.085,-0.166,-0.095,-0.031,-0.218,-0.069,-0.190,0.201,0.059,0.282,0.008,0.270,-0.245,0.209,0.333,0.019,0.229,-0.076],[0.098,0.057,-0.211,0.090,-0.344,0.074,0.178,-0.127,-0.043,0.139,-0.024,-0.058,-0.259,0.000,0.009,0.245,-0.009,0.090,0.178,0.227,-0.067,0.053,-0.174,0.032,0.029,0.012,0.201,0.084,-0.114,-0.235,-0.064,-0.023,-0.244,-0.001,-0.266,0.115,0.106],[0.012,0.057,0.261,-0.081,0.342,-0.005,-0.044,-0.010,-0.164,-0.129,-0.041,0.195,0.068,-0.152,-0.092,-0.433,-0.010,-0.158,-0.594,-0.271,-0.118,-0.372,-0.152,-0.069,-0.422,-0.142,-0.388,-0.225,-0.055,-0.242,-0.126,-0.158,-0.336,0.017,-0.212,0.076,0.499],[0.057,-0.123,-0.132,-0.013,-0.208,0.129,-0.016,-0.072,-0.001,-0.083,-0.088,-0.058,-0.115,-0.112,-0.056,0.176,-0.088,-0.035,0.116,-0.028,0.092,0.112,0.257,-0.003,0.024,-0.083,-0.014,0.032,0.119,0.017,-0.078,0.305,0.001,0.104,-0.161,-0.079,0.297],[-0.166,0.014,0.031,-0.115,0.186,-0.105,-0.004,0.021,-0.036,-0.051,-0.032,0.069,0.044,0.030,0.068,0.151,-0.033,-0.072,-0.130,0.003,-0.220,-0.265,-0.311,0.228,-0.045,0.064,-0.065,-0.039,-0.127,0.021,-0.168,0.303,-0.089,-0.145,-0.235,-0.554,0.093],[-0.091,-0.222,0.108,0.287,0.036,-0.225,-0.165,0.360,0.198,0.202,0.312,-0.087,-0.449,0.068,0.213,0.061,0.131,-0.378,-0.115,-0.219,0.287,-0.147,0.184,-0.101,-0.060,-0.007,-0.283,0.302,0.436,0.176,0.529,-0.277,0.061,-0.047,-0.165,-0.039,0.243],[-0.091,-0.149,-0.055,0.080,-0.111,-0.018,-0.015,0.010,-0.041,-0.017,-0.031,0.053,-0.045,0.112,-0.161,0.094,-0.238,-0.069,-0.243,-0.337,-0.025,-0.299,-0.125,-0.266,0.220,0.035,0.302,0.098,-0.069,-0.138,-0.101,0.340,-0.045,-0.116,-0.028,-0.072,0.025],[0.131,0.312,-0.097,-0.059,0.151,0.411,-0.047,-0.124,-0.071,0.090,0.082,0.337,0.093,0.082,0.047,0.092,0.074,0.092,0.100,0.184,0.010,0.108,-0.065,0.282,-0.103,0.186,0.001,-0.130,0.069,-0.088,0.176,0.337,-0.054,-0.330,-0.060,0.078,0.066],[0.018,-0.102,-0.028,-0.159,-0.102,0.086,0.057,-0.152,0.112,0.017,0.162,-0.037,-0.108,-0.046,-0.182,0.052,-0.167,-0.024,0.513,-0.232,-0.108,-0.186,-0.023,-0.027,-0.042,-0.066,-0.036,-0.004,-0.055,-0.055,-0.069,0.071,0.020,-0.162,0.054,0.013,0.021],[-0.274,0.310,0.050,0.425,0.341,-0.067,0.230,0.116,-0.212,0.028,-0.011,0.000,-0.063,0.013,-0.117,-0.043,-0.163,-0.219,-0.392,0.081,-0.197,-0.110,-0.153,-0.046,0.052,0.093,0.133,0.077,-0.156,-0.307,0.046,0.034,0.053,0.369,0.216,0.115,-0.037],[0.113,-0.117,0.289,-0.168,0.076,-0.050,0.208,-0.242,0.048,0.105,0.328,0.407,0.019,-0.166,0.134,-0.030,-0.118,-0.014,0.016,0.052,0.388,-0.247,-0.136,0.248,0.200,0.176,0.116,-0.139,-0.283,-0.254,0.093,-0.281,0.297,-0.095,0.141,0.148,-0.085],[0.046,0.008,0.392,-0.169,-0.160,-0.089,0.126,-0.095,0.363,0.034,-0.115,-0.104,-0.107,-0.001,0.455,0.198,0.291,-0.312,0.105,-0.224,0.122,0.200,-0.032,-0.110,-0.138,-0.131,0.080,-0.184,0.107,0.302,-0.195,0.044,-0.025,-0.219,-0.102,0.052,-0.198],[-0.059,0.315,-0.375,-0.311,0.284,-0.319,0.045,0.066,-0.232,0.134,0.443,-0.266,0.218,0.041,-0.040,-0.241,-0.231,0.275,0.116,0.083,-0.219,0.249,0.078,-0.087,0.004,-0.144,0.166,-0.144,0.360,-0.117,-0.180,-0.072,-0.060,0.052,0.276,-0.247,0.014],[-0.054,-0.029,-0.010,-0.030,-0.124,0.004,0.001,-0.036,-0.011,0.016,0.008,-0.005,-0.033,-0.003,-0.015,0.015,-0.106,-0.063,-0.045,-0.082,0.006,-0.012,-0.087,-0.010,0.036,-0.008,-0.056,-0.028,-0.092,-0.000,-0.011,-0.096,0.036,0.488,0.156,0.134,0.367],[-0.056,-0.036,-0.053,-0.031,-0.135,-0.033,0.037,-0.096,0.005,0.029,-0.029,-0.031,-0.033,-0.010,-0.024,0.010,-0.025,0.048,-0.044,-0.064,-0.100,-0.025,-0.165,0.138,-0.009,-0.108,-0.011,0.032,0.116,-0.117,-0.055,-0.066,0.070,0.400,0.038,-0.087,0.332],[-0.253,-0.113,-0.544,0.018,-0.334,-0.061,-0.000,-0.160,-0.007,0.015,-0.077,-0.060,-0.257,0.009,-0.037,-0.011,-0.078,-0.034,0.174,0.114,-0.079,0.083,-0.212,-0.065,0.059,0.027,0.058,0.002,0.011,-0.163,-0.128,-0.121,-0.335,0.131,-0.180,0.242,0.164],[0.010,0.148,0.015,0.214,-0.449,0.215,-0.156,-0.182,0.286,0.035,0.043,-0.029,0.194,0.066,0.121,-0.040,0.221,-0.095,0.180,-0.258,-0.216,0.030,-0.195,0.024,-0.077,0.323,-0.420,0.115,0.096,-0.020,0.193,0.009,-0.049,-0.079,0.461,0.207,0.231],[0.291,-0.105,-0.059,-0.146,-0.139,0.414,-0.398,0.315,0.122,-0.089,-0.271,-0.229,-0.045,-0.218,-0.062,-0.011,-0.057,-0.131,-0.611,-0.057,0.342,-0.007,0.213,-0.059,0.094,0.086,-0.270,-0.353,0.174,0.247,-0.066,0.284,0.062,0.405,0.139,0.136,-0.005],[-0.024,-0.068,-0.067,-0.140,-0.040,0.008,0.038,-0.080,-0.033,-0.005,-0.005,0.036,-0.009,-0.003,-0.088,0.013,-0.074,-0.002,-0.041,-0.087,-0.068,-0.057,-0.063,0.003,-0.011,-0.030,-0.005,0.036,0.038,0.032,0.050,0.116,0.161,0.039,0.083,0.313,0.081]]],
[[-0.005,-0.170,-0.228,-0.564,-0.134,-0.369,-0.196,-0.263,0.003,0.141,-0.033,0.177,-0.598,0.156,0.252,-0.354,-0.031,-0.089,-0.023,-0.339,-0.124,0.237,0.372,-0.063,0.231,0.267,-0.048,0.197,-0.357,0.003,0.141,0.098,-0.044,0.312,-0.293,-0.378,-0.198],
[0.031,0.024,0.034,0.025,0.033,0.022,0.014,0.033,0.020,0.019,0.031,0.014,0.028,0.027,0.027,0.023,0.046,0.027,0.068,0.046,0.053,0.057,0.027,0.048,0.036,0.025,0.025,0.013,0.030,0.029,0.012,0.033,0.016,0.023,0.021,0.012,0.023]])
		"""

	

		self.pass_check = 0


		#0.00198408

	"""best [7, 28, 14, 2], 0.001
	self.nn.InitByDumpNN([[[-0.290,0.241,0.033,-0.351,0.045,0.058,-0.130,-0.242,0.563,-0.249,-0.158,0.094,0.606,0.129,-0.179,-0.093,0.422,0.307,0.092,0.186,-0.040,-0.396,-0.006,-0.307,0.677,0.196,0.298,0.189],[-0.776,0.409,-0.896,-0.431,-0.615,-0.564,0.630,-0.088,0.371,-0.661,-0.840,0.249,-0.734,0.257,-0.535,0.605,0.251,0.474,0.217,0.410,-0.301,0.632,0.454,0.091,1.334,0.318,0.396,-0.593],[0.503,-0.415,0.633,0.285,0.523,0.602,-0.511,0.164,-0.001,0.665,0.483,-0.482,-0.022,-0.114,-0.069,-0.621,-0.194,-0.322,-0.106,0.201,0.883,-0.118,-0.262,-0.098,-0.661,-0.390,-0.331,0.656],[0.252,0.076,0.112,0.034,-0.266,-0.078,-0.370,0.115,-0.298,-0.292,-0.384,0.027,-0.064,-0.212,-0.197,-0.229,0.201,-0.297,-0.032,0.043,0.301,-0.083,0.316,0.473,-0.451,0.314,0.308,-0.070],[0.278,-0.581,0.359,-0.006,0.275,-0.212,-0.072,0.076,-0.121,0.125,-0.168,0.037,0.176,0.307,0.423,-0.576,0.258,-0.363,0.305,-0.401,-0.289,0.118,0.467,0.288,0.020,0.095,-0.106,0.359],[-0.194,0.370,-0.014,-0.077,-0.044,0.270,-0.003,0.166,0.251,-0.217,-0.560,-0.256,-0.648,0.200,0.344,0.066,-0.377,0.582,0.255,-0.086,-0.134,0.059,-0.449,-0.218,0.238,0.129,-0.300,0.059],[-0.217,0.773,-0.477,0.717,-0.467,0.366,0.635,-0.068,-0.475,-0.861,0.205,-0.323,0.324,0.499,-0.215,0.449,-0.084,-0.292,0.147,0.216,-0.806,-0.587,0.019,-0.162,0.390,-0.134,0.029,-0.493]],
[[0.347,0.438,0.158,0.326,0.103,-0.441,0.234,-0.213,-0.428,-0.449,-0.387,0.453,-0.498,-0.225],[-0.520,0.236,-0.030,0.316,0.325,-0.230,-0.462,0.158,0.654,0.255,-0.541,0.304,-0.131,0.041],[0.440,-0.338,-0.461,-0.171,0.090,-0.347,0.072,0.349,-0.763,0.102,-0.246,-0.308,0.250,-0.318],[-0.514,0.512,0.344,0.204,-0.570,-0.239,0.450,0.392,-0.099,0.464,-0.638,-0.278,-0.121,0.804],[0.474,0.041,0.153,-0.053,0.043,0.553,-0.488,-0.216,-0.148,0.197,0.140,0.075,0.389,-0.363],[0.079,0.399,0.283,0.356,-0.037,-0.239,-0.187,-0.366,0.081,-0.064,0.182,-0.231,-0.139,-0.436],[-0.181,-0.238,-0.176,0.760,0.383,-0.021,0.208,0.570,0.372,-0.072,-0.070,-0.299,-0.288,0.195],[-0.201,-0.378,-0.082,-0.425,-0.217,-0.498,0.139,-0.343,0.255,-0.110,0.138,-0.481,-0.293,0.124],[-0.079,-0.503,0.006,-0.402,0.150,0.306,0.248,0.522,-0.169,-0.230,-0.092,-0.368,0.269,-0.270],[0.169,-0.381,0.098,-0.154,-0.365,0.854,-0.350,-0.048,-0.220,-0.094,-0.015,-0.097,-0.108,-0.643],[-0.027,-0.184,0.348,0.211,-0.429,-0.045,0.345,-0.564,-0.289,0.070,0.226,0.368,-0.205,0.618],[-0.268,0.353,-0.459,-0.325,-0.285,0.336,0.280,-0.055,0.573,0.367,-0.320,0.181,0.477,0.373],[0.243,0.266,-0.201,0.259,-0.783,-0.463,-0.029,0.219,-0.055,-0.544,0.470,0.103,-0.413,0.090],[-0.765,0.382,-0.040,0.185,-0.075,0.351,-0.424,0.261,0.242,-0.343,-0.273,0.413,0.170,-0.233],[0.386,0.490,-0.363,0.031,0.328,-0.171,0.289,0.106,-0.143,-0.363,0.088,-0.003,0.523,-0.004],[0.103,0.333,-0.263,0.640,0.203,-0.159,-0.214,0.008,0.471,-0.168,-0.524,-0.297,-0.123,0.588],[-0.390,-0.145,0.004,0.227,0.206,0.009,-0.436,-0.128,-0.356,-0.274,-0.007,0.152,-0.253,-0.119],[0.045,-0.139,-0.270,0.071,-0.416,-0.281,0.534,-0.296,0.216,-0.113,0.211,0.046,-0.288,-0.435],[0.020,0.443,0.225,0.325,0.280,0.054,-0.241,0.070,-0.092,-0.191,0.149,-0.016,-0.070,0.155],[0.158,0.219,-0.136,0.358,0.175,-0.405,-0.449,-0.401,0.108,-0.332,0.054,-0.464,-0.190,0.478],[-0.091,-0.358,-0.596,-0.133,-0.296,0.646,0.242,-0.083,-0.287,-0.511,-0.008,-0.274,0.508,-0.146],[0.276,-0.230,0.235,0.504,-0.438,-0.259,0.186,-0.063,-0.410,0.067,-0.244,-0.489,-0.574,-0.221],[0.088,0.150,0.387,0.316,0.058,0.431,0.205,0.389,-0.079,-0.498,-0.331,0.114,-0.497,0.339],[0.215,-0.335,0.499,0.049,-0.052,-0.496,0.433,0.418,0.176,0.245,0.151,-0.066,0.038,0.191],[-0.692,0.033,-0.192,0.281,0.267,-0.555,-0.301,0.733,1.127,-0.254,-0.460,-0.282,-0.608,0.996],[-0.186,0.024,-0.046,0.401,-0.235,-0.366,-0.476,0.859,0.560,0.189,0.259,-0.453,0.258,-0.242],[-0.224,0.365,-0.196,0.019,-0.012,-0.091,0.321,0.326,-0.322,-0.324,-0.205,0.240,0.340,0.050],[0.549,0.116,0.142,0.002,-0.402,0.048,-0.655,-0.095,-0.476,-0.072,0.295,0.332,0.755,-0.539]],
[[0.460,-0.552],[-0.346,0.390],[0.068,0.360],[-0.061,1.069],[0.569,0.482],[0.187,-0.794],[-0.059,0.584],[0.407,0.478],[0.319,1.258],[-0.327,0.471],[0.055,0.363],[-0.399,-0.269],[0.257,-0.716],[-0.040,0.674]]],
[[0.142,0.018,0.459,-0.410,-0.251,-0.222,0.133,-0.304,0.431,0.052,-0.447,-0.332,-0.274,-0.037,0.249,0.219,-0.301,0.043,-0.316,0.590,-0.096,0.005,0.004,0.103,0.423,-0.156,-0.387,0.375],
[0.090,0.115,-0.287,-0.311,-0.046,0.627,0.285,-0.313,-0.438,-0.023,0.090,-0.124,0.494,0.459],
[0.092,0.440]])
"""

	def convolution1D(self, input_data, kernel):
		input_size = len(input_data)
		kernel_size = len(kernel)
		output_size = input_size - kernel_size + 1
		output = [0.0] * output_size

		# Appliquer la convolution
		for i in range(output_size):
			for j in range(kernel_size):
				output[i] += input_data[i + j] * kernel[j]

		return output

	def normalizeInput(self, input):
		# Calculate mean
		mean = sum(input) / len(input)

		# Calculate standard deviation
		stddev = math.sqrt(sum((val - mean) ** 2 for val in input) / len(input))

		# Normalize input data
		for i in range(len(input)):
			input[i] = (input[i] - mean) / stddev



	def write_features_to_file(self, filename, features):
		with open(filename, 'a') as file:
			for feature_set in features:
				line = ' '.join(map(str, feature_set)) + '\n'
				file.write(line)

	def write_rewards_to_file(self, filename, rewards):
		with open(filename, 'a') as file:
			line = ''
			for feature_set in rewards:
				line += str(feature_set) + ' '
			line += '\n'
			file.write(line)

		
	def calculate_features(self, checkpoint):
		next_check = (self.sim.check_point + 1) % len(checkpoint)
		last_check = (self.sim.check_point - 1 + len(checkpoint)) % len(checkpoint)
		x1, y1 = self.sim.pos.x, self.sim.pos.y
		x2, y2 = checkpoint[self.sim.check_point].x, checkpoint[self.sim.check_point].y
		x3, y3 = checkpoint[next_check].x, checkpoint[next_check].y
	
		angle = math.atan2(y1 - y2, x1 - x2) - math.atan2(y3 - y2, x3 - x2)
		angle = angle * 180.0 / math.pi
		angle = (angle + 180.0) % 360.0
		if angle < 0.0:
			angle += 360.0
		angle -= 180.0
	
		anglech = math.atan2(y2 - y1, x2 - x1)
		anglech = anglech * 180.0 / math.pi
		anglech = (anglech - self.sim.angletot + 540) % 360 - 180

		col = ((self.sim.speed.x * (checkpoint[self.sim.check_point].x - self.sim.pos.x) + self.sim.speed.y * (checkpoint[self.sim.check_point].y - self.sim.pos.y)) /
			   (math.sqrt(self.sim.speed.x * self.sim.speed.x + self.sim.speed.y * self.sim.speed.y) *
				math.sqrt((checkpoint[self.sim.check_point].x - self.sim.pos.x) * (checkpoint[self.sim.check_point].x - self.sim.pos.x) +
						  (checkpoint[self.sim.check_point].y - self.sim.pos.y) * (checkpoint[self.sim.check_point].y - self.sim.pos.y)) + 0.000001))
	
		dist_check = distance(checkpoint[self.sim.check_point], self.sim.pos)
		ndist_check = distance(checkpoint[self.sim.check_point], checkpoint[last_check])
		
				
		speed = norme(self.sim.speed)

		a1 = (angle + 180) / 360.0
		a2 = (anglech + 180) / 360.0
		a3 = (col + 1.0) / 2.0
		a4 = (2000 - dist_check) / 2000.0
		a5 = speed / 2000.0
		a6 = self.sim.angletot / 360.0
		a7 = float(4) / self.simulation.MAXTF
				

		self.write_features_to_file("dataset.txt", [(a1, a2, a3, a4, a5, a6, a7)])
		



	def Move(self, turn, time):

		self.calculate_features(self.simulation.checkpoints)

		self.simulation.play(self.sim, turn, time)

		maxl = -2000
		ind = -1
		for i in range(0, 37):
			if self.simulation.reward[i] > maxl:
				maxl = self.simulation.reward[i]
				ind = i

		rew = [0] * 37	
		rew[ind] = 1.0 
	
		self.write_rewards_to_file("rewards.txt",rew)

		solm = self.simulation.solution[0]
				
		self.write_features_to_file("dataset.txt", [(ind, 0)])

		anglef = int(self.sim.angletot + solm.moves1[0].angle + 360) % 360
		angleRad = anglef * PI / 180.0
		thrust = solm.moves1[0].thrust
		self.sim.thrust = thrust
		self.sim.angle = solm.moves1[0].angle
		print(str(thrust) + " " + str(solm.moves1[0].angle))
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
	

	def scale_output_value(self, output_value, new_min, new_max):
		scaled_value = output_value * (new_max - new_min) + new_min
		return scaled_value

	def softmax_rlp(self, tab):
		max_x = np.max(tab)  # Trouver la valeur maximale de x
		exp_x = np.exp(tab - max_x)  # Calculer les exponentielles des éléments du vecteur
		sum_exp_x = np.sum(exp_x)  # Calculer la somme des exponentielles

		# Calculer le softmax
		softmax_values = exp_x / sum_exp_x
		sum_softmax = np.sum(softmax_values)  # Calculer la somme des valeurs softmax
		softmax_values /= sum_softmax 
		return softmax_values

	def softmax_rl(self):
		max_x = np.max(self.nn.network[-1])  # Trouver la valeur maximale de x
		exp_x = np.exp(self.nn.network[-1] - max_x)  # Calculer les exponentielles des éléments du vecteur
		sum_exp_x = np.sum(exp_x)  # Calculer la somme des exponentielles

		# Calculer le softmax
		softmax_values = exp_x / sum_exp_x
		sum_softmax = np.sum(softmax_values)  # Calculer la somme des valeurs softmax
		softmax_values /= sum_softmax 
		return softmax_values

	def MoveNN(self, turn, time):
		start_time = datetime.datetime.now()
		def get_time():
			stop_time = datetime.datetime.now()
			duration = (stop_time - start_time).total_seconds() * 1000  # Convertir en millisecondes
			return duration <= time

		while(get_time()):
			pass

		checkpoint = self.simulation.checkpoints
		next_check = (self.sim.check_point + 1) % len(checkpoint)
		x1, y1 = self.sim.pos.x, self.sim.pos.y
		x2, y2 = checkpoint[self.sim.check_point].x, checkpoint[self.sim.check_point].y
		x3, y3 = checkpoint[next_check].x, checkpoint[next_check].y
	
		angle = math.atan2(y1 - y2, x1 - x2) - math.atan2(y3 - y2, x3 - x2)
		angle = angle * 180.0 / math.pi
		angle = (angle + 180.0) % 360.0
		if angle < 0.0:
			angle += 360.0
		angle -= 180.0
	
		anglech = math.atan2(y2 - y1, x2 - x1)
		anglech = anglech * 180.0 / math.pi
		anglech = (anglech - self.sim.angletot + 540) % 360 - 180

		col = ((self.sim.speed.x * (checkpoint[self.sim.check_point].x - self.sim.pos.x) + self.sim.speed.y * (checkpoint[self.sim.check_point].y - self.sim.pos.y)) /
			   (math.sqrt(self.sim.speed.x * self.sim.speed.x + self.sim.speed.y * self.sim.speed.y) *
				math.sqrt((checkpoint[self.sim.check_point].x - self.sim.pos.x) * (checkpoint[self.sim.check_point].x - self.sim.pos.x) +
						  (checkpoint[self.sim.check_point].y - self.sim.pos.y) * (checkpoint[self.sim.check_point].y - self.sim.pos.y)) + 0.000001))
	
		dist_check = distance(checkpoint[self.sim.check_point], self.sim.pos)
		speed = norme(self.sim.speed)

		a1 = (angle + 180) / 360.0
		a2 = (anglech + 180) / 360.0
		a3 = (col + 1.0) / 2.0
		a4 = (2000 - dist_check) / 2000.0
		a5 = speed / 2000.0
		a6 = self.sim.angletot / 360.0
		a7 = float(4.0) / self.simulation.MAXTF

		input_data = [a1, a2, a3, a4, a5, a6, a7]
		kernel = [0.5, 0.5]
		#self.normalizeInput(input_data)
		#self.nn.SetInput(self.convolution1D(input_data, kernel))
		self.nn.SetInput(input_data)
		self.nn.normalizeInput()
		self.nn.PredictNN()

		soft = self.softmax_rl();
		maxl =-20000
		ind = -1
		for i in range(0, 37):
			print(soft[i])
			if soft[i] > maxl:
				maxl = soft[i]
				ind = i

		_angle = ind - 18.0
		_thrust = 4#self.nn.network[-1][1] * self.simulation.MAXT
		#_angle = self.scale_output_value(self.nn.network[-1][0], -18, 18)
		#_thrust = self.scale_output_value(self.nn.network[-1][1], 0, 250)
		#_thrust *= 2
		#_angle *= 2
		#print(speed)
		#print(str(_angle) + " " + str(_thrust))

		anglef = int(self.sim.angletot + _angle + 360) % 360
		angleRad = anglef * PI / 180.0
		thrust = _thrust
		self.sim.thrust = thrust
		self.sim.angle = _angle
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

		self.sim.angletot = int(self.sim.angletot + _angle + 360) % 360


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

	
	
	checkpoint = [Checkpoint(220, 300), Checkpoint(1000, 150), Checkpoint(1500, 600), Checkpoint(1000, 400), Checkpoint(750, 700)]
	checkpointc = [Checkpoint(200*DX, 300*DY), Checkpoint(1000*DX, 150*DY), Checkpoint(1500*DX, 600*DY), Checkpoint(1000*DX, 400*DY), Checkpoint(750*DX, 700*DY)]
	
	pod = SuperPod(200*DX, 300*DY, 0, checkpointc)
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
		pod.MoveNN(turn, 10)
		#pod2.Move()
		d = distance(pod.sim.pos, checkpointc[pod.sim.check_point])
		#print("distance " + str(d))
		if(d <= 50):
			pod.sim.check_point = (pod.sim.check_point + 1) % len(checkpoint)
			pod.sim.check_pass += 1
			pod.pass_check = 1

		#for i in range(NBPOD):
		#	pods[i].Move()

		#print("angle " + str(ang) + ", thrust " + str(thrust) + ", check " + str(pod.nextCheckpoint))
		
		#direction = Point(math.cos(ang*3.14159/180.0) * 10000.0, math.sin(ang*3.14159/180.0) * 10000.0)
		#direction = checkpoint[pod.sim.check_point]
		pygame.draw.line(dis, purple, [pod.sim.pos.x/DX,pod.sim.pos.y/DY], [pod.sim.pos.x/DX+pod.sim.direction.x/DX, pod.sim.pos.y/DY+pod.sim.direction.y/DY])
		#direction2 = checkpoint[pod2.nextCheckpoint]
		#pygame.draw.line(dis, purple, [pod2.pos.x,pod2.pos.y], [direction2.x, direction2.y])


		#for i in range(NBPOD):
		#	directionp[i] = checkpoint[pods[i].nextCheckpoint]
		#	pygame.draw.line(dis, purple, [pods[i].pos.x,pods[i].pos.y], [directionp[i].x, directionp[i].y])


		

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
							  
		pygame.draw.rect(dis, color[0], [pod.sim.pos.x/DX, pod.sim.pos.y/DY, 50, 50])
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