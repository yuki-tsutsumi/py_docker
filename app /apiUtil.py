import uuid
import json
import redis

class ApiUtil:

    kvs = redis.Redis(host='kvs', port=6379, db=0)

    EXPIRE = 60*60
    REDIS_KEY_ID = "id"
    accessKey = None

    def activate(self,cookieVal):
        if self.getAccessKey(cookieVal) and self.getRedis(self.REDIS_KEY_ID):
            return "already" #Exceptionを投げたい

        accessKey = str(uuid.uuid4())
        redisVal = {'id':''}
        self.setAccessKey(accessKey)
        self.setRedis(self.REDIS_KEY_ID,json.dumps(redisVal),self.EXPIRE)
        return accessKey
    
    def getAccessKey(self,cookieVal):
        if self.accessKey == None:
            self.accessKey = cookieVal
        return self.accessKey

    def setAccessKey(self,accessKey):
        self.accessKey = accessKey

    # Redisに情報を保存する
    def setRedis(self,keyPrefix, value, expire = 60):
        key = keyPrefix + '::' + self.accessKey
        self.kvs.set(key, value)
        self.kvs.expire(key, expire)

    # Redisから情報を取得する
    def getRedis(self,keyPrefix,expire = 60):
        key = keyPrefix + '::' + self.accessKey
        value = self.kvs.get(key)
        if value:
            self.kvs.expire(key, expire) 
        return value
