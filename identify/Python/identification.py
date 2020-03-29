"""
    该模块以检测算法为基础,完成识别任务前端做人脸识别直接调用该模块
"""
# facenet模型路径
model_path = '../../models/20180408-102900'
from detection.Python import mtcnnDetection
from utils import image_processing
from core import face_recognition
from dataset.Python import database
from object.Python import feature

# 初始化facenet
face_net = face_recognition.facenetEmbedding(model_path)


def faceRecognition(photo):
    """
    :param photo: 前端发来的照片(原生照片，没有经过任何处理)
    :type photo: numpy.ndarray
    :return: 识别结果
    :rtype:
    """
    # 人脸检测、对齐
    # bboxes人脸框信息（左上角横纵坐标、右下角横纵坐标）
    # landmarks人脸五个关键点坐标（左右眼、鼻尖、左右嘴角）
    bboxes, landmarks, image = mtcnnDetection.photo_calculation_and_processing(photo_path)
    # 算法要求，将照片调整为160*160，输入到facenet中
    face_images = image_processing.get_bboxes_image(image, bboxes, 160, 160)
    face_images = image_processing.get_prewhiten_images(face_images)
    # 生成face_images的128维的人脸特征向量
    pred_emb = face_net.get_embedding(face_images)

    # 调用数据库模块,返回名字列表names_list,人脸特征向量数组dataset_emb(未实现)
    # 字典形式{name:[feature0,feature1,feature2]}
    db = database.Dao()
    dic = db.nameFeature_dic()
    fF = feature.Feature()
    show_info = fF.calculateDistance(pred_emb, dic, threshold)
    print(show_info)
    if show_info is not "unkonw":
        """签到成功"""
        pass
    else:
        """签到失败"""
