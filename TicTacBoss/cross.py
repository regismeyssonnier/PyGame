import sys
import pygame

class Cross:

    def __init__(self, x, y):
        self.cross = pygame.image.load("cross.png").convert_alpha()
        self.x = x
        self.y = y

    def get(self):
        return self.cross