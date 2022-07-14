# encoding:utf-8
import requests
import random


def getCaptcha(phone):
    #用户名 查看用户名请登录用户中心->验证码、通知短信->帐户及签名设置->APIID

    account = "C71764951"
    #这是我的用户名，请更换成自己的#密码 查看密码请登录用户中心->验证码、通知短信->帐户及签名设置->APIKEY
    password = "13de0fc1092c687b1414c16a95a8dea1" #这是我的密码，已重置，请更换成自己的
    #互亿无线请求发送短信验证码的网址，直接复制使用
    url= r'http://106.ihuyi.com/webservice/sms.php?method=Submit'
    #这里是要发送给用户的手机号码
    # mobile = "15272156747"
    #随机生成6个数字
    #现定义一个空字符串用于接收生成的6个数字
    code = ''
    #for循环生成数字
    for i in range(6):
    #使用random随机生成一个数字
        num = random.randint(0, 9)
        #对数字转换成字符串后进行拼接
        code += str(num)
    # print(code)
    #这里是要发送的内容, %s 是要发送的验证码，用于占位，
    text = "您的验证码是：%s。请不要把验证码泄露给其他人。"%code
    #通过查看互亿无线提供的技术文档，发送短信验证码需要提供的数据及格式，并用字典存在data中
    data = {'account': account, 'password' : password, 'content': text, 'mobile':phone,'format':'json' }
    #使用requests 发送POST请求给互亿无线，并接收返回的response内容
    # req = requests.post(url=url, data=data)
    # #使用.text读取返回的内容
    # content =req.text
    # content={}
    # content['captcha'] = code
    #打印出返回的内容
    print(code)
    return code

