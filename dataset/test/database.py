import MySQLdb
import cv2 as cv
# from object.test import feature, user
from object.test import user
import numpy as np

"""
    数据库模块，该模块完成对数据库的操作
"""


class Dao:
    def __init__(self, *args):
        if len(args) == 0:
            pass
        elif len(args) > 1:
            # 存储用户信息（user）
            self.user = args[0]
        else:
            # 存储人脸特征点
            self.feature = args[0]
            self.user = self.feature.user
            self.embeddings = self.feature.embeddings
        #    连接数据库
        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='123456789', db='fr', charset='gb2312')

    def setUp(self, sql):
        """
        建表函数，如果需要在mysql中建立新的表可以使用该函数
        :return:
        :rtype:
        """
        cursor = self.conn.cursor()
        cursor.execute(sql)

    def tearDown(self):
        """
        删表函数
        :return:
        :rtype:
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute("Drop Table %s")
        except:
            pass

    def appandUserInfo(self):
        """
        该函数用于向数据库表user_info中添加用户信息(已测试)
        :param user:
        :type user:
        :return:
        :rtype:
        """
        cursor = self.conn.cursor()
        print(self.user.stuId, self.user.photos[0].shape, self.user.photos[1].shape)
        # 存储照片的shape
        cursor.execute("INSERT INTO photo_shape (stuId,shape1,shape2) VALUES (%s,%s,%s)",
                       ([self.user.stuId, str(self.user.photos[0].shape), str(self.user.photos[1].shape)]))
        # 将图片转为byte对象,并存进图片列表
        photo1 = self.user.photos[0].tostring()
        photo2 = self.user.photos[1].tostring()
        cursor.execute("INSERT INTO user_info (name,stu_id,photo1,photo2) VALUES (%s,%s,%s,%s)",
                       ([self.user.name, self.user.stuId, photo1, photo2]))
        cursor.connection.commit()

    def appandFeatureInfo(self):
        """
        该函数用于向数据库表feature_info中添加用户人脸特征点信息
        """
        print(self.embeddings[0])
        feature0 = self.embeddings[0].tostring()
        feature1 = self.embeddings[1].tostring()
        print(feature0)
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO feature_info (stu_id,feature0,feature1) VALUES (%s,%s,%s)",
                       ([user.stuId, feature0, feature1]))
        cursor.close()

    def closeDb(self):
        """
        关闭数据库连接
        :return:
        :rtype:
        """
        self.conn.close()

    def findNameAndFeatureList(self):
        """
        该模块返回学号列表和人脸特征向量列表（这两个表一一对应）
        """
        # 学号列表
        stuIdList = []
        # 人脸特征向量列表
        embeddingsList = []
        cursor = self.conn.cursor()
        cursor.execute("select * from feature_info")
        rows = cursor.fetchall()
        for row in rows:
            stuId = row[0]
            embedding0 = np.frombuffer(row[1], dtype=np.float32)
            embedding1 = np.frombuffer(row[2], dtype=np.float32)
            # 重塑列表
            result0 = embedding0.reshape((1, 512))
            result1 = embedding1.reshape((1, 512))
            stuIdList.append(stuId)
            stuIdList.append(stuId)
            embeddingsList.append(result0)
            embeddingsList.append(result1)
        return stuIdList, embeddingsList

    def findPhoto(self, stuId):
        """
        该函数可以用于从数据库中查找指定学号的同学的照片（已测试）
        :return:照片数组
        :rtype:找到：return numpy.ndarray；未找到：return None
        """
        cursor = self.conn.cursor()
        cursor.execute("select photo1 from user_info where stu_id=(%s)", ([stuId]))
        row = cursor.fetchone()
        if row is not None:
            feature = np.frombuffer(row[0], dtype=np.uint8)
            result = feature.reshape(self.user.photos[0].shape)
            return result
        else:
            return None

    def findPhotoAndName(self, stuId):
        """
        该函数可以用于从数据库中查找指定学号的同学的名字和照片(已测试)
        :return:照片数组
        :rtype:找到：return numpy.ndarray；未找到：return None
        """
        shapeStr=self.findShape(stuId)
        if shapeStr is not None:
            shape = tuple(eval(shapeStr))
            cursor = self.conn.cursor()
            cursor.execute("select photo1,name from user_info where stu_id=(%s)", ([stuId]))
            row = cursor.fetchone()
            if row is not None:
                feature = np.frombuffer(row[0], dtype=np.uint8)
                photo = feature.reshape(shape)
                name = row[1]
                return photo, name
            else:
                return None
        else:
            return None

    def findShape(self, stuId):
        """
        根据学号查找照片shape（已测试）
        :param stuId: 学号
        :type stuId: String
        :return: shape,eg：(10,15,20)
        :rtype: 元组
        """
        cursor = self.conn.cursor()
        cursor.execute("select shape1 from photo_shape where stuid=(%s)", ([stuId]))
        row = cursor.fetchone()
        if row is not None:
            return row[0]
        else:
            return None


if __name__ == "__main__":
    photos = []
    # 照片路径不能包含中文

    photo1 = cv.imread("../../Image/huge1.jpg")
    photo2 = cv.imread("../../Image/huge2.jpg")
    print(photo1)
    print(photo2)

    photos.append(photo2)
    photos.append(photo1)

    user = user.User("胡歌", "201712", photos)
    # # 测试存储feature
    # testFeature = feature.Feature(user)
    # testDao = Dao(testFeature)
    # # 测试存储user
    testDao = Dao(user, "isUser")
    # # 测试查询人脸特征向量和名字列表
    # testDao = Dao()
    try:
        # photo, name = testDao.findPhotoAndName("201711")
        # 测试存储feature
        # testDao.appandFeatureInfo()
        # 测试存储user
        testDao.appandUserInfo()
        # print(testDao.findShape("201711"))
        # stuIdList, embeddingsList = testDao.findNameAndFeatureList()
        # print(photo)
        # cv.imshow("123", photo)
        # print(photo)
        # print(name)
        # cv.waitKey(0)
    finally:
        testDao.closeDb()
