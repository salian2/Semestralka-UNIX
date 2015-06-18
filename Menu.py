__author__ = 'salian'

from pygame import Rect, draw, display, mouse, event, QUIT, MOUSEBUTTONUP, time, quit, font,image
import Color
import sys
import pygame


class Menu:

    # Konstuktor inicializuje premenne.
    def __init__(self, pygameWindow,gameVariable,images):

        # bool hodnoty
        self.notOver = True
        self.startGame = False
        self.closeGame = False
        self.loadGame = False

        self.gameVariable = gameVariable

        # okno
        self.window = pygameWindow
        self.images = images

        #velkosti

        self.rectWidth = pygameWindow.get_width() / 3
        self.rectHeight = pygameWindow.get_height()  / 10

        self.rectX = (pygameWindow.get_width() / 2) - (self.rectWidth / 2)


        # Rect(top,left, width, height)
        self.nazovHryRect = Rect(0,0,self.window.get_width(),pygameWindow.get_height()/3)
        self.newGameRect = Rect(self.rectX, 150, self.rectWidth, self.rectHeight)
        self.loadGameRect = Rect(self.rectX, 250, self.rectWidth, self.rectHeight)
        self.exitRect = Rect(self.rectX, 350, self.rectWidth, self.rectHeight)

        # font a texty
        font.init()
        self.font = font.SysFont("norasi",int(self.rectHeight/2))

        #iniclializacia lablov
        self._initLabel()

    # Metoda zobrazi menu a spusti loop.
    def showMenu(self):

        self.clock = time.Clock()
        self.FPS = 30

        # DORIESIT SPUSTENIE
        while self.notOver:
            self.window.fill(Color.white)

            draw.rect(self.window, Color.blue, self.newGameRect)
            draw.rect(self.window,Color.green,self.loadGameRect)
            draw.rect(self.window, Color.red, self.exitRect)

            self._checkClick()
            self._showLabel()
            display.update()

            self.clock.tick(self.FPS)

    #overi klik
    def _checkClick(self):

        for actualEvent in event.get():
            if actualEvent.type == QUIT:
                quit()
                sys.exit()
            # overenie kliknutia, ak klikol overim, ci klikol na tlacidlo
            if actualEvent.type == MOUSEBUTTONUP:
                position = mouse.get_pos()
                self._checkIfInButton(position)


    def _checkIfInButton(self, position):

        # overenie new game tlacidla
        if self.newGameRect.collidepoint(position):
            self.gameVariable.newGame()
            self.notOver = False

        #load game tlacidlo
        elif self.loadGameRect.collidepoint(position):
            self.gameVariable.loadGame()
            self.notOver = False

        #exit game tlacidlo
        elif self.exitRect.collidepoint(position):
            quit()
            sys.exit()

    # inicializuje texty pre buttoni
    def _initLabel(self):

        textStart = "New Game"
        textExit = "Exit"
        gameName = "Unix-Semestralka HRA"
        textLoad = "Load Game"
        win = "Gratulujem, PREZIL SI!!"
        lose = "PREHRAL SI!"

        labelNewGame = self.font.render(textStart,1,Color.black)
        labelLoadGame = self.font.render(textLoad,1,Color.black)
        labelExit = self.font.render(textExit,1,Color.black)



        novyFont = font.SysFont("arial",50)
        labelHra = novyFont.render(gameName,1,Color.red)

        self.labelWin = novyFont.render(win,1,Color.red)
        self.labelLose = novyFont.render(lose,1,Color.red)

        self.buttons = [(self.newGameRect,labelNewGame),
                        (self.loadGameRect,labelLoadGame),
                        (self.exitRect,labelExit),
                        (self.nazovHryRect,labelHra)]



    def _showLabel(self):

        for button,label in self.buttons:
            x = (button.width - label.get_width())/2
            y = (button.height - label.get_height())/2

            self.window.blit(label,(button.x + x,button.y + y))



    def showWin(self):

        x = (self.window.get_width() - self.labelWin.get_width()) / 2
        y = (self.window.get_height() - self.labelWin.get_height()) / 2

        while True:
            self.window.fill(Color.white)
            for actualEvent in event.get():
                if actualEvent.type == QUIT:
                    quit()
                    sys.exit()
            self.window.blit(self.labelWin,(x,y))
            display.update()


    def showLose(self):
        x = (self.window.get_width() - self.labelLose.get_width()) / 2
        y = (self.window.get_height() - self.labelLose.get_height()) / 2

        while True:
            self.window.fill(Color.white)
            for actualEvent in event.get():
                if actualEvent.type == QUIT:
                    quit()
                    sys.exit()
            self.window.blit(self.labelLose,(x,y))
            display.update()

    def showTutorial(self):

        notEnd = True
        while notEnd:
            self.window.blit(self.images.tutorial,(0,0))
            for actualEvent in event.get():
                if actualEvent.type == QUIT:
                    quit()
                    sys.exit()
                elif actualEvent.type == pygame.KEYDOWN:          # check for key presses
                    if actualEvent.key == pygame.K_KP_ENTER or actualEvent.key == pygame.K_SPACE:
                        print("enter")
                        notEnd = False

            display.update()