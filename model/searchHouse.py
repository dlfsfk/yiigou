import re
import pandas
import pymysql
from sqlalchemy import create_engine


def search_acreage(n1, n2):
    db = pymysql.connect(host="127.0.0.1", user="root",

                         passwd="2458166022",

                         db="houseprice",

                         charset='utf8')
    cursor = db.cursor()
    sql = 'SELECT id,area FROM classify_data3 '
    cursor.execute(sql)
    pd = cursor.fetchall()
    # print(pd[0][1])
    num0 = []
    for i in range(0, 1000):
        # print(pd[i][1])
        if pd[i][1] == "None":
            continue
        num1 = re.findall("\d+", pd[i][1])
        # print(num1)
        num2 = []
        num2.append(i + 1)
        num2.append([int(x) for x in num1])
        num0.append(num2)
    # print(num0)
    id0 = []
    n3 = int(n1)
    n4 = int(n2)
    count0 = len(num0)
    # print(count)
    # if len(num0[26][1])==1:
    #     print("面积固定")
    for i in range(0, count0):
        # if (num0[i][1][0]>=n3 and num0[i][1][0]<=n4) or (num0[i][1][1]>=n3 and num0[i][1][1]<=n4) :
        #     id0.append(num0[i][0])
        if num0[i][1][0] >= n3 and num0[i][1][0] <= n4:
            id0.append(num0[i][0])
        if len(num0[i][1]) != 1:
            if num0[i][1][1] >= n3 and num0[i][1][1] <= n4:
                id0.append(num0[i][0])
    print(id0)

    engine = create_engine('mysql+pymysql://root:2458166022@localhost:3306/houseprice?charset=utf8')
    count1 = len(id0)
    print(count1)
    result = []
    for i in range(0, count1):
        sql = 'SELECT * FROM classify_data3 where id = %s' % id0[i]
        df = pandas.read_sql(sql, engine)
        # print(df)
        info = {}
        info["id"] = int(df.iloc[0][0])
        info["img"] = df.iloc[0][1]
        info["name"] = df.iloc[0][2]
        info["price"] = df.iloc[0][3]
        info["area"] = df.iloc[0][4]
        info["address"] = df.iloc[0][5]
        info["business"] = df.iloc[0][6]
        info["room"] = list(map(lambda x: (x.replace(' ', ''))[1:-1], (df.iloc[0][7][1:-1].split(","))))
        info["tag"] = list(map(lambda x: (x.replace(' ', ''))[1:-1], (df.iloc[0][8][1:-1].split(","))))
        info["total_price"] = df.iloc[0][9]
        result.append(info)
    print(result)
    return result


# search_acreage(10, 100)


def search_price(p1, p2, page):
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        db='yigou',
        user='root',
        password='root',
        charset='utf8'
    )
    cls = conn.cursor()
    sql = 'SELECT id,price FROM classify_data3 '
    cls.execute(sql)
    conn = cls.fetchall()
    print(conn)
    num0 = []
    for i in range(0, 1800):
        # print(pd[i][1])
        if conn[i][1] == "价格待定":
            continue
        num1 = re.findall("\d+", conn[i][1])
        # print(num1)
        num2 = []
        num2.append(i + 1)
        num2.append([int(x) for x in num1])
        num0.append(num2)
    # print(num0)
    pl = int(p1)
    ph = int(p2)
    id0 = []
    count0 = len(num0)
    for i in range(0, count0):
        if pl <= num0[i][1][0] <= ph:
            id0.append(num0[i][0])
    # print(id0)

    engine = create_engine('mysql+pymysql://root:2458166022@localhost:3306/houseprice?charset=utf8')
    count1 = len(id0)
    print(count1)
    result = []
    if page < int(count1 / 10 + 1):
        for i in range((page - 1) * 10, (page - 1) * 10 + 10):
            sql = 'SELECT * FROM classify_data3 where id = %s' % id0[i]
            df = pandas.read_sql(sql, engine)
            # print(df)
            info = {}
            info["id"] = int(df.iloc[0][0])
            info["img"] = df.iloc[0][1]
            info["name"] = df.iloc[0][2]
            info["price"] = df.iloc[0][3]
            info["area"] = df.iloc[0][4]
            info["address"] = df.iloc[0][5]
            info["business"] = df.iloc[0][6]
            info["room"] = list(map(lambda x: (x.replace(' ', ''))[1:-1], (df.iloc[0][7][1:-1].split(","))))
            info["tag"] = list(map(lambda x: (x.replace(' ', ''))[1:-1], (df.iloc[0][8][1:-1].split(","))))
            info["total_price"] = df.iloc[0][9]
            result.append(info)
        # print(result)
    if page == int(count1 / 10 + 1):
        for i in range((page - 1) * 10, (page - 1) * 10 + 7):
            sql = 'SELECT * FROM classify_data3 where id = %s' % id0[i]
            df = pandas.read_sql(sql, engine)
            # print(df)
            info = {}
            info["id"] = int(df.iloc[0][0])
            info["img"] = df.iloc[0][1]
            info["name"] = df.iloc[0][2]
            info["price"] = df.iloc[0][3]
            info["area"] = df.iloc[0][4]
            info["address"] = df.iloc[0][5]
            info["business"] = df.iloc[0][6]
            info["room"] = list(map(lambda x: (x.replace(' ', ''))[1:-1], (df.iloc[0][7][1:-1].split(","))))
            info["tag"] = list(map(lambda x: (x.replace(' ', ''))[1:-1], (df.iloc[0][8][1:-1].split(","))))
            info["total_price"] = df.iloc[0][9]
            result.append(info)
        # print(result)
    res = {}
    res["page"] = int(count1 / 10 + 1)
    res["info"] = result
    print(res)
    return res


search_price(11000, 15000)
