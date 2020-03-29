# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Check_in.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Check_in(object):
    def setupUi(self, Check_in):
        Check_in.setObjectName("Check_in")
        Check_in.resize(982, 600)
        font = QtGui.QFont()
        font.setFamily("华文宋体")
        Check_in.setFont(font)
        self.centralwidget = QtWidgets.QWidget(Check_in)
        self.centralwidget.setObjectName("centralwidget")
        self.qiandao = QtWidgets.QPushButton(self.centralwidget)
        self.qiandao.setGeometry(QtCore.QRect(10, 380, 93, 31))
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
        self.exit.setGeometry(QtCore.QRect(150, 380, 93, 31))
        self.exit.setObjectName("exit")
        self.photo = QtWidgets.QLabel(self.centralwidget)
        self.photo.setGeometry(QtCore.QRect(341, 340, 201, 161))
        self.photo.setObjectName("photo")
        self.zhuche = QtWidgets.QPushButton(self.centralwidget)
        self.zhuche.setGeometry(QtCore.QRect(10, 440, 93, 28))
        self.zhuche.setObjectName("zhuche")
        self.find = QtWidgets.QPushButton(self.centralwidget)
        self.find.setGeometry(QtCore.QRect(150, 440, 93, 28))
        self.find.setObjectName("find")
        # Check_in.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Check_in)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 982, 26))
        self.menubar.setObjectName("menubar")
        # Check_in.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Check_in)
        self.statusbar.setObjectName("statusbar")
        # Check_in.setStatusBar(self.statusbar)

        self.retranslateUi(Check_in)
        QtCore.QMetaObject.connectSlotsByName(Check_in)

    def retranslateUi(self, Check_in):
        _translate = QtCore.QCoreApplication.translate
        Check_in.setWindowTitle(_translate("Check_in", "MainWindow"))
        self.qiandao.setText(_translate("Check_in", "签到"))
        self.camera.setText(_translate("Check_in", "摄像头"))
        self.label.setText(_translate("Check_in", "签到情况"))
        self.exit.setText(_translate("Check_in", "退出"))
        self.photo.setText(_translate("Check_in", "照片"))
        self.zhuche.setText(_translate("Check_in", "注册"))
        self.find.setText(_translate("Check_in", "查询"))
