# -*- coding: utf-8 -*-

from threading import Thread
import struct
import json
##
## @brief      Class for u64-json-translator, derives from Thread
##
class U64JsonTranslator(Thread):
	##
	## @brief      Constructs the object, sets it as a daemonic thread and starts the run-loop
	##
	## @param      self         The object
	## @param      u64_stream   The u64 connection
	## @param      json_stream  The json connection
	## @param      instance_id  The unique identifier for the instance
	##
	def __init__(self,u64_stream,json_stream,instance_id):
		Thread.__init__(self)
		self.setDaemon(True)
		self.id = instance_id
		self.u64_stream = u64_stream
		self.json_stream = json_stream
		self.dictStorage = []
		self.json_stream.register(self.id)
		self.u64_stream.register(self.id)
		self.start()

	##
	## @brief      converts the binary u64 to a readable json-object
	##
	## @param      self  The object
	## @param      u64   The u64 binary
	##
	## @return     json object
	##
	def u64_to_json(self,u64):
		module_id = (struct.unpack('>H',u64[0:2])[0] & int(b'0011111110000000',2))//(2**7)
		command = (struct.unpack('>B',u64[1:2])[0] & int(b'00011110',2))//(2**1)
		upper_lower = struct.unpack('>B',u64[1:2])[0]  & int(b'00000001',2)
		address = struct.unpack('>H',u64[2:4])[0]
		value = struct.unpack('>I',u64[4:8])[0]
		
		if upper_lower == 1:
			jsondict = {"module":module_id,"command":command,"address":address,"value":value}
			self.dictStorage.append(jsondict)
		elif upper_lower == 0:
			if len(self.dictStorage) == 0:
				jsondict = {"module":module_id,"command":command,"address":address,"value":value}
				return json.dumps(jsondict)

			else:
				for i in self.dictStorage:
					if module_id == i["module"] and command == i["command"] and address == i["address"]:
						value = i["value"]*0xFFFFFFFF+value
						jsondict = {"module":module_id,"command":command,"address":address,"value":value}
						self.dictStorage.remove(i)
						return json.dumps(jsondict)

		
		

	##
	## @brief      converts the readable json-object to an unsigned 64 bit number -> u64
	##
	## @param      self        
	## @param      jsonobject  jsonobject
	##
	## @return     u64 as string
	##
	def json_to_u64(self,jsonobject):
		data = json.loads(jsonobject)
		value_test = '{0:032b}'.format(data["value"] % (1<<32))
		u64 = '{0:02b}'.format(0)
		u64 += '{0:07b}'.format(data["module"])
		u64 += '{0:02b}'.format(0)
		u64 += '{0:04b}'.format(data["command"])
		if len(value_test) <= 32:
			u64 += '{0:01b}'.format(0)
			u64 += '{0:016b}'.format(data["address"]%(1<<16))
			u64 += value_test
			u64 = int(u64,2).to_bytes(len(u64)//8,byteorder="big")
			return u64
		else:
			upper = u64
			lower = u64
			upper += '{0:01b}'.format(1)
			upper += '{0:016b}'.format(data["address"])
			upper += '{0:032b}'.format((int(value_test,2) & 0xFFFFFFFF00000000)//0xFFFFFFFF)
			lower += '{0:01b}'.format(0)
			lower += '{0:016b}'.format(data["address"])
			lower += '{0:032b}'.format(int(value_test,2) & 0xFFFFFFFF)
			lower, upper = int(lower,2).to_bytes(len(lower)//8,byteorder="big"), int(upper,2).to_bytes(len(upper)//8,byteorder="big")
			return [upper,lower]

	##
	## @brief      main-loop of the translator, peridodically checks both connections for input, translates it and forwards the translated data
	##
	## @param      self  
	##
	## @return     None
	##
	def run(self):
		while True:
			received_json = self.json_stream.receive(self.id)
			if received_json != "":
				u64 = self.json_to_u64(received_json)
				if type(u64) == list:
					self.u64_stream.send(u64[0],self.id)
					self.u64_stream.send(u64[1],self.id)
				else:
					self.u64_stream.send(u64,self.id)
			
			received_u64 = self.u64_stream.receive(self.id)
			if received_u64 != "":
				self.json_stream.send(self.u64_to_json(received_u64),self.id)




