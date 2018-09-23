# -*- coding: utf-8 -*-
import time
import json
import threading
import xml.etree.ElementTree
from ModuleRepresentation import Module



##
## @brief      Class for application logic.
##
class ApplicationLogic(threading.Thread):
	##
	## @brief      Constructs the object.
	##
	## @param      self             The object
	## @param      gui_conn         The connection to the gui
	## @param      translator_conn  The connection to the u64-json translator
	## @param      module_file		The file with the information about dependant addresses
	## @param      updateTime		The timespan after which an update of the value of the read-only gui elements should be requested
	## @param      idx              The identification number for the connections
	##
	def __init__(self,gui_conn,translator_conn,module_file,updateTime,idx):
		threading.Thread.__init__(self)
		self.gui_conn = gui_conn
		self.translator_conn = translator_conn
		self.id = idx
		self.gui_conn.register(self.id)
		self.translator_conn.register(self.id)
		self.createGuiHardwareDict(module_file)
		self.moduleList = Module.createModules(module_file)

		self.mainTask()
		self.getPeriodicalUpdates(updateTime)
		



	##
	## @brief      To use as decorator to make a function call threaded.
	##
	## @param      fn    The function
	##
	## @return     { description_of_the_return_value }
	##
	def threaded(fn):
		def wrapper(*args, **kwargs):
			thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
			thread.setDaemon(True)
			thread.start()
			return thread
		return wrapper

	##
	## @brief      main loop, periodically calls the 2 functions
	##
	## @param      self  The object
	##
	## @return     None
	##
	@threaded
	def mainTask(self):
		while True:
			self.guiToTranslator()
			self.translatorToGui()

	
	##
	## @brief      Gets the periodical updates of the read-only elements of the gui
	##
	## @param      self        The object
	## @param      updateTime  The update time
	##
	## @return     None
	##
	@threaded
	def getPeriodicalUpdates(self,updateTime):
		while True:
			for i in self.guiToPhyList:
				if i[2] == 5:
					jsonDict = {"module":i[0][0],"command":i[2],"address":i[1][0],"value":0}
					self.translator_conn.send(json.JSONEncoder().encode(jsonDict),self.id)
			time.sleep(updateTime)



	##
	## @brief      Reads the incoming data from gui_conn translates gui-json to phy-json, determines dependant fields, calculates them and sends them via the translator_conn. 
	##
	## @param      self  The object
	##
	## @return     None
	##
	def guiToTranslator(self):
		receivedJSON = self.gui_conn.receive(self.id)
		if receivedJSON != "":
			jsonDict = json.JSONDecoder().decode(receivedJSON)
			element = [x for x in self.guiToPhyList if [x[0][1],x[1][1]] == jsonDict["key"]]
			element = element.pop()
			element[3] = jsonDict["value"]

			jsonDict = [{"module":element[0][0],"command":element[2],"address":element[1][0],"value":element[3]}]
			module = [x for x in self.moduleList if x.moduleName == element[0][1]].pop()
			dependantAddressesAndValues = module.getDependantValues(element[1][1],element[3])
			dependantElements = [x for x in self.guiToPhyList if (x[0][1] == element[0][1] and x[1][1] in [i[0] for i in dependantAddressesAndValues])]
			for i in dependantElements:
				for j in dependantAddressesAndValues:
					if i[1][1] == j[0]:
						jsonDict.append({"module":i[0][0],"command":i[2],"address":i[1][0],"value":j[1]})
						i[3] = j[1]
			for i in jsonDict:
				self.translator_conn.send(json.JSONEncoder().encode(i),self.id)

	##
	## @brief      Reads incoming data from translator_conn and translates phy-json to gui-json, forwards data via gui_conn
	##
	## @param      self  The object
	##
	## @return     None
	##
	def translatorToGui(self):
		receivedJSON = self.translator_conn.receive(self.id)
		if receivedJSON != "":
			jsonDict = json.loads(receivedJSON)
			for i in self.guiToPhyList:
				if jsonDict["module"] == i[0][0] and jsonDict["address"] == i[1][0]:
					i[3] = jsonDict["value"]
					if i[2] == 5:
						jsonDict = {"key":(i[0][1],i[1][1]),"value":i[3]}
						self.gui_conn.send(json.JSONEncoder().encode(jsonDict),self.id)
					break


	##
	## @brief      Creates a gui-hardware dictionary-list which is read from a xml file.
	##
	## @param      self  The object
	##
	## @return     None
	##
	def createGuiHardwareDict(self,module_file):
		self.guiToPhyList = []
		tree = xml.etree.ElementTree.parse(module_file+'.xml')
		root = tree.getroot()
		for module in root.findall('module'):
			name = module.attrib["name"]
			number = int(module.attrib["number"])
			for address in module.findall('address'):
				addrName = address.attrib["name"]
				addrNumber = int(address.attrib["number"])
				command = int(address.find('command').text)
				self.guiToPhyList.append([(number,name),(addrNumber,addrName),command,0])

	## Sample of a possible guiToPhyList
	## self.guiToPhyList = [[(1,"Modem"),(1,"K"),4,0],
	##			[(1,"Modem"),(2,"K-1"),4,0],
	##			[(1,"Modem"),(3,"CP"),4,0],
	##			[(1,"Modem"),(4,"Signal Power"),5,0],
	##			[(2,"MAC"),(1,"MCS"),4,0],
	##			[(2,"MAC"),(2,"FER"),5,0]]
	##
		