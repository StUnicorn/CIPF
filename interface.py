import os
import time
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import ttk
from string import ascii_lowercase
from string import ascii_uppercase
from string import digits
from string import punctuation

import main as chif

length_password = 8

def encrypt(login, password):
    global frm, text
    if(password_verify(password)):
        filename = fd.askopenfilename()
        encrypt_function(filename, login, password)
    else:
        messagebox.showerror("Ошибка!", text.get())

def encrypt_function(filename, login, password):
    text = []
    key = chif.generate_string_to_numeric_hash(password, login)
    with open(filename, 'rb') as file:
        byte = file.read(1)
        while byte:
            text.append(ord(byte))
            byte = file.read(1)
    with open(filename, 'w') as file:
        start_time = time.time()
        print(*chif.cbc_e(text, key, chif.iv), file=file)
        print("Time :", time.time() - start_time)
        f = open("key.txt", 'w')
        f.write(str(key))
        f.close()
    print("Готово")

def encrypt_folder_function(file_path, login, password):
    for root, dirs, files in os.walk(file_path):
        for f in files:
            encrypt_function(os.path.join(root, f), login, password)
        for dir in dirs:
            encrypt_folder_function(os.path.join(root, dir), login, password)


def encrypt_folder(login, password):
    global text
    if (password_verify(password)):
        file = fd.askdirectory()
        encrypt_folder_function(file, login, password)
    else:
        messagebox.showerror("Ошибка!", text.get())

def dencrypt(login, password):
    global text
    if (password_verify(password)):
        filedir = fd.askopenfilename()
        decrypt_function(filedir, login, password)
    else:
        messagebox.showerror("Ошибка!", text.get())

def decrypt_folder(login, password):
    global text
    if (password_verify(password)):
        file = fd.askdirectory()
        decrypt_folder_function(file, login, password)
    else:
        messagebox.showerror("Ошибка!", text.get())

def decrypt_folder_function(file_path, login, password):
    for root, dirs, files in os.walk(file_path):
        for f in files:
            decrypt_function(os.path.join(root, f), login, password)
        for dir in dirs:
            decrypt_folder_function(os.path.join(root, dir), login, password)

def decrypt_function(file_path, login, password):
    f = open("key.txt", 'r')
    key = chif.generate_string_to_numeric_hash(password, login)
    f.close()
    with open(file_path) as file:
        text = file.read()
    with open(file_path, 'wb') as file:
        start_time = time.time()
        crypto_text = bytes(chif.cbc_d(text.split(), key, chif.iv))
        print("Time :", time.time() - start_time)
        file.write(crypto_text)
    print("Готово")

def password_verify(W):
    if (len(W) < 8):
        text.set("Пароль меньше 8")
        return False
    elif(len(set(ascii_lowercase).intersection(W)) == 0):
        text.set("Пароль должен содержать строчные буквы")
        return False
    elif (len(set(ascii_uppercase).intersection(W)) == 0):
        text.set("Пароль должен содержать прописные буквы")
        return False
    elif len(set(digits).intersection(W)) == 0:
        text.set("Пароль должен содержать цифры")
        return False
    elif len(set(punctuation).intersection(W)) == 0:
        text.set("Пароль должен специальные символы")
        return False
    elif len(''.join([char for index, char in enumerate(W) if char in W[0:index]])) != 0:
        text.set("Пароль должен содержать уникальные символы")
        return False
    else:
        text.set("")
        return True

root = Tk()
root.title("H-NyA")
frm = ttk.Frame(root)
text = StringVar()
frm.grid()
ttk.Label(frm, text="Login").grid(column=0, row=0, pady=(10, 0))
ttk.Label(frm, textvariable=text).grid(column=1, row=2, pady=(10, 0))
login_1 = StringVar()
password_1 = StringVar()
password_1.trace('w', lambda nm, idx, mode, var=password_1: password_verify(var.get()))
login = ttk.Entry(frm, textvariable=login_1).grid(column=1, row=0, padx=(0, 10), pady=(10, 0))
ttk.Label(frm, text="Password").grid(column=0, row=1, pady=(10, 0))
password = ttk.Entry(frm, textvariable=password_1, show="*").grid(column=1, row=1, pady=(10, 0), padx=(0, 10))
button_1 = ttk.Button(frm, text="Encrypt", command=lambda : encrypt(login_1.get(), password_1.get()))
button_1.grid(column=0, row=3, pady=(50, 10), padx=(10, 10))
button_2 = ttk.Button(frm, text="Decrypt", command=lambda : dencrypt(login_1.get(), password_1.get()))
button_2.grid(column=1, row=3, pady=(50, 10), padx=(10, 10), sticky= E)
button_3 = ttk.Button(frm, text="Encrypt Folder", command=lambda: encrypt_folder(login_1.get(), password_1.get()))
button_3.grid(column=0, row=4, pady=(5, 10), padx=(10, 10))
button_4 = ttk.Button(frm, text="Decrypt Folder", command=lambda: decrypt_folder(login_1.get(), password_1.get()))
button_4.grid(column=1, row=4, pady=(5, 10), padx=(10, 10), sticky= E)
root.mainloop()