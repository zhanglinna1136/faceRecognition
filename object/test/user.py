"""
    用户对象：和数据库中user_info对应
"""

class User:
    def __init__(self, name, stuId, photos):
        self.photos = photos
        self.name = name
        self.stuId = stuId


if __name__ == "__main__":
    user = User("杨亚龙", "20171112802", "123")
    print(user.photos)
    print(user.name)
