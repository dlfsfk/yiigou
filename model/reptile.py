from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from model.utils.html_downloader import HtmlDownloader

def search(city, district):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49"
    }
    url = f'https://xn.fangjia.com/zoushi?cityName={city}&__s=1&region=&keyword={district}'
    rs = requests.get(url, headers=headers)
    rs.encoding = "utf-8"
    soup = BeautifulSoup(rs.text, "html.parser")
    div = soup.find("div", attrs={"class": "trend01b"})
    em = div.find_all("em")
    res = {}
    analyze = {}
    graph = {"title": ["房价涨幅", "房价跌幅"]}
    inc = {"graphTitle": ["价格", "涨幅"]}
    dec = {"graphTitle": ["价格", "跌幅"]}
    if len(em) != 0:
        analyze["totalProperty"] = em[0].text
        analyze["averagePriceLastWeek"] = em[1].text
        analyze["averagePriceThisWeek"] = em[2].text
        analyze["quoteChange"] = em[3].text
    else:
        res["msg"] = "没有房价走势数据"
    res["analyze"] = analyze

    # 涨跌幅
    # 下载指定网页
    hd = HtmlDownloader()
    html = hd.download(url)

    # 读取网页的表格数据--抓取神器
    df = pd.read_html(html, encoding='utf-8', header=0)

    # 一页有多个表格，遍历
    exit = os.path.exists('result.csv')
    if exit:
        os.remove('result.csv')
    cnt = 0
    for df1 in df:
        cnt = cnt + 1
        results = list(df1.T.to_dict().values())  # 转换成列表嵌套字典的格式
        df1.to_csv("result.csv", mode='a', encoding="utf_8", index=False)
        # res[cnt] = results
    p = pd.read_csv("result.csv")
    c1 = list(p["本月价格"])
    c2 = []  # 存取价格
    c3 = []
    j = 0
    for a in c1:

        if j < 10:
            c1 = 0.001 * float(a)
            c2.append("{:.3f}".format(c1))
        if j > 10:
            c1 = 0.001 * float(a)
            c3.append("{:.3f}".format(c1))
        j += 1
    d1 = list(p["涨跌幅"])
    d2 = []
    d3 = []
    k = 0
    for a in d1:
        d1 = a[1:-1]
        if k < 10:
            d2.append(float(d1))
        if k > 10:
            d3.append(float(d1))
        k += 1
    e1 = list(p["小区名称"])
    e2 = []
    e3 = []
    i = 0
    for a in e1:
        if i < 10:
            e2.append(a)
        if i > 10:
            e3.append(a)
        i += 1
    res["graph"] = graph
    inc["graphName"] = e2
    inc["graphData"] = [c2, d2]
    dec["graphName"] = e3
    dec["graphData"] = [c3, d3]
    graph["data"] = [inc, dec]
    res["graph"] = graph
    return res
