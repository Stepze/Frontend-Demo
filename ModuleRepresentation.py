# -*- coding: utf-8 -*-

import json
import xml.etree.ElementTree

##
## @detailed    The purpose of this class is on the one hand to save some calculations on the FPGA by performing them remotely and
## @detailed	on the other hand objects of this class are intended to be a representation of the computing blocks of the FPGA and are used 
## @detailed	by the decode-logic to determine the dependencies between values which are of interest to the user and the ones which
## @detailed	are not. The dependencies can be given directly as a list of json objects, or the class method createModules() reads them from a file.
##
class Module:
	def __init__(self,moduleName, id_dependencies):
		self.moduleName = moduleName
		self.__id_dependencies = id_dependencies

	##
	## @brief      class method, which creates a list of instances of this class according to a input file
	##
	## @param      Module           necessary for the method to know of which class it is a class method
	## @param      dependencyFile   The input file
	##
	## @return     list of Module-objects
	##
	@classmethod
	def createModules(Module,dependencyFile):
		moduleObjectList = []
		tree = xml.etree.ElementTree.parse(dependencyFile+'.xml')
		root = tree.getroot()
		for module in root.findall("module"):
			jsonList = []
			for address in module.findall("address"):
				addrName = address.attrib["name"]
				jsonObj = "{\"address\": \""+addrName+"\","
				tester = jsonObj[:-1]+"}"
				for dependency in address.findall("dependency"):
					target = str(dependency.attrib["target"])
					dep = str(dependency.text)
					jsonObj += "\""+target+"\": "+dep+","
				jsonObj = jsonObj[:-1]+"}"
				if jsonObj != tester:
					jsonList.append(json.loads(jsonObj))

			moduleObjectList.append(Module(module.attrib["name"],jsonList))
			

		return moduleObjectList


	##
	## @brief      This method returns a list of tuples, of which the first entry is the address and the second is the calculated value.
	## @brief      If the returned list is empty, than there are no dependencies for the given address.
	##
	## @param      self     The object
	## @param      address  The address
	## @param      value    The value
	##
	## @return     list of tuples
	##
	def getDependantValues(self,address,value):
		return_list = []
		for i in self.__id_dependencies:
			if i.get("address") == address:
				for idy,dependency in i.items():
					if dependency == "+1":
						return_list.append((idy,value+1))
					elif dependency == "-1":
						return_list.append((idy,value-1))
					elif dependency == "/2":
						return_list.append((idy,value/2))
					#and so on


		return return_list
		