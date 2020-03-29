#摄像头捕捉一个超过阈值的人脸后就休眠，把cpu让给人脸比对的线程，这样人脸比对的线程就只用处理一张固定的人脸
import sys
import cv2
from Check_in import Ui_Check_in
from PyQt5 import QtCore, QtGui, QtWidgets
from detection import mtcnnDetection
from object import feature
from identify import identification
import threading
import time

#thstop=False#控制线程的结束
threshold = 0.99 #人脸检测的阈值
#lock=threading.Lock()#取锁

class mywindow(QtWidgets.QWidget,Ui_Check_in):
    def __init__(self, parent=None):
        super(mywindow, self).__init__(parent)  # 继承父类的构造函数

        self.CAM_NUM = 0  # 为0时表示视频流来自笔记本内置摄像头
        self.cap = cv2.VideoCapture()  # 创建一个VideoCapture对象

        self.setupUi(self)
        self.solt()

    def solt(self):
        self.qiandao.clicked.connect(self.thread_)
        self.exit.clicked.connect(self.Exit)

#打开摄像头，捕捉人脸
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
                faceCheck = mtcnnDetection.photo_calculation_and_processing(image, threshold)
                if (faceCheck != False):
                    global photos  # Feature里面的createFeature的参数必须是列表，所以每检测到一张人脸就添加到photos列表中
                    photos.append(image)
                    time.sleep(3)
                else:
                    print("未检测到人脸")


                # faceCheck=identification.faceRecognition(self.image)
                # if(faceCheck!=False):#如果检测到人脸并且超过所设置的阈值，那么就计算出这张人脸的特征向量
                #     print(faceCheck)

#人脸检测和计算人脸特征点
    def faceRecognition2(self):
        while True:
            # faceCheck = mtcnnDetection.photo_calculation_and_processing(image, threshold)
            # if (faceCheck != False):
            #     photos = []  # Feature里面的createFeature的参数必须是列表，所以每检测到一张人脸就添加到photos列表中
            #     photos.append(image)
                test = feature.Feature(False, photos)
                print(test.embeddings)
                test.embeddings=self.reduceDimen(test.embeddings)
                print(test.embeddings)
                result=feature.Feature.calculateDistance(test.embeddings)
                if result=="fail":
                    print("签到失败")
                else:
                    print("签到成功")
            # else:
            #     print("未检测到人脸")
        # while True:
        #     faceCheck=identification.faceRecognition(image)

#把三维列表降维一维列表
    def reduceDimen(self,list):
        result=[]
        for i in list:
            for j in i:
                for k in j:
                    result.append(k)
        return result



    def Exit(self):
        self.cap.release()#释放视频流
        sys.exit()

#多线程运行人脸检测和人脸识别
    def thread_(self):
        t1 = threading.Thread(target=self.openCamera)#线程1，进行人脸的捕捉
        t2 = threading.Thread(target=self.faceRecognition2)#线程2，进行人脸的比对
        # while True:
        t1.start()
        # time.sleep(3)#线程2必须要在线程1开启之后才能开启，因为线程2需要用到线程1所捕捉到的人脸
        t1.join()
        t2.start()
        # t2.join()



if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)  # 固定的，表示程序应用
    ui=mywindow()
    ui.show()
    sys.exit(app.exec_())