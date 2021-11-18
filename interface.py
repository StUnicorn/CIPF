import secrets
import time
import main as chif
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd

def encrypt(login, password):
    filename = fd.askopenfilename()
    text = []
    key = chif.generate_string_to_numeric_hash(password, login)
    with open(filename, 'rb') as file:
        byte = file.read(1)
        while byte:
            text.append(ord(byte))
            byte = file.read(1)
    with open(filename, 'w') as file:
        start_time = time.time()
        print(*chif.cbc_e(text,key, chif.iv), file=file)
        print("Time :", time.time() - start_time)
        f = open("key.txt", 'w')
        f.write(str(key))
        f.close()
    print("Готово")

def dencrypt(login, password):
    filename = fd.askopenfilename()
    f = open("key.txt", 'r')
    key = chif.generate_string_to_numeric_hash(password, login)
    f.close()
    with open(filename) as file:
        text = file.read()
    with open(filename, 'wb') as file:
        start_time = time.time()
        crypto_text = bytes(chif.cbc_d(text.split(), key, chif.iv))
        print("Time :", time.time() - start_time)
        file.write(crypto_text)
    print("Готово")

if __name__ == '__main__':
    root = Tk()
    root.title("CIPF")
    frm = ttk.Frame(root)
    frm.grid()
    ttk.Label(frm, text="Login").grid(column=0, row=0, pady=(10, 0))
    login_1 = StringVar()
    password_1 = StringVar()
    login = ttk.Entry(frm, textvariable=login_1).grid(column=1, row=0, padx=(0, 10), pady=(10, 0))
    ttk.Label(frm, text="Password").grid(column=0, row=1, pady=(10, 0))
    password = ttk.Entry(frm, textvariable=password_1).grid(column=1, row=1, pady=(10, 0), padx=(0, 10))
    button_1 = ttk.Button(frm, text="Encrypt", command=lambda : encrypt(login_1.get(), password_1.get()))
    button_1.grid(column=0, row=2, pady=(50, 10), padx=(10, 10))
    button_2 = ttk.Button(frm, text="Decrypt", command=lambda : dencrypt((login_1.get(), password_1.get())))
    button_2.grid(column=1, row=2, pady=(50, 10), padx=(10, 10), sticky= E)
    root.mainloop()