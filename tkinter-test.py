from tkinter import *

tk = Tk()


def event():
    label['text'] = 'pressed button!'


label = Label(tk, text='hello world!')
label.pack()

button1 = Button(tk, text='button1', command=event)
button2 = Button(tk, text='button2')
button1.pack(side=LEFT, padx=10, pady=10)
button2.pack(side=LEFT, padx=10, pady=10)


tk.mainloop()
