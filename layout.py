# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import timeit

class Ui_FrontendTest(QtWidgets.QMainWindow):
    def __init__(self, parent):
        self.start = timeit.default_timer()
        QtWidgets.QMainWindow.__init__(self)
        self.parent = parent
        self.resize(755, 419)
        self.centralwidget = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.gridLayout_2.addWidget(self.lineEdit, 4, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.groupBox_3.setTitle("")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.checkBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.gridLayout_3.addWidget(self.checkBox, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.spinBox_2 = QtWidgets.QSpinBox(self.groupBox_3)
        self.gridLayout_3.addWidget(self.spinBox_2, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_3, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.groupBox)
        self.gridLayout_2.addWidget(self.spinBox, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_2)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)
        self.spinBox_3 = QtWidgets.QSpinBox(self.groupBox_2)
        self.gridLayout_4.addWidget(self.spinBox_3, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.gridLayout_4.addWidget(self.label_5, 2, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_2.setReadOnly(True)
        self.gridLayout_4.addWidget(self.lineEdit_2, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 2)
        self.setCentralWidget(self.centralwidget)
       	
       	self.setWindowTitle("FPGA Frontend Test")
        self.groupBox.setTitle("Modem Module")
        self.checkBox.setText("use 1/4 K")
        self.label_2.setText("CP")
        self.label_3.setText("Signal Power")
        self.label.setText("K")
        self.groupBox_2.setTitle("MAC Module")
        self.label_4.setText("MCS")
        self.label_5.setText("FER")
        self.pushButton.setText("Refresh")
        self.pushButton.clicked.connect(self.refresh)

        if self.parent != "test":
        	self.parent.announceGuiElement(("Modem","K"),self.spinBox)
        	self.parent.announceGuiElement(("Modem","1/4K"),self.checkBox)
        	self.parent.announceGuiElement(("Modem","CP"),self.spinBox_2)
        	self.parent.announceGuiElement(("Modem","Signal Power"),self.lineEdit)
        	self.parent.announceGuiElement(("MAC","MCS"),self.spinBox_3)
        	self.parent.announceGuiElement(("MAC","FER"),self.lineEdit_2)
        self.stop = timeit.default_timer()
        print(str(self.stop-self.start)+" endInit")


    def refresh(self):
    	self.parent.refreshRequested = True


if __name__=="__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = Ui_FrontendTest("test")
	window.show()
	sys.exit(app.exec_())




