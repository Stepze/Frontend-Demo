from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import json
from AbstractGuiController import AbstractGuiController
from threading import Thread, Timer
import time

##
## @brief      Objects of this class are made to handle and display a QT-gui, as described in a gui-file.
##
class QtGuiController(AbstractGuiController):								
	##
	## @brief      Constructs the object. Sets the object as a daemonic thread and automatically starts it
	## @brief      The layout file with the qt-layout is imported during runtime.
	## 
	## @param      self        The object
	## @param      guifile     The guifile
	## @param      connection  The connection
	## @param      idx         The index
	##
	def __init__(self,guifile,connection,idx):
		Thread.__init__(self)
		self.setDaemon(True)														
		self.refreshRequested = False
		self.idLayoutDict = {}
		self.id = idx
		self.connection = connection
		self.connection.register(self.id)
		layout_module = __import__(guifile)									
		layout_class = getattr(layout_module,"Ui_FrontendTest")
		self.qtwindow = layout_class(self)									
		self.qtwindow.show()
		self.start()					

	##
	## @brief      The GuiController is the parent of the Layout class
	## @brief      Each gui-element has to announce itself, to fill the dictionary
	##
	## @param      self        The object
	## @param      element     The gui-element
	## @param      identifier  The identifier
	##
	## @return     None
	##
	def announceGuiElement(self,identifier,element):		         
		self.idLayoutDict.update({identifier:element})    
		



	##
	## @brief      Takes the id of a gui element and returns the data that is contained in that element.
	## @brief      The type of the data depends on the type of the gui-element.
	##
	## @param      self  The object
	## @param      idy   The id of the gui-object
	##
	## @return     returns the data read from the gui object
	##
	def readData(self,idy):
		a = self.idLayoutDict.get(idy) 
		if type(a) == QLabel:
			return int(a.text())
		elif type(a) == QLineEdit:
			return int(a.text())
		elif type(a) == QSpinBox:
			return a.value()
		elif type(a) == QCheckBox:
			return int(a.isChecked())

	##
	## @brief      Takes the id of a gui-element and the data that should be written to that element.
	## @brief      Updates the corresponding gui-element to display that data.
	##
	## @param      self  The object
	## @param      idy   The id of the gui-object
	## @param      data  The data to be written
	##
	## @return     None
	##
	def writeData(self,idy,data):											
		a = self.idLayoutDict.get(idy)		
		if type(a) == QLabel:
			a.setText(str(data))

		elif type(a) == QLineEdit:
			a.setText(str(data))

	##
	## @brief      Periodically checks all user-editable gui-elements for user input and 
	## @brief      forwards that input in form of a JSON-object via the connection.
	##
	## @param      self  The object
	##
	## @return     None
	##
	def run(self):															
		while True:															
			self.jsonToGui()
			if self.refreshRequested == True:	
				jsonList = self.guiToJson()
				for i in jsonList:
					self.connection.send(i,self.id)
				self.refreshRequested = False#
			time.sleep(0.05)
				


	##
	## @brief      { function_description }
	##
	## @param      self  The object
	##
	## @return     { description_of_the_return_value }
	##
	def jsonToGui(self):
		self.receivedJSON = self.connection.receive(self.id)			
		if self.receivedJSON != "":
			_buffer = json.loads(self.receivedJSON)
			module = _buffer["key"][0]
			address = _buffer["key"][1]
			key = (module,address)
			self.writeData(key, _buffer["value"])
	
	##
	## @brief      { function_description }
	##
	## @param      self  The object
	##
	## @return     { description_of_the_return_value }
	##
	def guiToJson(self):
		jsonList = []
		for key,value in self.idLayoutDict.items():
			b = self.readData(key)
			if b != "":
				jsonDict = {"key":key,"value":b}
				jsonList.append(json.JSONEncoder().encode(jsonDict))
		return jsonList

	