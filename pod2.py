# coding=utf-8
import pygame
import time 
import random
import math

dis_width = 1700
dis_height = 956
NBMAXTOUR = 10
SIMULATION_TURNS = 4
SOLUTION_COUNT = 6
#----------------------DICKHEAD
class Move:
	def __init__(self):
		self.rotation = 0
		self.thrust = 0
		self.shield = False
		self.boost = False

class Turn:
	def __init__(self):
		self.move = []
		for i in range(2):
			self.move.append(Move())

class Solution:
	def __init__(self):
		self.turns = []
		for i in range(SIMULATION_TURNS):
			self.turns.append(Turn())
		self.score = -1

class Simulation2:
	def __init__(self):
		self.checkpCount = 0
		self.maxCheckp = 0

	def InitCheckpointsFromInput(self, l, cc, check):
		self.laps = l
		self.checkpCount = cc
		self.checkpoint = check
		self.maxCheckp = self.laps * self.checkpCount

	def PlaySolution(self, pods, s):
		for i in range(SIMULATION_TURNS):
			self.PlayOneTurn(pods, s.turns[i])

	def PlayOneTurn(self, pods, turn):
		self.Rotate(pods, turn)
		self.Accelerate(pods, turn)
		self.UpdatePosition(pods)
		self.Friction(pods)
		self.EndTurn(pods)

	def Rotate(self, pods, turn):
		for i in range(2):
			pods[i].angle = (pods[i].angle + turn.move[i].rotation) % 360
			

	def Accelerate(self, pods, turn):
		for i in range(2):
			angleRad = pods[i].angle * 3.14159 / 180.0
			direction = Point(math.cos(angleRad), math.sin(angleRad));
			pods[i].v = Point(pods[i].v.x + turn.move[i].thrust * direction.x, pods[i].v.y + turn.move[i].thrust * direction.y)

	def UpdatePosition(self, pods):

		for i in range(2):
			pods[i].pos.x += pods[i].v.x
			pods[i].pos.y += pods[i].v.y

			if(distance(pods[i].pos, self.checkpoint[pods[i].nextCheckpoint]) <= 50):
				pods[i].nextCheckpoint = (pods[i].checkpass + 1) % self.checkpCount
				pods[i].checkpass += 1

	def Friction(self, pods):
		for i in range(2):
			pods[i].v.x *= 0.85
			pods[i].v.y *= 0.85

	def EndTurn(self, pods):
		for i in range(2):
			pods[i].v.x = int(pods[i].v.x)
			pods[i].v.y = int(pods[i].v.y)
			pods[i].pos.x = round(pods[i].pos.x)
			pods[i].pos.y = round(pods[i].pos.y)	


def ConvertSolutionToOutput(sol, pods):
	#for i in range(2):
	angle = (pods[0].angle + sol.turns[0].move[0].rotation) % 360
	angleRad = angle * 3.14159 / 180.0
	direction = Point(10000.0 * math.cos(angleRad), 10000.0 * math.sin(angleRad))
	target = Point(pods[0].pos.x + direction.x, pods[0].pos.y + direction.y)

	return Point(pods[0].pos.x, pods[0].pos.y)

