import sys
import pygame

class Circle:

    def __init__(self, x, y):
        self.circle = pygame.image.load("circle.png").convert_alpha()
        self.x = x
        self.y = y

    def get(self):
        return self.circle