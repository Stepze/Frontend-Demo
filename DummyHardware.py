# -*-  coding: utf-8 -*-
from threading import Thread
import struct
import random


class DummyHardware(Thread):
	def __init__(self,u64_conn,idx):
		Thread.__init__(self)
		self.u64_conn = u64_conn
		self.id = idx
		self.u64_conn.register(self.id)
		self.dictStorage = []
		self.setDaemon(True)
		self.start()

	
	def run(self):
		while True:
			u64 = self.u64_conn.receive(self.id)
			if u64 != "":
				u64_decoded = self.u64_to_json(u64)
				if u64_decoded["command"] == 5:
					u64 = '{0:02b}'.format(0)
					u64 += '{0:07b}'.format(u64_decoded["module"])
					u64 += '{0:02b}'.format(0)
					u64 += '{0:04b}'.format(u64_decoded["command"])
					u64 += '{0:01b}'.format(0)
					u64 += '{0:016b}'.format(u64_decoded["address"])
					u64 += '{0:032b}'.format(random.randint(1,100000))
					u64 = int(u64,2).to_bytes(len(u64)//8,byteorder="big")
					self.u64_conn.send(u64,self.id)



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
				return jsondict

			else:
				for i in self.dictStorage:
					if module_id == i["module"] and command == i["command"] and address == i["address"]:
						value = i["value"]*0xFFFFFFFF+value
						jsondict = {"module":module_id,"command":command,"address":address,"value":value}
						self.dictStorage.remove(i)
						return jsondict

