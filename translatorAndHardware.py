# -*- coding:utf-8 -*-
from DirectConnection import DirectConnection
from UdpConnection import UdpConnection
from U64JsonTranslator import U64JsonTranslator
from DummyHardware import DummyHardware

import time


def main():
	
	transToHard = DirectConnection()
	appToTrans = UdpConnection("127.0.0.1",40001,40000)
	trans = U64JsonTranslator(transToHard,appToTrans,3)
	hard = DummyHardware(transToHard,4)
	while True:
		time.sleep(1)


if __name__ == "__main__":
	main()
