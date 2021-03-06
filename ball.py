import direct.directbase.DirectStart
from panda3d.core import NodePath
from direct.gui.DirectGui import *
import sys

class Ball:
    def __init__(self, parent, pos, scale, texture):
        self.model = loader.loadModel("models/ball")
        self.model.reparentTo(parent)
        self.model.setScale(scale)
        self.model.setPos(pos)
        self.model_tex = loader.loadTexture(texture)
        self.model.setTexture(self.model_tex, 1)

    def rotate(self, target):
        if self.model.getPos(target).length() < 50:
            self.model.setH(self.model.getH() + 90 * globalClock.getDt())

    def position(self):
        return self.model.getPos()