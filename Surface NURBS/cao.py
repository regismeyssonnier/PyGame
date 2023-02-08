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
from quaternion import *
from trackball import *
from grid import *
from nurbs3 import *
from shader import *

pygame.init()

blue = (0, 0, 255)
red = (255, 0, 0)
dark_red = (120, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
g70 = (70, 70, 70)
yellow = (255, 255, 102)
green = (0, 255, 0)
purple = (200, 0, 255)
cyan = (0, 120, 255)
gray = (50, 50, 50)

color = [red, white, yellow, green, purple]

dis_width = 1700
dis_height = 800
dis = pygame.display.set_mode((dis_width,dis_height), pygame.OPENGL|pygame.DOUBLEBUF)
pygame.display.set_caption('CAO')

clock = pygame.time.Clock()
game_speed = 120

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
speed_font = pygame.font.SysFont("comicsansms", 100)





def gameloop():

	game_over = False

	last_time = 0
	ntime = 0

	shader = Shader(True)
	quat = Quaternion(0.0, 0.0, 1.0, 0.0)
	#vVertices = [0.0, 0.25, 0.0, 1.1, 0.25, 0.0, 0.0, -0.25, -1.5, 1.0, -0.25, -1.5, 0.0, 1.0, 0.0, 1.1, 1.0, 0.0, 0.0, 0.6, -1.5, 1.0, 1.0, -1.5]
	vVertices = [0.0, -0.25, -1.5, 1.0, -0.25, -1.5, 0.0, 0.6, -1.5]
	
	trackball = Trackball(dis_width, dis_height)
	trackball.set_active(True)
	trackball.set_mouse_keyboard(True, True)

	grid = Grid(5.0, 5.0, 5, dis_width, dis_height)
	grid.set_mouse_keyboard(False, True)

	d = 3
	tu=[]
	st = 1.0 / (16+d+1)
	i = 0.0
	v = 0.0
	while i < 16+d+1:
		tu.append(v)
		v+=st

		i+=1

	print ("v " + str(v))

	tv=[]


	st = 1.0 / (16+d+1)
	i = 0.0
	v= 0.0
	while i < 16+d+1:
		tv.append(v)
		v+=st
		i+=1

	tu[0] = 0.0
	tu[16+d] = 1.0
	tv[0] = 0.0
	tv[16+d] = 1.0

	tu = [0.0, 0.2, 0.3, 0.5, 0.6, 0.8, 0.9, 1.0]
	tv = [0.0, 0.2, 0.3, 0.5, 0.6, 0.8, 0.9, 1.0]

	#w = [1.0, 0.5, 1.0, 0.75, 0.6, 0.8, 0.9]
	w = []
	for i in range(16):
		r = random.randint(20, 150)
		if r < 0:r = 0
		if r > 100: r = 100
		r /= 100.0
		w.append(0.5)

	nurbs = Nurbs3(d, tu, tv, [], 0.025, w, dis_width, dis_height)
	nurbs.create_grid_base()
	nurbs.set_mouse_keyboard(True, True)
	nurbs.compute()
	nurbs.create_line()
	nurbs.create_triangle()
	nurbs.compute_normal(1)
	nurbs.create_shader()
	nurbs.create_line_normal()

	altlight = True
	mat_specular = [ 1.0, 1.0, 1.0, 1.0 ];
	mat_shininess = [ 50.0 ];
	light_position = [ 0.0, 0.5, 5.5, 0.0 ];

	while not game_over:

		
		for event in pygame.event.get():
			#print(event)
			if event.type == pygame.QUIT:
				game_over = True
			if event.type == pygame.MOUSEBUTTONDOWN:
				button_press = pygame.mouse.get_pressed()
				if button_press[0]:
					mc = pygame.mouse.get_pos()
					
			elif event.type == pygame.MOUSEBUTTONUP:
				button_press = pygame.mouse.get_pressed()

			elif event.type == pygame.MOUSEMOTION:
				mc = pygame.mouse.get_pos()
			elif event.type == pygame.KEYUP:		
				if event.key == pygame.K_KP9:
					altlight = not altlight
					if altlight:
						nurbs.compute_normal(1)
						nurbs.create_line_normal()
					else:
						nurbs.compute_normal(2)
						nurbs.create_line_normal()

			trackball.set_event(event)
			grid.set_event(event)
			nurbs.set_event(event)

		#dis.fill(blue)

		#OPENGL INIT [(+)]
		glEnable(GL_PROGRAM_POINT_SIZE)
		glEnable(GL_LINE_SMOOTH)
		glLineWidth(1.5)

		glEnable(GL_DEPTH_TEST)
		glClearColor(0.5, 0.5, 0.5, 1.0)
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		
		glMatrixMode(GL_PROJECTION)
		glViewport(0, 0, dis_width, dis_height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(45, (dis_width / dis_height), 0.1, 500.0)
		glMatrixMode (GL_MODELVIEW)
		glLoadIdentity()


	
		

		
		color = glGetAttribLocation(shader.get_v_program(), "c")
		vertices = glGetAttribLocation(shader.get_v_program(), "vert")
		"""v 0.0 0.25 0.0
v 1.1 0.25 0.0
v 0.0 0.25 -1.5  2
v 1.0 0.25 -1.5  3
v 0.0 1.0 0.0
v 1.1 1.0 0.0
v 0.0 1.0 -1.5   6
v 1.0 1.0 -1.5"""

		last_time = ntime
		ntime = pygame.time.get_ticks();
		diff_t = ntime - last_time		
		#print (diff_t)

		vIndices = [0,1,2]#2,3,6 3,7,6
		vColors = [1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0,  0.0, 1.0, 1.0, 1.0,  1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0,  0.0, 1.0, 1.0, 1.0]

		
		#glShadeModel (GL_SMOOTH);

		#glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular);
		#glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess);
		

		shader.use_program()

		glEnable(GL_LIGHTING);
		#glEnable(GL_LIGHT0);
		glLightfv(GL_LIGHT0, GL_POSITION, light_position);
		
		nurbs.update_pos_point_c(diff_t)
		nurbs.draw_point_control(shader.get_v_program())
		nurbs.update_pos_point_curve(diff_t)
		#nurbs.draw_pt_curve(shader.get_v_program())
		#nurbs.draw_line_curve(shader.get_v_program())
		nurbs.use_program()
		nurbs.update_pos_normal(diff_t)
		nurbs.draw_triangle_curve()
		#nurbs.update_pos_line_normal_curve(diff_t)
		#nurbs.draw_triangle_normal()
		glDisable(GL_LIGHTING)

		shader.use_program()
		grid.Update_pos(diff_t)
		grid.Draw(shader.get_v_program())
		
		vectq = trackball.get_vector()

		quat = Quaternion(0.0, vectq.x, vectq.y, vectq.z)

		if(trackball.get_update()):
			
			#trackball.set_update(False)
			o = Point(0, 0)
			x = 0
			y = 0
			z = 0
			"""for i in range(3):
				#print(str(vVertices[vIndices[i]*3]))
				x += vVertices[vIndices[i]*3]
				y += vVertices[vIndices[i]*3+1]
				z += vVertices[vIndices[i]*3+2]"""
			#print(str(x) + " " + str(y) + " " + str(z))
			x /= 3.0
			y /= 3.0
			z /= 3.0
			for i in range(3):
				#vVertices[vIndices[i]*3] -= x
				#vVertices[vIndices[i]*3+1] -= y
				vVertices[vIndices[i]*3+2] -= -1.5

			#print(str(x) + " " + str(y) + " " + str(z))
			rot = quat.get_mat3x3(trackball.get_angle()*(diff_t * 0.1 / 100))

			#update lightpos
			tl = []
			for y in  range(3):
				r = 0
				for x in range(3):
					r+= rot[y][x] * light_position[x]
					
				tl.append(r)
			light_position = tl

			i = 0
			ln = len(vVertices)
			rVert = []
			while i  < ln:
			
				for y in  range(3):
					r = 0
					for x in range(3):
						r += rot[y][x] * vVertices[i+x]

					rVert.append(r);
				i += 3

			for i in range(3):
				#rVert[vIndices[i]*3] += x
				#rVert[vIndices[i]*3+1] += y
				rVert[vIndices[i]*3+2] += -1.5

			vVertices = rVert;

			

			#pygame.time.wait(1000)

		#print (str(rot))

		#grid.set_active_trackball(True)

		"""fbo = 0
		glGenBuffers(1,fbo)
		cbo = 0
		glGenBuffers(1,cbo)

		glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, cbo)
		glVertexAttribPointer(color, 4, GL_FLOAT, GL_FALSE, 0, vColors)
		glEnableVertexAttribArray(color)

		glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, fbo)
		glVertexAttribPointer(vertices, 3, GL_FLOAT, GL_FALSE, 0, vVertices)
		glEnableVertexAttribArray(vertices)
		
		
		glDrawElements(GL_TRIANGLES, 3,  GL_UNSIGNED_INT, vIndices)"""

	

		pygame.display.flip()

		#pygame.display.update()

		
	pygame.quit()
	quit()


gameloop()