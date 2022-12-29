import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

import sqlite3


def open_add_window():
    global add_window
    add_window = tk.Toplevel()
    add_window.geometry("320x600+100+100")

    # type
    type_lbl = ttk.Label(add_window, text="type")
    type_lbl.pack()
    song_types = ['찬송가', 'CCM']
    type_combobox = ttk.Combobox(add_window, values=song_types, state='readonly')
    # type_combobox.current(0)
    type_combobox.pack()
    # title
    title_lbl = ttk.Label(add_window, text="title")
    title_lbl.pack()
    title_input = tk.Entry(add_window)
    title_input.pack()
    # lyrics
    lyrics_lbl = ttk.Label(add_window, text="lyrics")
    lyrics_lbl.pack()
    lyrics_text = tk.Text(add_window)
    lyrics_text.pack()
    # memo
    memo_lbl = ttk.Label(add_window, text="memo")
    memo_lbl.pack()
    memo_input = tk.Entry(add_window)
    memo_input.pack()

    def add_song():
        title = title_input.get().strip()
        lyrics = lyrics_text.get("1.0", tk.END)
        type = type_combobox.get()
        memo = memo_input.get().strip()

        if not title:
            messagebox.showerror('error', 'please input title')
            title_input.focus()
            return
        if lyrics == '\n' or (not lyrics):
            messagebox.showerror('error', 'please input lyrics')
            lyrics_text.focus()
            return
        if not type:
            messagebox.showerror('error', 'please select type')
            type_combobox.focus()
            return

        song = [title, lyrics, type, memo]
        insert_song(song)

    confirm_btn = tk.Button(add_window, text="등록", command=add_song)
    confirm_btn.pack()


def init_db():
    # DB 생성 (오토 커밋)
    conn = sqlite3.connect("./jeil.db", isolation_level=None)
    # 커서 획득
    c = conn.cursor()
    # 테이블 생성 (데이터 타입은 TEST, NUMERIC, INTEGER, REAL, BLOB 등)
    c.execute("CREATE TABLE IF NOT EXISTS song\
      (id integer PRIMARY KEY AUTOINCREMENT, title text NOT NULL, lyrics text NOT NULL, type text NOT NULL, memo text)")
    conn.close()


def select_songs(title):
    # DB 생성 (오토 커밋)
    conn = sqlite3.connect("./jeil.db", isolation_level=None)
    cur = conn.cursor()
    sql = "SELECT * FROM song WHERE title like ?"
    cur.execute(sql, ('%' + title + '%',))
    data = cur.fetchall()
    conn.close()

    return data


def insert_song(song):
    conn = None
    try:
        conn = sqlite3.connect("./jeil.db", isolation_level=None)
        cur = conn.cursor()
        sql = "INSERT INTO song(title, lyrics, type, memo) VALUES(?,?,?,?)"
        cur.execute(sql, song)
        messagebox.showinfo('success', 'insert success')
        add_window.destroy()
    except:
        messagebox.showerror('error', 'insert error')
    finally:
        conn.close()


root = tk.Tk()
root.title("PPT Subtitle Maker")
root.geometry("640x480")

init_db()
songs = []


def search_songs_enter(e):
    search_songs(entry.get())


def search_songs(title):
    if not title.strip():
        return

    data = select_songs(title)
    label.configure(text='검색결과 : ' + str(len(data)))
    if len(data) <= 0:
        messagebox.showwarning('', 'no search data')
    global songs
    songs = data.copy()
    set_treeview_items(songs)


def select_item(event):
    selected = treeview.focus()
    print(selected)
    if not selected:
        return

    # preview
    preview_text.delete("1.0", tk.END)
    preview_text.insert(tk.CURRENT, songs[int(selected)][2])


def clear_treeview():
    treeview.delete(*treeview.get_children())


def set_treeview_items(songs):
    clear_treeview()

    idx = 0
    for song in songs:
        treeview.insert(parent='', index='end', text=idx+1, values=song, iid=idx)
        idx += 1


frame1 = tk.Frame(root, relief="solid", bd=2)
frame1.pack(side="left", fill="both", expand=True)

frame2 = tk.Frame(root, relief="solid", bd=2)
frame2.pack(side="right", fill="both", expand=True)

treeview_frame = tk.Frame(frame1)

# combobox
values = ['전체', '제목', '가사']
combobox = ttk.Combobox(frame1, values=values, state='readonly')
combobox.current(0)
combobox.pack()

# entry
entry = tk.Entry(frame1)
entry.bind("<Return>", search_songs_enter)
entry.pack()
label = tk.Label(treeview_frame, text='검색결과 : ' + str(len(songs)))
label.pack(side="top")

search_btn = tk.Button(frame1, text='검색', command=lambda: search_songs(entry.get()))
search_btn.pack()

treeview = ttk.Treeview(treeview_frame, columns=["id", "title"], displaycolumns=["id", "title"])
treeview.pack(side="left")

scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=treeview.yview)
scrollbar.pack(side="right", fill="y")
treeview.configure(yscrollcommand=scrollbar.set)

# treeview["show"] = "headings"
treeview.column("#0", width=40, anchor="center")
treeview.column("#1", width=40, anchor="center")
treeview.column("#2", width=200)
treeview.heading("#0", text="no", anchor="center")
treeview.heading("#1", text="id", anchor="center")
treeview.heading("#2", text="title", anchor="center")
treeview.bind('<<TreeviewSelect>>', select_item)

treeview_frame.pack()


# buttons
select_btn = tk.Button(frame1, text='선택', command='')
select_btn.pack()
add_btn = tk.Button(frame1, text='가사 등록', command=open_add_window)
add_btn.pack()


# preview
preview_frame = tk.Frame(frame2)
preview_label = tk.Label(frame2, text='Preview')
preview_label.pack()
preview_text = ScrolledText(frame2)
preview_text.pack()
preview_frame.pack()

entry.focus()


if __name__ == '__main__':
    root.mainloop()
