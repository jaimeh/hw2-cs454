import __builtin__

""" Python Imports """
from hashlib import md5
from sys import exit
from time import strftime
import random, sys

""" Panda3D Imports """
from direct.directbase.DirectStart import *
from direct.showbase.DirectObject import DirectObject
from panda3d.core import Texture
from panda3d.core import WindowProperties
from panda3d.core import *
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import Sequence

from direct.showbase.ShowBase import ShowBase
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import PandaNode,NodePath,Camera,TextNode

from panda3d.core import ConnectionWriter
from panda3d.core import NetDatagram
from panda3d.core import QueuedConnectionListener
from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionReader



from common.Constants import Constants
from net.ConnectionManager import ConnectionManager


class login(DirectObject):
    TEXT_COLOR = (1,1,1,1)
    FONT_TYPE_01 = 0
    TEXT_SHADOW_COLOR = (0,0,0,0.5)
    usernameInput = ""
    passwordInput = ""
    frame = DirectFrame()
    username = OnscreenText()
    password = OnscreenText()
    cpassword = OnscreenText()
    failed = OnscreenText()
    userTextbox = DirectEntry()
    passTextbox = DirectEntry()
    submitBtn = DirectButton()
    registerBtn = DirectButton()
    cancelBtn = DirectButton()
    
    
    registerUsername = ""
    registerPassword = ""
    registerCPassword = ""
    
    regInputUser = DirectEntry()
    regInputPass = DirectEntry()
    regInputCPass = DirectEntry()
    
    regRegisterBtn = DirectButton()
    regCancelBtn = DirectButton()
    
    def __init__(self):
        print 'Loading Login...'
      #  self.cManager = ConnectionManager()
      #  self.startConnection()
      
        self.cManager = QueuedConnectionManager()
	self.cListener = QueuedConnectionListener(self.cManager, 0)
	self.cReader = QueuedConnectionReader(self.cManager, 0)
	self.cWriter = ConnectionWriter(self.cManager, 0)


	
        frame = DirectFrame(frameColor=(0, 0, 0, 1), #(R,G,B,A)
                            frameSize=(-1, 1, -1, 1),#(Left,Right,Bottom,Top)
                            pos=(-0.5, 0, 0.5))

        
        
        self.connection = self.cManager.openTCPClientConnection(Constants.SERVER_IP,
                                                                        Constants.SERVER_PORT,
                                                                        1000)

        if self.connection:
                self.cReader.addConnection(self.connection)

                taskMgr.add(self.updateRoutine, 'updateRoutine-Connection', -39)
                taskMgr.doMethodLater(5, self.checkConnection, 'checkConnection')

			
        self.createLoginWindow()
    def startConnection(self):
        """Create a connection to the remote host.

        If a connection cannot be created, it will ask the user to perform
        additional retries.

        """
        if self.cManager.connection == None:
            if not self.cManager.startConnection():
                return False

        return True
    def clearPassText(self):
        self.passTextbox.enterText('')
    def clearUserText(self):
        self.userTextbox.enterText('')
    def getUserText(self):
        self.usernameInput = self.userTextbox.get()
    def getPassText(self):
        self.passwordInput = self.passTextbox.get()
    def setUserText(self, textEntered):
        print "username: ",textEntered
        self.usernameInput = textEntered
    def setPassText(self, textEntered):
        print "password: ",textEntered
        self.passwordInput = textEntered
    def clickedSubmit(self):
        self.usernameInput = self.userTextbox.get().strip()
        self.passwordInput = self.passTextbox.get().strip()
        if(self.usernameInput is not "" and self.passwordInput is not ""):
            print "You pressed Submit", self.usernameInput, " ; ",self.passwordInput
           # self.cManager.sendRequest(Constants.CMSG_AUTH, self.usernameInput+" "+self.passwordInput);

            login_info = self.usernameInput + " " + self.passwordInput
            request = self.loginRequest(login_info)
            self.cWriter.send(request,self.connection)
        else:
            print "Please enter in a username and password"
    def clickedCancel(self):
        print "You pressed Cancel"
        exit()
    def clickedRegister(self):
        print "You pressed Register"
        self.createRegisterWindow()
    def clickedRegRegister(self):
        self.registerUsername = self.regInputUser.get()
        self.registerPassword = self.regInputPass.get()
        self.registerCPassword = self.regInputCPass.get()
        if self.registerPassword == self.registerCPassword:
            print "Success (",self.registerUsername, ", ",self.registerPassword,", ",self.registerCPassword,")"
            
            #self.cManager.sendRequest(Constants.CMSG_REGISTER, self.registerUsername+" "+self.registerPassword)
            register_info = self.registerUsername + " " + self.registerPassword
            request = self.registerRequest(register_info)
            self.cWriter.send(request,self.connection)
            self.createLoginWindow()
        else:
            self.failed = OnscreenText(text="Your password does not match Confirm Password.", pos=(-0.5, 0, 1), scale=0.06,fg=(1,0.5,0.5,1), align=TextNode.ACenter,mayChange=0)
            self.failed.reparentTo(self.frame)
            print "Failed (",self.registerUsername, ", ",self.registerPassword,", ",self.registerCPassword,")"
    def clickedRegCancel(self):
        self.destroyRegisterWindow()
        self.createLoginWindow()
    def destroyLoginWindow(self):
        self.frame.destroy()
        self.username.destroy()
        self.password.destroy()
        self.userTextbox.destroy()
        self.passTextbox.destroy()
        self.submitBtn.destroy()
        self.registerBtn.destroy()
        self.cancelBtn.destroy()
    def destroyRegisterWindow(self):
        self.frame.destroy()
        self.username.destroy()
        self.password.destroy()
        self.cpassword.destroy()
        self.regInputUser.destroy()
        self.regInputPass.destroy()
        self.regInputCPass.destroy()
        self.cancelBtn.destroy()
        self.registerBtn.destroy()
        self.failed.destroy();
    def createLoginWindow(self):
        self.frame = DirectFrame(frameColor=(0, 0, 0, 1), #(R,G,B,A)
                                frameSize=(-1, 1, -1, 1),#(Left,Right,Bottom,Top)
                                pos=(-0.5, 0, 0.5))
                
        self.username = OnscreenText(text = "username:", pos = (-0.1, 0.0), scale = 0.05,fg=(1,0.5,0.5,1),align=TextNode.ACenter,mayChange=0)
        self.password = OnscreenText(text="password: ", pos = (-0.1, -0.2), scale=0.05, fg=(1, 0.5,0.5,1), align=TextNode.ACenter, mayChange=0)
        self.username.reparentTo(self.frame)
        self.password.reparentTo(self.frame)
        self.userTextbox = DirectEntry(text = "" ,scale=.05,pos=(.1,0,0), command=self.setUserText,initialText="username", numLines = 1,focus=1,focusInCommand=self.clearUserText, focusOutCommand=self.getUserText)
        self.passTextbox = DirectEntry(text = "" ,scale=.05,pos=(.1,0, -.2),command=self.setPassText,initialText="password", numLines = 1,focus=0,focusInCommand=self.clearPassText, focusOutCommand=self.getPassText)
        self.userTextbox.reparentTo(self.frame)
        self.passTextbox.reparentTo(self.frame)
        self.submitBtn = DirectButton(text = ("Submit", "Login", "Submit", "disabled"), scale=.08, command=self.clickedSubmit, pos=(0.8, 0.0, -0.90))
        self.registerBtn =  DirectButton(text = ("Register", "Register", "Register", "disabled"), scale=.075, command=self.clickedRegister, pos=(0.5, 0.0, -0.90))
        self.cancelBtn =  DirectButton(text = ("Cancel", "Cancel", "Cancel", "disabled"), scale=.08, command=self.clickedCancel, pos=(0.2, 0.0, -0.90))
        self.submitBtn.reparentTo(self.frame)
        self.cancelBtn.reparentTo(self.frame)
        self.registerBtn.reparentTo(self.frame)
    def createRegisterWindow(self):
        self.frame = DirectFrame(frameColor=(0, 0, 0, 1), #(R,G,B,A)
                                frameSize=(-1, 1, -1, 1),#(Left,Right,Bottom,Top)
                                pos=(-0.5, 0, 0.5))
        self.username = OnscreenText(text = "Username:", pos = (-0.1, 0.0), scale = 0.05,fg=(1,0.5,0.5,1),align=TextNode.ACenter,mayChange=0)
        self.password = OnscreenText(text="Password: ", pos = (-0.1, -0.2), scale=0.05, fg=(1, 0.5,0.5,1), align=TextNode.ACenter, mayChange=0)
        self.cpassword = OnscreenText(text="Confirm Password: ", pos = (-0.15, -0.4), scale=0.05, fg=(1, 0.5,0.5,1), align=TextNode.ACenter, mayChange=0)
        self.username.reparentTo(self.frame)
        self.password.reparentTo(self.frame)
        self.cpassword.reparentTo(self.frame)
        self.regInputUser = DirectEntry(text = "" ,scale=.05,pos=(.1,0,0), command=self.setUserText,initialText="username", numLines = 1,focus=1,focusInCommand=self.clearUserText, focusOutCommand=self.getUserText)
        self.regInputPass = DirectEntry(text = "" ,scale=.05,pos=(.1,0, -.2),command=self.setPassText,initialText="password", numLines = 1,focus=0,focusInCommand=self.clearPassText, focusOutCommand=self.getPassText)
        self.regInputCPass = DirectEntry(text = "" ,scale=.05,pos=(.1,0, -.4),command=self.setPassText,initialText="confirm password", numLines = 1,focus=0,focusInCommand=self.clearPassText, focusOutCommand=self.getPassText)
        self.regInputUser.reparentTo(self.frame)
        self.regInputPass.reparentTo(self.frame)
        self.regInputCPass.reparentTo(self.frame)
        self.registerBtn =  DirectButton(text = ("Register", "Register", "Register", "disabled"), scale=.075, command=self.clickedRegRegister, pos=(0.8, 0.0, -0.90))
        self.cancelBtn =  DirectButton(text = ("Cancel", "Cancel", "Cancel", "disabled"), scale=.08, command=self.clickedRegCancel, pos=(0.2, 0.0, -0.90))
        self.cancelBtn.reparentTo(self.frame)
        self.registerBtn.reparentTo(self.frame)

    def check(self):
		while self.cReader.dataAvailable():
			
			datagram = NetDatagram()
			# Retrieve the contents of the datagram.
			if self.cReader.getData(datagram):
                            
				data = PyDatagramIterator(datagram)
				responseCode = data.getUint16()
				
				if responseCode == 1:
					self.getInt(data)
				elif responseCode == 201: #login code
					if (self.getString(data)=="Unsuccessful login"): #appears if login unsuccessful
                                                print " "
                                                print "Unsuccessful login"
                                                print " "
                                                self.createLoginWindow()
                                        else:
                                                print "Your are logged in" #appear if login successful
                                                self.createLoginWindow()#appears the login options
				elif responseCode == 203: #register code
					if (self.getString(data)=="Registration successful"): #appear if registration was successful
                                                print "You are now registered"
                                                print "Please login" #user must login
                                                print " "
                                                self.createLoginWindow() 
                                        else:
                                                print " "#appear if registration wasn't successful
                                                print "Registration was unsuccessful. Pick a different username and please try again "
                                                print " "
                                                self.createLoginWindow()#user must attempt to register again
				elif responseCode == 4:
					self.getFloat(data)
				else:
					print "nothing found"

    def updateRoutine(self,task):
		self.check()
		return task.again;

    def checkConnection(self, task):

        if not self.cReader.isConnectionOk(self.connection):
            self.closeConnection()
            self.showDisconnected(0)

            return task.done

        return task.again

    def closeConnection(self):
        """Close the current connection with the remote host.

        If an existing connection is found, remove both the Main task, which
        is responsible for the heartbeat, and the Connection task, which is
        responsible for reading packets from the socket, then properly close
        the existing connection.

        """
        if self.connection != None:
            taskMgr.remove('updateRoutine-Main')
            taskMgr.remove('updateRoutine-Connection')
            taskMgr.remove('checkConnection')

            self.cManager.closeConnection(self.connection)
            self.connection = None

    #function that unpackage the message from server
    def getString(self, data):
	msg = data.getString()
	return msg

    #package login request       
    def loginRequest(self, login_info):
		pkg = PyDatagram()
		pkg.addUint16(101)
		pkg.addString(login_info)
		return pkg
        #package register request
    def registerRequest(self, register_info):
		pkg = PyDatagram()
		pkg.addUint16(103)
		pkg.addString(register_info)
		return pkg
l = login()
run()
