import sys
import time
from queue import Queue
from random import random, randint

import pygame, os

class Player:
    def __init__(self):
        self.length = 1
        self.x = 100
        self.y = 100
        self.size = 20
        self.colour = (0, 150, 0)
        self.headcolour = (0, 255, 0)
        self.speed = 20
        self.lastMoves = []

    def draw(self):
        global screen
        global occupied
        global over
        if self.length == 0:
            return;
        if not over:
            self.lastMoves.append((self.x, self.y))
            occupied.append((self.x, self.y))
            while len(self.lastMoves) > self.length:
                occupied.remove(self.lastMoves[0])
                del self.lastMoves[0]
        for i in self.lastMoves:
            pygame.draw.rect(screen, self.colour, (i[0], i[1], self.size, self.size))
        pygame.draw.rect(screen, self.headcolour, (self.x, self.y, self.size, self.size))
        pygame.draw.rect(screen, (255, 0, 0), (foodPos[0], foodPos[1], self.size, self.size))

    def check(self):
        global foodPos
        global over
        if self.x == foodPos[0] and self.y == foodPos[1]:
            self.length += 1
            pygame.mixer_music.play()
            while True:
                foodPos = (randint(0, width / self.size - 1) * self.size, randint(0, height / self.size - 1) * self.size)
                yes = False
                for i in self.lastMoves:
                    if foodPos[0] == i[0] and foodPos[1] == i[1]:
                        yes = True
                        break
                if not yes:
                    break
        if self.x < 0 or self.x >= width or self.y < 0 or self.y >= height or self.length == 0:
            return True
        if (self.x, self.y) in occupied:
            occupied.remove((self.x, self.y))
        for i in occupied:
            if (self.x, self.y) in occupied:
                return True
        occupied.append((self.x, self.y))
        return False

    def comp(self):
        global foodPos
        global compDir
        self.xDis = self.x - foodPos[0]
        self.yDis = self.y - foodPos[1]
        if abs(self.xDis) > abs(self.yDis):
            if self.xDis > 0:
                if (self.x-self.speed, self.y) not in occupied:
                    return 1
                else:
                    return 2 if (self.x, self.y-self.speed) not in occupied and self.y-self.speed >= 0 else 4 if (self.x, self.y+self.speed) not in occupied and self.y+self.speed+self.speed <= height else 3
            elif self.xDis < 0:
                if (self.x+self.speed, self.y) not in occupied:
                    return 3
                else:
                    return 2 if (self.x, self.y-self.speed) not in occupied and self.y-self.speed >= 0 else 4 if (self.x, self.y+self.speed) not in occupied and self.y+self.speed+self.speed <= height else 1
        else:
            if self.yDis > 0:
                if (self.x, self.y-self.speed) not in occupied:
                    return 2
                else:
                    return 1 if (self.x-self.speed, self.y) not in occupied and self.x-self.speed >= 0 else 3 if (self.x+self.speed, self.y) not in occupied and self.x+self.speed+self.speed <= width else 4
            elif self.yDis < 0:
                if (self.x, self.y+self.speed) not in occupied:
                    return 4
                else:
                    return 1 if (self.x-self.speed, self.y) not in occupied and self.x-self.speed >= 0 else 3 if (self.x+self.speed, self.y) not in occupied and self.x+self.speed+self.speed <= width else 2

