# 数据库连接配置
import pymysql

conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        db='houseprice',
        user='root',
        password='2458166022',
        charset='utf8'
    )
