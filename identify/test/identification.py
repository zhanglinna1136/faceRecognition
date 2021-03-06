"""
    该模块以检测算法为基础,完成识别任务
    前端做人脸识别直接调用该模块即可
    前端向该模块传递一张数组定义的照片
"""
# facenet模型路径
from detection.test import mtcnnDetection
from utils import image_processing
from core import face_recognition

# 初始化facenet
face_net = face_recognition.facenetEmbedding()


def faceRecognition(photo_path):
    """
    Args:
        model_path (): facenet预训练模型的路径
        dataset_path (): 存放人脸特征数据库的路径
        filename (): 存放每张图片信息的txt文档路径
        photo_path:进行识别的图片的路径
        分别检测到照片
    """
    # 人脸检测、对齐
    # bboxes人脸框信息（左上角横纵坐标、右下角横纵坐标）
    # landmarks人脸五个关键点坐标（左右眼、鼻尖、左右嘴角）
    bboxes, landmarks, image = mtcnnDetection.photo_calculation_and_processing(photo_path)
    if bboxes == [] or landmarks == []:
        # 如果图片中没有人脸
        print("-----no face")
    print("-----image have {} faces".format(len(bboxes)))
    # 算法要求，将照片调整为160*160，输入到facenet中
    face_images = image_processing.get_bboxes_image(image, bboxes, 160, 160)
    face_images = image_processing.get_prewhiten_images(face_images)
    # 生成face_images的128维人脸特征向量
    pred_emb = face_net.get_embedding(face_images)
    print(pred_emb)

    # 调用数据库模块,返回名字列表names_list,人脸特征向量数组dataset_emb(未实现)
    # 字典形式{name:[feature0,feature1,feature2]}
    # db = database.Dao()
    # dic = db.nameFeature_dic()
    # fF = feature.Feature()
    # show_info = fF.calculateDistance(pred_emb, dic, threshold)
    # print(show_info)
    # if show_info is not "unkonw":
    #     """签到成功"""
    #     pass
    # else:
    #     """签到失败"""


if __name__ == "__main__":
    photo_path = "../../Image/zhoujielun1.jpg"
    faceRecognition(photo_path)
