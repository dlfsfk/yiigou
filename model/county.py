import requests
from bs4 import BeautifulSoup
from lxml import etree

def county(county):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71'
    }
    url = "https://www.gotohui.com/category/search.html?word={}".format(county)
    params = {"show_ram": 1}
    response = requests.get(url, params=params, headers=headers)  # 访问url
    soup = BeautifulSoup(response.text, 'html.parser')  # 获取网页源代码
    a1 = soup.find("div", class_='info').find("a", class_='name')
    a2 = a1["href"].split("/")[-1]
    listData = []
    url = "https://fangjia.gotohui.com/fjdata-{}".format(a2)
    html = requests.get(url)
    etree_html = etree.HTML(html.text)
    tr = etree_html.xpath('.//div[@class="recommend"][1]/table/tbody/tr')
    for j in tr:
        county = j.xpath('.//td[1]/a/text()')[0]
        if county=='市区':
            continue
        price = j.xpath('.//td[2]/text()')[0]
        listData.append([county,price])
    print(listData)

county("咸宁")
