
import requests

from bs4 import BeautifulSoup

from xpinyin import Pinyin
from model.county import county


def pcity(city):
    # 核心爬取代码
    headers = {

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71'

    }  # 爬虫[Requests设置请求头Headers],伪造浏览器
    p = Pinyin()
    city2 = p.get_pinyin(city, '')
    if city2=="zhongqing":
        city2="chongqing"
    if city=="陕西":
        city2="shan3xi"
    url= 'https://www.anjuke.com/fangjia/{}2022/'.format(city2)
    params = {"show_ram":1}
    listData = []  # 定义数组
    response = requests.get(url,params=params, headers=headers)#访问url
    soup = BeautifulSoup(response.text, 'html.parser')#获取网页源代码
    # if city2=="beijing" or city2=="tianjin" or city2=="chongqing" :
    #     p = soup.find('div', class_='fjlist-box boxstyle2').find_all('li')[0].find('span').text
    #     listData.append([city,p])
    # elif city2=="shanghai":
    #     listData.append([city,'49897元/㎡'])
    if city2 == "beijing" or city2 == "tianjin" or city2 == "chongqing" or city2=="shanghai":
        county(city)
    else:
        li = soup.find('div',class_='fjlist-box boxstyle1').find_all('li')#.find定位到所需数据位置 .find_all查找所有的tr(表格)
        for j in li[0:]:
            county2 = j.find('b')
            price = j.find('span')
            # print(price.text[0:-3])
            listData.append([county2.text,price.text])
        print(listData)#打印
        return listData
pcity("北京")