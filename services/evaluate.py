import pygame
import neat
from classes.Car import Car
from classes.Wall import Wall
from classes.ParkingSpace import ParkingSpace
import random
pygame.font.init()

STAT_FONT = pygame.font.SysFont("comicsans", 50)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def evaluate(genomes, config):
    cars = []
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    collidables = [Wall(0, 0, 10, 600), Wall(790, 0, 10, 600), Wall(0, 0, 800, 10), Wall(0,590, 800, 10)]

    parkingSlot = 0
    while (parkingSlot % 2 == 0):
        parkingSlot = random.randrange(0, 19)

    collidables.append(Wall(10, 540, 40 * (parkingSlot), 50))
    parkingSpot = ParkingSpace(10 + parkingSlot * 40, 540)
    collidables.append(parkingSpot)
    collidables.append(Wall(10 + (parkingSlot + 1) * 40, 540, 790 - 40 * (parkingSlot), 50))

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        g.fitness = 0
        cars.append(Car(random.randrange(50,750), random.randrange(50,300), parkingSpot, net, g))

    time = 0
    while True:
        #clock.tick(60)
        time += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        toPop = []
        for x, car in enumerate(cars):
            (carX,carY) = car.getCarXY()
            abs = car.getAbsDistances()
            output = cars[x].getNet().activate((carX, carY, car.orientation,
                                       parkingSpot.x, parkingSpot.y))

            if output[0] > 0.5:
                car.accelerate()
            if output[1] > 0.5:
                car.decelerate()
            if output[2] > 0.5:
                car.ccwTurn()
            if output[3] > 0.5:
                car.cwTurn()

            if update(screen, x, car, collidables):
                toPop.append(x)

        for i in toPop:
            cars.pop(i)
        if len(cars) == 0 or time > 5 * 60:
            break

        draw(screen, cars, collidables)

def update(screen, x, car, collidables):
    return car.update(collidables)

def draw(screen, cars, collidables):
    screen.fill((255,255,255))
    for car in cars:
        car.draw(screen)

    for collidable in collidables:
        collidable.draw(screen)

    pygame.display.update()
