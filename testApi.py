import requests
import json

body_add_order = {
        "customer_tg_id": 1,
        "shipping_address": 'Самовывоз',
        "comment": '111',
        "delivery_required": 0,
        "order_items": [
            {
                "vegetable_id": '1',
                "quantity": '1',
            }
        ],
    }
print(body_add_order)
body_add_order = json.dumps(body_add_order)
r = requests.post("http://localhost:8000/api2/addorder", data=body_add_order)

print(r)
