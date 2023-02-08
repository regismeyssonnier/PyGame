from quaternion import *
import pygame
import math
from trigo import *

class Trackball:

	def __init__(self, width, height):
		self.update_t = False
		self.active = False
		self.v = Point3(0,0,0)
		self.width = width
		self.height= height
		self.lv = Point(0, 0)
		self.coord = Point(0,0)
		self.down = False
		self.angle = 0
		self.langle = 0
		self.start = False
		self.start_pt = Point3(0.0, 0.0, 0.0)
		self.mouse = True
		self.keyboard = True

	def set_active(self, act):
		self.active = act

	def get_update(self):
		return self.update_t 

	def set_update(self, up):
		self.update_t = up

	def get_angle(self):
		return self.angle

	def set_mouse_keyboard(self, a, k):
		self.mouse = a
		self.keyboard = k
		

	def mouse_to_sphere(self, x, y):
		x, y = x * 2.0 / self.width - 1.0, 1.0 - y * 2.0 / self.height
		length = math.sqrt(x * x + y * y)
		if length > 1.0:
			return Point3(x / length, y / length, 0.0)
		else:
			return Point3(x, y, math.sqrt(1.0 - length * length))

	def set_event(self, event):
		
		if not self.active:
			return

		if event.type == pygame.MOUSEBUTTONDOWN:

			if not self.mouse:
				return

			button_press = pygame.mouse.get_pressed()
			if button_press[0]:
				mc = pygame.mouse.get_pos()
				print("press")				
				self.down = True
				self.update_t = True
				self.start_pt = self.mouse_to_sphere(mc[0], mc[1])
				# 1700 800
				"""x = mc[0] - (self.width / 2.0)
				y = mc[1] - (self.height / 2.0)

				p = normalize(Point(x, y))

				self.v = p"""

					
		elif event.type == pygame.MOUSEBUTTONUP:
			if not self.mouse:
				return
			button_press = pygame.mouse.get_pressed()
			self.update_t = False
			self.down = False


		elif event.type == pygame.MOUSEMOTION:
			if not self.mouse:
				return
			self.lv = Point(self.coord.x, self.coord.y)
			mc = pygame.mouse.get_pos()
			self.coord = Point(mc[0], mc[1])
			#print(str(self.lv.x) + " " + str(self.lv.y) + " " + str(self.coord.x) + " "  + str(self.coord.y)) 


			if not self.update_t:
				return

			end_pt = self.mouse_to_sphere(mc[0], mc[1])
			self.v = cross3(self.start_pt, end_pt)
			costh = dot3(self.start_pt, end_pt)
			if(costh < -1.0):costh = -1.0
			if(costh > 1.0):costh = 1.0
			self.angle = math.acos(costh)*2.0 * 180.0 / 3.14159
			

			"""x = mc[0] - (self.width / 2.0)
			y = mc[1] - (self.height / 2.0)
					
			p = normalize3(Point3(x, y, 1.0))
			self.langle = self.angle
			self.angle = angle_vec3(p,normalize3(Point3(0.0, 0.0, 1.0)), Point3(0.0, 0.0, 0.0))"""



			
			#print(str(self.angle) + " "+ str(self.langle))
			"""if(self.langle != self.angle):
				self.update_t = True
			else:
				self.update_t = False"""

			#self.v = p

		elif event.type == pygame.KEYDOWN:		
			if not self.keyboard:
				return
			if event.key == pygame.K_KP7:
				self.v = normalize3(Point3(0.0, 0.0, 1.0))
				self.angle = 90
				self.update_t = True
			elif event.key == pygame.K_KP8:
				self.v = normalize3(Point3(0.0, 0.0, 1.0))
				self.angle = -90
				self.update_t = True
			elif event.key == pygame.K_KP4:
				self.v = normalize3(Point3(0.0, 1.0, 0.0))
				self.angle = 90
				self.update_t = True
			elif event.key == pygame.K_KP5:
				self.v = normalize3(Point3(0.0, 1.0, 0.0))
				self.angle = -90
				self.update_t = True
			elif event.key == pygame.K_KP1:
				self.v = normalize3(Point3(1.0, 0.0, 0.0))
				self.angle = 90
				self.update_t = True
			elif event.key == pygame.K_KP2:
				self.v = normalize3(Point3(1.0, 0.0, 0.0))
				self.angle = -90
				self.update_t = True
		elif event.type == pygame.KEYUP:		
			if not self.keyboard:
				return
			if event.key == pygame.K_KP7:
				self.update_t = False
			elif event.key == pygame.K_KP8:
				self.update_t = False
			elif event.key == pygame.K_KP4:
				self.update_t = False
			elif event.key == pygame.K_KP5:
				self.update_t = False
			elif event.key == pygame.K_KP1:
				self.update_t = False
			elif event.key == pygame.K_KP2:
				self.update_t = False


	def get_vector(self):
		return self.v







