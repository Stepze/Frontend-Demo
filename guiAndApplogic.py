# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
import sys
from QtGuiController import QtGuiController
from DirectConnection import DirectConnection
from UdpConnection import UdpConnection
from ApplicationLogic import ApplicationLogic

import timeit


def main():
	
	app = QApplication(sys.argv)
	guiToApp = DirectConnection()
	appToTrans = UdpConnection("127.0.0.1",40000,40001)
	guictrl = QtGuiController("layout",guiToApp,1)

	applgc = ApplicationLogic(guiToApp,appToTrans,"ModuleFile",5,2)
	
	sys.exit(app.exec_())
	


if __name__ == "__main__":
	main()
