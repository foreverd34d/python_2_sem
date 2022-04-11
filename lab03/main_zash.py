import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image


def to_ascii(s):
    result = []
    for let in s:
        bin_let = bin(ord(let))[2:]
        result.append(bin_let)

    return result


def extend(a):
    for i in range(len(a)):
        while len(a[i]) < 8:
            a[i] = '0' + a[i]

    return a


def encode(img, msg):
    data = list(img.getdata())
    ascii_text = extend(to_ascii(msg))
    new_data: list = [list(data[i]) for i in range(len(ascii_text) * 4 + 1)]

    l = 0
    for sym in ascii_text:
        current_bit = 0
        for i in range(4):
            encoded_pixel = sym[current_bit] + sym[current_bit + 1] + str(new_data[l][0])[-1]
            new_data[i + l][0] = int(encoded_pixel)
            current_bit += 2
        l += 4

    encoded_pixel = '2' + str(new_data[l][0])[1:]
    new_data[l][0] = int(encoded_pixel)

    # Convert to tuple list
    for i in range(len(new_data)):
        new_data[i] = tuple(new_data[i])
    img.putdata(new_data)


def is_bmp(filename):
    _, ext = os.path.splitext(filename)
    if ext != '.bmp':
        messagebox.showerror('Oops!', 'Not a .bmp image')
        return False
    else:
        return True


def open():
    global file_name, img
    name = filedialog.askopenfilename()
    if is_bmp(name):
        file_name = name
        fn_var.set(file_name)
        img = Image.open(file_name)


def save(img, file_name):
    if is_bmp(file_name):
        img.save(file_name)


def write_and_save(msg, img, file_name):
    if img is None:
        messagebox.showerror('Oops!', 'File not selected')
    elif msg == '':
        messagebox.showerror('Oops!', 'Message not written')
    else:
        encode(img, msg)
        save(img, file_name)
        messagebox.showinfo('Done', 'Message written and image saved')


file_name = ""
img = None

root = tk.Tk()
root.resizable(False, False)
root.title('Защита')

fn_var = tk.StringVar()
fn_var.set(file_name)

message_label = ttk.Label(text="Message")
message_entry = ttk.Entry(width=35)

name_label = ttk.Label(text="File")
file_name_label = ttk.Label(textvariable=fn_var)

open_button = ttk.Button(text="Select file", command=open)
write_button = ttk.Button(text="Write and save",
        command=lambda: write_and_save(message_entry.get(), img,
                                                 file_name))

message_label.grid(row=0, column=0, sticky='w')
message_entry.grid(row=0, column=1, sticky='w')
name_label.grid(row=1, column=0, sticky='w')
file_name_label.grid(row=1, column=1, sticky='w')
open_button.grid(row=2, column=0, sticky='w')
write_button.grid(row=2, column=1, sticky='w')

root.mainloop()
