# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from threading import Thread



##
## @brief      This abstract class shows the usage of the GuiController interface.
##
class AbstractGuiController(ABC,Thread):
	##
	## @brief      This method is used to get the information which is displayed at a certain gui-element.
	## @brief      Each gui-element is provided with an id, with which it is identified. The type of the returned
	## @brief      data depends on the type of the gui-element.
	##
	## @param      self  The object
	##
	## @return     depends on gui-element
	##
	@abstractmethod
	def readData(self):							
		pass									
												
	##
	## @brief      This method is used to manipulate the contents of the gui-elements. Again the gui-elements are
	## @brief      found via an id and the data format depends on their type.
	##
	@abstractmethod									
	def writeData(self):							
		pass

	##
	## @brief      Since the GuiController needs to be running constantly and independant from any other parts of the
	## @brief      program, it needs to be a thread.
	##
	@abstractmethod									
	def run(self):									
		pass