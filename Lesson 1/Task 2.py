# Каждое из слов «class», «function», «method» записать в байтовом типе
# без преобразования в последовательность кодов (не используя методы encode и decode)
# и определить тип, содержимое и длину соответствующих переменных.

user_dict_1 = [b'class', b'function', b'method']
for el in user_dict_1:
    print(type(el))
    print(el)
    print(len(el))
