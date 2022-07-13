from bs4 import BeautifulSoup
import requests





def search(city,district):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49"
    }
    url = f'http://xn.fangjia.com/zoushi?cityName={city}&__s=1&region=&keyword={district}'
    rs = requests.get(url,headers=headers)
    rs.encoding="utf-8"
    soup = BeautifulSoup(rs.text, "html.parser")
    div = soup.find("div",attrs={"class":"trend01b"})
    em=div.find_all("em")
    result={}
    result["totalProperty"] = em[0].text
    result["averagePriceLastWeek"] = em[1].text
    result["averagePriceThisWeek"] = em[2].text
    result["quoteChange"] = em[3].text
    return result
