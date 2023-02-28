from Player import *
from grid import *
import random

class Boss(Player):

    def __init__(self, type):
        Player.__init__(self,type)

        

    def compute_game(self, grid, depth, alpha, beta, minmax):
        #grid.display()

        winner = grid.analyze_grid()
  
           
        if winner == 2:
            return 100
        elif winner == 1:
            return -100
        elif winner == 3:
            return  0
                        

        score = 0
        ind = 0
        if minmax:
            score = -float('inf')
            indice = []
            grid.get_possible_move(indice)
            for i in indice:
               
                copy_grid = []
                grid.get_copy(copy_grid)
                new_grid = Grid()
                new_grid.set_case(copy_grid)
                new_grid.set_case_occupied(i, 2)

                
                s  = self.compute_game(new_grid, depth-1, alpha, beta, not minmax)
                if score < s:
                    score = s

                if score >= beta:
                    return score
                alpha = max(alpha, score)

            return score

        else:
            score = float('inf')
            indice = []
            grid.get_possible_move(indice)
            for i in indice:
             
                copy_grid = []
                grid.get_copy(copy_grid)
                new_grid = Grid()
                new_grid.set_case(copy_grid)
                new_grid.set_case_occupied(i, 1)

                
                s= self.compute_game(new_grid, depth-1, alpha, beta, not minmax)
                if score > s:
                    score = s
                      
                if score <= alpha:
                    return score
                beta = min(beta, score)

            return score

      
        return score