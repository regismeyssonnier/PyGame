# coding=utf-8
import pygame
import time 
import random

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

dis_width = 1700
dis_height = 800
dis=pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Game')

clock = pygame.time.Clock()
game_speed = 50

score_font = pygame.font.SysFont("comicsansms", 35)
score = 0

def Your_score(score):
	value = score_font.render("Votre score : " + str(score), True, yellow)
	dis.blit(value, [0, 0]) 
	
def draw_Vaisseau(x, y, w, h, c):
	""" body """
	pygame.draw.rect(dis, c, [x, y, w, h])

	""" gun """
	#left
	pygame.draw.rect(dis, yellow, [x+10, y-40, 10, 10])
	pygame.draw.rect(dis, c, [x, y-30, 30, 30])
	#right
	pygame.draw.rect(dis, yellow, [x+w-20, y-40, 10, 10])
	pygame.draw.rect(dis, c, [x+w-30, y-30, 30, 30])
	
def draw_ammo(ammo):

	for a in ammo:
		pygame.draw.rect(dis, a[2], [a[0], a[1], 10, 10])
		
		
def draw_ennemy(ennemy):
	for e in ennemy:
		pygame.draw.rect(dis, e[2], [e[0], e[1], e[3], e[4]])

def test_hit(ax, ay, aw, ah, ex, ey, ew, eh):
	if (ex >= ax and ex <= (ax + aw) and ey >= ay and ey <= (ay + ah)) or ((ex + ew) >= ax and  (ex + ew) <= (ax + aw) and ey >= ay and ey <= (ay + ah)) or (ex >= ax and ex <= (ax + aw) and (ey + eh) >= ay and (ey + eh) <= (ay + ah)) or ((ex + ew) >= ax and (ex + ew) <= (ax + aw) and (ey + eh) >= ay and (ey + eh) <= (ay + ah)):
		return True
	else:
		return False 
	

