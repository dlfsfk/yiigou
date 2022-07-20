from config import conn

def echarts(address):
    cursor = conn.cursor()
    sql = 'SELECT * FROM fjdata where address = "武汉"'
    cursor.execute(sql)
    pd = cursor.fetchall()
    print(pd)
echarts("武汉")