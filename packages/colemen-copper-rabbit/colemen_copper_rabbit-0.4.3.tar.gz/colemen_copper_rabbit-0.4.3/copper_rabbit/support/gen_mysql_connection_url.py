import colemen_utils as _c


def gen_mysql_connection_url(data):
    user = _c.obj.get_arg(data,['user'],None,(str))
    password = _c.obj.get_arg(data,['password'],None,(str))
    host = _c.obj.get_arg(data,['host'],None,(str))
    port = _c.obj.get_arg(data,['port'],3306,(str,int))
    database = _c.obj.get_arg(data,['database'],None,(str))
    print(f"data:{data}")
    db_url = f"mysql://{user}:{password}@{host}:{port}/{database}"
    return db_url