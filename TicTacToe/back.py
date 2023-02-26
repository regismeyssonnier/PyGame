import sys
import pygame

class BackGrid:

    def __init__(self):
        self.background = pygame.image.load("back.png").convert_alpha()
        

    def get(self):
        return self.background