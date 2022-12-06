import pika


# メッセージ受信のたびに呼び出される関数
def callback(channel, method, properties, body):
    print(f" [x] Received {body}")
    message = body.decode()

    if message == "hey":
        print("hey there")
    elif message == "hello":
        print("well hello there")
    else:
        print(f"sorry i did not understand {body}")

    print(" [x] Done")
    # 受信したことをキューに知らせる
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    # 初期設定
    print(" [*] Connecting to server ...")
    # RabbitMQサーバと接続（ホスト名にはコンテナ名を指定しているが，Dockerを使ってない場合はIPアドレスを指定
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq"))
    # チャンネルの確立
    channel = connection.channel()
    # メッセージを受信するためのキュー(task_queue)が存在することを確認
    channel.queue_declare(queue="task_queue", durable=True)
    # 前のメッセージの処理が完了してACKが返るまで次のメッセージを送信しないようにするオプション
    channel.basic_qos(prefetch_count=1)
    # キュー(task_queue)にcallback関数をサブスクライブしてメッセージ受信のたびに実行
    channel.basic_consume(queue="task_queue", on_message_callback=callback)

    try:
        print(" [*] Waiting for messages. To exit press Ctrl+C")
        channel.start_consuming()
    except KeyboardInterrupt:
        print(" [x] Done")


if __name__ == '__main__':
    main()