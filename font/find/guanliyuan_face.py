# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guanliyuan_face.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Administrator(object):
    def setupUi(self, Administrator):
        Administrator.setObjectName("Administrator")
        Administrator.resize(861, 622)
        Administrator.setTabletTracking(False)
        self.centralwidget = QtWidgets.QWidget(Administrator)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(430, 490, 72, 15))
        self.label.setObjectName("label")
        self.table1 = QtWidgets.QTableWidget(self.centralwidget)
        self.table1.setGeometry(QtCore.QRect(210, 50, 600, 411))
        self.table1.setGridStyle(QtCore.Qt.SolidLine)
        self.table1.setObjectName("table1")
        self.table1.setColumnCount(0)
        self.table1.setRowCount(0)
        self.table1.horizontalHeader().setCascadingSectionResizes(False)
        self.table1.horizontalHeader().setSortIndicatorShown(False)
        self.table1.horizontalHeader().setStretchLastSection(False)
        self.table1.verticalHeader().setCascadingSectionResizes(False)
        self.table1.verticalHeader().setSortIndicatorShown(False)
        self.table1.verticalHeader().setStretchLastSection(False)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 60, 141, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.query = QtWidgets.QPushButton(self.centralwidget)
        self.query.setGeometry(QtCore.QRect(120, 90, 51, 31))
        self.query.setObjectName("query")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(30, 130, 115, 19))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(30, 160, 115, 19))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_3.setGeometry(QtCore.QRect(30, 190, 115, 19))
        self.radioButton_3.setObjectName("radioButton_3")
        self.fanhui = QtWidgets.QPushButton(self.centralwidget)
        self.fanhui.setGeometry(QtCore.QRect(20, 250, 93, 28))
        self.fanhui.setObjectName("fanhui")
        # Administrator.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Administrator)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 861, 26))
        self.menubar.setObjectName("menubar")
        # Administrator.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Administrator)
        self.statusbar.setObjectName("statusbar")
        # Administrator.setStatusBar(self.statusbar)

        self.retranslateUi(Administrator)
        QtCore.QMetaObject.connectSlotsByName(Administrator)

    def retranslateUi(self, Administrator):
        _translate = QtCore.QCoreApplication.translate
        Administrator.setWindowTitle(_translate("Administrator", "MainWindow"))
        self.label.setText(_translate("Administrator", "显示界面"))
        self.query.setText(_translate("Administrator", "查询"))
        self.radioButton.setText(_translate("Administrator", "班级"))
        self.radioButton_2.setText(_translate("Administrator", "个人"))
        self.radioButton_3.setText(_translate("Administrator", "日期"))
        self.fanhui.setText(_translate("Administrator", "主界面"))
