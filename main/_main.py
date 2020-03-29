import sys
import cv2
import threading
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from detection.Python import mtcnnDetection
from font.Checkin.Check_in import Ui_Check_in
from font.Take_pictures.show_Camera import Ui_MainWindow
from object.Python.user import User
from object.Python import feature, user
from dataset.Python.database import Dao
from font.find.guanliyuan_face import Ui_Administrator

Dao = Dao()

user = User("", "", "")  # user对象,用于向后台提供数据包
photos = []  # 用于存放照片（两张）
threshold = 0.99  # 人脸检测的阈值


class mywindow(QtWidgets.QWidget, Ui_Check_in):
    def __init__(self, parent=None):
        super(mywindow, self).__init__(parent)  # 继承父类的构造函数

        self.CAM_NUM = 0  # 为0时表示视频流来自笔记本内置摄像头
        self.cap = cv2.VideoCapture()  # 创建一个VideoCapture对象

        self.setupUi(self)
        self.solt()

    def solt(self):
        self.zhuche.clicked.connect(self.tiao)
        self.find.clicked.connect(self.tiao2)
        self.qiandao.clicked.connect(self.thread_)
        self.exit.clicked.connect(self.Exit)

    # 打开摄像头，捕捉人脸
    def openCamera(self):
        global image
        flag = self.cap.open(self.CAM_NUM)
        if flag == True:  # 如果摄像头打开正常
            while True:
                flag, image = self.cap.read()  # flag存储读取的状态，布尔值，image存储图像
                # if flag == False:  # 如果读取失败，进行下次循环，再读一次
                #     continue
                self.show = cv2.resize(image, (320, 240))  # 设置读取的帧数为320*240
                self.show = cv2.cvtColor(self.show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
                self.show = cv2.flip(self.show, 1, dst=None)  # 进行水平镜像处理，即摄像头中的方向和现实中的方向相同
                self.showImage = QtGui.QImage(self.show.data, self.show.shape[1], self.show.shape[0],
                                              QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
                self.camera.setPixmap(QtGui.QPixmap.fromImage(self.showImage))
                cv2.waitKey(1)  # 延时1ms读取一帧显示
                # faceCheck = mtcnnDetection.photo_calculation_and_processing(image, threshold)
                # if (faceCheck != False):
                #     global photos  # Feature里面的createFeature的参数必须是列表，所以每检测到一张人脸就添加到photos列表中
                #     photos.append(image)
                #     time.sleep(3)
                # else:
                #     print("未检测到人脸")

    # 人脸检测和计算人脸特征点
    def faceRecognition2(self):
        while True:
            faceCheck = mtcnnDetection.photo_calculation_and_processing(image, threshold)
            if (faceCheck != False):
                photos = []  # Feature里面的createFeature的参数必须是列表，所以每检测到一张人脸就添加到photos列表中
                photos.append(image)
                test = feature.Feature(False, photos)
                print(test.embeddings)
                test.embeddings = self.reduceDimen(test.embeddings)  # 将三维列表降为一维列表
                print(test.embeddings)
                result = test.calculateDistance(test.embeddings)
                if result is None:
                    msg1 = QtWidgets.QMessageBox.information(self, '提示信息', '签到失败，请重新签到')
                else:
                    # msg2 = QtWidgets.QMessageBox.information(self, '提示信息', '签到成功')
                    print(result)

            else:
                print("未检测到人脸")

    # 把三维列表降维一维列表
    def reduceDimen(self, list):
        result = []
        for i in list:
            for j in i:
                for k in j:
                    result.append(k)
        return result

    def Exit(self):
        self.cap.release()  # 释放视频流
        sys.exit()

    # 多线程运行人脸检测和人脸识别
    def thread_(self):
        t1 = threading.Thread(target=self.openCamera)  # 线程1，进行人脸的捕捉
        t2 = threading.Thread(target=self.faceRecognition2)  # 线程2，进行人脸的比对
        # while True:
        t1.start()
        time.sleep(3)  # 线程2必须要在线程1开启之后才能开启，因为线程2需要用到线程1所捕捉到的人脸
        # t1.join()
        t2.start()
        # t2.join()

    def tiao(self):
        self.hide()
        self.dia = mywindow2()
        self.dia.show()
        # self.dia.fanhui.clicked.connect(self.dia.fan)

    def tiao2(self):
        self.hide()
        self.dia2 = Myguanliyuan()
        self.dia2.show()


class mywindow2(QtWidgets.QWidget, Ui_MainWindow):  # 继承QtWidgets.QWidget, Ui_MainWindow
    def __init__(self, parent=None):
        super(mywindow2, self).__init__(parent)  # 继承父类的构造函数

        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.cap = cv2.VideoCapture()  # 创建一个VideoCapture对象
        self.CAM_NUM = 0  # 为0时表示视频流来自笔记本内置摄像头
        self.count = 0  # 用于记录“拍照”被点击的次数

        self.setupUi(self)  # 初始化程序界面
        self.slot_init()  # 初始化槽函数

    def slot_init(self):
        self.fanhui.clicked.connect(self.fan)
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
        if self.timer_camera.isActive() == False:  # 如果摄像头未开启
            msg = QtWidgets.QMessageBox.warning(self, 'warning', "请打开摄像头", buttons=QtWidgets.QMessageBox.Ok)
        else:
            if self.count % 2 == 0:
                self.showpictures.setPixmap(QtGui.QPixmap.fromImage(self.showImage))
                # print(type(self.showImage))showImage类型为<class 'PyQt5.QtGui.QImage'>
                test = photo_calculation_and_processing(self.show, threshold)
                if (test == False):  # 如果人脸检测失败，重新拍照
                    msg = QtWidgets.QMessageBox.warning(self, "警告", "请重新拍照", buttons=QtWidgets.QMessageBox.Ok)
                else:  # 输出人脸框和人脸特征点
                    photos.append(self.image)  # !!!添加到用户图片里的只能是原始格式，不能为self.show或self.showImage
                    msg = QtWidgets.QMessageBox.warning(self, "结果", "拍照成功", buttons=QtWidgets.QMessageBox.Ok)
                    self.count += 1


            else:
                self.showpictures2.setPixmap(QtGui.QPixmap.fromImage(self.showImage))
                test = photo_calculation_and_processing(self.show, threshold)
                if (test == False):  # 如果人脸检测失败，重新拍照
                    msg = QtWidgets.QMessageBox.warning(self, "警告", "请重新拍照", buttons=QtWidgets.QMessageBox.Ok)
                else:  # 输出人脸框和人脸特征点
                    photos.append(self.image)
                    msg = QtWidgets.QMessageBox.warning(self, "结果", "拍照成功", buttons=QtWidgets.QMessageBox.Ok)
                    self.count += 1

    user.photos = photos

    # print(user.photos)

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
            # 测试信息是否存入user中
            # print(user.name, user.stuId)
            # print(user.photos)
            # test = feature.Feature(False, user.photos)
            # print(test.embeddings)

            # 将用户信息存入user_info表

            testuser = Dao(user, "user")
            testuser.appandUserInfo()
            msg3 = QtWidgets.QMessageBox.information(self, '提示信息', '注册成功')
            testuser.closeDb()

            # 将数据存入feature_info表
            test1 = feature.Feature(True, user)
            print(test1.user)
            testDAO = Dao(test1)
            testDAO.appandFeatureInfo()
            msg3 = QtWidgets.QMessageBox.information(self, '提示信息', '注册成功')
            testDAO.closeDb()

    def fan(self):
        self.hide()
        self.di = mywindow()
        self.di.show()


class Myguanliyuan(QtWidgets.QWidget, Ui_Administrator):
    def __init__(self, parent=None):
        super(Myguanliyuan, self).__init__(parent)  # 父类的构造函数
        self.sm = []
        self.setupUi(self)
        self.pushbutton_init()

    def pushbutton_init(self):
        self.query.clicked.connect(self.query_click)
        self.fanhui.clicked.connect(self.fan2)
        self.radioButton.toggled.connect(lambda: self.btnstate(self.radioButton))
        self.radioButton_2.toggled.connect(lambda: self.btnstate(self.radioButton_2))
        self.radioButton_3.toggled.connect(lambda: self.btnstate(self.radioButton_3))

    def btnstate(self, btn):
        if btn.text() == "班级":
            if btn.isChecked() == True:
                self.sm = Dao.find_class(self.lineEdit.text())
            else:
                pass
        if btn.text() == "个人":
            if btn.isChecked() == True:
                self.sm = Dao.find_person(self.lineEdit.text())
            else:
                pass
        if btn.text() == "日期":
            if btn.isChecked() == True:
                self.sm = Dao.find_time(self.lineEdit.text())
            else:
                pass

    def query_click(self):
        # sm=self.btnstate()
        self.btnstate(self.radioButton)
        self.btnstate(self.radioButton_2)
        self.btnstate(self.radioButton_3)
        fields = Dao.find_lie()
        self.table(self.sm, fields)
        print(2)

    def table(self, sm, fields):
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

    def fan2(self):
        self.hide()
        self.di2 = mywindow()
        self.di2.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # 固定的，表示程序应用
    ui = mywindow()
    ui.show()
    # ui.zhuche.clicked.connect(ui.tiao)
    sys.exit(app.exec_())
