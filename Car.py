from math import asin, acos, pi

class Car:
    def __init__(self, parent, pos):
        self.model = loader.loadModel("models/vehicle")
        self.model.reparentTo(parent)
        self.model.setScale(.5)
        self.model.setPos(10,10,0)
        self.tooClose = 0
        
    def circle(self, target):
        if self.model.getPos(target).length() < 30:
            self.tooClose = pi/(asin(0.5 / self.model.getDistance(target))) + 40
        if self.tooClose > 40:
            self.model.lookAt(target)
            self.model.setH(self.model.getH() - acos(0.5 / self.model.getDistance(target)) * 180 / pi)
            self.model.setY(self.model, - 1)
            self.tooClose = self.tooClose - 1
        elif self.tooClose > 0:
            self.model.setY(self.model, -0.5)
            self.tooClose = self.tooClose - 1