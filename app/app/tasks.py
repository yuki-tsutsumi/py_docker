from celery import Celery
import os

# backend: 結果を保存する場所をmongodbに
# broker: キューをrabbitmqに設定

BACKEND_URL = "%s://%s:%s@%s:%d/%s" % (
    os.environ.get("MONGO_DATABASE_PROTOCOL"),os.environ.get("MONGO_DATABASE_USER"),
    os.environ.get("MONGO_DATABASE_PASSWORD"), os.environ.get("MONGO_DATABASE_HOST"), 
    int(os.environ.get("MONGO_DATABASE_PORT")), os.environ.get("MONGO_DATABASE_NAME"))

BROKER_URL = "%s://%s:%s@%s:%d" % (
    os.environ.get("BROKER_PROTOCOL"),os.environ.get("BROKER_USER"),
    os.environ.get("BROKER_PASSWORD"), os.environ.get("BROKER_HOST"), 
    int(os.environ.get("BROKER_PORT")))
app = Celery('tasks', backend=BACKEND_URL,
                        broker=BROKER_URL)

@app.task
def add(x, y):
    return x + y