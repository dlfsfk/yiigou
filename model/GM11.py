# -*-coding:utf-8 -*-
# author:sakia   
# time:2022-07-20 9:44
# -*-coding:utf-8 -*-
# author:sakia
# time:2022-07-19 16:50
import math
import random

import matplotlib.pyplot as plt
import pymysql
import re
import pandas as pd
import numpy as np

conn1 = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    db='houseprice',
    user='root',
    password='2458166022',
    charset='utf8'
)


def connect_database(address, flag):
    conn1.ping(reconnect=True)
    cls = conn1.cursor()
    if flag == 0:
        sql = "select year,month,oprice from fjdata where address = %s order by year DESC, month DESC limit 12"
    else:
        sql = "select year,month,nprice from fjdata where address = %s  order by year DESC, month DESC limit 12"
    cls.execute(sql, address)
    price_data = cls.fetchall()
    return price_data


def data_process(address, flag):
    tdata = connect_database(address, flag)  # 获取未处理数据
    df = np.array(tdata)  # 读成 array 形式
    nprice = df[:, 2]   # 获取 old or new price
    items = []
    for i in range(len(nprice)):
        mdata = re.findall(r"\d+\.?\d*", nprice[i])
        items.append(int(mdata[0]))
    # print(items)
    return items


def GM11(x,n):
    x1 = x.cumsum()  # 一次累加
    z1 = (x1[:len(x1) - 1] + x1[1:]) / 2.0  # 紧邻均值
    z1 = z1.reshape((len(z1), 1))
    B = np.append(-z1, np.ones_like(z1), axis=1)
    Y = x[1:].reshape((len(x) - 1, 1))
    # a为发展系数 b为灰色作用量
    [[a], [b]] = np.dot(np.dot(np.linalg.inv(np.dot(B.T, B)), B.T), Y)  # 计算参数
    result = (x[0] - b / a) * np.exp(-a * (n - 1)) - (x[0] - b / a) * np.exp(-a * (n - 2))
    S1_2 = x.var()  # 原序列方差
    e = list()  # 残差序列
    for index in range(1, x.shape[0] + 1):
        predict = (x[0] - b / a) * np.exp(-a * (index - 1)) - (x[0] - b / a) * np.exp(-a * (index - 2))
    e.append(x[index - 1] - predict)
    S2_2 = np.array(e).var()  # 残差方差
    C = S2_2 / S1_2  # 后验差比
    if C <= 0.35:
        assess = '后验差比<=0.35，模型精度等级为好'
    elif C <= 0.5:
        assess = '后验差比<=0.5，模型精度等级为合格'
    elif C <= 0.65:
        assess = '后验差比<=0.65，模型精度等级为勉强'
    else:
        assess = '后验差比>0.65，模型精度等级为不合格'
    # 预测数据
    predict = list()
    for index in range(x.shape[0] + 1, x.shape[0] + n + 1):
        predict.append((x[0] - b / a) * np.exp(-a * (index - 1)) - (x[0] - b / a) * np.exp(-a * (index - 2)))
    predict = np.array(predict)
    return {
        'a': {'value': a, 'desc': '发展系数'},
        'b': {'value': b, 'desc': '灰色作用量'},
        'predict': {'value': result, 'desc': '第%d个预测值' % n},
        'C': {'value': C, 'desc': assess},
        'predict': {'value': predict, 'desc': '往后预测%d个的序列' % (n)},
    }

# if __name__ == "__main__":
def return_data(address,flag):
    data =  data_process(address, flag)
    data.reverse()
    x = data[0:12]  # 输入数据
    x = np.array(data)
    y = data[0:12]  # 需要预测的数据
    result = GM11(x, len(y))
    predict = result['predict']['value']
    predict = np.round(predict, 1)
    # print('真实值:', y)
    # print('预测值:', predict)
    # print("模型参数",result)
    random.shuffle(predict)
    y.extend(predict)
    # print('真实值个数：',len(y))
    # print('预测值个数：', len(predict))
    x1 = ['2021-07','2021-08','2021-09','2021-10','2021-11','2021-12','2022-01','2022-02','2022-03','2022-04','2022-05','2022-06']
    x2 = ['2022-07','2022-08','2022-09','2022-10','2022-11','2022-12','2023-01','2023-02','2023-03','2023-04','2023-05','2023-06']
    x1.extend(x2)
    # 画图， 调用时 此部分可以注释掉
    # --------------------------------------------------
    # print('输入',x)
    plt.plot(x1[0:12], y[0:12], color='green', marker='o', linestyle='dashed', linewidth=2, markersize=12)
    # plt.flot(x, y, 'go--'，linewidth=2, markersize=12)
    # print('y是',y)

    # 可以在一个画布上绘制多张图片，
    plt.plot(x1[12:24], y[12:24], color='red', marker='*', linestyle='solid', linewidth=2, markersize=12)
    plt.show()
    # --------------------------------------------------
    return x1,x2,y,predict
# 测试部分 函数两个参数自己设置
# x1,x2,y,predict = return_data("武汉",1)
# print('预测数据：',predict)

# 注意  address 表示选中的地区地址， flag = 0 表示 二手房， flag = 1 表示 新房