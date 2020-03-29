"""
     测试模块，对前端发来的照片进行计算和处理,计算得出人脸得分、人脸边框、人脸关键点,处理后的照片交给facenet做识别
"""
import cv2 as cv
from core import face_recognition
threshold = 0.01

# 初始化mtcnn人脸检测
face_detect = face_recognition.Facedetection()


def photo_calculation_and_processing(photo_path):
    '''
    测试阶段:可以向该模块传图片的路径和阈值
    :param photo_path: 图片的路径
    :type photo_path: String
    :param threshold: 判断阈值
    :type threshold: double
    :return:得分最高的人脸对应的人脸框、人脸关键点坐标、未被处理过的图片
    :rtype:list、list、numpy.ndarray
    '''
    while True:
        img = cv.imread(photo_path)  # 读取图片
        # 转换图片格式
        cvimage = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        # target人脸得分
        # bboxes（type=list）人脸框信息（左上角横纵坐标、右下角横纵坐标）
        # landmarks(type=list)人脸五个关键点坐标（左右眼、鼻尖、左右嘴角）
        target, bboxes, landmarks = face_detect.detect_face(cvimage, True)
        # 将图片调整为等高的,算法要求
        bboxes = face_detect.get_square_bboxes(bboxes, fixed="height")
        # 获取照片中人脸的最高分
        highestscore = max(target)
        print(highestscore)
        highestscore_index = target.index(highestscore)
        if highestscore >= threshold:
            print("已检测到人脸")
            return [bboxes[highestscore_index]], [landmarks[highestscore_index]], img


if __name__ == "__main__":
    photo_path = "../../Image/zhoujielun1.jpg"
    test = photo_calculation_and_processing(photo_path)
    print(test)
