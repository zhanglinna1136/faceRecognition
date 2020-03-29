import sys
import MySQLdb
from PyQt5 import QtCore, QtGui, QtWidgets
from guanliyuan_face import Ui_Administrator
from dataset.test import  database

Dao=database.Dao()

class Myguanliyuan(QtWidgets.QWidget,Ui_Administrator):
    def __init__(self, parent=None):
        super(Myguanliyuan, self).__init__(parent)  # 父类的构造函数
        self.sm=[]
        self.setupUi(self)
        self.pushbutton_init()



    def pushbutton_init (self):
         self.query.clicked.connect(self.query_click)
         self.radioButton.toggled.connect(lambda:self.btnstate(self.radioButton))
         self.radioButton_2.toggled.connect(lambda: self.btnstate(self.radioButton_2))
         self.radioButton_3.toggled.connect(lambda: self.btnstate(self.radioButton_3))


    def btnstate(self,btn):
        if btn.text()=="班级":
            if btn.isChecked()==True:
               self.sm=Dao.find_class(self.lineEdit.text())
            else:
               pass
        if btn.text()=="个人":
            if btn.isChecked() == True:
               self.sm=Dao.find_person(self.lineEdit.text())
            else:
               pass
        if btn.text()=="日期":
            if btn.isChecked() == True:
               self.sm=Dao.find_time(self.lineEdit.text())
            else:
               pass

    def query_click (self):
        # sm=self.btnstate()
        self.btnstate(self.radioButton)
        self.btnstate(self.radioButton_2)
        self.btnstate(self.radioButton_3)
        fields=Dao.find_lie()
        self.table(self.sm,fields)
        print(2)
    def table (self,sm,fields):
        """
          查询学生签到表
          db-数据库连接
          c-数据表行数
          cursor-游标
          head-存放表头的list
          table1_表格显示界面
          sm行数
          fields 列数

          :return:
          """
        k = 0
        for c in sm:  # 获取行数第二种办法
            k = k + 1
        head = []
        # 或取数据库中表头
        for field in fields:
            head.append(field[0])
        self.table1.setRowCount(k)  # 设置表格行数
        self.table1.setColumnCount(len(head))  # 设置表格列数，即表头的个数
        self.table1.setHorizontalHeaderLabels(head)  # 设置表头
        # self.table1.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  # 使表格适应界面
        self.table1.setColumnWidth(0, 50)
        self.table1.setColumnWidth(1, 100)
        self.table1.setColumnWidth(2, 100)
        self.table1.setColumnWidth(3, 150)
        self.table1.setColumnWidth(4, 200)
        self.table1.verticalHeader().setVisible(False)  # 隐藏垂直表头
        self.table1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # QtWidgets.QTableWidget.resizeColumnsToContents(self.table1)
        # QtWidgets.QTableWidget.resizeRowsToContents(self.table1)
        a = 0
        # 将数据库中的表格元素显示在界面
        for t in sm:  # 行
            d = 0
            for b in t:  # 列
                newItem = QtWidgets.QTableWidgetItem(str(b))
                newItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)  # 文本内容居中对齐
                self.table1.setItem(a, d, newItem)
                d = d + 1
            a = a + 1
        # cursor.close()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui=Myguanliyuan()
    ui.show()
    sys.exit(app.exec_())


