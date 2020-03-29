import cv2
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from show_Camera import Ui_MainWindow
# from object.user import User
from object.Python.feature import *  # feature中导入了user
from detection.test.mtcnnDetection import *

user = User("", "", "")  # user对象,用于向后台提供数据包
# photos = []  # 用于存放照片（两张）
threshold = 0.99  # 人脸检测的阈值


class mywindow(QtWidgets.QWidget, Ui_MainWindow):
    def __init__(self, parent=None):
        super(mywindow, self).__init__(parent)  # 父类的构造函数
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.cap = cv2.VideoCapture()  # 创建一个VideoCapture对象
        self.CAM_NUM = 0  # 为0时表示视频流来自笔记本内置摄像头
        self.count = 0  # 用于记录“拍照”被点击的次数

        self.setupUi(self)  # 初始化程序界面
        self.slot_init()  # 初始化槽函数

    def slot_init(self)
        self.openCamera.clicked.connect(self.openCameraClicked)  # 如果该键被点击，就调用openCameraClicked函数
        self.timer_camera.timeout.connect(self.show_camera)  # 如果定时器结束，就调用show——camera显示图像
        self.TakePicture.clicked.connect(self.take_pictures)  # 如果拍照键被点击，调用take_pictures进行拍照
        self.nameInput.returnPressed.connect(self.input_name)  # 如果输入完成，调用input_name函数(returnPressed：当点击回车时事件触发)
        self.idInput.returnPressed.connect(self.input_id)  # 如果输入完成，调用input_id函数
        self.signin.clicked.connect(self.sign_in)  # 点击注册按钮时，调用sign_in函数

    # 打开或关闭定时器

    def openCameraClicked(self):
        if self.timer_camera.isActive() == False:  # 如果定时器未启动
            flag = self.cap.open(self.CAM_NUM)  # 打开笔记本内置摄像头
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, 'warning', "请检查相机于电脑是否连接正确", buttons=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头取一帧显示
                self.openCamera.setText("关闭摄像头")

        else:
            self.timer_camera.stop()  # 关闭定时器
            self.cap.release()  # 释放视频流
            self.SHOW.clear()  # 清空视频显示区域
            self.openCamera.setText("打开摄像头")

    # 调用摄像头

    def show_camera(self):

        flag, self.image = self.cap.read()  # 从视频流读取定时器的状态,flag存储定时器的状态，布尔值，image存储图像

        self.show = cv2.resize(self.image, (320, 240))  # 设置读取的帧数为320*240
        self.show = cv2.cvtColor(self.show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        self.show = cv2.flip(self.show, 1, dst=None)  # 进行水平镜像处理，即摄像头中的方向和现实中的方向相同
        self.showImage = QtGui.QImage(self.show.data, self.show.shape[1], self.show.shape[0],
                                      QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.SHOW.setPixmap(QtGui.QPixmap.fromImage(self.showImage))  # 在lable中显示视频

    # 进行拍照
    def take_pictures(self):
        photo = []
        if self.timer_camera.isActive() == False:  # 如果摄像头未开启
            msg = QtWidgets.QMessageBox.warning(self, 'warning', "请打开摄像头", buttons=QtWidgets.QMessageBox.Ok)
        else:
            if self.count % 2 == 0:
                self.showpictures.setPixmap(QtGui.QPixmap.fromImage(self.showImage))
                user.photos.append(self.show)
                test = photo_calculation_and_processing(self.show, threshold)
                # print(test)
                if test is False:  # 如果人脸检测失败，重新拍照
                    print(test)
                    msg = QtWidgets.QMessageBox.warning(self, "警告", "请重新拍照", buttons=QtWidgets.QMessageBox.Ok)
                else:
                    print(test)
                    self.count += 1
            else:
                self.showpictures2.setPixmap(QtGui.QPixmap.fromImage(self.showImage))
                self.count += 1
                user.photos.append(self.show)

    # 输入姓名

    def input_name(self):
        self.n = self.nameInput.text()  # 输入姓名
        user.name = self.n
        # print(user.name)

    # 输入学号

    def input_id(self):
        self.i = self.idInput.text()  # 输入学号
        user.stuId = self.i
        # print(user.id)

    # 注册
    def sign_in(self):
        if self.nameInput.text() == "":
            msg1 = QtWidgets.QMessageBox.warning(self, '警告', "请输入姓名", buttons=QtWidgets.QMessageBox.Ok)
        elif self.idInput.text() == "":
            msg2 = QtWidgets.QMessageBox.warning(self, '警告', "请输入学号", buttons=QtWidgets.QMessageBox.Ok)
        elif self.nameInput.text() != "" and self.idInput.text() != "":
            test1 = feature.Feature(user)
            testDAO = DAO(test1)
            try:
                testDAO.ppandFeatureInfo(testDAO)
                msg3 = QtWidgets.QMessageBox.information(self, '提示信息', '注册成功')
            finally:
                testDAO.closedb()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # 固定的，表示程序应用
    ui = mywindow()  # 实例化Ui_MainWindow
    ui.show()  # 调用ui的show()以显示。同样show()是源于父类QtWidgets.QWidget的
    sys.exit(app.exec_())  # 不加这句，程序界面会一闪而过
