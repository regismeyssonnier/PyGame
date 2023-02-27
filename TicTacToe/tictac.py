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
	player1 = Player(1)
	player2 = Player(2)
	there_is_winner = 0
	WINNER = -1
	scorep1 = scorep2 = 0
	boss = True
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
					#case 0  154, 53 /288 , 189
					#case 1  322, 53 /484, 189
					#case 2  515, 53 /647, 189
					#case 3  154, 226 /288, 369
					#case 4  322, 226 /484, 369
					#case 5  515, 226 /647, 369
					#case 6  154, 404 /288, 549
					#case 7  322, 404 /484, 549
					#case 8  515, 404 /647, 549
					if not boss:
						if mc[0] >= 154 and mc[0] <= 288 and mc[1] >= 53 and mc[1] <= 189:
							if grid.get_case_occupied(0) == 0:
								if alt:
									grid.set_case_occupied(0, 1)
									player1.cross.append(0)
									first_move = 1
								else:
									grid.set_case_occupied(0, 2)
									player2.circle.append(0)
								alt = not alt
						elif mc[0] >= 322 and mc[0] <= 484 and mc[1] >= 53 and mc[1] <= 189:
							if grid.get_case_occupied(1) == 0:
								if alt:
									grid.set_case_occupied(1, 1)
									player1.cross.append(1)
									first_move = 1
								else:
									grid.set_case_occupied(1, 2)
									player2.circle.append(1)
								alt = not alt
						elif mc[0] >= 515 and mc[0] <= 647 and mc[1] >= 53 and mc[1] <= 189:
							if grid.get_case_occupied(2) == 0:
								if alt:
									grid.set_case_occupied(2, 1)
									player1.cross.append(2)
									first_move = 1
								else:
									grid.set_case_occupied(2, 2)
									player2.circle.append(2)
								alt = not alt
						elif mc[0] >= 154 and mc[0] <= 288 and mc[1] >= 226 and mc[1] <= 369:
							if grid.get_case_occupied(3) == 0:
								if alt:
									grid.set_case_occupied(3, 1)
									player1.cross.append(3)
									first_move = 1
								else:
									grid.set_case_occupied(3, 2)
									player2.circle.append(3)
								alt = not alt
						elif mc[0] >= 322 and mc[0] <= 484 and mc[1] >= 226 and mc[1] <= 369:
							if grid.get_case_occupied(4) == 0:
								if alt:
									grid.set_case_occupied(4, 1)
									player1.cross.append(4)
									first_move = 1
								else:
									grid.set_case_occupied(4, 2)
									player2.circle.append(4)
								alt = not alt
						elif mc[0] >= 515 and mc[0] <= 647 and mc[1] >= 226 and mc[1] <= 369:
							if grid.get_case_occupied(5) == 0:
								if alt:
									grid.set_case_occupied(5, 1)
									player1.cross.append(5)
									first_move = 1
								else:
									grid.set_case_occupied(5, 2)
									player2.circle.append(5)
								alt = not alt
						elif mc[0] >= 154 and mc[0] <= 288 and mc[1] >= 404 and mc[1] <= 549:
							if grid.get_case_occupied(6) == 0:
								if alt:
									grid.set_case_occupied(6, 1)
									player1.cross.append(6)
									first_move = 1
								else:
									grid.set_case_occupied(6, 2)
									player2.circle.append(6)
								alt = not alt
						elif mc[0] >= 322 and mc[0] <= 484 and mc[1] >= 404 and mc[1] <= 549:
							if grid.get_case_occupied(7) == 0:
								if alt:
									grid.set_case_occupied(7, 1)
									player1.cross.append(7)
									first_move = 1
								else:
									grid.set_case_occupied(7, 2)
									player2.circle.append(7)
								alt = not alt
						elif mc[0] >= 515 and mc[0] <= 647 and mc[1] >= 404 and mc[1] <= 549:
							if grid.get_case_occupied(8) == 0:
								if alt:
									grid.set_case_occupied(8, 1)
									player1.cross.append(8)
									first_move = 1
								else:
									grid.set_case_occupied(8, 2)
									player2.circle.append(8)
								alt = not alt
					else:
						if mc[0] >= 154 and mc[0] <= 288 and mc[1] >= 53 and mc[1] <= 189:
							if grid.get_case_occupied(0) == 0:
								if alt:
									grid.set_case_occupied(0, 1)
									player1.cross.append(0)
									first_move = 1
								
								alt = not alt
						elif mc[0] >= 322 and mc[0] <= 484 and mc[1] >= 53 and mc[1] <= 189:
							if grid.get_case_occupied(1) == 0:
								if alt:
									grid.set_case_occupied(1, 1)
									player1.cross.append(1)
									first_move = 1
								
								alt = not alt
						elif mc[0] >= 515 and mc[0] <= 647 and mc[1] >= 53 and mc[1] <= 189:
							if grid.get_case_occupied(2) == 0:
								if alt:
									grid.set_case_occupied(2, 1)
									player1.cross.append(2)
									first_move = 1
								
								alt = not alt
						elif mc[0] >= 154 and mc[0] <= 288 and mc[1] >= 226 and mc[1] <= 369:
							if grid.get_case_occupied(3) == 0:
								if alt:
									grid.set_case_occupied(3, 1)
									player1.cross.append(3)
									first_move = 1
								
								alt = not alt
						elif mc[0] >= 322 and mc[0] <= 484 and mc[1] >= 226 and mc[1] <= 369:
							if grid.get_case_occupied(4) == 0:
								if alt:
									grid.set_case_occupied(4, 1)
									player1.cross.append(4)
									first_move = 1
								
								alt = not alt
						elif mc[0] >= 515 and mc[0] <= 647 and mc[1] >= 226 and mc[1] <= 369:
							if grid.get_case_occupied(5) == 0:
								if alt:
									grid.set_case_occupied(5, 1)
									player1.cross.append(5)
									first_move = 1
								
								alt = not alt
						elif mc[0] >= 154 and mc[0] <= 288 and mc[1] >= 404 and mc[1] <= 549:
							if grid.get_case_occupied(6) == 0:
								if alt:
									grid.set_case_occupied(6, 1)
									player1.cross.append(6)
									first_move = 1
								
								alt = not alt
						elif mc[0] >= 322 and mc[0] <= 484 and mc[1] >= 404 and mc[1] <= 549:
							if grid.get_case_occupied(7) == 0:
								if alt:
									grid.set_case_occupied(7, 1)
									player1.cross.append(7)
									first_move = 1
								
								alt = not alt
						elif mc[0] >= 515 and mc[0] <= 647 and mc[1] >= 404 and mc[1] <= 549:
							if grid.get_case_occupied(8) == 0:
								if alt:
									grid.set_case_occupied(8, 1)
									player1.cross.append(8)
									first_move = 1
								
								alt = not alt


					
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

	
		if player1.type == 1:
			
				for i in range(len(player1.cross)):
					num = player1.cross[i]
					screen.blit(cross[num].get(), (cross[num].x, cross[num].y))
		elif player1.type == 2:	
				for i in range(len(player1.circle)):
					num = player1.circle[i]
					screen.blit(circle[num].get(), (circle[num].x, circle[num].y))
		if not boss:
			if player2.type == 1:
			
					for i in range(len(player2.cross)):
						num = player2.cross[i]
						screen.blit(cross[num].get(), (cross[num].x, cross[num].y))
			elif player2.type == 2:	
					for i in range(len(player2.circle)):
						num = player2.circle[i]
						screen.blit(circle[num].get(), (circle[num].x, circle[num].y))

		else:
		
			if not alt and not grid.get_full() and not there_is_winner :

				if not start_game:
					#print("boss")
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
				else:
					ind = random.randint(0, 8)
					grid.set_case_occupied(ind, 2)
					#print("move " + str(ind) + " score " + str(score))
					bosspl.circle.append(ind)
					alt = not alt
					first_move = 1

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