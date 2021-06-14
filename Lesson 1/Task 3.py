# Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.

user_dict_en = [b'attribute', b'type']
for el in user_dict_en:
    print(type(el))
    print(el)

# user_dict_ru = [b'класс', b'функция'] # русские слова невозможно записать в байтовом типе.
# for el in user_dict_ru:
#     print(type(el))
#     print(el)
