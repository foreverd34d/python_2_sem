import os
import string
import encoder as en
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image


def is_bmp(filename):
    _, ext = os.path.splitext(filename)
    if ext != '.bmp':
        tk.messagebox.showerror('Oops!', 'Not a .bmp image')
        return False
    else:
        return True


def is_ascii(msg):
    for sym in msg:
        if sym not in string.printable:
            return False

    return True


def open():
    global file_name, image
    name = filedialog.askopenfilename()
    if name == '':
        pass
    elif is_bmp(name):
        name_label.configure(text=name)
        file_name = name
        image = Image.open(file_name)


def show(img):
    if img is None:
        tk.messagebox.showerror('Oops!', 'File not selected')
    else:
        img.show()


def save(img):
    name = filedialog.asksaveasfilename()
    if name == '':
        pass
    elif is_bmp(name):
        img.save(name)
        status.set("Saved")


def write_to_image(img, msg):
    if img is None:
        tk.messagebox.showerror('Oops!', 'File not selected')
    elif msg == '':
        tk.messagebox.showerror('Oops!', 'Message not written')
    elif len(msg) * 9 > img.size[0] * img.size[1]:
        tk.messagebox.showerror('Oops!', 'Message is too long')
    elif not is_ascii(msg):
        tk.messagebox.showerror('Oops!', 'Not-ASCII symbols found')
    else:
        en.encode(img, msg)
        status.set("Message written")


def read_from_image(img):
    if img is None:
        tk.messagebox.showerror('Oops!', 'File not selected')
    else:
        msg = en.decode(img)
        message_entry.delete(0, tk.END)
        message_entry.insert(0, msg)
        if msg == '':
            status.set("There's no message in image")
        else:
            status.set("Got message")


def rw_image(img, msg: str, mode: str):
    if mode == "Read":
        read_from_image(img)
    else:
        write_to_image(img, msg)


root = tk.Tk()
root.resizable(False, False)
root.title("Encoder")

io_frame = ttk.Frame(root)
button_frame = ttk.Frame(root)
mode_frame = ttk.Frame(root)

image = None
file_name: str = "None"
selected_mode: tk.StringVar = tk.StringVar()
selected_mode.set("Read")
status: tk.StringVar = tk.StringVar()
status.set('')

message_label = ttk.Label(io_frame, text="Message")
message_entry = ttk.Entry(io_frame, width=35)

selected_label = ttk.Label(io_frame, text="Selected file")
name_label = ttk.Label(io_frame, text=file_name, width=35)

status_label = ttk.Label(io_frame, textvariable=status)

select_button = ttk.Button(button_frame, text="Select file", command=open)
save_button = ttk.Button(button_frame,
                         text="Save file",
                         command=lambda: save(image))

rw_button = ttk.Button(
    button_frame,
    textvariable=selected_mode,
    command=lambda: rw_image(image, message_entry.get(), selected_mode.get()))

show_buttom = ttk.Button(button_frame,
                         text="Show image",
                         command=lambda: show(image))

read_mode = ttk.Radiobutton(io_frame,
                            text="Read",
                            variable=selected_mode,
                            value="Read")
write_mode = ttk.Radiobutton(io_frame,
                             text="Write",
                             variable=selected_mode,
                             value="Write")

message_label.grid(row=0, column=0, sticky='w')
message_entry.grid(row=0, column=1)

selected_label.grid(row=1, column=0, sticky='w', ipady=5)
name_label.grid(row=1, column=1, sticky='w')

read_mode.grid(row=2, column=0, sticky='w', ipady=5)
write_mode.grid(row=2, column=1, sticky='w', ipady=5)

status_label.grid(row=3, column=0, sticky='w', columnspan=2)

select_button.grid(row=0, column=0, sticky='ew')
save_button.grid(row=1, column=0, sticky='ew')
rw_button.grid(row=2, column=0, sticky='ew')
show_buttom.grid(row=3, column=0, sticky='ew')

io_frame.grid(padx=5, pady=5, row=0, column=0, sticky='n')
button_frame.grid(padx=5, pady=5, row=0, column=1)

root.mainloop()
