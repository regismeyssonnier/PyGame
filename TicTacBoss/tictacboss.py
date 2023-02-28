# coding=utf-8
import pygame
import time 
import random
from back import *
from grid import *
from cross import *
from circle import *
from Player import *
from Boss import *
from montecarlo import *

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

dis_width = 800
dis_height = 600
screen = pygame.display.set_mode((dis_width,dis_height), pygame.DOUBLEBUF)
pygame.display.set_caption('Tic Tac Toe')

clock = pygame.time.Clock()
game_speed = 120

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
speed_font = pygame.font.SysFont("comicsansms", 21)


def display_win(num):
	value = 0
	if num == 3:
		value = score_font.render("Match null", True, yellow)
	else:
		value = score_font.render("Winner is player : " + str(num), True, yellow)
	screen.blit(value, [200, 0]) 

def display_score(scorep1, scorep2):
	value = font_style.render("Player1 : " + str(scorep1), True, yellow)
	screen.blit(value, [20, 0])
	value = font_style.render("Player2 : " + str(scorep2), True, yellow)
	screen.blit(value, [20, 30])

def display_who_play(alt):
	if alt:
		value = speed_font.render("Player1 plays", True, yellow)
	else:
		value = speed_font.render("Player2 plays", True, yellow)
	screen.blit(value, [10, 100])

def gameloop():

	game_over = False

	background = BackGrid()
	grid = Grid()
	playermc = Player(1)
	there_is_winner = 0
	WINNER = -1
	scorep1 = scorep2 = 0
	boss = True
	computer = True
	start_game= True
	first_move = 0

	bosspl = Boss(2)

	add_case = -1
	cross = []
	cross.append(Cross(154, 53))
	cross.append(Cross(322, 53))
	cross.append(Cross(515, 53))
	cross.append(Cross(154, 226))
	cross.append(Cross(322, 226))
	cross.append(Cross(515, 226))
	cross.append(Cross(154, 404))
	cross.append(Cross(322, 404))
	cross.append(Cross(515, 404))

	circle = []
	circle.append(Circle(154, 53))
	circle.append(Circle(322, 53))
	circle.append(Circle(515, 53))
	circle.append(Circle(154, 226))
	circle.append(Circle(322, 226))
	circle.append(Circle(515, 226))
	circle.append(Circle(154, 404))
	circle.append(Circle(322, 404))
	circle.append(Circle(515, 404))


	alt = True

	last_time = 0
	ntime = 0
	while not game_over:
	
		last_time = ntime
		ntime = pygame.time.get_ticks();
		diff_t = ntime - last_time		
		#print (diff_t)
		
		for event in pygame.event.get():
			#print(event)
			if event.type == pygame.QUIT:
				game_over = True

			if event.type == pygame.MOUSEBUTTONDOWN:
				button_press = pygame.mouse.get_pressed()
				if button_press[0]:
					mc = pygame.mouse.get_pos()
									
			if event.type == pygame.MOUSEBUTTONUP:
				pass
			if event.type == pygame.MOUSEMOTION:
				mc = pygame.mouse.get_pos()
				#print(str(mc[0]) + " " + str(mc[1]))
		
			if event.type == pygame.KEYDOWN:				
				if event.key == pygame.K_r:
					if there_is_winner:
						grid = Grid()
						player1 = Player(1)
						player2 = Player(2)
						bosspl = Boss(2)
						playermc = Player(1)
						there_is_winner = 0
						WINNER = -1
						start_game = True
						first_move = 0

				if event.key == pygame.K_b:
					if not first_move:
						boss = True
				if event.key == pygame.K_u:
					if not first_move:
						boss = False
						
		#print(str(boss) + ' '+ str(first_move))
		
		screen.blit(background.get(), (0, 0))

		winner = WINNER
		if there_is_winner == 0:
			winner = grid.analyze_grid()
			if winner == 1:
				scorep1 +=1
			elif winner == 2:
				scorep2 += 1
		if winner != -1 or there_is_winner:
			WINNER = winner
			display_win(winner)
			there_is_winner = 1
			first_move = 0

			
				
		if alt and not grid.get_full() and not there_is_winner :

			if not start_game:
				montecarlo = MonteCarlo()
				ind = montecarlo.Simulate(grid, 500, 1)

				grid.set_case_occupied(ind, 1)
				#print("move " + str(ind) + " score " + str(score))
				playermc.cross.append(ind)
				alt = not alt
				first_move = 1

			else:

				ind = random.randint(0, 8)
				grid.set_case_occupied(ind, 1)
				#print("move " + str(ind) + " score " + str(score))
				playermc.cross.append(ind)
				alt = not alt
				first_move = 1


		if not alt and not grid.get_full() and not there_is_winner :

			#if not start_game:
			score = -float("inf")
			ind = 0
			for j in range(9):
				#print(j)
				if grid.get_case_occupied(j) == 0:
					copy_grid = []
					grid.get_copy(copy_grid)
					new_grid = Grid()
					new_grid.set_case(copy_grid)
					new_grid.set_case_occupied(j, bosspl.type)
					s = bosspl.compute_game(new_grid, 16, -float('inf'), float('inf'), 0)
					if s > score:
						score = s
						ind = j
			grid.set_case_occupied(ind, 2)
			#print("move " + str(ind) + " score " + str(score))
			bosspl.circle.append(ind)
			alt = not alt
			first_move = 1
			"""else:

				ind = random.randint(0, 8)
				grid.set_case_occupied(ind, 2)
				#print("move " + str(ind) + " score " + str(score))
				bosspl.circle.append(ind)
				alt = not alt
				first_move = 1"""

		for i in range(len(playermc.cross)):
			num = playermc.cross[i]
			screen.blit(cross[num].get(), (cross[num].x, cross[num].y))

		for i in range(len(bosspl.circle)):
			num = bosspl.circle[i]
			screen.blit(circle[num].get(), (circle[num].x, circle[num].y))

		
							
		start_game  =False

		display_score(scorep1, scorep2)
		display_who_play(alt)

		pygame.display.flip()

		
	pygame.quit()
	quit()


gameloop()