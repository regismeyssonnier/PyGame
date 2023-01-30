# coding=utf-8
import pygame
import time 
import random
import math

dis_width = 1700
dis_height = 956

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
pygame.display.set_caption('Bezier')


clock = pygame.time.Clock()
interval_tour = 100;

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

#-----------------------
def distance(p1, p2):
	return math.sqrt((p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y))


#--------------------CLASS
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Bezier:

	def __init__(self, point, st):
		self.point_c = point
		self.nb_point_c = len(point)
		self.step = st
		self.pt_curve = []
		self.upd_pt = -1
		self.fact = []

		x = 1
		i = 1
		self.fact.append(1)
		while i <= self.nb_point_c:
			x = x * i
			self.fact.append(x)
			i+=1

		#for i in range(len(self.fact)):
		#	print (str(self.fact[i]))

	def cb(self, n, k):
		return self.fact[n] / (self.fact[k] * self.fact[n - k])

	def compute(self):
		self.pt_curve = []
		t = 0
		while(t <= 1.0):
			p = Point(0, 0)
			p.x = ((1.0-t)**3.0) * self.point_c[0].x + (3*(1-t)**2) * t * self.point_c[1].x + (3*(1-t)*t*t) * self.point_c[2].x + (t*t*t) * self.point_c[3].x
			p.y = ((1.0-t)**3.0) * self.point_c[0].y + (3*(1-t)**2) * t * self.point_c[1].y + (3*(1-t)*t*t) * self.point_c[2].y + (t*t*t) * self.point_c[3].y
			self.pt_curve.append(p)
							
			t += self.step

	def compute_n(self):
		self.pt_curve = []
		t = 0
		
		while(t <= 1.0):
			p = Point(0, 0)
			i = 0
			n = self.nb_point_c-1
			while i <= n:
				p.x += self.cb(n, i) * (t**i) * ((1.0 - t)**(n-i)) * self.point_c[i].x
				p.y += self.cb(n, i) * (t**i) * ((1.0 - t)**(n-i)) * self.point_c[i].y

				i+=1
			
			self.pt_curve.append(p)
			
			t += self.step


	def display(self):
		ln = len(self.pt_curve)-1
		for i in range(ln):
			pygame.draw.aaline(dis, red, [self.pt_curve[i].x, self.pt_curve[i].y], [self.pt_curve[i+1].x, self.pt_curve[i+1].y])

		#pygame.draw.aaline(dis, red, [self.pt_curve[ln-1].x, self.pt_curve[ln-1].y], [self.pt_curve[i+1].x, self.pt_curve[i+1].y])



	def display_pt_control(self, pt):
		ln = len(self.point_c)-1
		for i in range(ln):
			pygame.draw.line(dis, cyan, [self.point_c[i].x, self.point_c[i].y], [self.point_c[i+1].x, self.point_c[i+1].y])

		if(pt):
			for i in range(ln+1):
				pygame.draw.circle(dis, black, [self.point_c[i].x, self.point_c[i].y], 5)

	def get_point_cont_mouse(self, pt):
		ln = len(self.point_c)
		self.upd_pt = -1
		for i in  range(ln):
			if(distance(pt, self.point_c[i]) <= 5):
				self.upd_pt = i
				break

		return self.upd_pt

	def Update_point_control(self, pt):
		if(self.upd_pt != -1):
			self.point_c[self.upd_pt].x = pt.x
			self.point_c[self.upd_pt].y = pt.y



#---------------------END CLASS


def gameloop():

	game_over = False

	NB = 20
	ptc = [Point(200, 500), Point(300, 400), Point(400, 400), Point(500, 500), Point(600, 400)]
	for i in range(NB-5):
		ptc.append(Point(random.randint(0, 1700), random.randint(0, 956)))


	bezier = Bezier(ptc, 0.001)
	bezier.compute_n()


	update_b = False
	while not game_over:
		
		for event in pygame.event.get():
			#print(event)
			if event.type == pygame.QUIT:
				game_over = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				button_press = pygame.mouse.get_pressed()
				if button_press[0]:
					mc = pygame.mouse.get_pos()
					r = bezier.get_point_cont_mouse(Point(mc[0], mc[1]))
					if(r != -1 and update_b == False):
						update_b = True
					if update_b:
						bezier.Update_point_control(Point(mc[0], mc[1]))
		
			elif event.type == pygame.MOUSEBUTTONUP:
				update_b = False
				bezier.compute_n()
			elif event.type == pygame.MOUSEMOTION:
				mc = pygame.mouse.get_pos()
				if update_b:
					bezier.Update_point_control(Point(mc[0], mc[1]))
		



		dis.fill(blue)
		
		bezier.display_pt_control(True)
		bezier.display()

		pygame.display.update()

		
	pygame.quit()
	quit()
	


gameloop()


