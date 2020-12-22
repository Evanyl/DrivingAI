import pygame
from pygame import Rect

class Wall:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (130, 130, 130), self.rect)

    def getXY(self):
        return (self.x, self.y)

    def getWidthHeight(self):
        return (self.width, self.height)