from direct.actor.Actor import Actor
from panda3d.core import NodePath

class Ralph:
    def __init__(self, parent, pos):
        self.actor = Actor("models/ralph",
                                 {"run":"models/ralph-run",
                                  "walk":"models/ralph-walk"})
        self.actor.reparentTo(parent)
        self.actor.setScale(.2)
        self.actor.setPos(pos)

    def position(self):
        return self.actor.getPos()
