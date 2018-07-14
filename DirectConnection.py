# -*- coding: utf-8 -*-
from AbstractConnection import AbstractConnection
##
##	Objects of this class can be used to establish a connection between parts of the
##	frontend, that run on the same machine.
##
class DirectConnection(AbstractConnection):													
	##
	## @brief      Constructs the object.
	##
	## @param      self  The object
	##
	def __init__(self):
		self.jsonList = [[],[]]															#This is the bi-directional buffer for the JSON-objects.											
		self.id1 = -1																	#Because the connection object initially has no clue which two partners it connects
		self.id2 = -1																	#and what their ids are, the ids are initialized with -1. As long as one id is -1
																						#it is clear that at least one partner has not registered yet.

	##
	## @brief      { function_description }
	##
	## @param      self  The object
	## @param      idx   The index
	##
	## @return     { description_of_the_return_value }
	##
	def register(self,idx):																#The register() method changes the initial -1s of the ids to the actual ids of
		if idx not in [self.id1,self.id2] and (self.id1 == -1 or self.id2 == -1):		#the connection partners. If the id which is requested to be added already known or 	
			if self.id1 == -1:															#if not at least one id is at its initial value -1, the method just passes.								
				self.id1 = idx
			else:
				self.id2 = idx	
	

	def send(self,jsonobj,idx):															#The send() method appends a given JSON-object to the corresponding position in the 
		if idx == self.id1:																#bi-directional buffer. But first it is checked if the senders id is known.
			self.jsonList[0].append(jsonobj)											#self.jsonList[0] buffers the values from partner 1 sent to partner 2 
		elif idx == self.id2:															#and self.jsonList[1] vice versa
			self.jsonList[1].append(jsonobj)											
		else:
			raise Exception("unknown id")

	def receive(self,idx):																#The receive() method also firstly checks the id of the calling object. If the id is															
		if idx == self.id1 and len(self.jsonList[1]) > 0:								#known, it pops the first element of the corresponding part of the buffer and returns it.
			return self.jsonList[1].pop(0)												#The buffer is a bi-directional FIFO datastructure.
		elif idx == self.id2 and len(self.jsonList[0]) > 0:								#As above already mentioned self.jsonList[0] contains JSON-objects for partner 2 (id2)
			return self.jsonList[0].pop(0)												#and self.jsonList[1] contains JSON-objects for partner 1 (id1).
		elif idx != self.id1 and idx != self.id2:
			raise Exception("unknown id")
		else:
			return ""

		

