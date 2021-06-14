# Преобразовать слова «разработка», «администрирование», «protocol», «standard»
# из строкового представления в байтовое и выполнить обратное преобразование
# (используя методы encode и decode).

user_dict_1 = ['разработка', 'администрирование', 'protocol', 'standard']
for el in user_dict_1:
    el_enc = str.encode(el, encoding='utf-8')
    print(el_enc)
    el_dec = bytes.decode(el_enc, encoding='utf-8')
    print(el_dec)
    print()