class Solver:

	def __init__(self, parSim):
		self.solutions = []
		self.sim = parSim
		self.InitPopulation()

	def keepsolving(self, start, time):
		now = pygame.time.get_ticks();
		d = now - start
		return d < time


	def Solve(self, pods, time):
	

		for i in range(SOLUTION_COUNT):
			self.ShiftByOneturn(self.solutions[i])
			self.ComputeScore(self.solutions[i], pods)

		start = pygame.time.get_ticks();
		while(self.keepsolving(start, time)):
			for i in range(SOLUTION_COUNT):
				self.solutions[SOLUTION_COUNT+i] = self.solutions[i]
				self.Mutate(self.solutions[SOLUTION_COUNT+i])
				self.ComputeScore(self.solutions[SOLUTION_COUNT+i], pods)

				self.solutions = sorted(self.solutions, reverse=True, key=lambda x: x.score)

		#for i in range(SOLUTION_COUNT):
		#	print("sol " + str(self.solutions[i].score))

		return self.solutions[0]

	def InitPopulation(self):
		for i in range(SOLUTION_COUNT*2):
			self.solutions.append(Solution())

		for s in range(SOLUTION_COUNT):
			for t in range(SIMULATION_TURNS):
				for i in range(2):
					self.Randomize(self.solutions[s].turns[t].move[i], True)

	def Randomize(self, m, modf):

		all = -1
		rotation = 0
		thrust = 1
		pr = 5
		pt = pr+5
		ps = pt+1
		pb = ps+0

		
		if modf == True:
			mod = random.randint(0, 1)
		else :
			mod = False
		
		modif = random.randint(0, pb)

		if(mod == 1 or modif <= pr):
			r = random.randint(-2*18, 3*18)
			if(r > 2*18):
				m.rotation = 0;
			else:
				if(r < -18):
					m.rotation = -18
				if(r > 18):
					m.rotation = 18

		if(mod == 1 or (modif >= pr and modif < pt )):
			r = random.randint(-2/2, 2*2)
			if(r < 0):
				m.thrust = 0
			if(r > 2):
				m.thrust = 2

	def ShiftByOneturn(self, s):
		for t in range(SIMULATION_TURNS):
			for i in range(2):
				s.turns[t-1].move[i] = s.turns[t].move[i] 

		for i in range(2):
			self.Randomize(s.turns[SIMULATION_TURNS-1].move[i], True)

	def Mutate(self, s):

		k = random.randint(0, SIMULATION_TURNS)
		self.Randomize(s.turns[k/2].move[k%2], False)

	def ComputeScore(self, sol, pods):
		podsc = []
		p = Pod(pods[0].pos.x, pods[0].pos.y, pods[0].angle, pods[0].checkpoint)
		p.v = Point(pods[0].v.x, pods[0].v.y)
		p.nextCheckpoint = pods[0].nextCheckpoint
		podsc.append(p)
		p = Pod(pods[0].pos.x, pods[0].pos.y, pods[0].angle, pods[0].checkpoint)
		p.v = Point(pods[0].v.x, pods[0].v.y)
		p.nextCheckpoint = pods[0].nextCheckpoint
		podsc.append(p)
		self.sim.PlaySolution(podsc, sol)
		sol.score = self.RateSolution(podsc)
		return sol.score

	def podScore(self, p):
		dist = distance(p.pos, self.sim.checkpoint[p.nextCheckpoint])
		return 30000.0 * p.checkpass - dist

	def RateSolution(self, pods):

		for i in range(2):
			pods[i].score = self.podScore(pods[i])


		return pods[0].score


		 
#---------------------END DICKHEAD

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

    def __init__(self, g, check):
        self.g = g
        self.checkpt = check
        self.podsl = []

    def Simulate_One_TourV2(self, p, i):

        vec = Point(0,0);

        a = int(p.angle +\
         self.g.population[i].angle) % 360;
        vec.x = math.cos(a*3.1415/180.0);
        vec.y = math.sin(a*3.1415/180.0);

        vec.x *= self.g.population[i].thrust;
        vec.y *= self.g.population[i].thrust;


        return vec

    def Simulate_One_TourV22(self, p, g):

        vec = Point(0,0);

        a = int(p.angle + g.angle) % 360;
        vec.x = math.cos(a*3.1415/180.0);
        vec.y = math.sin(a*3.1415/180.0);

        vec.x *= g.thrust;
        vec.y *= g.thrust;


        return vec

    def play(self, pod, j):
               
        pt = self.Simulate_One_TourV2(pod, j)

        p = Pod(pod.pos.x, pod.pos.y, pod.v.x, pod.v.y, pod.angle, pod.nextCheckpoint, [])
       
        p.v.x += pt.x
        p.v.y += pt.y
        p.pos.x = round(p.pos.x+p.v.x)    
        p.pos.y = round(p.pos.y+p.v.y)
        p.v.x *= 0.85
        p.v.y *= 0.85
        p.v.x = int(p.v.x)
        p.v.y = int(p.v.y)

        d = distance(p.pos, self.checkpt[p.nextCheckpoint])
        if d <= 50:
            p.checkpass += 1
            p.nextCheckpoint = (p.nextCheckpoint + 1) % len(self.checkpt)


        self.g.population[j].x = p.pos.x
        self.g.population[j].y = p.pos.y
        self.g.population[j].vx = p.v.x
        self.g.population[j].vy = p.v.y
    
        self.g.population[j].score =  p.checkpass * 30000 - d

    def play2(self, gg, pod, j):
               
        pt = self.Simulate_One_TourV2(pod, j)

        p = Pod(pod.pos.x, pod.pos.y, pod.v.x, pod.v.y, pod.angle, pod.nextCheckpoint, [])
           
        p.v.x += pt.x
        p.v.y += pt.y
        p.pos.x = round(p.pos.x+p.v.x)    
        p.pos.y = round(p.pos.y+p.v.y)
        p.v.x *= 0.85
        p.v.y *= 0.85
        p.v.x = int(p.v.x)
        p.v.y = int(p.v.y)
        p.angle += self.g.population[j].angle
        #print(str(p.pos.x), file=sys.stderr, flush=True)
        d = distance(p.pos, self.checkpt[p.nextCheckpoint])
        if d <= 50:
            p.checkpass += 1
            p.nextCheckpoint = (p.nextCheckpoint + 1) % len(self.checkpt)

        gg.podst.append(p)

        self.g.population[j].score = p.checkpass * 30000 - d

    def simulate_nturn(self, pod, nbtour):
        gg = self.g.get_bestfit()
        angle = self.g.get_bestfit().angle
        thrust = 0
        genetic = 0
        p = Pod(pod.pos.x, pod.pos.y, pod.v.x, pod.v.y, pod.angle, pod.nextCheckpoint, [])
      
        for i in range(nbtour):
            #print(str(p.pos.x), file=sys.stderr, flush=True)
            genetic = GeneticPod(10, 4, fitness_settings, 4, 5, self.checkpt, p)
            genetic.create_generation22(8)
            genetic.display_population()
            gg = genetic.get_bestfit()
            thrust += gg.thrust
            self.podsl.append(genetic.get_bestfit().pod)
            p = genetic.get_bestfit().pod
        return angle, int(thrust/nbtour)


