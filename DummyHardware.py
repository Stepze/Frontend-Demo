# -*-  coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from threading import Thread
import struct
import random
import time


class DummyHardware(QtCore.QThread):
	recvSignal = QtCore.pyqtSignal()
	sentSignal = QtCore.pyqtSignal()


	def __init__(self,u64_conn,idx):
		QtCore.QThread.__init__(self)
		self.qtWindow = hardwareGui(self)
		self.recvSignal.connect(self.qtWindow.updateReceivedU64)
		self.sentSignal.connect(self.qtWindow.updateSentU64)
		self.qtWindow.show()
		self.u64_conn = u64_conn
		self.id = idx
		self.u64_conn.register(self.id)
		self.dictStorage = []
		self.start()

	
	def run(self):
		while True:
			u64 = self.u64_conn.receive(self.id)
			if u64 != "":
				u64_decoded = self.u64_to_json(u64)
				self.a = '{0:064b}'.format(int.from_bytes(u64,byteorder="big"))
				self.b = str(u64_decoded)

				self.recvSignal.emit()

				if u64_decoded["command"] == 5:
					u64 = '{0:02b}'.format(0)
					u64 += '{0:07b}'.format(u64_decoded["module"])
					u64 += '{0:02b}'.format(0)
					u64 += '{0:04b}'.format(u64_decoded["command"])
					u64 += '{0:01b}'.format(0)
					u64 += '{0:016b}'.format(u64_decoded["address"])
					u64 += '{0:032b}'.format(random.randint(1,100000))
					self.a = u64
					u64 = int(u64,2).to_bytes(len(u64)//8,byteorder="big")
					self.b = str(self.u64_to_json(u64))
					self.u64_conn.send(u64,self.id)

					self.sentSignal.emit()

			time.sleep(0.1)



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




class hardwareGui(QtWidgets.QMainWindow):
	def __init__(self,parent):
		self.parent = parent
		QtWidgets.QMainWindow.__init__(self)
		self.resize(1072, 459)
		self.centralwidget = QtWidgets.QWidget()
		self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
		self.sentGroupBox = QtWidgets.QGroupBox(self.centralwidget)
		self.gridLayout_2 = QtWidgets.QGridLayout(self.sentGroupBox)
		self.scrollSentRaw = QtWidgets.QScrollArea(self.sentGroupBox)
		self.scrollSentRaw.setWidgetResizable(True)
		self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
		self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 245, 395))
		self.gridLayout_6 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
		self.textEdit_3 = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents_2)
		self.textEdit_3.setReadOnly(True)
		self.textEdit_3.setMaximumBlockCount(10)
		self.gridLayout_6.addWidget(self.textEdit_3, 1, 0, 1, 1)
		self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
		self.gridLayout_6.addWidget(self.label_3, 0, 0, 1, 1)
		self.scrollSentRaw.setWidget(self.scrollAreaWidgetContents_2)
		self.gridLayout_2.addWidget(self.scrollSentRaw, 0, 0, 1, 1)
		self.scrollSentDecoded = QtWidgets.QScrollArea(self.sentGroupBox)
		self.scrollSentDecoded.setWidgetResizable(True)
		self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
		self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 245, 395))
		self.gridLayout_7 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_3)
		self.textEdit_4 = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents_3)
		self.textEdit_4.setReadOnly(True)
		self.textEdit_4.setMaximumBlockCount(10)
		self.gridLayout_7.addWidget(self.textEdit_4, 1, 0, 1, 1)
		self.label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
		self.gridLayout_7.addWidget(self.label_4, 0, 0, 1, 1)
		self.scrollSentDecoded.setWidget(self.scrollAreaWidgetContents_3)
		self.gridLayout_2.addWidget(self.scrollSentDecoded, 0, 1, 1, 1)
		self.gridLayout.addWidget(self.sentGroupBox, 0, 1, 1, 1)
		self.receivedGroupBox = QtWidgets.QGroupBox(self.centralwidget)
		self.gridLayout_3 = QtWidgets.QGridLayout(self.receivedGroupBox)
		self.scrollReceivedRaw = QtWidgets.QScrollArea(self.receivedGroupBox)
		self.scrollReceivedRaw.setWidgetResizable(True)
		self.scrollAreaWidgetContents = QtWidgets.QWidget()
		self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 245, 395))
		self.gridLayout_4 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
		self.textEdit = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents)
		self.textEdit.setReadOnly(True)
		self.textEdit.setMaximumBlockCount(10)
		self.gridLayout_4.addWidget(self.textEdit, 1, 0, 1, 1)
		self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)
		self.scrollReceivedRaw.setWidget(self.scrollAreaWidgetContents)
		self.gridLayout_3.addWidget(self.scrollReceivedRaw, 0, 0, 1, 1)
		self.scrollReceivedDecoded = QtWidgets.QScrollArea(self.receivedGroupBox)
		self.scrollReceivedDecoded.setWidgetResizable(True)
		self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
		self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 245, 395))
		self.gridLayout_5 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_4)
		self.textEdit_2 = QtWidgets.QPlainTextEdit(self.scrollAreaWidgetContents_4)
		self.textEdit_2.setReadOnly(True)
		self.textEdit_2.setMaximumBlockCount(10)
		self.gridLayout_5.addWidget(self.textEdit_2, 1, 0, 1, 1)
		self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
		self.gridLayout_5.addWidget(self.label_2, 0, 0, 1, 1)
		self.scrollReceivedDecoded.setWidget(self.scrollAreaWidgetContents_4)
		self.gridLayout_3.addWidget(self.scrollReceivedDecoded, 0, 1, 1, 1)
		self.gridLayout.addWidget(self.receivedGroupBox, 0, 0, 1, 1)
		self.setCentralWidget(self.centralwidget)


	def updateReceivedU64(self):
		self.textEdit_3.appendPlainText(self.parent.a)
		self.textEdit_4.appendPlainText(self.parent.b)
		
	def updateSentU64(self):
		self.textEdit.appendPlainText(self.parent.a)
		self.textEdit_2.appendPlainText(self.parent.b)

