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
pygame.display.set_caption('Pod')


clock = pygame.time.Clock()
interval_tour = 100;

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

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
	def compute(self):
		t = 0
		while(t <= 1.0):
			p = Point(0, 0)
			p.x = ((1.0-t)**3.0) * self.point_c[0].x + (3*(1-t)**2) * t * self.point_c[1].x + (3*(1-t)*t*t) * self.point_c[2].x + (t*t*t) * self.point_c[3].x
			p.y = ((1.0-t)**3.0) * self.point_c[0].y + (3*(1-t)**2) * t * self.point_c[1].y + (3*(1-t)*t*t) * self.point_c[2].y + (t*t*t) * self.point_c[3].y
			self.pt_curve.append(p)
							
			t += self.step

	def display(self):
		ln = len(self.pt_curve)-1
		for i in range(ln):
			pygame.draw.line(dis, red, [self.pt_curve[i].x, self.pt_curve[i].y], [self.pt_curve[i+1].x, self.pt_curve[i+1].y])


	def display_pt_control(self):
		ln = len(self.point_c)-1
		for i in range(ln):
			pygame.draw.line(dis, cyan, [self.point_c[i].x, self.point_c[i].y], [self.point_c[i+1].x, self.point_c[i+1].y])




#---------------------END CLASS


def gameloop():

	game_over = False

	ptc = [Point(200, 500), Point(300, 400), Point(400, 400), Point(500, 500)]

	bezier = Bezier(ptc, 0.1)
	bezier.compute()



	while not game_over:
		
		for event in pygame.event.get():
			#print(event)
			if event.type == pygame.QUIT:
				game_over = True

		dis.fill(blue)
		
		bezier.display_pt_control()
		bezier.display()


		pygame.display.update()

		
	pygame.quit()
	quit()
	


gameloop()
