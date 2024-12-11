from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import requests
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

observers = {}

def get_currency_rates():
    return requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()

def currency_updater():
    while True:
        data = get_currency_rates()
        for sid, (currency_code) in observers.items():
            if currency_code in data['Valute']:
                currency_info = data['Valute'][currency_code]
                socketio.emit('update', {
                    'currency_code': currency_code,
                    'current_rate': currency_info['Value'],
                    'previous_rate': currency_info['Previous']
                }, room=sid)
        time.sleep(5)

@socketio.on('connect')
def handle_connect():
    sid = request.sid
    emit('connected', {'message': 'Connected', 'id': sid})

@socketio.on('select_currency')
def handle_select_currency(data):
    currency_code = data.get('currency_code')
    observers[request.sid] = currency_code
    print(f"Клиент {request.sid} подключился и выбрал валюту: {currency_code}")
    emit('currency_selected', {'message': f'You selected {currency_code}', 'id': request.sid})

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in observers:
        print(f"Клиент {sid} отключился")
        del observers[sid]

if __name__ == "__main__":
    threading.Thread(target=currency_updater, daemon=True).start()
    socketio.run(app, host='localhost', port=5000, allow_unsafe_werkzeug=True)