__author__ = 'salian'

from pygame import sprite,Rect
from Spell import *

#HERO CLASS
class Hero(sprite.Sprite):

    def __init__(self,x,y,gameImage):

        sprite.Sprite.__init__(self)
        self.gameImage = gameImage
        self.x = x
        self.y = y
        self.image = gameImage.hero
        self.rect = Rect(x,y,self.image.get_rect().width,self.image.get_rect().height)

        self.index = 0
        self.heroWidth = self.image.get_rect().width / 4
        self.heroHeight = self.image.get_rect().height / 4
        self.imagePosition = (0,96,self.heroWidth,self.heroHeight)
        self.direction = "right"

        self.speed = 2

        self.level = 1
        self.hp = 100

        self.canLeft = True
        self.canRight = True
        self.canUp = True
        self.canDown = True

        self.isAlive = True
        self.isImmune = False
        self.npcKilled = 0

        self.shotTimer = 0
        self.aoeTimer = 0
        self.teleportTimer = 0
        self.shieldTimer = 0

        self.canShot = False
        self.canAoe = False
        self.canShield = False
        self.canTeleport = False

        self.cooldown = {}
        self._initCooldown()

    def update(self):
        self.rect = Rect(self.x,self.y,self.heroWidth,self.heroHeight)
        self.aoeTimer +=1
        self.shotTimer += 1
        self.shieldTimer += 1
        self.teleportTimer +=1

        if self.shotTimer > self.cooldown["shot"]:
            self.canShot = True
        if self.aoeTimer > self.cooldown["aoe"]:
            self.canAoe = True
        if self.shieldTimer > self.cooldown["shield"]:
            self.canShield = True
        if self.teleportTimer > self.cooldown["teleport"]:
            self.canTeleport = True

        if self.hp <= 0:
            self.isAlive = False
        needForLevel = self.level * 2
        if self.npcKilled >= needForLevel:
            self.npcKilled = 0
            self._lvlUp()

    def castSpell(self,spellType):
        if spellType == "shot" and self.canShot:
            self.canShot = False
            self.shotTimer = 0
            return self._shotSpell()
        elif spellType == "shield" and self.canShield:
            self.canShield = False
            self.shieldTimer = 0
            return self._shieldSpell()
        elif spellType == "teleport" and self.canTeleport:
            self.canTeleport = False
            self.teleportTimer = 0
            return self._teleportSpell()
        elif spellType == "frostNova" and self.canAoe:
            self.canAoe = False
            self.aoeTimer = 0
            return self._frostSpell()


    def _shotSpell(self):
        dmg = 10 + 5*self.level
        spellSpeed = (10 + self.level) / 10
        x = self.x + abs((self.heroWidth - self.gameImage.fireball.get_rect().width) / 2)
        y = self.y + abs((self.heroHeight - self.gameImage.fireball.get_rect().height) / 2)

        return ShotSpell(x,y,dmg,self.gameImage.fireball,self.direction,spellSpeed)

    def _teleportSpell(self):
        dmg = 10 + 10*self.level
        distance = 100 + 5*self.level
        delay = 5
        x = self.x - abs((self.heroWidth - self.gameImage.teleport.get_rect().width) / 2)
        y = self.y - abs((self.heroHeight - self.gameImage.teleport.get_rect().height) / 2)
        return TeleportSpell(x,y,dmg,distance,self.gameImage.teleport,delay,self.direction)

    def _frostSpell(self):
        x = self.x - abs((self.heroWidth - self.gameImage.frostNova.get_rect().width) / 2)
        y = self.y - abs((self.heroHeight - self.gameImage.frostNova.get_rect().height) / 2)
        return AoeSpell(x,y,self.level,self.gameImage.frostNova,10,"frost")

    def _shieldSpell(self):

        time = self.level*5 + 25
        return ShieldSpell(self,self.x,self.y,0,time,self.gameImage.shield)

    def moveHero(self,direction):

        if direction == "up":
            self.direction = "up"
            self._moveUp()
        elif direction == "right":
            self.direction = "right"
            self._moveRigth()
        elif direction == "left":
            self.direction = "left"
            self._moveLeft()
        elif direction == "down":
            self.direction = "down"
            self._moveDown()

    def canMove(self):
        self.canLeft = True
        self.canRight = True
        self.canUp = True
        self.canDown = True

    def cantMove(self,direction):
        if direction == "up":
            self.canUp = False
        elif direction == "right":
            self.canRight = False
        elif direction == "left":
            self.canLeft = False
        elif direction == "down":
            self.canDown = False

    def _moveRigth(self):
        self.index = (self.index + 1) % 4
        self.imagePosition = (self.index*self.heroWidth,2*self.heroHeight,self.heroWidth,48)
        self.x += self.speed

    def _moveLeft(self):
        self.index = (self.index + 1) % 4
        self.imagePosition = (self.index*self.heroWidth,1*self.heroHeight,self.heroWidth,48)
        self.x += -self.speed

    def _moveUp(self):
        self.index = (self.index + 1) % 4
        self.imagePosition = (self.index*self.heroWidth,3*self.heroHeight,self.heroWidth,48)
        self.y += -self.speed

    def _moveDown(self):
        self.index = (self.index + 1) % 4
        self.imagePosition = (self.index*self.heroWidth,0*self.heroHeight,self.heroWidth,48)
        self.y += self.speed

    def _lvlUp(self):

        self.hp = self.hp + 20 * self.level
        self.speed += 0.5
        if self.cooldown["shot"] > 35:
            self.cooldown["shot"] = self.cooldown["shot"] - self.level*2
        if self.cooldown["teleport"] > 35:
            self.cooldown["teleport"] = self.cooldown["teleport"] - self.level * 3
        if self.cooldown["aoe"] > 50:
            self.cooldown["aoe"] = self.cooldown["aoe"] - self.level * 5
        if self.cooldown["shield"] > 150:
            self.cooldown["shield"] = self.cooldown["shield"] - self.level * 4
        self.level += 1
        print(self.cooldown)
        print(self.speed)

    def _initCooldown(self):

        self.cooldown = {"shot":100,"teleport":125,"aoe":80,"shield":300}

