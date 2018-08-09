# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

##
## @brief      abstract class to show the usage of the connection interface.
##
class AbstractConnection(ABC):		
	
	##
	## @brief      Both ends of the connection are needed to have an unique id, with which they register at the connection object so that it
	## @brief      knows both its partners and does not provide any information to a third one.
	##
	@abstractmethod					
	def register(self):				
		pass						

	##
	## @brief      This is the method used to send a JSON-object to the other partner.
	## @brief      The JSON object and the id of the sender have to be given.
	##
	@abstractmethod					
	def send(self):					
		pass

	##
	## @brief      This is the method used to receive a JSON-object from the other partner.
	## @brief      The id of the receiver has to be given.
	##
	@abstractmethod					
	def receive(self):				
		pass
