from grid import *
import random
import math

class Node:
    def __init__(self):
        self.child = []
        self.parent = None
        self.w = 0
        self.n = 0
        self.ucb = 0
        self.num = 0
        self.grid = Grid()
        self.score = 0

class MonteCarlo:

    def __init__(self):
        self.root = Node()
        

    def Simulation(self, node, plr):
        pl = plr
        score = 0
        ngame = 0
                
        copy_grid = []
        node.grid.get_copy(copy_grid)
        new_grid = Grid()
        new_grid.set_case(copy_grid)
        while 1:
            indice = []
            new_grid.get_possible_move(indice)
            if len(indice) > 0:
                num = random.randint(0, len(indice)-1)
                if pl == 2:
                    new_grid.set_case_occupied(indice[num], 2)
                    pl = 1
                else:
                    new_grid.set_case_occupied(indice[num], 1)
                    pl = 2

            winner = new_grid.analyze_grid()
            if winner == plr:
                
                return 100
                break
            if winner != plr and winner != -1:
                if winner == 3:
                    return 0
                else:
                    return -100
                break
    
    def Simulate(self, grid, depth, plr):
        tnode = []
        self.root.n = 1
        for d in range(depth):
            self.root.grid.case = []
            grid.get_copy(self.root.grid.case)

            node = self.root

            D = 0
            alt  =True
            while len(node.child) >0:
                maxucb = -float('inf')
                ind = 0
                tchild = []
                for i in range(len(node.child)):
                    
                    if node.child[i].n ==0:
                        node.child[i].ucb = float('inf')
                    else:
                        node.child[i].ucb = node.child[i].score / node.child[i].n +  math.sqrt(2*(math.log(node.n) / node.child[i].n))
                    tchild.append(node.child[i])
                    #if node.child[i].ucb > maxucb:
                    #    maxucb = node.child[i].ucb
                    #    ind = i
                tchild.sort(key=lambda x:x.ucb, reverse=True)
                n= len(tchild)
                if n > 3:
                    n = 3
                else:
                    n = len(tchild)-1
                node = tchild[0]#random.randint(0, n)]
                alt = not alt


           
            indice = []
            node.grid.get_possible_move(indice)
            if node.grid.analyze_grid() == -1:
                #print(indice)
                rem = len(indice)
                for i in range(rem):
                    n = Node()
                    n.parent = node
                    n.num = indice[i]
                    n.grid.case = []
                    node.grid.get_copy(n.grid.case)
                    pl = plr
                    if alt:
                        pl = 2
                    else:
                        pl = 1
                    n.grid.set_case_occupied(indice[i], pl)
                    node.child.append(n)
                    tnode.append(n)
            

                if rem > 0:

                    for n in node.child:
                        #n = node.child[random.randint(0, len(node.child)-1)]
                        #n.grid.display()

                        #print()

                        pl = plr
                        if alt:
                            pl = 2
                        else:
                            pl = 1

                        for sim in range(100):
                            score = self.Simulation(n, pl)
                
                            w = 50
                            w2= 50
                            if score > 0:
                                if alt:
                                    w = 100
                                    w2= 0
                                else:
                                    w = 0
                                    w2= 100
                            elif score < 0:
                                if alt:
                                    w = 0
                                    w2= 100
                                else:
                                    w = 100
                                    w2= 0
                            #print(str(w) + ' '+ str(w2))
                            child = n
                            alt2 = alt
                            while child is not None:
                                child.n += 1
                                if alt2:
                                    child.score += w
                        
                                else:
                                    child.score += w2
                                                    
                                child = child.parent
                                alt2 = not alt2

        best_child = None
        maxscore = -float('inf')
        for child in self.root.child:
                       #
            print(str(child.score) + "/" + str(child.n) + " " + str(child.ucb))
            #if child.n > 0:
            score = child.score / child.n
            #score = child.score / child.n +  math.sqrt(2*(math.log(child.parent.n) / child.n))
            if score > maxscore:
                maxscore = score
                best_child = child


        print(str(self.root.score) + "/" + str(self.root.n))
        print()

        return best_child.num


