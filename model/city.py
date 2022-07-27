import requests

from bs4 import BeautifulSoup
from xpinyin import Pinyin
headers = {

'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71'

}#爬虫[Requests设置请求头Headers],伪造浏览器
def getCityData(province):
    # 核心爬取代码
    p = Pinyin()
    province = p.get_pinyin(province, '')
    url= 'https://www.anjuke.com/fangjia/{}2022/'.format(province)
    params = {"show_ram": 1}
    response = requests.get(url, params=params, headers=headers)  # 访问url
    listData = []  # 定义数组
    soup = BeautifulSoup(response.text, 'html.parser')  # 获取网页源代码
    li = soup.find('div', class_='fjlist-box boxstyle1').find_all('li')  # .find定位到所需数据位置 .find_all查找所有的tr(表格)
    for j in li[0:]:
        city = {}
        name = j.find('b').text[5:-2]
        price = j.find('span').text[0:-3]
        city["name"] = name + "市"
        city["value"] = int(price)
        listData.append(city)
    print(listData)
    return listData