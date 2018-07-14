# -*-coding: utf-8 -*-
from AbstractConnection import AbstractConnection
from threading import Thread
import socket
import time
import json

##
## @detailed		Objects of this class are used to establish a connection between two parts of the program
## @detailed      	running on different computers, connected via Ethernet. To get a working connection between
## @detailed      	the splitup parts, each part needs to have a connection-object.So in this case there are
## @detailed      	2 connection objects needed for one physical connection in contrast to the direct 
## @detailed      	connection, where one object per connection was enough.
## @detailed		Each connection object now only has one direct partner with an id. Instead of the second id
## @detailed		the connection object now needs to know on what port incoming packages will occur and to
## @detailed		which ip-adress and what port outgoing packages should be forwarded.
##
class UdpConnection(AbstractConnection,Thread):									

	def __init__(self,ip,rcvport,destport):															
		Thread.__init__(self)													
		self.setDaemon(True)													
		self.jsonList = []
		self.id1 = -1
		self.ip = ip
		self.recvPort = rcvport
		self.destPort = destport
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)			#A udp-socket object is used to handle the network traffic.
		self.sock.bind(("",self.recvPort))										#The port for incoming packages is bound to the socket.
		self.start()
		
		
	##
	## @brief     	The register() method works just like the one in DirectConnection.py
	## @brief     	but with the difference, that here only one partner needs to register,
	## @brief      	because the other one is on ther other side of the network.
	##
	## @param      self  The object
	## @param      idx   The id of the object that wants to register
	##
	## @return     None
	##
	def register(self,idx):														
		if idx != self.id1 and self.id1 == -1:									
			self.id1 = idx														
	
	##
	## @brief      The send() method checks if the id of the sender is the registered one.
	## @brief      If that is the case, the JSON.object is encoded to to a byte-string		
	## @brief      and is then sent to the other end of the udp connection.
	##
	## @param      self     The object
	## @param      jsonObj  The json object
	## @param      idx      The id of the sending object
	##
	## @return    None
	##
	def send(self,jsonObj,idx):													
		if idx == self.id1:																												
			self.sock.sendto(str(jsonObj).encode(), (self.ip,self.destPort))	
		else:
			raise Exception("unknown id")

	##
	## @brief      The receive() method works just like the one in DirectConnection.py
	## @brief      but with the difference that the buffer is only one-directional, because there is only
	## @brief      one partner directly connected. 
	##
	## @param      self  The object
	## @param      idx   The id of the receiving object
	##
	## @return     json-object or ""
	##
	def receive(self,idx):														
		if idx == self.id1 and len(self.jsonList)>0:							
			return self.jsonList.pop(0)											
		elif idx == self.id1:
			return ""
		elif idx != self.id1:
			raise Exception("unknown id")

	##
	## @brief      Since the connection needs to permanently look for incoming traffic at its port it needs
	## @brief      to be a thread, which receives the incoming data, decodes it ad appends it to the buffer.
	##
	## @param      self  The object
	##
	## @return     None
	##
	def run(self):																
		while True:																
			data = self.sock.recv(1024)
			self.jsonList.append(data.decode('utf-8'))



