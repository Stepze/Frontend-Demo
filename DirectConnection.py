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
		##
		## This is the bi-directional buffer for the JSON-objects.
		##
		self.jsonList = [[],[]]
		##
		## Because the connection object initially has no clue which two partners it connects
		## #and what their ids are, the ids are initialized with -1. As long as one id is -1
		## it is clear that at least one partner has not registered yet.
		##											
		self.id1 = -1																	
		self.id2 = -1																	
																	

	##
	## @brief      The register() method changes the initial -1s of the ids to the actual ids of
	## @brief      the connection partners. If the id which is requested to be added already known or 
	## @brief      if not at least one id is at its initial value -1, the method just passes.	
	##
	## @param      self  The object
	## @param      idx   The id
	##
	## @return     None
	##
	def register(self,idx):																
		if idx not in [self.id1,self.id2] and (self.id1 == -1 or self.id2 == -1):			
			if self.id1 == -1:																						
				self.id1 = idx
			else:
				self.id2 = idx	
	

	##
	## @brief      The send() method appends a given JSON-object to the corresponding position in the 
	## @brief      bi-directional buffer. But first it is checked if the senders id is known.
	## @brief      self.jsonList[0] buffers the values from partner 1 sent to partner 2 and self.jsonList[1] vice versa
	##
	## @param      self     The object
	## @param      jsonobj  The jsonobj
	## @param      idx      The id
	##
	## @return     None
	##
	def send(self,jsonobj,idx):															
		if idx == self.id1:																
			self.jsonList[0].append(jsonobj)											
		elif idx == self.id2:															
			self.jsonList[1].append(jsonobj)											
		else:
			raise Exception("unknown id")

	
	##
	## @brief      The receive() method also firstly checks the id of the calling object. If the id is	
	## @brief      known, it pops the first element of the corresponding part of the buffer and returns it.
	## @brief      The buffer is a bi-directional FIFO datastructure. As above already mentioned self.jsonList[0] 
	## @brief      contains JSON-objects for partner 2 (id2) and self.jsonList[1] contains JSON-objects for partner 1 (id1).
	##
	## @param      self  The object
	## @param      idx   The id
	##
	## @return     the first json-object in the corresponding list
	##
	def receive(self,idx):																														
		if idx == self.id1 and len(self.jsonList[1]) > 0:								
			return self.jsonList[1].pop(0)												
		elif idx == self.id2 and len(self.jsonList[0]) > 0:								
			return self.jsonList[0].pop(0)												
		elif idx != self.id1 and idx != self.id2:
			raise Exception("unknown id")
		else:
			return ""

		

