__author__ = 'salian'

import pickle

class GameVariable:

    def loadGame(self):

        try:
            with open("myGame.dat","rb") as file:
                vars = pickle.load(file)

            self.level = vars["level"]
            self.hp = vars["hp"]
            self.endTime = vars["time"]
            self.x = vars["x"]
            self.y = vars["y"]
            self.speed = vars["speed"]
        except FileNotFoundError:
            self.newGame()

    def saveGame(self,vars):
        with open("myGame.dat", "wb") as file:
            pickle.dump(vars, file)

    def newGame(self):
        self.level = 1
        self.hp = 100
        self.endTime = 600
        self.x = 250
        self.y = 250
        self.speed = 2