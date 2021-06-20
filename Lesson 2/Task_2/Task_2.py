import json


def write_order_to_json(item, quantity, price, buyer, date, **kwargs):
    product = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    }

    with open('orders.json', 'r') as file_r:
        orders_data = json.load(file_r)

        if 'orders' not in orders_data:
            orders_data['orders'] = []
        orders_data['orders'].append(product)

        with open('orders.json', 'w', encoding='utf-8') as file_w:
            file_w.write(json.dumps(orders_data, indent=4))


write_order_to_json('Авто', 1, 123456, 'Питон', '20.06.2021')
write_order_to_json('Ноутбук', 2, 67890, 'Джон', '08.08.2020')
write_order_to_json('bed', 1, 10000, 'Alex', '18.03.2094')
write_order_to_json('flat', 1, 12345679, 'Vlad', '18.03.2024')
