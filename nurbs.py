# coding=utf-8
import pygame
import time 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.ARB.framebuffer_object import *
from OpenGL.GL.EXT.framebuffer_object import *
import random
import math
from trigo import *

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


class Nurbs:

    def __init__(self, k, t, ptc, st, w):
        self.k = k
        self.t = t
        self.m = len(ptc)
        self.point_c = ptc
        self.steps = st
        self.w = w
        self.pt_curve=[]

    def cox_de_boor(self, k, t, i, u):
        #k degre
        #t vecteur nodaux
        #index
        #point d'evaluation
        if k == 0:
            if t[i] <= u < t[i+1]:
                return 1
            else:
                return 0
        else:
            denom1 = t[i+k] - t[i]
            if denom1 == 0:
                c1 = 0
            else:
                c1 = (u - t[i]) / denom1 * self.cox_de_boor(k-1, t, i, u)
        
            denom2 = t[i+k+1] - t[i+1]
            if denom2 == 0:
                c2 = 0
            else:
                c2 = (t[i+k+1] - u) / denom2 * self.cox_de_boor(k-1, t, i+1, u)
        
            return c1 + c2


    def compute(self):
        self.pt_curve = []
        t = 0.1
        while t <= 1.0:
            p = Point(0.0,0.0)
            numx = 0
            for i in range(self.m):
                numx += self.w[i] * self.point_c[i].x * self.cox_de_boor(self.k, self.t, i, t)
            denx=  0.0
            for i in range(self.m):
                denx += self.w[i] * self.cox_de_boor(self.k, self.t, i, t)
            numy = 0.0
            for i in range(self.m):
                numy += self.w[i] * self.point_c[i].y * self.cox_de_boor(self.k, self.t, i, t)
            
            if denx == 0:
				p.x = 0.0
				p.y = 0.0
            else:
				p.x = numx / denx
				p.y = numy / denx

            if(p.x != 0.0 and p.y != 0.0):
				self.pt_curve.append(p)

            t+=self.steps
    
    def display(self):
		ln = len(self.pt_curve)-1
		for i in range(ln):
			pygame.draw.aaline(dis, red, [self.pt_curve[i].x, self.pt_curve[i].y], [self.pt_curve[i+1].x, self.pt_curve[i+1].y])

		#pygame.draw.aaline(dis, red, [self.pt_curve[ln-1].x, self.pt_curve[ln-1].y], [self.pt_curve[i+1].x, self.pt_curve[i+1].y])


    def display_pt_control(self, pt):
		ln = len(self.point_c)-1
		for i in range(ln):
			pygame.draw.line(dis, cyan, [self.point_c[i].x, self.point_c[i].y], [self.point_c[i+1].x, self.point_c[i+1].y], 2)

		if(pt):
			for i in range(ln+1):
				pygame.draw.circle(dis, black, [self.point_c[i].x, self.point_c[i].y], 10)

    def get_point_cont_mouse(self, pt):
		ln = len(self.point_c)
		self.upd_pt = -1
		for i in  range(ln):
			if(distance(pt, self.point_c[i]) <= 10):
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

	NB = 7
	ptc = [Point(200, 500), Point(300, 400), Point(400, 400), Point(500, 500), Point(600, 400)]
	for i in range(NB-5):
		ptc.append(Point(random.randint(0, 1700), random.randint(0, 956)))

	d = 3
	#t = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 0.91, 0.92, 0.93, 0.94, 0.95, 0.98, 1.0]
	t=[]
	st = 1.0 / (NB+d+1)
	i = 0
	while i <= 1.0:
		t.append(i)
		i+=st

	#w = [1.0, 0.5, 1.0, 0.75, 0.6, 0.8, 0.9]
	w = []
	for i in range(NB):
		r = random.randint(1, 150)
		if r < 0:r = 0
		if r > 100: r = 100
		r /= 100.0
		w.append(r)


	nurbs = Nurbs(3, t, ptc, 0.005, w)
	nurbs.compute()

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
					r = nurbs.get_point_cont_mouse(Point(mc[0], mc[1]))
					if(r != -1 and update_b == False):
						update_b = True
					if update_b:
						nurbs.Update_point_control(Point(mc[0], mc[1]))
		
			elif event.type == pygame.MOUSEBUTTONUP:
				update_b = False
				nurbs.compute()
			elif event.type == pygame.MOUSEMOTION:
				mc = pygame.mouse.get_pos()
				if update_b:
					nurbs.Update_point_control(Point(mc[0], mc[1]))
					nurbs.compute()



		dis.fill(blue)
		
		nurbs.display_pt_control(True)
		nurbs.display()

		pygame.display.update()

		
	pygame.quit()
	quit()
	


gameloop()


