"""
     该模块实现人脸检测功能，对前端发来的照片进行计算和处理,计算得出人脸得分、人脸边框、人脸关键点,处理后的照片交给facenet做识别
"""
import cv2 as cv
from core import face_recognition

# 初始化mtcnn人脸检测
face_detect = face_recognition.Facedetection()
# 阈值设置
threshold = 0.99


def photo_calculation_and_processing(photo):
    """
    :param photo:前端发来的照片(原生照片，没有经过任何处理)
    :type photo:numpy.ndarray
    :return:得分最高的人脸对应的人脸框、人脸关键点坐标、未被处理过的图片
    :rtype:list、list、numpy.ndarray
    """

    while True:
        # 调整需要识别的图片，将格式转为RGB
        img = cv.cvtColor(photo, cv.COLOR_BGR2RGB)
        # 将照片放进mtcnn神经网络中
        # target人脸得分
        # bboxes人脸框信息（左上角横纵坐标、右下角横纵坐标）
        # landmarks人脸五个关键点坐标（左右眼、鼻尖、左右嘴角）
        target, bboxes, landmarks = face_detect.detect_face(img, True)
        # 将图片调整为等高的,facenet算法要求
        bboxes = face_detect.get_square_bboxes(bboxes, fixed="height")
        # 获取照片中人脸的最高分
        highestscore = max(target)
        # 获取人脸最高分对应的下标
        highestscore_index = target.index(highestscore)
        if highestscore >= threshold:
            return [bboxes[highestscore_index]], [landmarks[highestscore_index]], photo


if __name__ == "__main__":
    # 往上跳两级
    photo_path = "../../Image/zhoujielun1.jpg"
    photo = cv.imread(photo_path)
    test = photo_calculation_and_processing(photo)
    print(test)
