import redis

r = redis.Redis(host='kvs', port=6379, db=0)

# Redisに情報を保存する
def setRedis(body, expire = 60):
    r.set(body.key, body.value)
    r.expire(body.key, expire)

# Redisから情報を取得する
def getRedis(key):
    return r.get(key)
