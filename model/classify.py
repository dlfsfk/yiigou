
import pymysql
import pandas as pd
from sqlalchemy import create_engine
# 创建create_engine对象(格式类似于URL地址)：
def classify(page):
    engine = create_engine('mysql+pymysql://root:2458166022@localhost:3306/houseprice?charset=utf8')
    # 创建SQL查询语句：
    sql = 'SELECT * FROM classify_data3 limit {},10'.format((page - 1) * 10)
    # 使用pandas读取数据库：
    df = pd.read_sql(sql, engine)
    print(df)
    result=[]
    # print(df.iloc[0])

    col=len(df.count())
    for j in range(0,10):
        info = {}
        info["id"] = int(df.iloc[j][0])
        info["img"] = df.iloc[j][1]
        info["name"] = df.iloc[j][2]
        info["price"] = df.iloc[j][3]
        info["area"] = df.iloc[j][4]
        info["address"] = df.iloc[j][5]
        info["business"] = df.iloc[j][6]
        info["room"] = list(map(lambda x: (x.replace(' ', ''))[1:-1], (df.iloc[j][7][1:-1].split(","))))
        info["tag"] = list(map(lambda x: (x.replace(' ', ''))[1:-1], (df.iloc[j][8][1:-1].split(","))))
        info["total_price"] = df.iloc[j][9]
        result.append(info)
        j += 1
    print(result)
    return list
classify(2)