def fitness_settings():
    thrust = random.randint(0, 4)
    angle = random.randint(-180, 180)

    return angle, thrust

def fitness_settings200():
    thrust = 200
    angle = random.randint(-18, 18)

    return angle, thrust

def fitness_settings0():
    thrust = 0
    angle = random.randint(-180, 180)

    return angle, thrust

class Settings:

    def __init__(self, t, a):
        self.thrust = t
        self.angle = a
        self.score = -10000000000000000
        self.id = 0
        self.pod = Pod(0,0,0,0,0, 0,[])
        self.x=0
        self.y=0
        self.vx=0
        self.vy=0
        self.angle = 0

class GeneticPod:

    def __init__(self, sz, nbg, fit, nbcross, nbmutation, check, _pod):
        self.size = sz
        self.num_gen = nbg
        self.population = []
        self.func_fit = fit
        self.nb_cross = nbcross
        self.nb_mutation = nbmutation
        self.checkpt = check
        self.pod = _pod
        self.bestfit = Settings(0,0)
               
        self.podst = []

    def fitness(self, func):
        return func()

    def init_population(self):
        for i in range(self.size):
            an, th = self.fitness(self.func_fit)
            s = Settings(th, an)
            self.population.append(s)
            self.adjust_settings(i)
            simulation = Simulation(self, self.checkpt)
            simulation.play(self.pod, i)

        self.keep_bestfit()

    def init_population2(self):
        for i in range(self.size):
            an, th = self.fitness(self.func_fit)
            s = Settings(th, an)
            self.population.append(s)
            self.adjust_settings(i)
            simulation = Simulation(self, self.checkpt)
            simulation.play2(self, self.pod, i)

        self.keep_bestfit2()


    def adjust_settings(self, num):
        if self.population[num].thrust > 4:
            self.population[num].thrust = 4
        if self.population[num].thrust < 0:
            self.population[num].thrust = 0

        if self.population[num].angle > 180:
            self.population[num].angle = 180
        if self.population[num].angle < -180:
            self.population[num].angle = -180

    def adjust_settings_v(self, thrust, angle):
        if thrust > 4:
            thrust = 4
        if thrust < 0:
            thrust = 0

        if angle > 180:
            angle = 180
        if angle < -180:
            angle = -180

        return thrust, angle

    def mutation(self):
        for i in range(self.nb_mutation):
            an, th = self.fitness(self.func_fit)
            rth = random.randint(0, 10)
            if rth < 5:th = -th
            num = random.randint(0, self.size-1)
            self.population[num].angle += an /2
            self.population[num].angle += th
                
            self.adjust_settings(num)
                      
                       

    def cross_over(self):
        self.population.sort(key=lambda x:x.score, reverse=True)
        j = 0
        for i in range(self.nb_cross):
            nth = int((self.population[j].thrust+self.population[j+1].thrust) /2)
            na = int((self.population[j].angle+self.population[j+1].angle) /2)

            s = Settings(nth, na)
            self.population.append(s)
            j+=2
               
        for i in range(self.nb_cross*2):
            self.population.pop(0)
                    

        for i in range(self.nb_cross):
            an, th = self.fitness(self.func_fit)
            th, an = self.adjust_settings_v(th, an)
            s = Settings(th, an)
            self.population.append(s)
           

    def cross_over2(self, nbkill):
        self.population.sort(key=lambda x:x.score, reverse=True)
        j = 0
        for i in range(self.nb_cross):
            nth = int((self.population[j].thrust+self.population[j+1].thrust) /2)
            na = int((self.population[j].angle+self.population[j+1].angle) /2)

            s = Settings(nth, na)
            self.population.append(s)

            j+=2
        
        
        for i in range(self.nb_cross):
            an, th = self.fitness(self.func_fit)
            th, an = self.adjust_settings_v(th, an)
            s = Settings(th, an)
            self.population.append(s)

        for i in range(self.size-1, (self.size-1)-(nbkill),-1):
            self.population.pop(i)
      

    def create_generation(self):
        self.init_population()
        for i in range(self.num_gen):
            self.cross_over()
            self.mutation()
            simulation = Simulation(self, self.checkpt)
            for j in range(self.size):
                simulation.play(self.pod, j)
            self.keep_bestfit()

    def create_generation2(self, nbkill):
        self.init_population()
        for i in range(self.num_gen):
            self.cross_over2(nbkill)
            self.mutation()
            simulation = Simulation(self, self.checkpt)
            for j in range(self.size):
                #print("posx "  + str(self.pod.pos.x))
                simulation.play(self.pod, j)
            self.keep_bestfit()

    def create_generation22(self, nbkill):
        self.init_population2()
        for i in range(self.num_gen):
            self.cross_over2(nbkill)
            self.mutation()
            simulation = Simulation(self, self.checkpt)
            for j in range(self.size):
                #print("posx "  + str(self.pod.pos.x))
                simulation.play2(self, self.pod, j)
            self.keep_bestfit2()

    def keep_bestfit(self):
        f = 0
        ind = 0
        mx = self.bestfit.score
        for i in range(self.size):
            if self.population[i].score > mx:
                mx = self.population[i].score
                f = 1
                ind = i

        if f:
            self.bestfit.id = ind
            self.bestfit = self.population[ind]
         
    def keep_bestfit2(self):
        f = 0
        ind = 0
        mx = self.bestfit.score
        for i in range(self.size):
            if self.population[i].score > mx:
                mx = self.population[i].score
                f = 1
                ind = i

        if f:
            self.bestfit.id = ind
            self.bestfit = self.population[ind]
            if len(self.podst) > 0:
                self.bestfit.pod = self.podst[ind]

    def get_bestfit(self):
        return self.bestfit

    def display_ind(self, i):
        print(str(self.population[i].angle) + " " + str(self.population[i].thrust)+ " " + str(self.population[i].score))


    def display_population(self):

        for i in range(len(self.population)):
            print(str(self.population[i].angle) + " " + str(self.population[i].thrust)+" " + str(self.population[i].score))


        print("------------------------------")



