import sys
import random
import secrets
import time
from tkinter import *
from tkinter import ttk
import hashlib

size_block = 64

size_key = 256
rounds_size = 32


s = (
    (4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3),
    (14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9),
    (5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11),
    (7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3),
    (6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2),
    (4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14),
    (13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12),
    (1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12),
)

iv = 18318279387912387912789378912379821879387978238793278872378329832982398023031


def create_sub_keys(key):
    return [(key >> (32 * i)) & 0xFFFFFFFF for i in range(8)]


def encrypt_and_permutation_block(right_block, key):
    global s
    temp = right_block ^ key
    encrypt_block = 0
    for i in range(8):
        encrypt_block |= ((s[i][(temp >> (4*i)) & 0b1111]) << (4 * i))
    return ((encrypt_block >> 11) | (encrypt_block << (32 - 11))) & 0xFFFFFFFF


def concat_e(left_block, right_block, round_key):
    return right_block, left_block ^ encrypt_and_permutation_block(right_block, round_key)


def encrypt_function(byte, sub_keys):
    left_block = byte >> 32
    right_block = byte & 0xFFFFFFFF
    for i in range(rounds_size):
        round_key = sub_keys[i % 8] if (i < 24) else sub_keys[(rounds_size - 1) - i]
        left_block, right_block = concat_e(left_block, right_block, round_key)
    return (left_block << 32) | right_block


def concat_d(left_block, right_block, round_key):
    return right_block ^ encrypt_and_permutation_block(left_block, round_key), left_block


def decrypt_function(byte, sub_keys):
    left_block = int(byte) >> 32
    right_block = int(byte) & 0xFFFFFFFF
    for i in range(rounds_size):
        round_key = sub_keys[i] if (i < 8) else sub_keys[((rounds_size - 1) - i) % 8]
        left_block, right_block = concat_d(left_block, right_block, round_key)
    return (left_block << 32) | right_block

def cbc_e(blocks, key, iv):
    data_block = []
    res = iv
    for i in range(len(blocks)):
        x = blocks[i] ^ res
        res = encrypt_function(x, create_sub_keys(key))
        data_block.append(res)
    return data_block

def cbc_d(data_block,key, iv):
    block =[]
    res = iv
    for i in range(len(data_block)):
        data_b = decrypt_function(data_block[i], create_sub_keys(key))
        block.append(data_b ^ int(res))
        res = data_block[i]
    return block

def generate_string_to_numeric_hash(password, salt):
    result = int.from_bytes(hashlib.pbkdf2_hmac('sha256', bytes(password, encoding="UTF-8"), bytes(salt, encoding="UTF-8"), 10000, dklen=32), "big")
    return result


if __name__ == '__main__':
    start_time = ""
    if (len(sys.argv) != 3) and (sys.argv[1] != "-e" and sys.argv[1] != "-d"):
        print('''Проверь аргументы : 
        -e/-d (шифрование/дешифрование) название файла''')
    if sys.argv[1] == "-e":
        text = []
        key = secrets.randbits(256)
        with open(sys.argv[2], 'rb') as file:
            byte = file.read(1)
            while byte:
                text.append(ord(byte))
                byte = file.read(1)
        with open("_encrypt.txt", 'w') as file:
            start_time = time.time()
            print(*cbc_e(text, iv), file=file)
            print("Time :", time.time() - start_time)
        print("Готово")
    if sys.argv[1] == "-d":
        with open(sys.argv[2]) as file:
            text = file.read()
        with open("_decrypt.txt", 'wb') as file:
            start_time = time.time()
            crypto_text = bytes(cbc_d(text.split(), iv))
            print("Time :", time.time() - start_time)
            file.write(crypto_text)
        print("Готово")






