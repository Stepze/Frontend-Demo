# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

##
## @brief      Class for abstract connection.
##
class AbstractConnection(ABC):		#abstract class to show the usage of the connection interface.
	
	##
	## Both ends of the connection are needed to have an unique id, with which they register at the connection object so that it
	## knows both its partners and does not provide any information to a third one.
	##
	@abstractmethod					
	def register(self):				
		pass						

	##
	## This is the method used to send a JSON-object to the other partner.
	## The JSON object and the id of the sender have to be given.
	##
	@abstractmethod					
	def send(self):					
		pass

	##
	## This is the method used to receive a JSON-object from the other partner.
	## The id of the receiver has to be given.
	##
	@abstractmethod					
	def receive(self):				
		pass
