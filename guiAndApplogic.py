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
	start = timeit.default_timer()
	guictrl = QtGuiController("layout",guiToApp,1)
	stop = timeit.default_timer()
	print(str(stop-start)+" guictrl")

	applgc = ApplicationLogic(guiToApp,appToTrans,"moduleFile",1,2)
	
	sys.exit(app.exec_())
	


if __name__ == "__main__":
	main()
