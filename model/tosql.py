import xlrd2

import pymysql


# import importlib

# importlib.reload(sys) #出现呢reload错误使用


def open_excel():
    try:

        book = xlrd2.open_workbook("房价.xlsx")  # 文件名，把文件与py文件放在同一目录下

    except:

        print("open excel file failed!")

    try:

        sheet = book.sheet_by_name("Sheet1")  # execl里面的worksheet1

        return sheet

    except:

        print("locate worksheet in excel failed!")


# 连接数据库

try:

    db = pymysql.connect(host="127.0.0.1", user="root",

                         passwd="2458166022",

                         db="houseprice",

                         charset='utf8')

except:

    print("could not connect to mysql server")


def search_count():
    cursor = db.cursor()

    select = "select year,month from fjdata where address = '武汉'"  # 获取表中xxxxx记录数

    cursor.execute(select)  # 执行sql语句

    pd = cursor.fetchall()

    print(pd)


def insert_deta():
    sheet = open_excel()

    cursor = db.cursor()
    print(sheet.nrows)
    for i in range(1, sheet.nrows):  # 第一行是标题名，对应表中的字段名所以应该从第二行开始，计算机以0开始计数，所以值是1

        area = sheet.cell(i, 0).value  # 取第i行第0列
        year = sheet.cell(i, 1).value  # 取第i行第1列，下面依次类推
        month = sheet.cell(i, 2).value
        old = sheet.cell(i, 3).value
        new = sheet.cell(i, 4).value

        value = (area,year,month,old,new)

        print(value)

        sql = "INSERT INTO info(area,year,month,old,new)VALUES(%s,%s,%s,%s,%s)"

        cursor.execute(sql, value)  # 执行sql语句

        db.commit()

    cursor.close()  # 关闭连接


# insert_deta()
search_count()
db.close()  # 关闭数据

print("ok ")
