import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import sqlite3
import os
import ppt_maker

root = tk.Tk()
root.title("PPT Subtitle Maker")
root.geometry("640x600+100+100")

frame1 = tk.Frame(root, relief="solid", bd=1, width=100)
frame1.pack(side="left", fill="both")

frame2 = tk.Frame(root, relief="sunken", bd=1)
frame2.pack(side="right", fill="both")

# 추가된 곡 건수 label
lb_container = tk.Label(frame1)
lb_container.pack()

label_var = tk.StringVar(value='추가된 곡 : 0건')
label = tk.Label(lb_container, textvariable=label_var)
label.grid(row=0, column=0)

clear_btn = tk.Button(lb_container, text="clear")
clear_btn.grid(row=0, column=1, padx=4)

# 추가된 곡 리스트
treeview_frame = tk.Frame(frame1)
# treeview_frame.grid(row=1, column=0, columnspan=5, padx=4, pady=4)
treeview_frame.pack()
treeview = ttk.Treeview(treeview_frame, columns=["title"], displaycolumns=["title"])
treeview.pack(side="left")
scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=treeview.yview)
scrollbar.pack(side="right", fill="y")
treeview.configure(yscrollcommand=scrollbar.set)


# buttons
lb_buttons = tk.Label(frame1)
lb_buttons.pack()
search_btn = tk.Button(lb_buttons, text='추가')
search_btn.pack(side="left")
# update_btn = tk.Button(frame1, text='수정', command=update_song_btn)
# update_btn.grid(row=3, column=1)
remove_btn = tk.Button(lb_buttons, text='삭제')
remove_btn.pack(side="left")
generate_btn = tk.Button(frame1, text='generate', width=20)
# generate_btn.grid(row=4, column=1, columnspan=3, pady=8)


root.mainloop()
