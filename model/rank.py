import pandas
from sqlalchemy import create_engine
def rank1(city):
    engine = create_engine('mysql+pymysql://root:2458166022@localhost:3306/houseprice?charset=utf8')
    sql = 'SELECT * FROM fj_rank_data where address = "%s"' % city
    df = pandas.read_sql(sql, engine)
    count1=len(df)
    area=[]
    price = []
    for i in range(0,count1):
        area.append(df["area"][i])
        price.append(df["mean_price"][i])
    res = {}
    res["title"] = ["县区房价排名"]
    basicGraph = {}
    basicGraph["graphTitle"] = area
    basicGraph["graphName"] = ["县区房价排名"]
    basicGraph["graphData"] =price
    print(basicGraph)
    return basicGraph
rank1("武汉")
