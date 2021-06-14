# Создать текстовый файл test_file.txt, заполнить его тремя строками:
# «сетевое программирование», «сокет», «декоратор».
# Проверить кодировку файла по умолчанию.
# Принудительно открыть файл в формате Unicode и вывести его содержимое.

text = ['сетевое программирование', 'сокет', 'декоратор']
with open('test_file.txt', 'w', encoding='utf-8') as f:
    for line in text:
        f.write(line + '\n')

with open('test_file.txt', 'r', encoding='utf-8') as f:
    for line in f:
        print(line, end='')
