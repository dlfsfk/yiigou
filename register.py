from config import conn
from flask import request, app, Flask

app = Flask(__name__)  # 实例化app对象


def add_user(account, password, name):
    cls = conn.cursor()
    sql = "INSERT INTO user(account, password, name, authority) VALUES ('%s','%s','%s', 0)" % (account, password, name)
    cls.execute(sql)
    conn.commit()
    sql = "select * from user where account=%s and password=%s"
    cls.execute(sql, [account, password])
    result = cls.fetchone()
    return result
    conn.close()


@app.route("/register", methods=['POST'])
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


if __name__ == '__main__':
    app.run(host='0.0.0.0',  # 任何ip都可以访问
            port=7777,  # 端口
            debug=True
            )

