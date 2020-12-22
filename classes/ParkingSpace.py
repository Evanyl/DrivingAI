import pygame
from pygame import Rect

SPACE_WIDTH = 40
SPACE_HEIGHT = 50

class ParkingSpace:
    def __init__(self, x, y):
        self.width = SPACE_WIDTH
        self.height = SPACE_HEIGHT
        self.x = x
        self.y = y
        self.rect = Rect(x, y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect, 3)

    def getXY(self):
        return (self.x + self.width / 2, self.y + self.height * 3 / 4)

    def getWidthHeight(self):
        return (self.width / 2, self.height / 4)