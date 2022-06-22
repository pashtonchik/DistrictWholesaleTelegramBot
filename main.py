import requests
import json
import datetime
order_info = {'name': 'Mikhail Prokhrov', 'phone_number': '89266806345',
 'shipping_address': {'country_code': 'RU', 'state': 'Москва',
  'city': 'Москва', 'street_line1': '13', 'street_line2': 'Дубосековская', 
  'post_code': '1337'}}

def get_customer(info):
    url = 'http://194.58.107.7:8000'
    req = f"""{url}/api/resource/Selling%20Order%20OneTwoSneaker"""

    headers = {
    'Authorization': "token ed87374be6f1468:769aa1df0bae7f5"
    }
    response = requests.get(req, headers=headers)
    print(type(response))
    dict = json.loads(response.text)
    print(dict)

def insert_order(info):
    print(datetime.datetime.now().date())
    date = str(datetime.datetime.now().date())
    url = 'http://194.58.107.7:8000'
    req = f"""{url}/api/resource/Selling%20Order%20OneTwoSneaker"""
    jn = {"customer_name": info["name"],
        "date": date,
        "phone_number": info["phone_number"],
        "address1": info["shipping_address"]["street_line1"],
        "address2": info["shipping_address"]["street_line2"],
        "city": info["shipping_address"]["city"],
        "state": info["shipping_address"]["state"],
        "postcode": info["shipping_address"]["post_code"],
        "product" : [{
            "product_name": "Adidas",
            "size": "39",
            "quantity": "1",
            "price": "19000"
        }]
    }
    headers = {
    'Authorization': "token ed87374be6f1468:769aa1df0bae7f5",
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }
    data = json.dumps(jn)
    response = requests.post(url = req, data = data, headers=headers)
    print(response.text)




if __name__=='__main__':
    sneaker = [{'title': 'Adidas Yeezy', 'price': 17999, 'Image': '/static/media/AdidasYeezy.e1c6eeeb8323e15174ac.png', 'id': 0, 'sizes': [36, 37, 38, 44], 'size': 44, 'quantity': 1}, {'title': 'Adidas Yung 1', 'price': 5350, 'Image': '/static/media/AdidasYung1.6e3ebe4e98b530282e76.png', 'id': 1, 'sizes': [1, 2, 3, 4], 'size': 2, 'quantity': 1}, {'title': 'Nike Air Force 1', 'price': 13999, 'Image': '/static/media/NikeAirForce1.0e0f760de735209fc567.png', 'id': 2, 'sizes': [1, 2, 3, 4], 'size': 2, 'quantity': 1}]
    for i in (sneaker):
        print(i['title'])
