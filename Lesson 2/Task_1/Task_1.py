import csv
from re import findall


def get_data(files: list, parameters: list):
    list_files = files
    result_data = [parameters]
    for file_name in list_files:
        with open(file_name, 'r', encoding='windows-1251') as file:
            file_data = file.read()
            os_prod_list = findall(parameters[0] + r".+", file_data)[0].split('  ')[-1].strip()
            os_name_list = findall(parameters[1] + r".+", file_data)[0].split('  ')[-1].strip()
            os_code_list = findall(parameters[2] + r".+", file_data)[0].split('  ')[-1].strip()
            os_type_list = findall(parameters[3] + r".+", file_data)[0].split('  ')[-1].strip()

            data = [os_prod_list, os_name_list, os_code_list, os_type_list]
            result_data.append(data)

    print(result_data)
    return result_data


def write_to_csv(file_name, files: list, parameters: list):
    list_to_write = get_data(files, parameters)

    with open(file_name, 'w', encoding='utf-8') as file:
        file_writer = csv.writer(file)
        for row in list_to_write:
            file_writer.writerow(row)


files_list = ['info_1.txt', 'info_2.txt', 'info_3.txt']
params_list = ["Изготовитель системы", "Название ОС", "Код продукта", "Тип системы"]
write_to_csv('result.csv', files_list, params_list)
