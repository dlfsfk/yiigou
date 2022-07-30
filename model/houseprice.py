# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# import random
# from io import StringIO
# import time
# import pymysql
#
# url = "https://fangjia.gotohui.com/fjdata-17"
# city_url = []
# name = []
#
# # web请求头，简单伪装浏览器信息
# headers = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
# }
#
# # 获取各地网址并存储到city_url列表
# html = requests.get(url, headers=headers)
# soup = BeautifulSoup(html.text, "html.parser")
# for i in soup.find_all("tr")[1:]:
#     city_url.append(i.find("a")["href"])
#     name.append(i.find("a").text)
#
#
# def get(x, file_name):
#     html = requests.get(x, headers=headers) # 获取带有年份网址的源码
#     soup = BeautifulSoup(html.text, "html.parser")
#     x1 = "/".join(html.url.split("/")[:-1]) # 获取带有年份网址的源码的网址，用来构造各地年份网址
#     d = soup.find("table", {"class":"ntable table-striped table-hover"})
#
#     table1 = [] # 用来存储2019-2022的房价数据
#     table2 = [] # 用来存储2019-2022的房价排名数据
#
#     for i in soup.find("div", {"class":"more_nian"}).find_all("a"):
#         for year in ["2021", "2020", "2019"]:
#             if year in i["href"]:
#                 html = requests.get(x1+i["href"], headers=headers) # 通过构造的某地某年的网址获取源码
#                 soup = BeautifulSoup(html.text, "html.parser")
#                 k = 0
#                 for j in soup.find_all("table", {"class":"ntable table-striped"}):
#                     name = j.find("b", {"class":"f18"}).text
#                     time.sleep(random.randint(1, 4)) # 使用随机数进行休眠
#                     t = StringIO(str(j)) # 将对应的表格源码标签转为字符串IO
#                     df = pd.read_html(t, skiprows=1)
#                     if k==0:
#                         df[0].insert(0, "年份", [year+"年" for i in range(df[0].shape[0])])
#                         table1.append(df[0])
#                     elif k==1:
#                         df[0].insert(0, "年份", [year+"年" for i in range(df[0].shape[0])])
#                         table2.append(df[0])
#                     k = k+1
#
#     t = StringIO(str(d)) # 将对应的表格源码标签转为字符串IO
#     df = pd.read_html(t)[0] # 将字符串IO转为pandas DataFrame结构
#     df[df.columns[1]] = [str(k) for k in df[df.columns[1]].values]
#     df = df[df[df.columns[1]].str.contains("2022")]
#     year = [str(int(i.split("-")[0]))+"年" for i in df[df.columns[1]].values]
#     month = [str(int(i.split("-")[-1]))+"月" for i in df[df.columns[1]].values]
#
#     df = df[df.columns[-3:-1]]
#     df.insert(0, "月份", month)
#     df.insert(0, "年份", year)
#     df.columns = ["年份", "月份", "二手房均价", "新房均价"]
#     df["二手房均价"] = [str(i)+"元/㎡" for i in df["二手房均价"].values] # 规范二手房均价列数据
#     df["新房均价"] = [str(i)+"元/㎡" for i in df["新房均价"].values] # 规范新房均价列数据
#
#     d1, d2 = [], []
#     table1 = [df]+table1
#     table1 = table1[::-1]  #将表1数据按19年1月-22年6月显示
#     table2 = table2[::-1]
#     if len(table1)>0:
#         df1 = pd.concat(table1, axis=0) # 将列表中的DataFrame纵向合并
#         df1.insert(0, "地区", [file_name for i in range(df1.shape[0])]) # 添加地址
#         d1.append(df1)
#     if len(table2)>0:
#         df2 = pd.concat(table2, axis=0) # 将列表中的DataFrame纵向合并
#         df2.insert(0, "地区", [file_name for i in range(df2.shape[0])]) # 添加地址
#         d2.append(df2)
#     return d1, d2
#
# # ------------------------------写入数据库部分--------------------------------------------------
#
# # 创建房价数据库表语句
# ceate_table1_sql = """CREATE TABLE if NOT EXISTS fjdata (
# adress varchar(20),
# year varchar(20),
# month varchar(20),
# old_house_mean_price varchar(40),
# new_house_mean_price varchar(40)
# );
# """
# head1 = ("adress", "year", "month", "old_house_mean_price", "new_house_mean_price")
# name1 = "fjdata"
#
# # 创建房价排名数据库表语句
# ceate_table2_sql = """CREATE TABLE if NOT EXISTS fj_rank_data (
# adress varchar(20),
# year varchar(20),
# rank int,
# area varchar(40),
# mean_price int
# );
# """
# head2 = ("adress", "year", "rank", "area", "mean_price")
# name2 = "fj_rank_data"
#
#
# # 将数据写入数据库函数
# def data_to_mysql(data, createtable_sql, table_head, table_name):
#     # 打开数据库并连接
#     db = pymysql.connect(host='localhost',      # 数据库服务器位置
#                          user='root',           # 数据库用户
#                          password='root',   # 数据库用户密码
#                          database='pachong')    # 数据库名称
#
#     # 插入语句， 后面括号里面的%s与前面括号里面的列数值对应，用来防止sql注入的数据插入替换
#     insert_sql = "INSERT INTO "+table_name+" ("+", ".join(table_head)+") VALUES ("+", ".join(["%s"]*len(table_head))+");"
#     print(insert_sql)
#     cursor = db.cursor()
#     cursor.execute(createtable_sql)
#     cursor.execute("alter table "+table_name+" convert to character set utf8mb4 collate utf8mb4_bin")  #修改数据库表字符串编码
#     for i in data:
#         i = [str(j) for j in i]  #将所有数据变为字符串(处理数据库不兼容空值报错)
#         cursor.execute(insert_sql, tuple(i))  # 使用execute()方法执行sql查询， 第一个参数为sql语句，第二个参数为%s对应的数据元组
#         db.commit()
#
#     cursor.close()
#     db.close()
#     print("Data to mysql sucess......")
#
# if __name__=="__main__":
#     t1, t2 = [], []
#     for i, j in list(zip(city_url, name)):
#         x1, x2 = get(i, j)
#         t1 = t1+x1
#         t2 = t2+x2
#
#         print(j)
#
#         df1 = pd.concat(t1, axis=0) # 将列表中的DataFrame纵向合并
#         df2 = pd.concat(t2, axis=0)
#         df1.to_excel("房价.xlsx", index=False)
#         df2.to_excel("各区县房价.xlsx", index=False)
#
#     print("获取成功...") # 爬取成功标识信息
#
#     data_to_mysql(df1.values, ceate_table1_sql, head1, name1)
#     data_to_mysql(df2.values, ceate_table2_sql, head2, name2)
