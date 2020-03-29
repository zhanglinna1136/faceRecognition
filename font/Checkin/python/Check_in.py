# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Check_in.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Check_in(object):
    def setupUi(self, Check_in):
        Check_in.setObjectName("Check_in")
        Check_in.resize(982, 600)
        self.centralwidget = QtWidgets.QWidget(Check_in)
        self.centralwidget.setObjectName("centralwidget")
        self.qiandao = QtWidgets.QPushButton(self.centralwidget)
        self.qiandao.setGeometry(QtCore.QRect(10, 380, 93, 28))
        self.qiandao.setObjectName("qiandao")
        self.camera = QtWidgets.QLabel(self.centralwidget)
        self.camera.setGeometry(QtCore.QRect(10, 80, 261, 231))
        self.camera.setObjectName("camera")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(330, 80, 641, 231))
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(580, 50, 72, 15))
        self.label.setObjectName("label")
        self.exit = QtWidgets.QPushButton(self.centralwidget)
        self.exit.setGeometry(QtCore.QRect(150, 380, 93, 28))
        self.exit.setObjectName("exit")
        #Check_in.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Check_in)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 982, 26))
        self.menubar.setObjectName("menubar")
        #Check_in.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Check_in)
        self.statusbar.setObjectName("statusbar")
        #Check_in.setStatusBar(self.statusbar)

        self.retranslateUi(Check_in)
        QtCore.QMetaObject.connectSlotsByName(Check_in)

    def retranslateUi(self, Check_in):
        _translate = QtCore.QCoreApplication.translate
        Check_in.setWindowTitle(_translate("Check_in", "MainWindow"))
        self.qiandao.setText(_translate("Check_in", "签到"))
        self.camera.setText(_translate("Check_in", "摄像头"))
        self.label.setText(_translate("Check_in", "签到情况"))
        self.exit.setText(_translate("Check_in", "退出"))