def gameLoop():
	game_over = False
	game_close = False
	
	""" Vaisseau variables """
	X_speed = 30
	Y_speed = 30
	x1 = dis_width / 2
	y1 = dis_height / 2
	x1_change = 0
	y1_change = 0
	V_width = 100
	V_height = 50
	#ammo
	ammo = []
	ammo_speed = 50
	""" Fin Vaisseau """
	
	""" ennemy """
	nb_ennemy = 400
	ennemy = []
	ennemy_X_speed = 44
	ennemy_Y_speed = 5
	ennemy_width = 20
	ennemy_height = 20
	score_value = 1000000000
	x = 10
	y = 10
	for i in range(nb_ennemy):
		ennemy.append([x, y, cyan, ennemy_width, ennemy_height])
		x += 50
		if x > dis_width:
			x = 10
			y += 25
			
		
	
	""" Keyboard """
	d_up = False
	d_down = False
	d_left = False
	d_right = False
	k_space = False
	
	score = 0
	
	
	
	while not game_over:
	
		""" Touche du clavier """
		for event in pygame.event.get():
			#print(event)
			if event.type == pygame.QUIT:
				game_over = True
				
			if event.type == pygame.KEYDOWN:				
				if event.key == pygame.K_KP4:
					d_left = True
					d_right = False
					x1_change = -X_speed
						
				elif event.key == pygame.K_KP6:
					d_right = True
					d_left = False
					x1_change = X_speed
						
				elif event.key == pygame.K_KP8:
					d_up = True
					d_down = False
					y1_change = -Y_speed
						
				elif event.key == pygame.K_KP5:
					d_down = True
					d_up = False
					y1_change = Y_speed
					
				elif event.key == pygame.K_SPACE:
					k_space = True
										
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_KP4:
					d_left = False
						
				elif event.key == pygame.K_KP6:
					d_right = False
						
				elif event.key == pygame.K_KP8:
					d_up = False
						
				elif event.key == pygame.K_KP5:
					d_down = False
					
				elif event.key == pygame.K_SPACE:
					k_space = False

		dis.fill(purple)
		
		#print("L:" + str(d_left) + " R:" + str(d_right) + " U:" + str(d_up) + " D:" + str(d_down)) 
		
					
		 
		""" Vaisseau MAJ """
		if d_left == True :
			if (x1+x1_change) >= 0 :
				x1 += x1_change
			else:
				x = 0
		if d_right == True :
			if (x1+V_width+x1_change) <= dis_width:
				x1 += x1_change
			else:
				x1 = dis_width - V_width
					
		if d_up == True :
			if (y1+y1_change) >= 0: 
				y1 += y1_change
			else:
				y1 = 0
				
		if d_down == True :
			if (y1+V_height+y1_change)  <= dis_height: 
				y1 += y1_change
			else:
				y1 = dis_height - V_height
				
		""" Keyboard """
		if k_space == True:
			ammo.append([x1-5, y1-40, yellow, 10, 10])
			ammo.append([x1+10, y1-40, yellow, 10, 10])
			ammo.append([x1+25, y1-40, yellow, 10, 10])
			
			ammo.append([x1+V_width-35, y1-40, yellow, 10, 10])
			ammo.append([x1+V_width-20, y1-40, yellow, 10, 10])
			ammo.append([x1+V_width-5, y1-40, yellow, 10, 10])
			
		""" Update coord ammo """
		listsa = []		
		i = 0
		for a in ammo:
			if a[1] > 0: 
				a[1] -= random.randrange(ammo_speed / 2, ammo_speed)
			else:
				#del ammo[i]
				listsa.append(i)
			i+=1	
			
		if(len(listsa) > 0):
			new_ammo = []
			la = len(ammo)
			for am in range(la):
				suppr = False	
				for a in listsa:
					if am == a:
						suppr = True
				if suppr == False:
					new_ammo.append([ammo[am][0], ammo[am][1], ammo[am][2], ammo[am][3], ammo[am][4]])			
			ammo=[]
			ammo = 	list(new_ammo)
			
		""" Update ennemy """
		i = 0
		listse = []
		for e in ennemy:
			if e[1] < dis_height: 
				e[1] += random.randrange(ennemy_Y_speed / 2, ennemy_Y_speed)
			else:
				#del ennemy[i]
				listse.append(i)
			i+=1
			
		new_ennemy = []
			
		if(len(listse) > 0):
			le = len(ennemy)
			for en in range(le):
				suppr = False	
				for e in listse:
					if en == e:
						suppr = True
				if suppr == False:		
					new_ennemy.append([ennemy[en][0],ennemy[en][1], ennemy[en][2], ennemy[en][3], ennemy[en][4]]) 
			ennemy=[]
			ennemy = list(new_ennemy)
			
		if len(ennemy) == 0:
			x = 10
			y = 10
			for i in range(nb_ennemy):
				ennemy.append([x, y, cyan, ennemy_width, ennemy_height])
				x += 50
				if x > dis_width:
					x = 10
					y += 25
		
		""" hit test """
		listse = []
		listsa = []
		ia = 0		
		for a in ammo:
			ie = 0
			suppr = False
			for e in ennemy:
				if test_hit(a[0], a[1], a[3], a[4], e[0], e[1], e[3], e[4]) == True:
					try:
						listse.append(ie)
						listsa.append(ia)
						score += score_value
						
					except:
						print("OOps" + str(ia))
				ie += 1 
			ia += 1
			
		#print(listse)
			
		""" Update list ennemy and ammo """
		if(len(listse) > 0):
			new_ennemy = []
			
			le = len(ennemy)
			for en in range(le):
				suppr = False	
				for e in listse:
					if en == e:
						suppr = True
				if suppr == False:		
					new_ennemy.append([ennemy[en][0],ennemy[en][1], ennemy[en][2], ennemy[en][3], ennemy[en][4]]) 
			ennemy=[]
			ennemy = list(new_ennemy)
			#print(ennemy)
		
		if(len(listsa) > 0):
			new_ammo = []
			la = len(ammo)
			for am in range(la):
				suppr = False	
				for a in listsa:
					if am == a:
						suppr = True
				if suppr == False:
					new_ammo.append([ammo[am][0], ammo[am][1], ammo[am][2], ammo[am][3], ammo[am][4]])			
			ammo=[]
			ammo = 	list(new_ammo)
			
			
		""" draw """
		draw_Vaisseau(x1, y1, V_width, V_height, blue)
		draw_ammo(ammo)
		
		draw_ennemy(ennemy)
		
		Your_score(score)
		
		pygame.display.update()
		
		
		clock.tick(game_speed)

	pygame.quit()
	quit()
	

gameLoop()
