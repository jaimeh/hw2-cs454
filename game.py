# Roaming-Ralph was modified to remove collision part.

import direct.directbase.DirectStart
from panda3d.core import Filename,AmbientLight,DirectionalLight
from panda3d.core import PandaNode,NodePath,Camera,TextNode
from panda3d.core import Vec3,Vec4,BitMask32
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
import random, sys, os, math
from panda import Panda
from car import Car
from ball import Ball
from ralph import Ralph

SPEED = 0.5

# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1),
                        pos=(-1.3, pos), align=TextNode.ALeft, scale = .05)

# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1,1,1,1),
                        pos=(1.3,-0.95), align=TextNode.ARight, scale = .07)

class World(DirectObject):

    def __init__(self):

        self.keyMap = {"left":0, "right":0, "forward":0, "reverse":0, "cam-left":0, "cam-right":0, "speed-toggle":0}
        base.win.setClearColor(Vec4(0,0,0,1))

        # Post the instructions

        self.inst1 = addInstructions(0.95, "[ESC]: Quit")
        self.inst2 = addInstructions(0.90, "[A]: Rotate Ralph Left")
        self.inst3 = addInstructions(0.85, "[D]: Rotate Ralph Right")
        self.inst4 = addInstructions(0.80, "[W]: Run Ralph Forward")
        self.inst5 = addInstructions(0.75, "[S]: Run Ralph Backwards")
        self.inst6 = addInstructions(0.70, "[Left Arrow]: Rotate Camera Left")
        self.inst7 = addInstructions(0.65, "[Right Arrow]: Rotate Camera Right")
        self.inst8 = addInstructions(0.60, "[Tab]: Slow Down Ralph")

        # Set up the environment

        self.environ = loader.loadModel("models/square")
        self.environ.reparentTo(render)
        self.environ.setPos(0,0,0)
        self.environ.setScale(100,100,1)
        self.moon_tex = loader.loadTexture("models/moon_1k_tex.jpg")
        self.environ.setTexture(self.moon_tex, 1)

        # Create the main character, Ralph

        playerChoice = raw_input('Select character [ralph, panda, car]: ')

        self.player = self.loadCharacter(playerChoice)

        ############ Removed Pandas and Car as they are not needed ###########
        # Creating Pandas

        #self.panda1 = Panda(render, globalClock.getFrameTime(), (30, 20, 0))
        #self.panda2 = Panda(render, globalClock.getFrameTime(), (20, 40, 0))

        # Creating Car

        # self.car = Car(render, (10, 10, 0))

        # Creating Ball

        self.ball1 = Ball(render, (10, 0, 0.35), 0.3, ("models/sun_1k_tex.jpg"))
        self.ball2 = Ball(render, (0, -20, 0.59), 0.6, ("models/mars_1k_tex.jpg"))
        self.ball3 = Ball(render, (-30, 0, 0.95), 1, ("models/venus_1k_tex.jpg"))

        # Create a floater object.  We use the "floater" as a temporary
        # variable in a variety of calculations.

        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)

        # Accept the control keys for movement and rotation

        self.accept("escape", sys.exit)
        self.accept("a", self.setKey, ["left",1])
        self.accept("d", self.setKey, ["right",1])
        self.accept("w", self.setKey, ["forward",1])
        self.accept("s", self.setKey, ["reverse",1])
        self.accept("tab", self.setKey, ["speed-toggle",1])
        self.accept("arrow_left", self.setKey, ["cam-left",1])
        self.accept("arrow_right", self.setKey, ["cam-right",1])
        self.accept("a-up", self.setKey, ["left",0])
        self.accept("d-up", self.setKey, ["right",0])
        self.accept("w-up", self.setKey, ["forward",0])
        self.accept("s-up", self.setKey, ["reverse",0])
        self.accept("tab-up", self.setKey, ["speed-toggle",0])
        self.accept("arrow_left-up", self.setKey, ["cam-left",0])
        self.accept("arrow_right-up", self.setKey, ["cam-right",0])

        taskMgr.add(self.move,"moveTask")

        # Game state variables

        self.isMoving = False
        self.isWalking = False

        # Can ralph move (for collision)
        self.canMove = True;

        # Set up the camera

        base.disableMouse()
        base.camera.setPos(self.player.getX(),self.player.getY()+10,2)

        # Create some lighting

        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(Vec4(.3, .3, .3, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(Vec3(-5, -5, -5))
        directionalLight.setColor(Vec4(1, 1, 1, 1))
        directionalLight.setSpecularColor(Vec4(1, 1, 1, 1))
        render.setLight(render.attachNewNode(ambientLight))
        render.setLight(render.attachNewNode(directionalLight))

    #Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value

    # Character name needs to be: car, ralph or panda
    def loadCharacter(self, name):
        if name == 'ralph':
            return Ralph(render, (30, 30, 0)).actor
        elif name == 'car':
            return Car(render, (10, 10, 0)).model
        elif name == 'panda':
            return Panda(render, (20, 20, 0)).actor
    # Accepts arrow keys to move either the player or the menu cursor,
    # Also deals with grid checking and collision detection

    def checkCollision(self):

        if ((self.player.getPos() - self.ball1.position()).length() < 0.5):
            self.canMove=False

        elif (self.player.getPos() - self.ball2.position()).length() < 1.0:
            self.canMove=False

        elif (self.player.getPos() - self.ball3.position()).length() < 1.6:
            self.canMove=False

        # elif (self.player.getPos() - self.car.position()).length() < 1.6:
        #     self.canMove=False

        # elif (self.player.getPos() - self.panda1.position()).length() < 1.6:
        #     self.canMove=False
        #
        # elif (self.player.getPos() - self.panda2.position()).length() < 1.6:
        #     self.canMove=False

        else:
            self.canMove=True

        return not self.canMove

    def move(self, task):

        # If the camera-left key is pressed, move camera left.
        # If the camera-right key is pressed, move camera right.

        base.camera.lookAt(self.player)
        if (self.keyMap["cam-left"]!=0):
            base.camera.setX(base.camera, -20 * globalClock.getDt())
        if (self.keyMap["cam-right"]!=0):
            base.camera.setX(base.camera, +20 * globalClock.getDt())

        # save ralph's initial position so that we can restore it,
        # in case he falls off the map or runs into something.

        startpos = self.player.getPos()

        # If a move-key is pressed, move ralph in the specified direction.

        if (self.keyMap["left"]!=0):
            if not(self.canMove):
                self.canMove=True
            self.player.setH(self.player.getH() + 300 * globalClock.getDt())
        if (self.keyMap["right"]!=0):
            if not(self.canMove):
                self.canMove=True
            self.player.setH(self.player.getH() - 300 * globalClock.getDt())
        if (self.keyMap["forward"]!=0):
            if (self.keyMap["speed-toggle"]!=0):
                self.player.setY(self.player, -10 * globalClock.getDt())
                if self.checkCollision():
                    self.player.setY(self.player, +10 * globalClock.getDt())
            else:
                self.player.setY(self.player, -25 * globalClock.getDt())
                if self.checkCollision():
                    self.player.setY(self.player, +25 * globalClock.getDt())

        if (self.keyMap["reverse"]!=0):
            if (self.keyMap["speed-toggle"]!=0):
                self.player.setY(self.player, +10 * globalClock.getDt())
                if self.checkCollision():
                    self.player.setY(self.player, -10 * globalClock.getDt())
            else:
                self.player.setY(self.player, +25 * globalClock.getDt())
                if self.checkCollision():
                    self.player.setY(self.player, -250 * globalClock.getDt())

        # If ralph is moving, loop the run animation.
        # If he is standing still, stop the animation.

        if ((self.keyMap["forward"]!=0) or (self.keyMap["left"]!=0) or
            (self.keyMap["right"]!=0)) and (self.keyMap["speed-toggle"]!=0):
            if self.isWalking is False:
                self.isWalking = True
                self.player.setPlayRate(1, "walk")
                self.player.loop("walk")

        elif ((self.keyMap["forward"]!=0) or (self.keyMap["left"]!=0) or
            (self.keyMap["right"]!=0)):
            if self.isMoving is False or self.isWalking:
                self.isWalking = False
                self.isMoving = True
                self.player.setPlayRate(1, "run")
                self.player.loop("run")

        elif (self.keyMap["reverse"]!=0) and (self.keyMap["speed-toggle"]!=0):
            if self.isWalking is False:
                self.isWalking = True
                self.player.setPlayRate(-1, "walk")
                self.player.loop("walk")

        elif (self.keyMap["reverse"]!=0):
            if self.isMoving is False or self.isWalking:
                self.isWalking = False
                self.isMoving = True
                self.player.setPlayRate(-1, "run")
                self.player.loop("run")
        else:
            if self.isMoving:
                self.player.stop()
                self.player.pose("walk",5)
                self.isMoving = False
                self.isWalking = False

        # If the camera is too far from ralph, move it closer.
        # If the camera is too close to ralph, move it farther.

        camvec = self.player.getPos() - base.camera.getPos()
        camvec.setZ(0)
        camdist = camvec.length()
        camvec.normalize()
        if (camdist > 10.0):
            base.camera.setPos(base.camera.getPos() + camvec*(camdist-10))
            camdist = 10.0
        if (camdist < 5.0):
            base.camera.setPos(base.camera.getPos() - camvec*(5-camdist))
            camdist = 5.0


        # The camera should look in ralph's direction,
        # but it should also try to stay horizontal, so look at
        # a floater which hovers above ralph's head.

        self.floater.setPos(self.player.getPos())
        self.floater.setZ(self.player.getZ() + 2.0)
        base.camera.lookAt(self.floater)

        # Panda action

        #self.panda1.follow(self.player, globalClock.getFrameTime())
        #self.panda2.follow(self.player, globalClock.getFrameTime())
        #self.panda1.waitedTooLong(globalClock.getFrameTime())
        #self.panda2.waitedTooLong(globalClock.getFrameTime())

        # Car action

        # self.car.circle(self.player)

        # Ball action

        self.ball1.rotate(self.player)
        self.ball2.rotate(self.player)
        self.ball3.rotate(self.player)

        return task.cont


w = World()
run()
