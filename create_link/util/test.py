import redis   #导入redis模块

# 建议使用以下连接池的方式
# 设置decode_responses=True，写入的KV对中的V为string类型，不加则写入的为字节类型。
pool = redis.ConnectionPool(host='42.193.11.20', port=6379, db=0, decode_responses=True)
rs = redis.Redis(connection_pool=pool, password="test.2021")
rs.set('color', 'red', ex=5)

