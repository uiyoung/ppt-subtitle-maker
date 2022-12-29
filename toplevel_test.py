import tkinter as tk
from tkinter import *

my_w = tk.Tk()
my_w.geometry("200x200")  # Size of the window
my_w.title("www.plus2net.com")  # Adding a title

# create one lebel
my_str = tk.StringVar()
l1 = tk.Label(my_w, textvariable=my_str)
l1.grid(row=1, column=2)
my_str.set("Hi I am main window")
# add one button
b1 = tk.Button(my_w, text='Clik me to open new window', command=lambda: my_open())
b1.grid(row=2, column=2)


def my_open():
    my_w_child = Toplevel(my_w)  # Child window
    my_w_child.geometry("250x200")  # Size of the window
    my_w_child.title("www.plus2net.com")

    l1 = tk.Label(my_w_child,  text='Your Name', width=10)
    l1.grid(row=1, column=1)
    e1 = tk.Entry(my_w_child, width=20, bg='yellow')
    e1.grid(row=1, column=2)
    b2 = tk.Button(my_w_child, text='Submit', command=lambda: my_str.set(e1.get()))
    b2.grid(row=2, column=2)
    b3 = tk.Button(my_w_child, text=' Close Child', command=my_w_child.destroy)
    b3.grid(row=3, column=2)


my_w.mainloop()
