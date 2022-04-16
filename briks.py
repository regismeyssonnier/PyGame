# coding=utf-8
import pygame
import time 
import random
import math

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

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
score = 0

def message(msg,color):
	mesg = font_style.render(msg, True, color)
	dis.blit(mesg, [dis_width/3, dis_height/3])

def Your_score(score):
	value = score_font.render("Votre score : " + str(score), True, yellow)
	dis.blit(value, [0, 0]) 
	
		
def draw_head(x, y, w, h):
	#head
	pygame.draw.ellipse(dis, blue, [x, y, w, h])
	#eye
	pygame.draw.ellipse(dis, white, [x+w*0.75, y+h/3, w/10, h/10])
	#mouth
	pygame.draw.line(dis, black, [x+w*0.75, y+h*0.6], [x+w-3, y+h*0.6], 2)	
		

def draw_body(x, y, w, h):
	pygame.draw.ellipse(dis, cyan, [x, y, w, h])
	
def draw_leg(x, y, w, h, c):
	pygame.draw.rect(dis, c, [x, y, w, h])
	pygame.draw.rect(dis, c, [x, y+h, w+10, h/10])
	
def draw_leg_move(x, y, w, h, c):
	pygame.draw.polygon(dis, c, [(x, y), (x+w, y), (x+w*2.5, y+h), (x+w*1.5, y+h)])
	pygame.draw.rect(dis, c, [x+w*1.5, y+h, w+10, h/10])
	
def draw_arm(x, y, w, h, c):
	pygame.draw.rect(dis, c, [x, y, w, h])
	
def draw_forearm(x, y, w, h, c):
	pygame.draw.polygon(dis, c, [(x, y), (x+w, y), (x+w*2, y+h), (x+w, y+h)])
	
def droite(x, y, w, h, c):
	pygame.draw.rect(dis, c, [x, y, w, h])
	pygame.draw.polygon(dis, c, [(x+w, y), (x+w*2.0, y-10), (x+w*2.0, y+h-10), (x+w, y+h-1)])
	
def draw_ball(x, y, r, c):
	pygame.draw.circle(dis, c, (x, y), r)
	pygame.draw.circle(dis, white, (x+r/5, y-r/5), r/10)
		
		
def draw_racket(x, y, w, h, r, c):
	pygame.draw.circle(dis, yellow, (x, y+h/2), r)
	pygame.draw.circle(dis, yellow, (x+w, y+h/2), r)
	pygame.draw.rect(dis, c, [x, y, w, h])
	pygame.draw.rect(dis, cyan, [x+10, y+10, w-20, h /10])	
	
def draw_brick(x, y, w, h, c):
	pygame.draw.rect(dis, c, [x, y, w, h])
	pygame.draw.rect(dis, white, [x+10, y+10, w-20, h /10])	
	

def test_hit(ax, ay, aw, ah, ex, ey, ew, eh):
	if (ex >= ax and ex <= (ax + aw) and ey >= ay and ey <= (ay + ah)) or ((ex + ew) >= ax and  (ex + ew) <= (ax + aw) and ey >= ay and ey <= (ay + ah)) or (ex >= ax and ex <= (ax + aw) and (ey + eh) >= ay and (ey + eh) <= (ay + ah)) or ((ex + ew) >= ax and (ex + ew) <= (ax + aw) and (ey + eh) >= ay and (ey + eh) <= (ay + ah)):
		return True
	else:
		return False 
		
def test_hit_circle(br, bx, by, x, y):
	d = math.sqrt(pow(x - bx, 2) + pow(y - by, 2))
	if d <= br:
		return True
	else:
		return False
	

