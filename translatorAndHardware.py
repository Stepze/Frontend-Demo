# -*- coding:utf-8 -*-
from DirectConnection import DirectConnection
from UdpConnection import UdpConnection
from U64JsonTranslator import U64JsonTranslator
from DummyHardware import DummyHardware

import time
import sys
import PyQt5.QtWidgets

##
## @brief      this function starts the dummy-hardware and the U64-JSON-translator
## @brief      connection between dummy-hardware and the translator is direct, the connection between translator and 
## @brief      application logic is done via udp
##
## @return     None
##
def main():
	transToHard = DirectConnection()
	appToTrans = UdpConnection("127.0.0.1",40001,40000)
	trans = U64JsonTranslator(transToHard,appToTrans,3)
	app = PyQt5.QtWidgets.QApplication(sys.argv)
	hard = DummyHardware(transToHard,4)
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()
