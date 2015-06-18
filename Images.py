__author__ = 'salian'

from pygame import image


class GameImage():


    def __init__(self):

        self.npc = []

        self._initSpellImage()
        self._initBackgroundImage()
        self._initHeroImage()
        self._initNpcImage()
        self._initIconImage()

    def _initSpellImage(self):

        self.fireball = image.load("Res/fireball.png")
        self.teleport = image.load("Res/teleport.png")
        self.frostNova = image.load("Res/frostnova.png")
        self.fireNova = image.load("Res/firenova.jpg")
        self.shield = image.load("Res/shield.png")


    def _initBackgroundImage(self):

        self.background = image.load("Res/game_background.png")
        self.tutorial = image.load("Res/tutorial.png")

    def _initHeroImage(self):

        self.hero = image.load('Res/death_scythe.png')

    def _initNpcImage(self):

        leviathan = image.load("Res/leviathan.png")
        bahamut = image.load("Res/bahamut.png")
        ifrit = image.load("Res/ifrit.png")
        self.npc.append(leviathan)
        self.npc.append(bahamut)
        self.npc.append(ifrit)

    def _initIconImage(self):

        self.iconFireball = image.load("Res/iconFireball.png")
        self.iconShield = image.load("Res/iconShield.png")
        self.iconNova = image.load("Res/iconNova.png")
        self.iconTeleport = image.load("Res/iconTeleport.png")
