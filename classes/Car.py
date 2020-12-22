import pygame
from classes.ImageHandler import *
from classes.ParkingSpace import ParkingSpace
import random
import math


class Car:
    def __init__(self, x, y, parkingSpot, net, g):
        self.img = pygame.image.load(getCarImgDir()).convert_alpha()
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = x
        self.y = y
        self.velocity = 0
        self.terminalVelocity = 8
        self.accel = 0.2
        self.friction = 0.05
        self.wheelAngle = 1
        self.offsetOrientation = 90
        self.orientation = random.randrange(0, 360)
        self.projections = [(0,0), (0,0)]
        self.raycastLength = 50
        self.net = net
        self.g = g
        self.parkingSpot = parkingSpot
        self.remainingX = self.getRemainingX()
        self.recordX = self.remainingX
        self.initialX = self.remainingX
        self.remainingY = self.getRemainingY()
        self.recordY = self.remainingY
        self.initialY = self.remainingY


    def getNet(self):
        return self.net

    def accelerate(self):
        self.velocity += self.accel
        if self.velocity > self.terminalVelocity:
            self.velocity = self.terminalVelocity

    def decelerate(self):
        self.velocity -= self.accel
        if self.velocity < -self.terminalVelocity:
            self.velocity = -self.terminalVelocity

    def cwTurn(self):
        self.turnAngle = self.wheelAngle * math.fabs(self.velocity)

        if self.velocity > 0:
            self.orientation -= self.turnAngle
        else:
            self.orientation += self.turnAngle

    def ccwTurn(self):
        self.turnAngle = self.wheelAngle * math.fabs(self.velocity)

        if self.velocity > 0:
            self.orientation += self.turnAngle
        else:
            self.orientation -= self.turnAngle

    def getVectors(self, angle):
        xVector = math.cos(math.radians(angle))
        yVector = math.sin(math.radians(angle))

        return (xVector, yVector)

    def getRemainingX(self):
        return math.fabs(self.parkingSpot.x - self.x)

    def getRemainingY(self):
        return math.fabs(self.parkingSpot.y - self.y)

    def update(self, collidables):
        (xVector, yVector) = self.getVectors(self.orientation)

        if self.notMoving():
            self.g.fitness -= 0.1

        self.x += self.velocity * xVector
        self.y -= self.velocity * yVector
        self.velocity -= self.friction * self.velocity

        self.remainingX = self.getRemainingX()
        self.remainingY = self.getRemainingY()

        xDiff = self.remainingX - self.recordX
        yDiff = self.remainingY - self.recordY

        if self.remainingX < 50:
            self.g.fitness += 0.5
        if self.remainingX < 100:
            self.g.fitness += 0.2
        if self.remainingX < 200:
            self.g.fitness += 0.1
        if self.remainingY < 50:
            self.g.fitness += 0.5
        if self.remainingY < 100:
            self.g.fitness += 0.2
        if self.remainingY < 150:
            self.g.fitness += 0.1

        if xDiff < 0:
            self.g.fitness += 0.1
            self.recordX = self.remainingX
        else:
            self.g.fitness -= 0.1

        if yDiff < 0:
            self.g.fitness += 0.1
            self.recordY = self.remainingY
        else:
            self.g.fitness -= 0.1

        if self.orientation > 360:
            self.orientation -= 360
        elif self.orientation < 0:
            self.orientation += 360

        #for x in range(len(self.projections)):
        #    self.projections[x] = self.project(collidables, x)

        for collidable in collidables:
            if self.near(collidable):
                if (isinstance(collidable, ParkingSpace)):
                    if self.collide(collidable):
                        if self.notMoving():
                            self.g.fitness += 1000
                            return True
                else:
                    if self.collide(collidable):
                        self.x -= 2 * self.velocity * xVector
                        self.y += 2 * self.velocity * yVector
                        self.velocity = - self.velocity * 0.6
                        self.g.fitness -= 1
        return False

    def near(self, collidable):
        if math.fabs(self.x - collidable.x) - collidable.width - self.width < 100 and math.fabs(self.y - collidable.y) - self.height - collidable.height< 100:
            return True
        return False


    def draw(self, screen):
        (rotated_img, new_rect) = self.getRotate(self.getOrientation())
        screen.blit(rotated_img, new_rect.topleft)

        #for projection in self.projections:
        #    pygame.draw.line(screen, (255, 0, 0), self.getCarXY(), projection)

    def getMask(self):
        (rotated_img, _) = self.getRotate(self.getOrientation())
        return pygame.mask.from_surface(rotated_img)

    def getOrientation(self):
        return self.orientation - self.offsetOrientation

    def getRotate(self, angle):
        rotated_img = pygame.transform.rotate(self.img, angle)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        return (rotated_img, new_rect)

    def getXY(self):
        (_, new_rect) = self.getRotate(self.getOrientation())
        return new_rect.topleft

    def getCarXY(self):
        (_, new_rect) = self.getRotate(self.getOrientation())
        (x, y) = new_rect.topleft

        (xVector, yVector) = self.getVectors(self.getOrientation())

        if self.getOrientation() >= -90 and self.getOrientation() < 0:
            x -= -new_rect.width + math.fabs(xVector * self.width)
        elif self.getOrientation() < 90:
            y += self.width * yVector
        elif self.getOrientation() < 180:
            y += new_rect.height
            x += math.fabs(xVector * self.width)
        else:
            x += new_rect.width
            y -= -new_rect.height + math.fabs(yVector * self.width)

        return (x, y)

    def collide(self, collidable):
        carMask = self.getMask()
        (thisX, thisY) = self.getXY()
        collidableMask = pygame.mask.from_surface(pygame.Surface(collidable.getWidthHeight()))
        (thatX, thatY) = collidable.getXY()
        offset = (round(thatX - thisX), round(thatY - thisY))

        if carMask.overlap(collidableMask, offset):
            return True
        else:
            return False

    def notMoving(self):
        if math.fabs(self.velocity) < 0.1:
            return True
        else:
            return False

    def checkPointCollide(self, x, y, collidables):
        for collidable in collidables:
            if self.near(collidable):
                thisMask = pygame.mask.from_surface(pygame.Surface((1,1)))
                collidableMask = pygame.mask.from_surface(pygame.Surface(collidable.getWidthHeight()))
                (thatX, thatY) = collidable.getXY()
                offset = (round(thatX - x), round(thatY - y))

                if thisMask.overlap(collidableMask, offset):
                    return True

        return False

    def project(self, collidables, iteration):
        (x,y) = self.getCarXY()
        (thatX, thatY) = (x, y)
        (xVector, yVector) = self.getVectors(self.orientation + 45 - 90 * iteration)

        for i in range(0, int(self.raycastLength / 10)):
            thatX += 10 * xVector
            thatY -= 10 * yVector
            if self.checkPointCollide(thatX, thatY, collidables):
                break

        return thatX, thatY

    def getAbsDistances(self):
        arr = []
        for i in range(0, 2):
            (x, y) = self.getCarXY()
            arr.append(math.sqrt((self.projections[i][0] - x)**2 + (self.projections[i][1] - y)**2))

        return arr