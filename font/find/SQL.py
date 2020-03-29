import MySQLdb
import numpy as np


def initsql():
    db = MySQLdb.connect(host='106.52.85.106', user='root', passwd='sspu2017@', db='fr')
    db.set_character_set('utf8')
    print("ok")
    cursor = db.cursor()
    name = "吴凯文"
    stu_id = "20171112816"

    cursor.execute('insert into Checkin_info(name,stu_id) values(%s,%s)', ([name, stu_id]))
    print("2")
    db.commit()

    db.close()


if __name__ == '__main__':
    initsql()
