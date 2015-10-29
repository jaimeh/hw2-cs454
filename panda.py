from direct.actor.Actor import Actor
from panda3d.core import NodePath

class Panda:
    def __init__(self, parent, time, pos):
        self.actor = Actor("models/panda-model",
                           {"walk": "models/panda-walk4"})
        self.actor.reparentTo(parent)
        self.actor.setScale(.002)
        self.actor.setPos(pos)
        self.timer = time
        self.grav = 1
        self.falling = False
        self.moving = False
    
    def follow(self, target, time):
        if 20 < self.actor.getPos(target).length() < 50:
            self.timer = time
            self.actor.lookAt(target)
            self.actor.setH(self.actor.getH() - 180)
            self.actor.setY(self.actor, -10)
        
        if 20 < self.actor.getPos(target).length() < 50:
            if self.moving == False:
                self.moving = True
                self.actor.loop("walk")
        else:
            self.moving = False
            self.actor.stop()
            self.actor.pose("walk", 3)
            self.actor.setZ(0)
            self.actor.setP(0)
            self.actor.setR(0)
        
    def waitedTooLong(self, time):
        if time - self.timer > 20:
            if not self.grav > 0:
                self.falling = True
            if not self.falling:
                self.actor.setZ(self.actor.getZ() + self.grav)
                self.grav = self.grav - .05
            else:
                self.actor.setZ(self.actor.getZ() - self.grav)
                self.grav = self.grav + .05
                if not self.actor.getZ() > 0:
                    self.actor.setZ(0)
                    self.actor.setR(0)
                    self.actor.setP(0)
                    self.falling = False
                    self.timer = time
                    self.grav = 1

    def position(self):
        return self.actor.getPos()
                    