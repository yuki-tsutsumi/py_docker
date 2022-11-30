import redisService
import uuid
import json
import redis

class ApiUtil:

    kvs = redis.Redis(host='kvs', port=6379, db=0)

    EXPIRE = 60*60
    REDIS_KEY_ID = "id"
    accessKey = None

    def activate(self):
        accessKey = str(uuid.uuid4())
        redisVal = {'id':''}
        self.setAccessKey(accessKey)
        self.setRedis(self.REDIS_KEY_ID,json.dumps(redisVal),self.EXPIRE)
        return accessKey
    
    def setAccessKey(self,accessKey):
        self.accessKey = accessKey

    # Redisに情報を保存する
    def setRedis(self,keyPrefix, value, expire = 60):
        key = keyPrefix + '::' + self.accessKey
        self.kvs.set(key, value)
        self.kvs.expire(key, expire)

    # Redisから情報を取得する
    def getRedis(self,key):
        return self.kvs.get(key)
