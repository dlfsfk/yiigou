import urllib

from flask import Flask, request
from flask_cors import CORS
import json
from model.login import login
from model.register import add_user, find_user_by_account, find_user_by_name
from model.reptile import search
from model.captcha import getCaptcha

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
        response['result'] = "登录失败"
        response['code'] = 0
    return response


@app.route("/register", methods=['POST', 'OPTIONS'])
def register():
    data = str(request.get_data())[2:-1]
    params = json.loads(data)
    account = params['account']
    password = params['password']
    name = urllib.parse.unquote(params['name'])
    result = add_user(account, password, name)
    response = {}
    info = {}
    if result:
        info['success'] = 1
        response['msg'] = "注册成功"
        response['result'] = info
        response['code'] = 1
    else:
        info['success'] = 0
        response['msg'] = "注册失败"
        response['result'] = info
        response['code'] = 0
    return response

@app.route("/checkAccount", methods=['GET', 'OPTIONS'])
def checkAccount():
    account = request.values.get("account")
    result = find_user_by_account(account)
    response = {}
    if result:
        response['msg'] = "手机号已被注册"
        response['result'] = {}
        response['code'] = 0
    else:
        response['code'] = 1
    return response


@app.route("/checkName", methods=['GET', 'OPTIONS'])
def checkName():
    name = urllib.parse.unquote(request.values.get("name"))
    result = find_user_by_name(name)
    response = {}
    if result:
        response['msg'] = "用户名已存在"
        response['result'] = {}
        response['code'] = 0
    else:
        response['code'] = 1
    return response

@app.route("/housePriceTrend", methods=['GET', 'OPTIONS'])
def housePriceTrend():
    city = request.values.get("city")
    area = request.values.get("area")
    result = search(city, area)
    response = {}
    if result and not ('msg' in result.keys()):
        response['msg'] = "搜索成功"
        response['result'] = result
        response['code'] = 1
    elif result and 'msg' in result.keys():
        response['msg'] = result["msg"]
        response['result'] = result
        response['code'] = 1
    else:
        response['msg'] = "没有数据，请检查城市小区是否输入正确！"
        response['result'] = {}
        response['code'] = 0
    return response


@app.route("/getCaptcha")
def captchaRouter():
    # 用户名 查看用户名请登录用户中心->验证码、通知短信->帐户及签名设置->APIID
    phone = request.values.get("phone")
    result = getCaptcha(phone)
    response = {}
    if result:
        response['msg'] = "验证码发送成功"
        response['result'] = result
        response['code'] = 1
    else:
        response['msg'] = "验证码发送失败"
        response['result'] = {}
        response['code'] = 0
    return response


if __name__ == '__main__':
    app.run(
        debug=True
    )
