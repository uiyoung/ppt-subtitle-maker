import tkinter as tk

root = tk.Tk()
root.title("PPT Subtitle Maker")
root.geometry("640x500+100+100")


# songs = [
#     (1, 'title1', 'lyrics1', None, None),
#     (2, 'title_2', 'lyrics_2', None, None),
# ]
songs = [
    'title_1',
    'title_2',
    'title_3',
    'title_4',
    'title_5',
    'title_6',
    'title_7',
    'title_8',
    'title_9',
    'title_10',
    'title_10',
    'title_10',
    'title_10',
    'title_10',
    'title_10',
]


def generate_ppt():
    label['text'] = 'pressed button!'


def search():
    window2 = tk.Tk()
    text = tk.Text(window2, width=50, height=10)
    text.pack()


def add(event):
    songs.append(entry.get())
    print(songs)
    list_var.set(songs)
    # clear entry
    entry.delete(0, tk.END)


def delete():
    selected = song_listbox.curselection()
    print(selected)
    for i in selected:
        print(i)
        songs.pop(i)

    print(songs)
    list_var.set(songs)
    song_listbox.select_clear(0, tk.END)


def select_item(event):
    selected = song_listbox.curselection()
    print(selected)


frame = tk.Frame(root, relief="solid", bd=2)

label = tk.Label(frame, text='list')
label.configure(text="size : " + str(len(songs)))
label.pack(side="top")

list_var = tk.StringVar(value=songs)
song_listbox = tk.Listbox(frame, selectmode='extended', listvariable=list_var, activestyle='none')
song_listbox.pack(side="left")
scrollbar = tk.Scrollbar(frame, command=song_listbox.yview)
scrollbar.pack(side="right", fill="y")
song_listbox.configure(yscrollcommand=scrollbar.set)
frame.pack()


# entry
entry = tk.Entry(root)
entry.bind("<Return>", add)
entry.pack()

# preview
preview_text = tk.Text(root, width=50, height=10)
preview_text.pack()


# buttons
add_btn = tk.Button(root, text='+', command=add)
remove_btn = tk.Button(root, text='-', command=delete)
generate_btn = tk.Button(root, text='generate', command=generate_ppt)
add_btn.pack()
remove_btn.pack()
generate_btn.pack()


if __name__ == '__main__':
    root.mainloop()
