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
		self.centralwidget = QtWidgets.QWidget()
		self.setCentralWidget(self.centralwidget)
		self.layout = QtWidgets.QGridLayout()
		self.centralwidget.setLayout(self.layout)
		
		self.receivedBox = QtWidgets.QGroupBox("received")
		self.receivedLayout = QtWidgets.QGridLayout()
		self.receivedBox.setLayout(self.receivedLayout)
		self.binaryTextrecvd = QtWidgets.QPlainTextEdit()
		self.binaryTextrecvd.setReadOnly(True)
		self.receivedLayout.addWidget(self.binaryTextrecvd,0,0)
		self.decodedTextrecvd = QtWidgets.QPlainTextEdit()
		self.decodedTextrecvd.setReadOnly(True)
		self.receivedLayout.addWidget(self.decodedTextrecvd,1,0)

		self.sentBox = QtWidgets.QGroupBox("sent")
		self.sentlayout = QtWidgets.QGridLayout()
		self.sentBox.setLayout(self.sentlayout)
		self.binaryTextSent = QtWidgets.QPlainTextEdit()
		self.binaryTextSent.setReadOnly(True)
		self.sentlayout.addWidget(self.binaryTextSent,0,0)
		self.decodedTextSent = QtWidgets.QPlainTextEdit()
		self.decodedTextSent.setReadOnly(True)
		self.sentlayout.addWidget(self.decodedTextSent,1,0)

		self.layout.addWidget(self.receivedBox,0,0)
		self.layout.addWidget(self.sentBox,1,0)
		self.resize(self.sizeHint())


	def updateReceivedU64(self):
		if self.binaryTextrecvd.blockCount() > 10:
			cursor1 = self.binaryTextrecvd.textCursor()
			cursor1.movePosition(QtGui.QTextCursor.Start)
			cursor1.movePosition(QtGui.QTextCursor.Down, QtGui.QTextCursor.MoveAnchor,0)
			cursor1.select(QtGui.QTextCursor.LineUnderCursor)
			cursor1.removeSelectedText()
			cursor1.deleteChar()
			cursor2 = self.decodedTextrecvd.textCursor()
			cursor2.movePosition(QtGui.QTextCursor.Start)
			cursor2.movePosition(QtGui.QTextCursor.Down, QtGui.QTextCursor.MoveAnchor,0)
			cursor2.select(QtGui.QTextCursor.LineUnderCursor)
			cursor2.removeSelectedText()
			cursor2.deleteChar()
		self.binaryTextrecvd.appendPlainText(self.parent.a)
		self.decodedTextrecvd.appendPlainText(self.parent.b)
		
	def updateSentU64(self):
		if self.binaryTextSent.blockCount() > 10:
			cursor1 = self.binaryTextSent.textCursor()
			cursor1.movePosition(QtGui.QTextCursor.Start)
			cursor1.movePosition(QtGui.QTextCursor.Down, QtGui.QTextCursor.MoveAnchor,0)
			cursor1.select(QtGui.QTextCursor.LineUnderCursor)
			cursor1.removeSelectedText()
			cursor1.deleteChar()
			cursor2 = self.decodedTextSent.textCursor()
			cursor2.movePosition(QtGui.QTextCursor.Start)
			cursor2.movePosition(QtGui.QTextCursor.Down, QtGui.QTextCursor.MoveAnchor,0)
			cursor2.select(QtGui.QTextCursor.LineUnderCursor)
			cursor2.removeSelectedText()
			cursor2.deleteChar()
		self.binaryTextSent.appendPlainText(self.parent.a)
		self.decodedTextSent.appendPlainText(self.parent.b)

