import yaml

data_to_write_yaml = {
    'list': [1, 2, 3, 4, 5],
    'int': 190,
    'dict': {
        'symbol_1': '€',
        'symbol_2': 'ʬ'
    }
}

with open('file.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(data_to_write_yaml, file, default_flow_style=True, allow_unicode=True)

with open('file.yaml') as file:
    file_data = yaml.load(file, Loader=yaml.FullLoader)
    print(f'Исходные данные ->', data_to_write_yaml)
    print(f'Совподадение с исходными данными =', data_to_write_yaml == file_data)
    print(f'Полученные данные ->', file_data)
