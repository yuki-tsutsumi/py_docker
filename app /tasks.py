from celery import Celery

# backend: 結果を保存する場所をmongodbに
# broker: キューをrabbitmqに設定
app = Celery('tasks', backend='mongodb://root:root@mongodb:27017/first_test',
                        broker='amqp://guest:guest@rabbitmq:5672')

@app.task
def add(x, y):
    # from time import sleep
    # sleep(5)
    return x + y