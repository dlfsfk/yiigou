from config import conn


def login(account, password):
    conn.ping(reconnect=True)
    cls = conn.cursor()
    sql = "select * from user where account=%s and password=%s"
    cls.execute(sql, [account, password])
    result = cls.fetchone()
    return result
    conn.close()



