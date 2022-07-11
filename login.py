import pymysql
from flask import request, app, Flask

app = Flask(__name__)#实例化app对象

def login(account,password):
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        db='houseprice',
        user='root',
        password='2458166022',
        charset='utf8'
    )
    cls = conn.cursor()
    sql="select * from user where account=%s and password=%s"
    cls.execute(sql,[account,password])
    result =cls.fetchone()
    return result
    conn.close()
#print(login(111111,111111))

@app.route('/login',methods=['POST'])
def loginRoute():
    #inputData = request.json.get('inputData')
    account=request.form['account']
    password=request.form['password']
    result=login(account,password)
    response = {}
    if result:
        userInfo = {}
        userInfo['name'] = result[3]
        userInfo['id'] = result[0]
        response['msg'] = ""
        response['result'] = userInfo
        response['code'] = 1
    else:
        response['msg'] = "没有拿到数据"
        response['result'] = {}
        response['code'] = 0

    return response


if __name__ == '__main__':
  app.run(host='0.0.0.0',#任何ip都可以访问
      port=7777,#端口
      debug=True
      )
