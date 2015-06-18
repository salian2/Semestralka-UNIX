__author__ = 'salian'

import sys

import pygame
from Menu import Menu
import Spell
import GameSprite
import Collision
import Spawner
import time
import Images
import GameVariable

#inicliazujem moduly
pygame.init()
pygame.font.init()


#images
images = Images.GameImage()

# game variable
gameVariable =  GameVariable.GameVariable()
hero = GameSprite.Hero(250,250,images)


#hracie okno
displayWidth = images.background.get_rect().width
displayHeight = images.background.get_rect().height
spellBook = Spell.SpellBook(0,displayHeight,displayWidth,displayHeight // 5,len(hero.cooldown),images,hero)
gameDisplay = pygame.display.set_mode((displayWidth,displayHeight+spellBook.height),0,32)

#menu
menu = Menu(gameDisplay,gameVariable,images)
menu.showTutorial()
menu.showMenu()

hero.x = gameVariable.x
hero.y = gameVariable.y
hero.hp = gameVariable.hp
hero.level = gameVariable.level

#font
font = pygame.font.SysFont("Arial",30)
text = font.render('Hello WORLD',True,(150,150,150))


kolizia = Collision.CollisionDetect(hero,displayWidth,displayHeight)

delayPohyb = 0

clock = pygame.time.Clock()
FPS = 30

pressed_right = False
pressed_left = False
pressed_up = False
pressed_down = False

npcSpawner = Spawner.Spawner(hero,images,displayHeight,displayWidth)

spellGroup = pygame.sprite.Group()

northBound = GameSprite.Bound(0,0,displayWidth,1,"up")
southBound = GameSprite.Bound(0,displayHeight,displayWidth,1,"down")
westBound = GameSprite.Bound(displayWidth,0,1,displayHeight,"right")
eastBound = GameSprite.Bound(0,0,1,displayHeight,"left")

boundGroup = pygame.sprite.Group()
boundGroup.add(northBound,southBound,westBound,eastBound)

npcGroup = pygame.sprite.Group()

currentSpell = "shot"

now = time.time()
endTime = time.time() + gameVariable.endTime

while True:
    gameDisplay.blit(images.background,(0,0))

    if time.time() > endTime:
        menu.showWin()

    if not hero.isAlive:
        menu.showLose()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            vars = {"level":hero.level,"hp":hero.hp,"x":hero.x,"y":hero.y,"speed":hero.speed,"time":deltaTime}
            gameVariable.saveGame(vars)
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:          # check for key presses
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                pressed_left = True
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                pressed_right = True
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                pressed_up = True
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                pressed_down = True
            if event.key == pygame.K_v or event.key == pygame.K_u :
                currentSpell = "shot"
            elif event.key == pygame.K_b or event.key == pygame.K_i:
                currentSpell = "shield"
            elif event.key == pygame.K_n or event.key == pygame.K_o:
                currentSpell = "teleport"
            elif event.key == pygame.K_m or event.key == pygame.K_p:
                currentSpell = "frostNova"
            if event.key == pygame.K_SPACE:
                spella = hero.castSpell(currentSpell)
                if spella is not None:
                    spellGroup.add(spella)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                pressed_left = False
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                pressed_right = False
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                pressed_up = False
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                pressed_down = False

    if delayPohyb > 3:
        delayPohyb = 0
        if pressed_right and hero.canRight:
            hero.moveHero("right")
        elif pressed_left and hero.canLeft:
            hero.moveHero("left")
        elif pressed_down and hero.canDown:
            hero.moveHero("down")
        elif pressed_up and hero.canUp:
            hero.moveHero("up")
        npcGroup.update()

    if npcSpawner.canSpawn:
        npcGroup.add(npcSpawner.spawnNpc())

    kolizia.detectCollisionSpellNpc(spellGroup,npcGroup)
    kolizia.detectCollision(npcGroup)
    kolizia.detectCollisionSpellBound(spellGroup, boundGroup)
    kolizia.spellEffect(spellGroup,npcGroup)

    #kolizia hero s hranicami
    kolizia.detectHeroCollisionBound()


    #UPDATY
    npcSpawner.update()
    hero.update()
    spellGroup.update()
    spellBook.update()

    #DRAW
    spellGroup.draw(gameDisplay)
    for npc in npcGroup:
            gameDisplay.blit(npc.image,(npc.x,npc.y),npc.imagePosition)
    gameDisplay.blit(hero.image,(hero.x,hero.y),hero.imagePosition)
    spellBook.draw(gameDisplay)

    deltaTime = int(endTime - time.time())
    pygame.display.set_caption('Hero level:'+str(hero.level)+' , hero hp:'+str(hero.hp) + " time to win:"+str(deltaTime))
    delayPohyb += 1

    pygame.display.update()
    clock.tick(FPS)