#HRANICA
class Bound(sprite.Sprite):

    def __init__(self,x,y,width,height,direction):
        sprite.Sprite.__init__(self)

        self.rect = Rect(x,y,width,height)
        self.direction = direction


#NPC CLASS
class Npc(sprite.Sprite):


    def __init__(self,x,y,dmg,image,hero,speed,direction):

        sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.dmg = dmg
        self.image = image
        self.rect = Rect(x,y,image.get_rect().width,image.get_rect().height)

        self.index = 0
        self.npcWidth = self.image.get_rect().width / 4
        self.npcHeight = self.image.get_rect().height / 4

        self.direction = direction
        self._initPosition()

        self.speed = speed
        self.hero = hero
        self.deltaX = 0
        self.deltaY = 0

        self.canMove = True
        self.timer = 0
        self.count = 0

    def update(self):
        if self.canMove:
            self._getDeltaMove()
            self._move()
            self.rect = Rect(self.x,self.y,self.npcWidth,self.npcHeight)
        else:
            if self.timer <= self.count:
                self.canMove = True
                self.count = 0
            else:
                self.count += 1


    def stopNpc(self,time):
        self.canMove = False
        self.timer = time

    def _move(self):
        if self.direction == "up":
            self._moveUp()
        elif self.direction == "right":
            self._moveRigth()
        elif self.direction == "left":
            self._moveLeft()
        elif self.direction == "down":
            self._moveDown()

    def _getDeltaMove(self):

        heroX = self.hero.x
        heroY = self.hero.y

        if abs(heroX - self.x) > abs(heroY - self.y):
            self.deltaY = 0
            if heroX - self.x > 0:
                self.direction = "right"
                self.deltaX = self.speed #doprava
            else:
                self.direction = "left"
                self.deltaX = -self.speed #dolava
        else:
            self.deltaX = 0
            if heroY - self.y > 0:
                self.direction = "down"
                self.deltaY = self.speed
            else:
                self.direction = "up"
                self.deltaY = -self.speed



    def _moveRigth(self):
        self.index = (self.index + 1) % 4
        self.imagePosition = (self.index*self.npcWidth,2*self.npcHeight,self.npcWidth,self.npcHeight)
        self.x += self.deltaX

    def _moveLeft(self):
        self.index = (self.index + 1) % 4
        self.imagePosition = (self.index*self.npcWidth,1*self.npcHeight,self.npcWidth,self.npcHeight)
        self.x += self.deltaX

    def _moveUp(self):
        self.index = (self.index + 1) % 4
        self.imagePosition = (self.index*self.npcWidth,3*self.npcHeight,self.npcWidth,self.npcHeight)
        self.y += self.deltaY

    def _moveDown(self):
        self.index = (self.index + 1) % 4
        self.imagePosition = (self.index*self.npcWidth,0*self.npcHeight,self.npcWidth,self.npcHeight)
        self.y += self.deltaY

    def _initPosition(self):

        if self.direction == "up":
            self.imagePosition = (0,3*self.npcHeight,self.npcWidth,self.npcHeight)
        elif self.direction == "down":
            self.imagePosition = (0,0*self.npcHeight,self.npcWidth,self.npcHeight)
        elif self.direction == "right":
            self.imagePosition = (0,2*self.npcHeight,self.npcWidth,self.npcHeight)
        elif self.direction == "left":
            self.imagePosition = (0,1*self.npcHeight,self.npcWidth,self.npcHeight)
        else:
            self.imagePosition = (0,3*self.npcHeight,self.npcWidth,self.npcHeight)