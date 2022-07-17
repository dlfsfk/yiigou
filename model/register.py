from config import conn


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




