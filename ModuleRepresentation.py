# -*- coding: utf-8 -*-

#The purpose of this class is on the one hand to save some calculations on the FPGA by performing them remotely and
#on the other hand objects of this class are intended to be a representation of the computing blocks of the FPGA and are used 
#by the decode-logic to determine the dependencies between values which are of interest to the user and the ones which
#are not. The dependencies can be given directly as a list of json objects, or the class method create_ids() reads them from a file.
import json


class Module:
	def __init__(self,moduleName, id_dependencies):
		self.moduleName = moduleName
		self.__id_dependencies = id_dependencies


	@classmethod
	def createModules(Module,dependency_file):
		moduleObjectList = []
		file_content = open(dependency_file,"r").read()
		file_content = file_content.split("\n")
		for i in range(len(file_content)):
			a = file_content[i].find("#")										#remove all the comments at first
			if a != -1:
				file_content[i] = file_content[i][:a]
			file_content[i] = file_content[i].strip()							#remove all the remaining whitespaces at the end

		file_content = list(filter(lambda x : x != "",file_content))			#delete all elements which are empty

		for i in range(len(file_content)):
			moduleName = ""
			json_list = []
			if file_content[i][0] == "@":
				moduleName = file_content[i][1:]
				for j in range(i+1,len(file_content)):
					if file_content[j][0] == "{":
						json_list.append(json.loads(file_content[j]))
					if file_content[j][0]== "@" or j==len(file_content)-1:
						if json_list != []:
							moduleObjectList.append(Module(moduleName,json_list))
						break
		return moduleObjectList


#This method returns a list of tuples, of which the first entry is the address and the second is the calculated value.
#If the returned list is empty, than there are no dependencies for the given address.
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
		