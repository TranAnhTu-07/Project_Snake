# food.py
import pygame
from random import randint
from settings import *

class Food:
    def __init__(self):
        self.position = [0, 0]
        self.randomize()

    def randomize(self):
        self.position = [randint(0, GRID_WIDTH - 1), randint(0, GRID_HEIGHT - 1)]

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.position[0] * BLOCK_SIZE, self.position[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))