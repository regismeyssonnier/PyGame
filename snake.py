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
pygame.display.set_caption('Jeu du serpent')



snake_block = 30


clock = pygame.time.Clock()
snake_speed = 20

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def Your_score(score):
	value = score_font.render("Votre score : " + str(score), True, yellow)
	dis.blit(value, [0, 0]) 

def our_snake(snake_block, snake_list):
	for x in snake_list:
		pygame.draw.rect(dis, cyan, [x[0], x[1], snake_block, snake_block])

def message(msg,color):
	mesg = font_style.render(msg, True, color)
	dis.blit(mesg, [dis_width/3, dis_height/3])

def gameLoop():

	game_over = False
	game_close = False

	x1 = dis_width/2
	y1 = dis_height/2

	x1_change = 0
	y1_change = 0
	
	snake_List = []
	Length_of_snake = 1

	food_List = []
	Length_food = 100
	count_food = 0
	
	win = False
	start = True 
	mode_food = 2 
	
	for i in range(Length_food):
		if mode_food == 1:
			foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
			foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
			food_List.append([foodx, foody])
		elif mode_food == 2:
			foodx = random.randrange(0, dis_width - snake_block) 
			foody = random.randrange(0, dis_height - snake_block)
			food_List.append([foodx, foody])
		#print(i)
		#print("foodx:" + str(foodx) + ", foody:" + str(foody)) 
		
	
	while not game_over:
	
		while game_close == True:
			dis.fill(blue)
			if win == True:
				message("Vous avez gagne ! Q-Quitter C-Continuer", red)
			else:
				message("Vous avez perdu ! Q-Quitter C-Continuer", red)
			Your_score(Length_of_snake-1)
			pygame.display.update()
			
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						game_over = True
						game_close = False
						
					elif event.key == pygame.K_c:
						gameLoop()
						
		for event in pygame.event.get():
			#print(event)
			if event.type == pygame.QUIT:
				game_over = True
			if event.type == pygame.KEYDOWN:				
				if event.key == pygame.K_KP4:
					x1_change = -snake_block
					y1_change = 0
	
				elif event.key == pygame.K_KP6:
					x1_change = snake_block
					y1_change = 0
	
				elif event.key == pygame.K_KP8:
					y1_change = -snake_block
					x1_change = 0
	
				elif event.key == pygame.K_KP5:
					y1_change = snake_block
					x1_change = 0
					
				if start == True:
					start = False
			
				
		if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
			game_close = True
			win = False
	
		x1 += x1_change
		y1 += y1_change
		dis.fill(blue)
		c = 0;
		for fd in food_List:
			pygame.draw.rect(dis, color[c], [fd[0], fd[1], snake_block, snake_block])
			c = (c + 1) % len(color);
		
		snake_Head = []
		snake_Head.append(x1);
		snake_Head.append(y1);
		snake_List.append(snake_Head)
		
		if len(snake_List) > Length_of_snake:
			del snake_List[0]
			
			
		if start == False:
			for x in snake_List[:-1]: 
				if x == snake_Head:
					game_close = True
		
				
		our_snake(snake_block, snake_List)
		Your_score(Length_of_snake-1)
		
		#pygame.draw.rect(dis, black, [x1, y1, snake_block, snake_block])
		pygame.display.update()
		i = 0
		for fd in food_List:
			if (x1 >= fd[0] and x1 < (fd[0] + snake_block) and y1 >= fd[1] and y1 < (fd[1] + snake_block)) or ((x1 + snake_block) >= fd[0] and  (x1 + snake_block) < (fd[0] + snake_block) and y1 >= fd[1] and y1 < (fd[1] + snake_block)) or (x1 >= fd[0] and x1 < (fd[0] + snake_block) and (y1 + snake_block) >= fd[1] and (y1 + snake_block) < (fd[1] + snake_block)) or ((x1 + snake_block) >= fd[0] and (x1 + snake_block) < (fd[0] + snake_block) and (y1 + snake_block) >= fd[1] and (y1 + snake_block) < (fd[1] + snake_block)):
				del food_List[i]
				"""if mode_food == 1:
					foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
					foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
					food_List.append([foodx, foody])
				elif mode_food == 2:
					foodx = random.randrange(0, dis_width - snake_block) 
					foody = random.randrange(0, dis_height - snake_block)
					food_List.append([foodx, foody])"""
				#print("foodx:" + str(foodx) + ", foody:" + str(foody)) 
				#food_List.append([foodx, foody])
						
				count_food += 1
				if count_food == Length_food:
					win = True
					game_close = True
				Length_of_snake += 1
			i+=1

		clock.tick(snake_speed)
			
	pygame.quit()
	quit()
	


gameLoop()





















