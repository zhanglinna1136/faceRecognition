import sys
import cv2
import Check_in
from Check_in import Ui_Check_in
from PyQt5 import QtCore, QtGui, QtWidgets
from threading import *


# thstop=False#控制线程的结束

class mywindow(QtWidgets.QWidget, Ui_Check_in):
    def __init__(self, parent=None):
        super(mywindow, self).__init__(parent)  # 继承父类的构造函数

        self.CAM_NUM = 0  # 为0时表示视频流来自笔记本内置摄像头
        self.cap = cv2.VideoCapture()  # 创建一个VideoCapture对象

        self.setupUi(self)
        self.solt()

    def solt(self):
        self.qiandao.clicked.connect(self.openCamera)
        self.exit.clicked.connect(self.Exit)

    def openCamera(self):
        flag = self.cap.open(self.CAM_NUM)
        if flag == True:
            while True:
                flag, self.image = self.cap.read()  # flag存储定时器的状态，布尔值，image存储图像
                if flag == False:  # 如果读取失败，进行下次循环，再读一次
                    continue
                self.show = cv2.resize(self.image, (320, 240))  # 设置读取的帧数为320*240
                self.show = cv2.cvtColor(self.show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
                self.show = cv2.flip(self.show, 1, dst=None)  # 进行水平镜像处理，即摄像头中的方向和现实中的方向相同
                self.showImage = QtGui.QImage(self.show.data, self.show.shape[1], self.show.shape[0],
                                              QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
                self.camera.setPixmap(QtGui.QPixmap.fromImage(self.showImage))
                cv2.waitKey(1)  # 延时1ms读取一帧显示

    def Exit(self):
        self.cap.release()  # 释放视频流
        sys.exit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # 固定的，表示程序应用
    ui = mywindow()
    ui.show()
    sys.exit(app.exec_())
