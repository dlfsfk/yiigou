from bs4 import BeautifulSoup
import requests
from html_downloader import HtmlDownloader
import pandas as pd


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
    result = {}
    result["totalProperty"] = em[0].text
    result["averagePriceLastWeek"] = em[1].text
    result["averagePriceThisWeek"] = em[2].text
    result["quoteChange"] = em[3].text
    res[0] = result
    # print(result)
    # 涨跌幅
    # 下载指定网页
    hd = HtmlDownloader()
    html = hd.download(url)

    # 读取网页的表格数据--抓取神器
    df = pd.read_html(html, encoding='utf-8', header=0)

    # print(df)
    # 一页有多个表格，遍历
    cnt = 0
    for df1 in df:
        cnt = cnt + 1
        results = list(df1.T.to_dict().values())  # 转换成列表嵌套字典的格式
        df1.to_csv(" result.csv", mode='a', encoding="utf_8", index=False)
        res[cnt] = results
        # print(results)
    print(res)
    return res


search('咸宁', '嘉鱼')