pygame.mixer.init()
pygame.mixer_music.load("pop.mp3")
pygame.init()
myFont = pygame.font.SysFont("Microsoft Yahei UI Light", 40)
myyFont = pygame.font.SysFont("Microsoft Yahei UI Light", 30)
os.environ['SDL_VIDEO_CENTERED'] = '1'
width = 640
height = 640
over = False
win = False
start = False
keyQueue = []
dir = 4
dirdir = 0
compDir = -3
occupied = []
screen = pygame.display.set_mode((width + 300, height))
p = Player()
c = Player()
mouseOver = False
c.colour = (100, 100, 100)
c.headcolour = (200, 200, 200)
c.x = width - 100
mousePos = None
screen.fill((0, 0, 0))
pygame.draw.rect(screen, (200, 200, 200), (width, 0, 300, height))
foodPos = (-20, -20)
startTime = 0
while True:
    screen.fill((0, 0, 0))
    mousePos = pygame.mouse.get_pos()
    if time.time() - startTime > 5 and start and not over:
        startTime = time.time()
        c.length -= 1
    pygame.draw.rect(screen, (200, 200, 200), (width, 0, 300, height))
    if start and not over:
        timeLabel = myyFont.render("CPU shortens in: " + "{0:.3f}".format(5 - time.time() + startTime), 1, (255, 255, 255))
        screen.blit(timeLabel, (width+30, 400))
    if mousePos[0] >= width + 50 and mousePos[0] < width + 250 and mousePos[1] >= 200 and mousePos[1] <= 200 + 100:
        pygame.draw.rect(screen, (170, 170, 170), (width + 50, 200, 200, 100))
        mouseOver = True
    else:
        pygame.draw.rect(screen, (120, 120, 120), (width + 50, 200, 200, 100))
        mouseOver = False
    if not start:
        label1 = myFont.render("Start", 1, (255, 255, 255))
    else:
        label1 = myFont.render("Reset", 1, (255, 255, 255))
    screen.blit(label1, (width + 60, 210, 200, 100))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and mouseOver:
            startTime = time.time()
            start = True
            over = False
            p.lastMoves.clear()
            c.lastMoves.clear()
            p = Player()
            c = Player()
            c.colour = (100, 100, 100)
            c.headcolour = (200, 200, 200)
            c.colour = (100, 100, 100)
            c.x = width - 100
            keyQueue.clear()
            occupied.clear()
            dir = 4
            while True:
                foodPos = (randint(0, width / p.size - 1) * p.size, randint(0, height / p.size - 1) * p.size)
                yes = False
                for i in occupied:
                    if foodPos[0] == i[0] and foodPos[1] == i[1]:
                        yes = True
                        break
                if not yes:
                    break
        if not start:
            continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                keyQueue.insert(0, 1)
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                keyQueue.insert(0, 2)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                keyQueue.insert(0, 3)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                keyQueue.insert(0, 4)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                dir = keyQueue.pop(keyQueue.index(1))
            elif event.key == pygame.K_UP:
                dir = keyQueue.pop(keyQueue.index(2))
            elif event.key == pygame.K_RIGHT:
                dir = keyQueue.pop(keyQueue.index(3))
            elif event.key == pygame.K_DOWN:
                dir = keyQueue.pop(keyQueue.index(4))
    if over:
        if win:
            label = myFont.render("You Win", 1, (255, 255, 255))
            screen.blit(label, (int((width - myFont.size("You Win")[0]) / 2), int((height - myFont.size("You Win")[1]) / 2)))
        else:
            label = myFont.render("You Lose", 1, (255, 255, 255))
            screen.blit(label, (int((width - myFont.size("You Lose")[0]) / 2), int((height - myFont.size("You Lose")[1]) / 2)))
    elif start:
        if len(keyQueue) > 0 and (p.length == 1 or abs(keyQueue[0] - dirdir) != 2):
            dirdir = keyQueue[0]
        elif p.length == 1 or abs(dir - dirdir) != 2:
            dirdir = dir
        if dirdir == 1:
            p.x -= p.speed
        elif dirdir == 2:
            p.y -= p.speed
        elif dirdir == 3:
            p.x += p.speed
        elif dirdir == 4:
            p.y += p.speed
        compDir = c.comp()
        if compDir == 1:
            c.x -= c.speed
        elif compDir == 2:
            c.y -= c.speed
        elif compDir == 3:
            c.x += c.speed
        elif compDir == 4:
            c.y += c.speed
    c.draw()
    if c.check() and not over:
        win = True
        over = True
    p.draw()
    if p.check() and not over:
        over = True
        win = False
    pygame.display.update()
    pygame.time.Clock().tick(15)


