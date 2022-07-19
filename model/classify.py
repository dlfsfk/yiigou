
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
    list=[]
    col=len(df.count())
    for j in range(0,10):
        list.append([])
        for i in range(0,col):
            data0 = df.iloc[j][i]
            list[j].append(data0)
            i+=1
        j+=1
    print(list)
    return list
classify(2)