# 数据库连接配置
import pymysql

conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        db='yigou',
        user='root',
        password='root',
        charset='utf8'
    )