class Pod:
	def __init__(self, x, y,vx, vy, angle,nxtc, checkpoint):
		self.pos = Point(x, y)
		self.last_v = Point(1, 1)
		self.v = Point(vx, vy)
		self.angle = angle
		self.nextCheckpoint = nxtc
		self.vdir = Point(0.0, 0.0)
		self.time = 0;
		self.last_time = 0;
		self.checkpoint = checkpoint
		self.checkpass = 0
		self.start = True
		self.playret = False
		self.lock = False
		#self.simulation = Simulation([], checkpoint, 25, 10)
		self.score = 0
		self.podst = []

	def sel_checkpoint(self, check):
		self.checkpoint = check

	def get_direction(self):
		return self.vdir

	def Move(self):
		

		self.last_time = self.time
		self.time = pygame.time.get_ticks();
		diff_t = self.time - self.last_time

		genetic = GeneticPod(10, 4, fitness_settings, 4, 5, self.checkpoint, self)
		genetic.create_generation2(8)
		#genetic.display_population()
		simulation = Simulation(genetic, self.checkpoint)
		pod = Pod(self.pos.x, self.pos.y, self.v.x,self.v.y, self.angle, self.nextCheckpoint, [])
		angle , thrust = simulation.simulate_nturn(pod, 10)
		self.pos.x = genetic.get_bestfit().x
		self.pos.y = genetic.get_bestfit().y
		self.v.x = genetic.get_bestfit().vx
		self.v.y = genetic.get_bestfit().vy
		self.angle = (self.angle + genetic.get_bestfit().angle) % 360
		self.podst = simulation.podsl

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
	pod = Pod(X, Y,0.0001,0, 0, 0, checkpoint)
	pod.sel_checkpoint(checkpoint)
	direction = Point(checkpoint[pod.nextCheckpoint].x, checkpoint[pod.nextCheckpoint].y)
	
	pod2 = Pod(X, Y,0.0001,0, 0, 0, checkpoint)
	pod2.sel_checkpoint(checkpoint)
	direction2 = Point(checkpoint[pod2.nextCheckpoint].x, checkpoint[pod2.nextCheckpoint].y)
	
	NBPOD = 0
	directionp=[]
	pods=[]
	for i in range(NBPOD):
		p = Pod(X, Y,0.0001,0, 0, 0, checkpoint)
		p.sel_checkpoint(checkpoint)
		pods.append(p)
		d = Point(checkpoint[pods[i].nextCheckpoint].x, checkpoint[pods[i].nextCheckpoint].y)
		directionp.append(d)


	
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
		pod.Move()
		pod2.Move()

		for i in range(NBPOD):
			pods[i].Move()

		#print("angle " + str(ang) + ", thrust " + str(thrust) + ", check " + str(pod.nextCheckpoint))
		
		#direction = Point(math.cos(ang*3.14159/180.0) * 10000.0, math.sin(ang*3.14159/180.0) * 10000.0)
		direction = checkpoint[pod.nextCheckpoint]
		pygame.draw.line(dis, purple, [pod.pos.x,pod.pos.y], [direction.x, direction.y])
		direction2 = checkpoint[pod2.nextCheckpoint]
		pygame.draw.line(dis, purple, [pod2.pos.x,pod2.pos.y], [direction2.x, direction2.y])


		for i in range(NBPOD):
			directionp[i] = checkpoint[pods[i].nextCheckpoint]
			pygame.draw.line(dis, purple, [pods[i].pos.x,pods[i].pos.y], [directionp[i].x, directionp[i].y])


		d = distance(pod.pos, checkpoint[pod.nextCheckpoint])
		#print("distance " + str(d))
		if(d <= 50):
			pod.nextCheckpoint = (pod.nextCheckpoint + 1) % len(checkpoint)
			pod.checkpass += 1

	
		d = distance(pod2.pos, checkpoint[pod2.nextCheckpoint])
		#print("distance " + str(d))
		if(d <= 50):
			pod2.nextCheckpoint = (pod2.nextCheckpoint + 1) % len(checkpoint)
			pod2.checkpass += 1

		for i in range(NBPOD):
			d = distance(pods[i].pos, checkpoint[pods[i].nextCheckpoint])
			#print("distance " + str(d))
			if(d <= 50):
				pods[i].nextCheckpoint = (pods[i].nextCheckpoint + 1) % len(checkpoint)
				pods[i].checkpass += 1
	
			
		#p = ConvertSolutionToOutput(solver.Solve([pod, Pod(0,0,0,[])], 0.95), [pod, Pod(0,0,0,[])])
							  
		pygame.draw.rect(dis, color[0], [pod.pos.x, pod.pos.y, 50, 50])
		#print ("x " + str(pod.pos.x) + " y " + str(pod.pos.y))

		pygame.draw.rect(dis, purple, [pod2.pos.x, pod2.pos.y, 50, 50])

		for i in range(NBPOD):
			pygame.draw.rect(dis, color[i%len(color)], [pods[i].pos.x, pods[i].pos.y, 50, 50])
		


		draw_checkpoint(checkpoint)
		pygame.draw.line(dis, yellow, [pod.pos.x,pod.pos.y], [pod.pos.x+pod.get_direction().x*400.0, pod.pos.y+pod.get_direction().y*400.0])
		#pygame.draw.line(dis, yellow, [pod2.pos.x,pod2.pos.y], [pod2.pos.x+pod2.get_direction().x*400.0, pod2.pos.y+pod2.get_direction().y*400.0])

		for i in range(NBPOD):
			pygame.draw.line(dis, yellow, [pods[i].pos.x,pods[i].pos.y], [pods[i].pos.x+pods[i].get_direction().x*400.0, pods[i].pos.y+pods[i].get_direction().y*400.0])
		

		for i in range(len(pod.podst)):
			pygame.draw.rect(dis, green, [pod.podst[i].pos.x, pod.podst[i].pos.y, 5, 5])
		
		for i in range(len(pod2.podst)):
			pygame.draw.rect(dis, green, [pod2.podst[i].pos.x, pod2.podst[i].pos.y, 5, 5])
		
		for p in range(NBPOD):
			for i in range(len(pods[p].podst)):
				pygame.draw.rect(dis, green, [pods[p].podst[i].pos.x, pods[p].podst[i].pos.y, 5, 5])
		
		pygame.display.update()

		#clock.tick(1000)

	
	pygame.quit()
	quit()
	


gameLoop()