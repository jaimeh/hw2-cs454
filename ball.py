import direct.directbase.DirectStart
from panda3d.core import NodePath
from direct.gui.DirectGui import *
import sys

class Ball:
    def __init__(self, parent, pos, scale):
        self.model = loader.loadModel("models/ball")
        self.model.reparentTo(parent)
        self.model.setScale(scale)
        self.model.setPos(pos)