def gameLoop():
	game_over = False
	game_close = False
	
	""" racket variables """
	X_speed = 50
	Y_speed = 20
	
	x1_change = 0
	y1_change = 0
	#size
	R_width = 600
	R_height = 50
	x1 = dis_width / 2
	y1 = dis_height - R_height
	
	""" Fin racket """
	
	""" Ball """
	B_radius = 20 
	B_X = random.randrange(dis_width / 2, dis_width)
	B_Y = dis_height / 2
	B_X_prec = B_X
	B_Y_prec = B_Y
	B_X_speed = 15
	B_Y_speed = 15
	B_Y_speedorig = B_Y_speed
	B_X_spin = 0
	B_Y_spin = 0
	B_Dir = 1 
	
	""" Bricks """
	bricks = []
	Br_width = 100
	Br_height = 25
	nb_bricks = 210
	ct_bricks = 0
	x = 10
	y = 10
	for i in range(nb_bricks):
		bricks.append([x, y, Br_width, Br_height, blue])
		x += Br_width + 10
		if (x + Br_width) > dis_width:
			y += Br_height + 10
			x = 10 
	
	
	""" Keyboard """
	d_up = False
	d_down = False
	d_left = False
	d_right = False
	k_space = False
	
	score = 0
	win = False
	high_speed = True
	nhs = 0
	game_blocked = False
	nb_coup_block = 20
	coup_block = 0
	
	while not game_over:
		
		while game_close == True:
			dis.fill(purple)
			if win == True:
				message("Vous avez gagne ! Q-Quitter C-Continuer", red)
			else:
				message("Vous avez perdu ! Q-Quitter C-Continuer", red)
			Your_score(score)
			pygame.display.update()
			
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						game_over = True
						game_close = False
						ct_bricks = 0
						
					elif event.key == pygame.K_c:
						gameLoop()
				pygame.display.update()
	
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
			if (x1+R_width+x1_change) <= dis_width:
				x1 += x1_change
			else:
				x1 = dis_width - R_width
					
		if d_up == True :
			if (y1+y1_change) >= 0: 
				y1 += y1_change
			else:
				y1 = 0
				
		if d_down == True :
			if (y1+R_height+y1_change)  <= dis_height: 
				y1 += y1_change
			else:
				y1 = dis_height - R_height
			
		if B_Dir == 1:
			B_X += -B_X_speed 
			B_Y += -(B_Y_speed + B_Y_spin) 	
		elif B_Dir == 2:
			B_X += B_X_speed
			B_Y += -(B_Y_speed + B_Y_spin) 	
		elif B_Dir == 3:
			B_X += B_X_speed
			B_Y += B_Y_speed + B_Y_spin	
		elif B_Dir == 4:
			B_X += -B_X_speed
			B_Y += B_Y_speed + B_Y_spin
		elif B_Dir == 5:
			B_X += 0
			B_Y += 0
			
		if B_Y < 0:
			if B_Dir == 1:
				B_Dir = 4
			elif B_Dir == 2:
				B_Dir = 3
		elif B_Y > (dis_height - R_height):
			if B_Dir == 3:
				B_Dir = 2
			elif B_Dir == 4:
				B_Dir = 1
		elif B_X < 0:
			if B_Dir == 1:
				B_Dir = 2
			elif B_Dir == 4:
				B_Dir = 3
		
		elif B_X > dis_width:		
			if B_Dir == 2:
				B_Dir = 1
			elif B_Dir == 3:
				B_Dir = 4
				
		cp = False
		if (B_Y ) > (dis_height - R_height) :
			if B_X >= (x1-R_height) and B_X <= x1:
				B_Y_speed = 5
				cp = True
			elif B_X >= (x1+R_width) and B_X <= (x1+R_width+R_height):
				B_Y_speed = 5
				cp = True
			elif (B_X >= (x1) and B_X <= (x1+R_width)):
				B_Y_speed = B_Y_speedorig
				B_Y_spin = random.randrange(1, 3)
				B_X_spin = random.randrange(1, 3)
				cp = True
			else:
				B_Dir = 5
				game_close = True
				
		if cp == True:
			
			coup_block+=1
			if coup_block == nb_coup_block:
				game_blocked = True
				game_close = True	
				win = True
				coup_block = 0
				
			
		listb = []
		ib = 0	
		add = 0
		# x y w h c
		"""for b in bricks:
			append = 0
			if (B_X) >= b[0] and (B_X) <= (b[0] + b[2]) and (B_Y) >= b[1] and (B_Y) <= (b[1] + b[3]):
				listb.append(ib)
				append = 1
				add = 1 
				if B_Dir == 1:
					B_Dir = 4
				elif B_Dir == 2:
					B_Dir = 3
				elif B_Dir == 3:
					B_Dir = 2
				elif B_Dir == 4:
					B_Dir = 1
					
				score += 1 
				ct_bricks+=1
				B_Y_spin = 0
				#print("0")
				
			#hg	
			if append == 0:
				if test_hit_circle(B_radius, B_X, B_Y, b[0], b[1]):
					append = 1
					add = 1 
					listb.append(ib)
					score += 1
					ct_bricks+=1
					if B_Dir == 1:
						B_Dir = 2
					elif B_Dir == 2:
						B_Dir = 1
					elif B_Dir == 3:
						B_Dir = 2
					elif B_Dir == 4:
						B_Dir = 1
					#print("1")
					B_Y_spin = random.randrange(1, 5)
				
			
				elif test_hit_circle(B_radius, B_X, B_Y, b[0]+b[2], b[1]):
					append = 1
					add = 1 
					listb.append(ib)
					score += 1
					ct_bricks+=1
					if B_Dir == 1:
						B_Dir = 2
					elif B_Dir == 2:
						B_Dir = 1
					elif B_Dir == 3:
						B_Dir = 2
					elif B_Dir == 4:
						B_Dir = 1
					#print("2")
					B_Y_spin = random.randrange(1, 5)
			
				elif test_hit_circle(B_radius, B_X, B_Y, b[0]+b[2], b[1]+b[3]):
					append = 1
					add = 1 
					listb.append(ib)
					score += 1
					ct_bricks+=1
					if B_Dir == 1:
						B_Dir = 4
					elif B_Dir == 2:
						B_Dir = 3
					elif B_Dir == 3:
						B_Dir = 4
					elif B_Dir == 4:
						B_Dir = 3
					#print("3")	
					B_Y_spin = random.randrange(1, 5)
			
				elif test_hit_circle(B_radius, B_X, B_Y, b[0], b[1]+b[3]):
					append = 1
					add = 1 
					listb.append(ib)
					score += 1
					ct_bricks+=1
					if B_Dir == 1:
						B_Dir = 4
					elif B_Dir == 2:
						B_Dir = 3
					elif B_Dir == 3:
						B_Dir = 4
					elif B_Dir == 4:
						B_Dir = 3
					#print("4")
					B_Y_spin = random.randrange(1, 5)
					
			ib+=1"""
			
		#print("hs : " + str(high_speed) + ", append :" + str(append))
		if high_speed == True and add == 0:
			#print("high_speed_test enter")
			dx = B_X - B_X_prec
			dy = B_Y - B_Y_prec 
			#print("dx : " + str(dx) + ", dy :" + str(dy))
			# x y w h c
			nhs += 1
			ib = 0
			for b in bricks:
				pdx = dx / 10.0#(b[2]/ 10.0)+ 1.0
				pdy = dy / 10.0#(b[3]/ 10.0 )+ 1.0
				#print("pdx : " + str(pdx) + ", pdy :" + str(pdy))
				ddx = B_X_prec
				ddy = B_Y_prec
				n = 10
				addin = 0
				for i in range(int(n)):
					#print("high_speed_test")
					
					if ddx >= b[0] and ddx <= (b[0] + b[2]) and ddy >= b[1] and ddy <= (b[1] + b[3]):
						listb.append(ib) 
						addin = 1
						add = 1
						if B_Dir == 1:
							B_Dir = 4
						elif B_Dir == 2:
							B_Dir = 3
						elif B_Dir == 3:
							B_Dir = 2
						elif B_Dir == 4:
							B_Dir = 1
						#print("high_speed" + str(nhs) + " n: " + str(n) + " - " + str(ib))
						score += 1
						ct_bricks+=1
						
						
					if(addin == 0):
						if test_hit_circle(B_radius, ddx, ddy, b[0], b[1]):
							listb.append(ib) 
							score += 1
							ct_bricks+=1
							addin = 1
							add = 1
							#print("high_speedcirc" + str(nhs) + " n: " + str(n) + " - " + str(ib))
							if B_Dir == 1:
								B_Dir = 2
							elif B_Dir == 2:
								B_Dir = 1
							elif B_Dir == 3:
								B_Dir = 2
							elif B_Dir == 4:
								B_Dir = 1
						elif test_hit_circle(B_radius, ddx, ddy, b[0]+b[2], b[1]):
							listb.append(ib) 
							score += 1
							ct_bricks+=1
							addin = 1
							add = 1
							#print("high_speedcirc" + str(nhs) + " n: " + str(n) + " - " + str(ib))
							if B_Dir == 1:
								B_Dir = 2
							elif B_Dir == 2:
								B_Dir = 1
							elif B_Dir == 3:
								B_Dir = 2
							elif B_Dir == 4:
								B_Dir = 1
						elif test_hit_circle(B_radius, ddx, ddy, b[0]+b[2], b[1]+b[3]):
							listb.append(ib) 
							score += 1
							ct_bricks+=1
							addin = 1
							add = 1
							#print("high_speedcirc" + str(nhs) + " n: " + str(n) + " - " + str(ib))
							if B_Dir == 1:
								B_Dir = 4
							elif B_Dir == 2:
								B_Dir = 3
							elif B_Dir == 3:
								B_Dir = 4
							elif B_Dir == 4:
								B_Dir = 3
						elif test_hit_circle(B_radius, ddx, ddy, b[0], b[1]+b[3]):
							listb.append(ib) 
							score += 1
							ct_bricks+=1
							addin = 1
							add = 1
							#print("high_speedcirc" + str(nhs) + " n: " + str(n) + " - " + str(ib))
							if B_Dir == 1:
								B_Dir = 4
							elif B_Dir == 2:
								B_Dir = 3
							elif B_Dir == 3:
								B_Dir = 4
							elif B_Dir == 4:
								B_Dir = 3
						
							
					if addin == 1:
						break
					ddx += pdx
					ddy += pdy
				ib+=1
				
				
			
		""" Update list bricks """
		if(len(listb) > 0):
			new_bricks = []
			
			lb = len(bricks)
			for eb in range(lb):
				suppr = False	
				for b in listb:
					if eb == b:
						suppr = True
				if suppr == False:		
					new_bricks.append([bricks[eb][0],bricks[eb][1], bricks[eb][2], bricks[eb][3], bricks[eb][4]]) 
			bricks=[]
			bricks = list(new_bricks)
			
		#print("ct_bricks:" + str(ct_bricks) + ", nb_bricks:" + str(nb_bricks))
		if add == 1:
			coup_block = 0
				
			
		if ct_bricks == nb_bricks:
			game_close = True	
			win = True
				
		""" draw """
		for b in bricks:
			draw_brick(b[0], b[1], b[2], b[3], b[4])
		
		x1 = B_X-R_width/2
		draw_racket(x1, y1, R_width, R_height, R_height/2, blue) 
		draw_ball(B_X, B_Y, B_radius, red)
		
		Your_score(score)
		
		pygame.display.update()
		
		B_X_prec = B_X
		B_Y_prec = B_Y
		
		clock.tick(game_speed)
		#print(L_delay_v)

	pygame.quit()
	quit()
	

gameLoop()
