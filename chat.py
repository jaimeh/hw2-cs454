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

import random, sys, os, math

class MyApp(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		
		self.cManager = QueuedConnectionManager()
		self.cListener = QueuedConnectionListener(self.cManager, 0)
		self.cReader = QueuedConnectionReader(self.cManager, 0)
		self.cWriter = ConnectionWriter(self.cManager, 0)
		
		host = "localhost"
		port = 9252
		self.connection = self.cManager.openTCPClientConnection(host, port, 10000)
		
		self.received = 1
		
		if self.connection:
			self.cReader.addConnection(self.connection)                	
			taskMgr.add(self.updateRoutine, 'updateRoutine')
			
			
		
		print 'Hello You Are Now Connected To The Server'
		#self.heartbeat()
		self.options()

	#options for the clients when game starts	
        def options(self):
                self.option = 0
		self.option = str(raw_input("Please Selection An Option\n1-Enter Chat\n2-Messages\n3-Quit\n"))
                if self.option == "1":
                        self.chat()
                if self.option == "2":
                        self.messages()
                if self.option == "3":
                        sys.exit(0)
                        
       
        #function to chat
        def chat(self):
                self.username = ""
                self.message = ""
                self.username = str(raw_input("Please enter your username: "))
                self.message = str(raw_input("Please enter your message: "))
                
                chat_message = self.username + " " + self.message
                request = self.chatRequest(chat_message)
                self.cWriter.send(request,self.connection)
                

        #package chat request       
        def chatRequest(self, chat_info):
		pkg = PyDatagram()
		pkg.addUint16(112)
		pkg.addString(chat_info)
		return pkg

	#message options for the clients when game starts	
        def messages(self):
                self.option = 0
		self.option = str(raw_input("Please Selection An Option\n1-Send A Message\n2-Check Messages\n3-Return\n"))
                if self.option == "1":
                        self.message()
                if self.option == "2":
                        self.checkMessages()
                if self.option == "3":
                        self.options()

        #function to message
        def checkMessages(self):
                self.username = str(raw_input("Please enter your username: "))
                chat_message = self.username
                request = self.checkMessagesRequest(chat_message)
                self.cWriter.send(request,self.connection)
                

        #package message request       
        def checkMessagesRequest(self, chat_info):
		pkg = PyDatagram()
		pkg.addUint16(116)
		pkg.addString(chat_info)
		return pkg
       
        #function to send a message
        def message(self):
                self.from_Username = ""
                self.to_Username = " "
                self.message = ""
                
                self.from_Username = str(raw_input("Please enter your username: "))
                self.to_Username = str(raw_input("Please enter which username you want to send the message: "))
                self.message = str(raw_input("Please enter your message: "))
                
                chat_message = self.from_Username + " " +self.to_Username+ " " + self.message
                request = self.messageRequest(chat_message)
                self.cWriter.send(request,self.connection)
                

        #package message request       
        def messageRequest(self, chat_info):
		pkg = PyDatagram()
		pkg.addUint16(115)
		pkg.addString(chat_info)
		return pkg

        
        #check for messages for server
	def check(self):
		while self.cReader.dataAvailable():
			
			datagram = NetDatagram()
			# Retrieve the contents of the datagram.
			if self.cReader.getData(datagram):
				data = PyDatagramIterator(datagram)
				responseCode = data.getUint16()
				
				if responseCode == 212:
					print self.getString(data)
					self.options()
				elif responseCode == 201: #login code
					if (self.getString(data)=="Unsuccessful login"): #appears if login unsuccessful
                                                print " "
                                                print "Unsuccessful login"
                                                print " "
                                                self.options()
                                        else:
                                                print "Your are logged in" #appear if login successful
                                                self.login_options()#appears the login options
				elif responseCode == 203: #register code
					if (self.getString(data)=="Registration successful"): #appear if registration was successful
                                                print "You are now registered"
                                                print "Please login" #user must login
                                                print " "
                                                self.options() 
                                        else:
                                                print " "#appear if registration wasn't successful
                                                print "Registration was unsuccessful. Pick a different username and please try again "
                                                print " "
                                                self.options()#user must attempt to register again
				elif responseCode == 215:
					print self.getString(data)
					self.messages()
				elif responseCode == 216:
					print self.getString(data)
					self.messages()
				else:
					print "nothing found"
					
	#function that unpackage the message from server
        def getString(self, data):
		msg = data.getString()
		return msg

        #heart beat function
	def heartbeat(self):
                request = self.heartbeatRequest()
                self.cWriter.send(request,self.connection)
                

        #heart beat packaged
        def heartbeatRequest(self):
		pkg = PyDatagram()
		pkg.addUint16(123)
		return pkg
	
        #updateRoutine for the program
	def updateRoutine(self,task):
                self.heartbeat()
		self.check()
		return task.again;
	
app = MyApp()
app.run() #enters the panda3D main loop
