import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# Устанавливаем соединение с RabbitMQ-брокером, работающим на локальном хосте.
# pika.BlockingConnection - создает блокирующее соединение.
# pika.ConnectionParameters(host='localhost') - задает параметры соединения, в данном случае, хост.

channel = connection.channel()
# Создаем канал (channel) для взаимодействия с брокером.  
# Канал используется для отправки и получения сообщений,  управление очередями и т.д.

channel.queue_declare(queue='orders')
# Объявляем очередь с именем 'orders'.

def callback(ch, method, properties, body):
    order = json.loads(body)
    print(f"Received order: {order}")
    # В этом примере - лишь вывод информации на консоль.


channel.basic_consume(queue='orders', on_message_callback=callback, auto_ack=True)
# on_message_callback=callback - функция обратного вызова, которая будет вызываться при получении сообщения.

print(' [*] Ожидается сообщение. Для выхода нажмите CTRL+C')
channel.start_consuming()
# Начинает прослушивание очереди. Эта функция блокируется, ожидая сообщений.  Ctrl+С прерывает выполнение.