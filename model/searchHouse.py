import re
import pandas
import pymysql

from config import conn
from sqlalchemy import create_engine

def searchByArea(n1,n2,page):
    conn.ping(reconnect=True)
    cursor = conn.cursor()
    sql = 'SELECT id,area FROM house '
    cursor.execute(sql)
    pd = cursor.fetchall()
    num0 = []
    for i in range(0, 1000):
        if pd[i][1] == "None":
            continue
        num1 = re.findall("\d+", pd[i][1])
        num2 = []
        num2.append(i + 1)
        num2.append([int(x) for x in num1])
        num0.append(num2)
    id0 = []
    n3 = int(n1)
    n4 = int(n2)
    count0 = len(num0)
    for i in range(0, count0):
        if num0[i][1][0] >= n3 and num0[i][1][0] <= n4:
            id0.append(num0[i][0])
        elif len(num0[i][1]) != 1:
            if num0[i][1][1] >= n3 and num0[i][1][1] <= n4:
                id0.append(num0[i][0])
    engine = create_engine('mysql+pymysql://root:123123@localhost:3306/yigou?charset=utf8')
    count1 = len(id0)
    count2 = count1 - int(count1 / 10) * 10
    result = []
    if page < int(count1 / 10 + 1):
        for i in range((page - 1) * 10, (page - 1) * 10 + 10):
            sql = 'SELECT * FROM house where id = %s' % id0[i]
            df = pandas.read_sql(sql, engine)

            info = {}
            info["id"] = int(df.iloc[0][0])
            info["img"] = df.iloc[0][1]
            info["name"] = df.iloc[0][2]
            info["price"] = df.iloc[0][3][:-7].replace(' ','')
            info["area"] = df.iloc[0][4]
            info["address"] = df.iloc[0][5]
            info["business"] = df.iloc[0][6]
            info["room"] = list(map(lambda x: (x.replace(' ', ''))[1:-1], (df.iloc[0][7][1:-1].split(","))))
            info["tag"] = list(map(lambda x: (x.replace(' ', ''))[1:-1], (df.iloc[0][8][1:-1].split(","))))
            info["total_price"] = df.iloc[0][9]
            result.append(info)

    if page == int(count1 / 10 + 1):
        for i in range((page - 1) * 10, (page - 1) * 10 + count2):
            sql = 'SELECT * FROM house where id = %s' % id0[i]
            df = pandas.read_sql(sql, engine)
            info = {}
            info["id"] = int(df.iloc[0][0])
            info["img"] = df.iloc[0][1]
            info["name"] = df.iloc[0][2]
            info["price"] = df.iloc[0][3][:-7].replace(' ','')
            info["area"] = df.iloc[0][4]
            info["address"] = df.iloc[0][5]
            info["business"] = df.iloc[0][6]
            info["room"] = list(map(lambda x: (x.replace(' ', ''))[1:-1], (df.iloc[0][7][1:-1].split(","))))
            info["tag"] = list(map(lambda x: (x.replace(' ', ''))[1:-1], (df.iloc[0][8][1:-1].split(","))))
            info["total_price"] = df.iloc[0][9]
            result.append(info)
    res = {}
    res["total"] = count1
    res["info"] = result
    return res

def searchByprice(p1, p2, page):
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        db='yigou',
        user='root',
        password='123123',
        charset='utf8'
    )
    cls = conn.cursor()
    sql = 'SELECT id,price FROM house '
    cls.execute(sql)
    conn = cls.fetchall()
    num0 = []
    for i in range(0, 1800):
        if conn[i][1] == "价格待定":
            continue
        num1 = re.findall("\d+", conn[i][1])
        num2 = []
        num2.append(i + 1)
        num2.append([int(x) for x in num1])
        num0.append(num2)
    pl = int(p1)
    ph = int(p2)
    id0 = []
    count0 = len(num0)
    for i in range(0, count0):
        if pl <= num0[i][1][0] <= ph:
            id0.append(num0[i][0])
    engine = create_engine('mysql+pymysql://root:123123@localhost:3306/yigou?charset=utf8')
    count1 = len(id0)
    result = []
    count2 = count1-int(count1/10)*10
    if page < int(count1 / 10 + 1):
        for i in range((page - 1) * 10, (page - 1) * 10 + 10):
            sql = 'SELECT * FROM house where id = %s' % id0[i]
            df = pandas.read_sql(sql, engine)
            info = {}
            info["id"] = int(df.iloc[0][0])
            info["img"] = df.iloc[0][1]
            info["name"] = df.iloc[0][2]
            info["price"] = df.iloc[0][3][:-7].replace(' ','')
            info["area"] = df.iloc[0][4]
            info["address"] = df.iloc[0][5]
            info["business"] = df.iloc[0][6]
            info["room"] = list(map(lambda x: (x.replace(' ', ''))[1:-1], (df.iloc[0][7][1:-1].split(","))))
            info["tag"] = list(map(lambda x: (x.replace(' ', ''))[1:-1], (df.iloc[0][8][1:-1].split(","))))
            info["total_price"] = df.iloc[0][9]
            result.append(info)
    if page == int(count1 / 10 + 1):
        for i in range((page - 1) * 10, (page - 1) * 10 + count2):
            sql = 'SELECT * FROM house where id = %s' % id0[i]
            df = pandas.read_sql(sql, engine)
            info = {}
            info["id"] = int(df.iloc[0][0])
            info["img"] = df.iloc[0][1]
            info["name"] = df.iloc[0][2]
            info["price"] = df.iloc[0][3][:-7].replace(' ','')
            info["area"] = df.iloc[0][4]
            info["address"] = df.iloc[0][5]
            info["business"] = df.iloc[0][6]
            info["room"] = list(map(lambda x: (x.replace(' ', ''))[1:-1], (df.iloc[0][7][1:-1].split(","))))
            info["tag"] = list(map(lambda x: (x.replace(' ', ''))[1:-1], (df.iloc[0][8][1:-1].split(","))))
            info["total_price"] = df.iloc[0][9]
            result.append(info)
    res = {}
    res["total"] = count1
    res["info"] = result
    return res
