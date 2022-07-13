from bs4 import BeautifulSoup
from flask import Flask,render_template,request
import requests
import xlwt
import xlrd
from xlutils.copy import copy

from util.html_downloader import HtmlDownloader

import pandas as pd





def search(city,district):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49"
    }

    # url="http://xn.fangjia.com/zoushi?cityName=%s&__s=1&region=&keyword=%s" %(city,district)
    url = f'http://xn.fangjia.com/zoushi?cityName={city}&__s=1&region=&keyword={district}'
    # url="http://xn.fangjia.com/zoushi?cityName=%E5%92%B8%E5%AE%81&__s=1&region=&keyword=%E7%A2%A7%E6%A1%82%E5%9B%AD"
    # print(url)
    # hd = HtmlDownloader()
    # html = hd.download(url)
    # print(html)

    rs = requests.get(url,headers=headers)
    rs.encoding="utf-8"
    soup = BeautifulSoup(rs.text, "html.parser")
    div = soup.find("div",attrs={"class":"trend01b"})
    # print(div.div.em.text)
    #print(div)
    em=div.find_all("em")
    # print(em)
    # wb = xlrd.open_workbook("excelTest.xls")
    # all_sheet = wb.sheet_names()
    # first_sheet = wb.sheet_by_name(all_sheet[0])
    # rows = first_sheet.nrows
    # new_workbook = copy(wb)
    # new_sheet = new_workbook.get_sheet(0)

    # sheet = wb.add_sheet("主页数据",cell_overwrite_ok=True)
    # sheet = wb.get_sheet(1)
    # i=0
    result={}
    result["楼盘总量"] = em[0].text
    result["上周均价"] = em[1].text
    result["本周均价"] = em[2].text
    result["涨跌幅度"] = em[3].text
    # for a in em:
    #     new_sheet.write(rows,i,a.text)
    #
    #     i+=1
    # new_workbook.save("excelTest.xls")
    # print(result)
    return result
    # print(result)
    # df = pd.read_html(html)
    # # print(df)
    # # 新建文件存放表格数据
    # writer = pd.ExcelWriter("上海小区.xlsx")
    # # 一页有多个表格，遍历
    # cnt = 0
    # for df1 in df:
    #     cnt = cnt + 1
    #     # 写进文件
    #     df1.to_excel(writer, sheet_name='表' + str(cnt))
    #
    # # 写完关闭文件
    # writer.close()
# search("襄阳","宜城")