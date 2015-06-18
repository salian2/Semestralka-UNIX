__author__ = 'salian'

import random
import GameSprite

class Spawner():

    def __init__(self,hero,images,gameHeight,gameWidth):

        self.hero = hero
        self.counter = 0
        self.gameImage = images
        self.image = None

        self.canSpawn = False
        self.width = gameWidth
        self.height = gameHeight

    def update(self):

        spawnTime = 100 + 100 / self.hero.level
        if self.counter >= spawnTime:
            self.counter = 0
            self.canSpawn = True
        else:
            self.counter += 1

    def spawnNpc(self):
        self.canSpawn = False
        dmg = 10 + 2*self.hero.level
        speed = 1 + 0.5*self.hero.level
        image = self._getRandomUnit()
        x,y = self._getRandomPosition(image)
        direction = self._getDirection()
        return GameSprite.Npc(x,y,dmg,image,self.hero,speed,direction)


    def _getDirection(self):
        direction = None
        if self.hero.direction == "up":
            direction = "down"
        elif self.hero.direction == "down":
            direction = "up"
        elif self.hero.direction == "right":
            direction = "left"
        elif self.hero.direction == "left":
            direction = "right"
        return direction


    def _getRandomPosition(self,image):

        imageWidth = image.get_rect().width
        imageHeight = image.get_rect().height

        x = random.randint(0,self.width - imageWidth/4)
        y = random.randint(0,self.height - imageHeight/4)
        return x,y

    def _getRandomUnit(self):

        number = random.randint(1,len(self.gameImage.npc))

        return self.gameImage.npc[number-1]

