# -*-coding: utf-8 -*-
"""
    该模块用于创建人脸特征向量,生成Feature对象
    Feature对象：和数据库中feature_info对应
"""
from object.Python.user import User  # 导入同级包中类
import numpy as np
import cv2 as cv
from core import face_recognition
from utils import image_processing  # 导入上一级包中的模块
import dataset.test.database as db

resize_width = 160
resize_height = 160
# 显示全部
np.set_printoptions(threshold=np.inf)

# 初始化mtcnn人脸检测
face_detect = face_recognition.Facedetection()
# 初始化facenet
face_net = face_recognition.facenetEmbedding()
# 初始化数据库对象，查询出学号列表和人脸特征向量列表
testDao = db.Dao()
stuIdList, embeddingsList = testDao.findNameAndFeatureList()
# 定义阈值常量
THRESHOLD = 0.7


class Feature:

    def __init__(self, user):
        '''
      创建feature对象
      :param user: user对象
      :type user: user
      '''
        if user is not None:
            self.user = user
            self.embeddings = self.createFeature(user.photos)
        else:
            pass

    def createFeature(self, photos):
        """
       创建人脸特征，返回人脸特征向量列表
        :param photos:图片列表
        :type photos:list
        :return:embeddings列表
        :rtype:list
        """
        embeddings = []  # 用于保存人脸特征数据库
        for photo in photos:
            image = image_processing.change_image(photo)
            # 进行人脸检测，获得bounding_box
            bboxes, landmarks = face_detect.detect_face(image, False)
            # 返回人脸框和5个关键点
            bboxes = face_detect.get_square_bboxes(bboxes, landmarks)
            # 获得人脸区域
            face_images = image_processing.get_bboxes_image(image, bboxes, resize_height, resize_width)
            # 人脸预处理，归一化
            face_images = image_processing.get_prewhiten_images(face_images, normalization=True)
            # 获得人脸特征
            pred_emb = face_net.get_embedding(face_images)
            embeddings.append(pred_emb)

        embeddings = np.asarray(embeddings)  # 将元组转为列表
        print(type(embeddings[0]))
        return embeddings

    def testCalculateDistance(self, embedding, embeddings):
        """
        该函数用于测试计算欧式距离(未测试)
        :param embedding单个人脸特征向量:
        :type embeddings人脸特征向量列表:
        :return:
        :rtype:
        """
        distlist = []
        for j in range(len(embeddings)):
            # 计算需要欧式距离，并求和
            dist = np.sqrt(np.sum(np.square(np.subtract(embedding[:], embeddings[j][0][:]))))
            # 与每张脸的欧式距离
            distlist.append(dist)
        minvalue = min(distlist)
        return minvalue, distlist

    def calculateDistance(self, predEmb):
        '''
        :param predEmb: 前来识别的用户的人脸特征向量,形如[1.53171383e-02 -3.97704430e-02 -3.35174240e-02 -1.86988339e-03]
        :type predEmb: list
        :param embeddingsList: 数据库中人脸特征向量字典列表[[用户1的人脸特征向量1],[用户1的人脸特征向量2],[用户2的人脸特征向量1],[用户2的人脸特征向量2]]
        :type embeddingsList: list
        :param nameList: 学号列表
        :type nameList: ["用户1的学号"，"用户1的学号","用户2的学号","用户2的学号"]
        :return: 识别成功返回用户名字和照片，失败返回失败提示
        :rtype: String
        '''

        distlist = []
        for embeddings in embeddingsList:
            # 计算需要欧式距离，并求和
            dist = np.sqrt(np.sum(np.square(np.subtract(predEmb[:], embeddings[0][:]))))
            # 与每张脸的欧式距离
            distlist.append(dist)
        minvalue = min(distlist)
        if minvalue < THRESHOLD:
            # 通过学号查询人名和照片
            stuId=stuIdList[distlist.index(minvalue)]
            photo, name = testDao.findPhotoAndName(stuId)
            return photo, name


if __name__ == "__main__":
    # photos = []
    # photos1 = []
    photo1_test = [cv.imread("../../Image/zhoujielun_pre.jpg")]
    # # 照片路径不能包含中文
    # photo1 = cv.imread("../../Image/zhoujielun1.jpg")
    # photo2 = cv.imread("../../Image/zhoujielun2.jpg")
    # photo3 = cv.imread("../../Image/yangyalong.jpg")

    # photos.append(photo1)
    # photos.append(photo2)
    # photos.append(photo3)
    # user = User("杨亚龙", "20171112802", photos)
    user_none = User(None, None, photo1_test)
    test_none = Feature(user_none)
    photo, name = test_none.calculateDistance(test_none.embeddings[0][0])
    print(photo)
    print(name)
