import random
from random import choice
from string import ascii_lowercase

def generate_key_gamm(length):
    return [choice(ascii_lowercase) for i in range(length)]

def generate_key_sub():
    key = []
    numbers = [i for i in range(256)]
    summ = [-1 for i in range(256)]
    rand = random.randint(0, 256)
    for i in range(256):
        while (rand + i) % 256 in summ:
            if len(numbers) == 0:
                rand = random.randint(1,256)
            else:
                rand = random.choice(numbers)
                numbers.remove(rand)
        summ[i] = (rand + i) % 256
        key.append(rand)
        rand = random.randint(1, 256)
    return key, summ

def generate_key_perm(length):
    numbers = [i for i in range(length)]
    key = []
    for i in range(length):
        rand = random.choice(numbers)
        key.append(rand)
        numbers.remove(rand)
    return key

def sub_e(data):
    key, summ = generate_key_sub()
    data_ = []
    for i in range(len(data)):
        data_.append((data[i] + key[data[i]]) % 256)
    return data_, key, summ

def sub_d(data_, key,summ):
    key_d = [256 - i for i in key]
    data__ = []
    for i in range(len(data_)):
        data__.append((data_[i] + key_d[summ.index(data_[i])]) % 256)
    return data__

def perm_e(data, length):
    le = len(data) % length
    data = list(data)
    for i in range(length - le):
        data.append(255)
    key = generate_key_perm(length)
    data_ = []
    l = 0
    for i in range(len(data)):
        j = key[i % length]
        if i % length == 0 and i != 0:
            l = l + length
        data_.append(data[j + l])
    return data_, key, le

def perm_d(data_, key, le):
    key_d = [i for i in range(len(key))]
    for i in range(len(key)):
        key_d[key[i]] = i
    data__ = []
    l = 0
    for i in range(len(data_)):
        j = key_d[i % len(key)]
        if i % len(key) == 0 and i != 0:
            l = l + len(key)
        data__.append(data_[j + l])
    for i in range(len(key) - le):
        del data__[-1]
    return data__

def gamm_e(data, length):
    le = len(data) % length
    data = list(data)
    for i in range(length - le):
        data.append(255)
    key = generate_key_gamm(length)
    data_ = []
    l = 0
    for i in range(len(data)):
        j = key[i % length]
        if i % length == 0 and i != 0:
            l = l + length
        data_.append((data[i] + ord(j))% 256)
    return data_, key, le

def gamm_d(data_,key, le):
    data__ = []
    l = 0
    for i in range(len(data_)):
        j = key[i % len(key)]
        if i % len(key) == 0 and i != 0:
            l = l + len(key)
        data__.append((data_[i] + (256 - ord(j))) % 256)
    for i in range(len(key) - le):
        del data__[-1]
    return data__

def generate_rounds(length):
    round = [-1 for i in range(length)]
    r = random.randint(0,2)
    round[0] = r
    while r == round[0]:
        r = random.randint(0,2)
    round[1] = r
    i = 2
    while i != length:
        while r == round[i-1] or (r == round[i-2] and (r == 0 or r == 1)):
            r = random.randint(0,2)
        round[i] = r
        i = i + 1
    return round

def cicle_e(data):
    r = random.randint(1, 7)
    data_ = []
    for i in range(len(data)):
        data_.append(data[i] << r)
    return data_, r

def cicle_d(data, r):
    data_ = []
    for i in range(len(data)):
        data_.append(data[i] >> r)
    return data_

def round_e(data, rounds, length):
    print("------Шифрование-----------")
    print('Раунды: ',rounds)
    data_ = data
    key1, key2 = length_keys()
    keys = []
    for i in range(length):
        if rounds[i] == 0:
            print('Перестановка')
            data_, key_p, le_p = perm_e(data_, key1)
            keys.extend([key_p, le_p])
        elif rounds[i] == 1:
            print('Подстановка')
            data_, key_s, summ = sub_e(data_)
            keys.extend([key_s, summ])
        elif rounds[i] == 2:
            print('Гаммирование')
            data_, key_g, le_g = gamm_e(data_, key2)
            keys.extend([key_g, le_g])
        elif rounds[i] == 3:
            print('Сдвиг')
            data_, r = cicle_e(data_)
            keys.append(r)
    return data_, keys

def round_d(data, rounds, keys):
    print("------Дешифрование-----------")
    rounds_d = list(reversed(rounds))
    print('Раунды', rounds_d)
    data_ = data
    for i in range(len(rounds_d)):
        if rounds_d[i] == 0:
            print('Перестановка')
            le_p = keys.pop()
            key_p = keys.pop()
            data_ = perm_d(data_, key_p,  le_p)
        elif rounds_d[i] == 1:
            print('Подстановка')
            summ = keys.pop()
            key_s = keys.pop()
            data_ = sub_d(data_, key_s, summ)
        elif rounds_d[i] == 2:
            print('Гаммирование')
            le_g = keys.pop()
            key_g = keys.pop()
            data_ = gamm_d(data_, key_g,  le_g)
        elif rounds_d[i] == 3:
            print('Сдвиг')
            r = keys.pop()
            data_ = cicle_d(data_, r)
    return data_

def length_keys():
    return random.randint(3,10), random.randint(5,15)

def main():
    length = int(input('Введите количество раундов: '))
    f = open('hello.jpg', 'rb')
    data = f.read()
    f.close()
    rounds = generate_rounds(length)
    data_, keys = round_e(data, rounds,length)
    data__ = round_d(data_, rounds, keys)
    print(data == bytes(data__)) # одинаковы или нет
    file = open('w1.jpg', 'wb')
    file.write(bytes(data__))
    print('Итоговый результат записан в файл', file.name)
    file.close()
if __name__ == '__main__':
    main()