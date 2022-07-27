
import requests

from bs4 import BeautifulSoup

headers = {

'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71'

}#爬虫[Requests设置请求头Headers],伪造浏览器

    # 核心爬取代码
def pprovince():
    url= 'https://www.maigoo.com/news/480610.html'

    params = {"show_ram":1}

    response = requests.get(url,params=params, headers=headers)#访问url

    listData=[]#定义数组

    soup = BeautifulSoup(response.text, 'html.parser')#获取网页源代码

    tr = soup.find('table',class_='mod_table table1 fcolor30').find_all('tr')#.find定位到所需数据位置 .find_all查找所有的tr(表格)

    # 去除标签栏

    for j in tr[1:]: #tr2[1:]遍历第1列到最后一列，表头为第0列

        td = j.find_all('td')#td表格

        city = td[1].get_text().strip()

        price = td[2].get_text().strip()

        listData.append([city,price])

    print (listData)#打印
    return listData
pprovince()