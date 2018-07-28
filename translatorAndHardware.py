# -*- coding:utf-8 -*-
from DirectConnection import DirectConnection
from UdpConnection import UdpConnection
from U64JsonTranslator import U64JsonTranslator
from DummyHardware import DummyHardware

import time
import sys
import PyQt5.QtWidgets


def main():
	transToHard = DirectConnection()
	appToTrans = UdpConnection("127.0.0.1",40001,40000)
	trans = U64JsonTranslator(transToHard,appToTrans,3)
	app = PyQt5.QtWidgets.QApplication(sys.argv)
	hard = DummyHardware(transToHard,4)
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()
