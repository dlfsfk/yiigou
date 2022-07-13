from flask import Flask, request
from flask_cors import CORS
import json
from util.login import login
from util.register import add_user
from util.reptile import search

app = Flask(__name__)
CORS(app, resources=r'/*')


@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return environ



@app.route('/login', methods=['POST', 'OPTIONS'])
def loginRoute():
    data = str(request.get_data())[2:-1]
    params = json.loads(data)
    account = params['loginId']
    password = params['loginPwd']
    result = login(account, password)
    response = {}
    if result:
        userInfo = {}
        userInfo['name'] = result[3]
        userInfo['loginId'] = result[1]
        response['msg'] = "登录成功"
        response['result'] = userInfo
        response['code'] = 1
    else:
        response['msg'] = "登录失败，账号或密码错误"
        response['result'] = {}
        response['code'] = 0
    return response


@app.route("/register", methods=['POST', 'OPTIONS'])
def register():
    account = request.form['account']
    password = request.form['password']
    name = request.form['name']
    result = add_user(account, password, name)
    response = {}
    if result:
        response['msg'] = "注册成功"
        response['result'] = {}
        response['code'] = 1
    else:
        response['msg'] = "注册失败"
        response['result'] = {}
        response['code'] = 0
    return response


@app.route("/housePriceTrend", methods=['GET', 'OPTIONS'])
def housePriceTrend():
    city = request.values.get("city")
    area = request.values.get("area")
    result = search(city, area)
    response = {}
    if result:
        response['msg'] = "搜索成功"
        response['result'] = result
        response['code'] = 1
    else:
        response['msg'] = "搜索失败，城市或区域错误"
        response['result'] = {}
        response['code'] = 0
    return response


if __name__ == '__main__':
    app.run(
        debug=True
    )
