import hashlib
import requests
import datetime


def create_link():
    current_time = datetime.datetime.now()
    a = 'qee,w  sldlflsl' + str(current_time.timestamp())
    signature = hashlib.sha256(a.encode('utf-8')).hexdigest()
    url = 'https://api.freekassa.ru/v1/orders/create'
    data = {'shopId': 18316, 'nonce': 1, 'signature': signature, 'i': 6, 'email': 'kisell22@yandex.ru',
            'ip': '89.208.113.66', 'amount': 100, 'currency': 'RUB'}
    x = requests.post(url, data=data)
    print(x.text)
    url1 = 'https://api.freekassa.ru/v1/currencies'
    data1 = {'shopId': 18316, 'nonce': 1, 'signature': signature}
    x1 = requests.post(url, data=data)
    print(x1.text)