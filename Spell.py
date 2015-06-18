

__author__ = 'salian'

from pygame import sprite,Rect,draw
import Color


#hlavna trieda, ostatne z nej dedia
class Spell(sprite.Sprite):

    def __init__(self,x,y,dmg,image):

        sprite.Sprite.__init__(self)
        self.dmg = dmg
        self.x = x
        self.y = y

        self.image = image
        self.spellWidth = image.get_rect().width
        self.spellHeight = image.get_rect().height
        self.rect = Rect(x,y,self.spellWidth,self.spellHeight)


#Spella ktoru hrdina vystreli a bude letiet pokym niekoho netrafi
class ShotSpell(Spell):

    def __init__(self,x,y,dmg,image,direction,speed):

        Spell.__init__(self,x,y,dmg,image)
        self.speed = speed
        self.direction = direction

        self.deltaX = 0
        self.deltaY = 0
        self._initSpell()


    def update(self):

        self.x += self.deltaX
        self.y += self.deltaY
        self.rect = Rect(self.x,self.y,self.spellWidth,self.spellHeight)


    def _initSpell(self):

        if self.direction == "up":
            self.deltaY = -self.speed
        elif self.direction == "down":
            self.deltaY = self.speed
        elif self.direction == "right":
            self.deltaX = self.speed
        elif self.direction == "left":
            self.deltaX = -self.speed



class AoeSpell(Spell):

    def __init__(self,x,y,dmg,image,delay,school):

        Spell.__init__(self,x,y,dmg,image)
        self.dmg = dmg

        self.delay = delay
        self.count = 0
        self.canRemove = False
        self.school = school

    def update(self):

        if self.count >= self.delay:
            self.canRemove = True
        else:
            self.count += 1

class TeleportSpell(Spell):

    def __init__(self,x,y,dmg,distance,image,delay,direction):

        Spell.__init__(self,x,y,dmg,image)
        #delay po akom case sa spusti kuzlo, pocitadlo pocita tiky
        self.delay = delay
        self.count = 0
        self.distance = distance

        self.direction = direction

        self.deltaX = 0
        self.deltaY = 0
        self.isTeleported = False
        self._initDeltaPosition()


    def update(self):

        if self.count >= self.delay:
            width = self.image.get_rect().width
            height = self.image.get_rect().height
            self.isTeleported = True
            self.rect = Rect(self.x + self.deltaX,self.y + self.deltaY,width,height)
            self.count = 0
        else:
            self.count += 1


    def _initDeltaPosition(self):

        if self.direction == "up":
            self.deltaY = -self.distance
        elif self.direction == "down":
            self.deltaY = self.distance
        elif self.direction == "right":
            self.deltaX = self.distance
        elif self.direction == "left":
            self.deltaX = -self.distance

class ShieldSpell(Spell):

    def __init__(self,hero,x,y,dmg,time,image):

        Spell.__init__(self,x,y,dmg,image)

        self.hero = hero
        self.canRemove = False
        self.time = time
        self.counter = 0
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height

        self.hero.isImmune = True

    def update(self):
        deltaX = (self.hero.heroWidth - self.width) / 2
        deltaY = (self.hero.heroHeight - self.height) / 2
        self.rect = Rect(self.hero.x + deltaX,self.hero.y + deltaY,self.width,self.height)

        if self.counter >= self.time:
            self.canRemove = True


        else:
            self.counter += 1


class SpellBook():

    def __init__(self,x,y,windowWidth,bookHeight,numberOfSpell,images,hero):

        self.x = x
        self.y = y
        self.width = windowWidth
        self.height = bookHeight

        self.hero = hero
        self.numberOfSpell = numberOfSpell
        self.images = images
        self.spells = []

        self.iconImages = []
        self.iconColor = []

        self.__initArrays()
        self.__initRectSpell()
        self.__getMiddle()

    def update(self):
        boolHodnoty = [self.hero.canShot,self.hero.canShield,self.hero.canTeleport,self.hero.canAoe]

        for i in range(self.numberOfSpell):
            if boolHodnoty[i] and self.iconColor[i] != Color.green:
                self.iconColor[i] = Color.green
            elif not boolHodnoty[i] and self.iconColor[i] != Color.red:
                self.iconColor[i] = Color.red


    def draw(self,gameDisplay):

        index = 0
        for spell in self.spells:
            draw.rect(gameDisplay,self.iconColor[index],spell)
            draw.rect(gameDisplay,Color.black,spell,4)
            gameDisplay.blit(self.iconImages[index],(spell.x+self.deltaX,spell.y+self.deltaY))
            index += 1


    def __initRectSpell(self):

        x = self.x
        y = self.y
        rectWidth = self.width / self.numberOfSpell
        print(str(rectWidth) + '   ' + str(self.height))
        for i in range(self.numberOfSpell):
            rect = Rect(x,y,rectWidth,self.height)
            self.spells.append(rect)
            x += rectWidth


    def __getMiddle(self):

        #vsetky obrazky aj obdlzniky maju rovnake velkosti
        rect = self.spells[0]
        image = self.iconImages[0]
        self.deltaX = (rect.w / 2) - (image.get_width() / 2)
        self.deltaY = (rect.h / 2) - (image.get_height() / 2)


    def __initArrays(self):

        for i in range(self.numberOfSpell):
            if i == 0:
                self.iconColor.append(Color.green)
            else:
                self.iconColor.append(Color.red)

        for j in range(self.numberOfSpell):

            if j==0:
                self.iconImages.append(self.images.iconFireball)
            elif j==1:
                self.iconImages.append(self.images.iconShield)
            elif j==2:
                self.iconImages.append(self.images.iconTeleport)
            elif j==3:
                self.iconImages.append(self.images.iconNova)

