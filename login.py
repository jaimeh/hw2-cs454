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

    #character selection varaiables
    createCharacter = DirectButton()
    deleteCharacter = DirectButton()
    selectCharacter = OnscreenText()
    selectCharacterTextbox = DirectEntry()
    selectCharacterInput=''
    referenceForSelection = OnscreenText()
    myScrolledList = DirectScrolledList()
    submitBtn = DirectButton()
    cancelBtn = DirectButton()
    
    #character deletion varaiables
    selectCharactertodelete = OnscreenText()
    deleteBtn = DirectButton()
    delCancelBtn = DirectButton()
    CharacterToDeleteTextbox = DirectEntry()
    referenceForDeletion = OnscreenText()
    CharacterToDeleteInput = ' '
    
    #character creation varaiables
    v=[0]
    v1=[0]
    nameOfChar = OnscreenText()
    nameOfCharTextbox = DirectEntry()
    factionSelection = OnscreenText()
    nameOfCharInput =''
    
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

    def func1(self):
        self.clickedSubmit()
        self.createSelectionWindow()

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
            self.createSelectionWindow()

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
        self.submitBtn = DirectButton(text = ("Submit", "Login", "Submit", "disabled"), scale=.08, command=self.func1, pos=(0.8, 0.0, -0.90))
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
                                                self.showRalph()      
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
		return 

    def showRalph(self):
        self.environ = loader.loadModel("models/square")
        self.environ.reparentTo(render)
        self.environ.setPos(0,0,0)
        self.environ.setScale(100,100,1)
        self.moon_tex = loader.loadTexture("models/moon_1k_tex.jpg")
        self.environ.setTexture(self.moon_tex, 1)

        # Create the main character, Ralph

        self.ralph = Actor("models/ralph",
                                 {"run":"models/ralph-run",
                                  "walk":"models/ralph-walk"})
        self.ralph.reparentTo(render)
        self.ralph.setScale(.2)
        self.ralph.setPos(0,0,0)

    #character Creation        
    def createCreateCharWindow(self):
        self.frame = DirectFrame(frameColor=(0, 0, 0, 1), #(R,G,B,A)
                                frameSize=(-3, 3, -3, 3),#(Left,Right,Bottom,Top)
                                pos=(-0.5, 0, 0.9))
        self.buttons = [
        DirectRadioButton(text = ' Sword ', variable=self.v, value=[0], scale=0.07, pos=(-0.4,0,0.32), command=self.setText),
        DirectRadioButton(text = ' Axe ', variable=self.v, value=[1], scale=0.07, pos=(0.2,0,0.32), command=self.setText)
        ]
 
        for button in self.buttons:
            button.setOthers(self.buttons)
        
        self.nameOfChar = OnscreenText(text = "Name The Character :", pos = (-0.2, -0.75), scale = 0.08,fg=(1,0.5,0.5,1),align=TextNode.ACenter,mayChange=0)
        self.nameOfChar.reparentTo(self.frame)    
        self.nameOfCharTextbox = DirectEntry(text = "" ,scale=.07,pos=(0.25,0, -.75),command=self.setnameOfChar,initialText="name of character", numLines = 1,focus=0,focusInCommand=self.clearnameOfChar, focusOutCommand=self.getnameOfChar)
        self.nameOfCharTextbox.reparentTo(self.frame)   
        
        self.factionSelection = OnscreenText(text = "Faction Selection :", pos = (-0.15, -0.95), scale = 0.08,fg=(1,0.5,0.5,1),align=TextNode.ACenter,mayChange=0)
        self.factionSelection.reparentTo(self.frame)
        
        self.factionBtns = [
        DirectRadioButton(text = ' Blue ', variable=self.v1, value=[0], scale=0.07, pos=(-0.05,0,-0.05), command=self.setfaction),
        DirectRadioButton(text = ' Red ', variable=self.v1, value=[1], scale=0.07, pos=(0.3,0,-0.05), command=self.setfaction)
        ]
         
        for button1 in self.factionBtns:
            button1.setOthers(self.factionBtns)
        self.okForCreateBtn = DirectButton(text = ("Ok", "Ok", "Ok", "disabled"), scale=.08, command=self.clickedOkForCreateBtn, pos=(-0.05, 0.0, -1.25))
        self.cancelForCreateBtn =  DirectButton(text = ("Cancel", "Cancel", "Cancel", "disabled"), scale=.08, command=self.clickedCancelForCreateBtn, pos=(0.4, 0.0, -1.25))
        self.okForCreateBtn.reparentTo(self.frame)
        self.cancelForCreateBtn.reparentTo(self.frame)
        
    def destroyCreateCharWindow(self):
        self.frame.destroy()
        self.nameOfChar.destroy()
        self.nameOfCharTextbox.destroy()
        self.factionSelection.destroy()
        self.okForCreateBtn.destroy()
        self.cancelForCreateBtn.destroy()
                                
    def clearnameOfChar(self):
        self.nameOfCharTextbox.enterText('')
        
    def getnameOfChar(self):
        self.nameOfCharInput = self.nameOfCharTextbox.get()
    
    def setnameOfChar(self, textEntered):
        print "name Of Char: ",textEntered
        self.nameOfChar = textEntered
        
    def clickedOkForCreateBtn(self):
        print "you have pressed the ok button for creating a character"
     
    def clickedCancelForCreateBtn(self):
        print "you have press the cancel button from the create character frame"
        self.destroyCreateCharWindow()
        self.createSelectionWindow()    
    
    def setText(status=None):
        bk_text = "CurrentValue "
        
    def setfaction(status=None):
        bk_text = "CurrentValue "    
        
    #character deletion        
    def createDeleteCharWindow(self):
        self.frame = DirectFrame(frameColor=(0, 0, 0, 1), #(R,G,B,A)
                                frameSize=(-3, 3, -3, 3),#(Left,Right,Bottom,Top)
                                pos=(-0.5, 0, 0.9))
        
        self.selectCharactertodelete = OnscreenText(text = "Select Character :", pos = (-0.02, -0.35), scale = 0.08,fg=(1,0.5,0.5,1),align=TextNode.ACenter,mayChange=0)
        self.selectCharactertodelete.reparentTo(self.frame)
        self.selectCharacterToDeleteTextbox = DirectEntry(text = "" ,scale=.07,pos=(0.45,0, -.35),command=self.setselectCharacterToDelete,initialText="name of character", numLines = 1,focus=0,focusInCommand=self.clearselectCharacterToDelete, focusOutCommand=self.getselectCharacterToDelete)
        self.selectCharacterToDeleteTextbox.reparentTo(self.frame)
        self.referenceForDeletion = OnscreenText(text = "Reference to Character List:", pos = (-0.15, -0.75), scale = 0.08,fg=(1,0.5,0.5,1),align=TextNode.ACenter,mayChange=0)
        self.referenceForDeletion.reparentTo(self.frame)
        self.deleteScrolledList = DirectScrolledList(
        decButton_pos= (0.35, 0, 0.53),
        decButton_text = "Dec",
        decButton_text_scale = 0.04,
        decButton_borderWidth = (0.005, 0.005),
 
        incButton_pos= (0.35, 0, -0.02),
        incButton_text = "Inc",
        incButton_text_scale = 0.04,
        incButton_borderWidth = (0.005, 0.005),
        
        
        pos = (0.7, 0, -0.99),
        numItemsVisible = 4,
        forceHeight = .11,
        itemFrame_frameSize = (-0.6, 0.6, -0.37, 0.11),
        itemFrame_pos = (0.35, 0, 0.4))
        
        for playerchar in ['xxxbluesword', 'xxxblueaxe', 'xxxredsword', 'xxxredsword01','xxx_red_sword04']:
            l = DirectLabel(text = playerchar, text_scale=0.1)
            self.deleteScrolledList.addItem(l)
            
        self.deleteScrolledList.reparentTo(self.frame)
        self.deleteBtn = DirectButton(text = ("Delete", "Delete", "Delete", "disabled"), scale=.08, command=self.clickedDelete, pos=(-0.2, 0.0, -1.25))
        
        self.delCancelBtn =  DirectButton(text = ("Cancel", "Cancel", "Cancel", "disabled"), scale=.08, command=self.clickedDelCancel, pos=(0.3, 0.0, -1.25))
        self.deleteBtn.reparentTo(self.frame)
        self.delCancelBtn.reparentTo(self.frame)
        
    def destroyDeleteCharWindow(self):
        self.frame.destroy()
        self.selectCharactertodelete.destroy()
        self.deleteBtn.destroy()
        self.delCancelBtn.destroy()
        self.selectCharacterToDeleteTextbox.destroy()
        self.referenceForDeletion.destroy()
        
    def clearselectCharacterToDelete(self):
        self.selectCharacterToDeleteTextbox.enterText('')
        
    def getselectCharacterToDelete(self):
        self.selectCharacterToDeleteInput = self.nameOfCharTextbox.get()
    
    def setselectCharacterToDelete(self, textEntered):
        print "name Of Char: ",textEntered
        self.selectCharacterToDelete = textEntered
        
    def clickedDelete(self):
        print "You pressed delete a character"
        
    def clickedDelCancel(self):
        print "to go back to slection menu"
        self.destroyDeleteCharWindow()
        self.createSelectionWindow()
            
    
    #character Selection
    def createSelectionWindow(self):
        self.frame = DirectFrame(frameColor=(0, 0, 0, 1), #(R,G,B,A)
                                frameSize=(-3, 3, -3, 3),#(Left,Right,Bottom,Top)
                                pos=(-0.5, 0, 0.9))
                
        self.createCharacter = DirectButton(text = ("Create Character","Create Character","Create Character","disabled"), scale=.08, command = self.clickedCreateChar, pos=(-0.14,0.0,-0.25))
        self.deleteCharacter = DirectButton(text = ("Delete Character","Delete Character","Delete Character","disabled"), scale=.08, command = self.clickedDeleteChar, pos=(-0.14,0.0,-0.40))
        self.createCharacter.reparentTo(self.frame)
        self.deleteCharacter.reparentTo(self.frame)
        self.selectCharacter = OnscreenText(text = "Select Character :", pos = (-0.12, -0.55), scale = 0.08,fg=(1,0.5,0.5,1),align=TextNode.ACenter,mayChange=0)
        self.selectCharacter.reparentTo(self.frame)
        
        self.myScrolledList = DirectScrolledList(
        decButton_pos= (0.35, 0, 0.53),
        decButton_text = "Dec",
        decButton_text_scale = 0.04,
        decButton_borderWidth = (0.005, 0.005),
 
        incButton_pos= (0.35, 0, -0.02),
        incButton_text = "Inc",
        incButton_text_scale = 0.04,
        incButton_borderWidth = (0.005, 0.005),
 
        
        pos = (0.05, 0, -0.3),
        numItemsVisible = 4,
        forceHeight = .11,
        itemFrame_frameSize = (-0.6, 0.6, -0.37, 0.11),
        itemFrame_pos = (0.35, 0, 0.4),
        )
        
        self.selectCharacterTextbox = DirectEntry(text = "" ,scale=.07,pos=(0.28,0, -.55),command=self.setselectCharacterTextbox,initialText="name of character", numLines = 1,focus=0,focusInCommand=self.clearselectCharacterTextbox, focusOutCommand=self.getselectCharacterTextbox)
        self.selectCharacterTextbox.reparentTo(self.frame)
        self.referenceForSeletion = OnscreenText(text = "Reference to Character List:\n that already exists", pos = (-0.30, -0.75), scale = 0.08,fg=(1,0.5,0.5,1),align=TextNode.ACenter,mayChange=0)
        self.referenceForSeletion.reparentTo(self.frame)
      
        for playerchar in ['xxxbluesword', 'xxxblueaxe', 'xxxredsword', 'xxxredsword01','xxx_red_sword04']:
            l = DirectLabel(text = playerchar, text_scale=0.1)
            self.myScrolledList.addItem(l) 
        
        self.submitBtn = DirectButton(text = ("Start", "Start", "Start", "disabled"), scale=.08, command=self.clickedSubmit, pos=(-0.2, 0.0, -1.45))
        
        self.cancelBtn =  DirectButton(text = ("Cancel", "Cancel", "Cancel", "disabled"), scale=.08, command=self.clickedCancel, pos=(0.3, 0.0, -1.45))
        self.submitBtn.reparentTo(self.frame)
        self.cancelBtn.reparentTo(self.frame)
        
    def destroySelectionWindow(self):
        self.frame.destroy()
        self.selectCharacter.destroy()
        self.createCharacter.destroy()
        self.deleteCharacter.destroy()
        self.submitBtn.destroy()        
        self.cancelBtn.destroy()
    
    def clearselectCharacterTextbox(self):
        self.selectCharacterTextbox.enterText('')
        
    def getselectCharacterTextbox(self):
        self.selectCharacterTextbox = self.selectCharacterTextbox.get()
    
    def setselectCharacterTextbox(self, textEntered):
        print "name Of Char: ",textEntered
        self.selectCharacterTextbox = textEntered
        
    def clickedCreateChar(self):
        print "You pressed create a new character"
        self.destroySelectionWindow()
        self.createCreateCharWindow()  
    
    def clickedDeleteChar(self):
        print "You pressed delete a character"
        self.destroySelectionWindow()
        self.createDeleteCharWindow()  
        
    def clickedSubmit(self):
        print "you pressed start button"
  
    def clickedCancel(self):
        print "You pressed Cancel"

l = login()
run()
