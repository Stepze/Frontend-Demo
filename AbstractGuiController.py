# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from threading import Thread

class AbstractGuiController(ABC,Thread):			#This abstract class shows the usage of the GuiController interface.
	@abstractmethod
	def readData(self):							#This method is used to get the information which is displayed at a certain gui-element.
		pass										#Each gui-element is provided with an id, with which it is identified. The type of the returned
													#data depends on the type of the gui-element.
	
	@abstractmethod									#This method is used to manipulate the contents of the gui-elements. Again the gui-elements are
	def writeData(self):							#found via an id and the data format depends on their type.
		pass

	@abstractmethod									#Since the GuiController needs to be running constantly and independant from any other parts of the
	def run(self):									#program, it needs to be a thread.
		pass