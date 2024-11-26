import pika
import json
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='orders')

def publish_order(order):
    channel.basic_publish(exchange='',
                          routing_key='orders',
                          body=json.dumps(order))
    print(f"Order {order['orderID']} published")


# Пример данных (имитация данных из базы)
products = {
    1: {'ProductName': 'paper', 'Price': 159.99},
    2: {'ProductName': 'rolton', 'Price': 44.50},
    3: {'ProductName': 'oreo', 'Price': 79.99}
}

# Добавляем заказы в очередь
for i in range(5):
    order = {
        'orderID': i + 1,
        'customerID': i * 2 + 1,
        'items': [
            {'productID': 1, 'quantity': 2},
            {'productID': 2, 'quantity': 1}
        ]
    }
    publish_order(order)
    time.sleep(1) # Имитация задержки между заказами

connection.close()


