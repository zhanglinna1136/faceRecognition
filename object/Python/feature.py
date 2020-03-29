# -*-coding: utf-8 -*-
"""
    该模块用于创建人脸特征向量(做识别的时候，前来识别的用户的特征向量不需要这个模块生成),生成Feature对象
    Feature对象：和数据库中feature_info对应
"""
from object.Python.user import User  # 导入同级包中类
import numpy as np
import cv2 as cv
from core import face_recognition
from utils import image_processing  # 导入上一级包中的模块
import dataset.Python.database as db


resize_width = 160
resize_height = 160
# 初始化mtcnn人脸检测
face_detect = face_recognition.Facedetection()
# 初始化facenet
face_net = face_recognition.facenetEmbedding()
# 初始化数据库对象，查询出学号列表和人脸特征向量列表
testDao = db.Dao()
# embeddingsList数据库中人脸特征向量列表[[用户1的人脸特征向量1],[用户1的人脸特征向量2],[用户2的人脸特征向量1],[用户2的人脸特征向量2]]
# stuIdList数据库中的学号列表["用户1的学号"，"用户1的学号","用户2的学号","用户2的学号"]
# 两者一一对应
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
        self.user = user
        self.embeddings = self.createFeature(user.photos)

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
        print(embeddings)
        return embeddings

    def calculateDistance(self, predEmb):
        '''
        :param predEmb: 前来识别的用户的人脸特征向量,形如[1.53171383e-02 -3.97704430e-02 -3.35174240e-02 -1.86988339e-03]
        :type predEmb: list
        :return: 识别成功返回用户名字和照片，失败返回fail
        :rtype: numpy.ndarray、String或者String
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
            stuId = stuIdList[distlist.index(minvalue)]
            photo, name = testDao.findPhotoAndName(stuId)
            return photo, name
        else:
            "fail"


if __name__ == "__main__":
    photos = []
    photos1 = []
    # 照片路径不能包含中文
    photo1 = cv.imread("../../Image/zhoujielun1.jpg")
    photo2 = cv.imread("../../Image/zhoujielun2.jpg")

    photos.append(photo1)
    photos.append(photo2)
    user = User("杨亚龙", "20171112802", photos)
    test = Feature(user)
    print(test.embeddings)
