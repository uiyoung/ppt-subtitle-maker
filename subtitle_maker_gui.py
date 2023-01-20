import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import tkinter.font as font
import sqlite3
import os
import subtitle_maker


# song_id, title, lyrics, type, memo
songs = [
    # (4, '꽃 들도2', '꽃들도2 테수투\n입니당\n\n깔깔\n', 'CCM', '굳굳'),
    # (5, '꽃들도3', '꽃들도 세번째\n테수투 쿠쿠\n', 'CCM', '베리굿'),
    # (6, '꽃들도5', '꽃들도5입니닫ㅇ\n', '찬송가', ''),
    # (7, '꽃들도6', '하하동\n', 'CCM', '오오')
]

song_types = ['찬송가', 'CCM', '기타']


def init_db():
    # DB 생성 (오토 커밋)
    conn = sqlite3.connect("./jeil.db", isolation_level=None)
    # 커서 획득
    c = conn.cursor()
    # 테이블 생성 (데이터 타입은 TEST, NUMERIC, INTEGER, REAL, BLOB 등)
    c.execute("CREATE TABLE IF NOT EXISTS song\
    (song_id integer PRIMARY KEY AUTOINCREMENT, title text NOT NULL, lyrics text NOT NULL, type text NOT NULL, memo text)")
    conn.close()


def select_songs_from_db(title):
    # DB 생성 (오토 커밋)
    conn = sqlite3.connect("./jeil.db", isolation_level=None)
    cur = conn.cursor()
    sql = "SELECT * FROM song WHERE REPLACE(title, ' ', '') like '%' || REPLACE(?, ' ', '') || '%' "
    cur.execute(sql, (title,))
    data = cur.fetchall()
    conn.close()

    return data


def insert_song_to_db(song):
    conn = None
    try:
        conn = sqlite3.connect("./jeil.db", isolation_level=None)
        cur = conn.cursor()
        sql = "INSERT INTO song(title, lyrics, type, memo) VALUES(?,?,?,?)"
        cur.execute(sql, song)
        messagebox.showinfo('success', 'insert success')
    except Exception as e:
        messagebox.showerror('insert', 'error :' + e)
    finally:
        conn.close()


def update_song_to_db(song, song_id):
    conn = None
    try:
        conn = sqlite3.connect("./jeil.db", isolation_level=None)
        cur = conn.cursor()
        sql = "UPDATE song SET title=?, lyrics=?, type=?, memo=? WHERE song_id = ?"
        cur.execute(sql, song + (song_id,))
        messagebox.showinfo('success', 'update success')
    except Exception as e:
        messagebox.showerror('update', 'error : ' + e)
    finally:
        conn.close()


def delete_song_from_db(song_id):
    conn = None
    try:
        conn = sqlite3.connect("./jeil.db", isolation_level=None)
        cur = conn.cursor()
        sql = "DELETE from song WHERE song_id = ?"
        cur.execute(sql, (song_id,))
        messagebox.showinfo('delete', 'success', parent=search_window)
    except Exception as e:
        messagebox.showerror('delete', 'error : ' + e)
    finally:
        conn.close()


def open_search_window():
    """ 가사 검색&선택  윈도우 """

    def search_songs_enter(e):
        search_songs(entry.get())

    def search_songs(title):
        if not title.strip():
            return

        search_result_tv.delete(*search_result_tv.get_children())   # clear

        global results
        results = select_songs_from_db(title)
        label.configure(text='검색 결과 : ' + str(len(results)) + '건')
        if len(results) <= 0:
            messagebox.showwarning('검색', '검색 결과가 없습니다.', parent=search_window)
            entry.focus()
            return

        for i in range(len(results)):
            search_result_tv.insert(parent='', index='end', text=i+1, values=results[i], iid=i)

    def preview_item(e):
        selected = search_result_tv.focus()
        print(selected)
        if not selected:
            return

        preview_text.delete("1.0", tk.END)
        preview_text.insert(tk.CURRENT, results[int(selected)][2])

    def select_song():
        selected = search_result_tv.focus()
        if not selected:
            return

        selected_song = results[int(selected)]
        add_song_list(selected_song)
        messagebox.showinfo('선택', selected_song[1] + ' 곡이 목록에 추가되었습니다.')
        search_window.focus()

    def delete_song():
        selected = search_result_tv.focus()
        if not selected:
            messagebox.showwarning('삭제', '삭제할 곡을 먼저 선택해 주세요.', parent=search_window)
            return

        selected_song = results[int(selected)]
        if messagebox.askokcancel('삭제', selected_song[1] + " 곡을 DB에서 삭제하시겠습니까?", parent=search_window):
            delete_song_from_db(selected_song[0])
            search_songs(entry.get())

    global search_window
    search_window = tk.Toplevel(root)
    search_window.title("Search Lyrics")
    search_window.geometry("640x420+400+100")

    search_frame1 = tk.Frame(search_window, relief="solid", bd=1)
    search_frame1.pack(side="left", fill="both", expand=True)

    search_frame2 = tk.Frame(search_window, relief="solid", bd=1)
    search_frame2.pack(side="right", fill="both", expand=True)

    treeview_frame = tk.Frame(search_frame1)

    # combobox
    values = ['전체', '제목', '가사']
    combobox = ttk.Combobox(search_frame1, values=values, state='readonly')
    combobox.current(0)
    combobox.pack()

    # search entry
    entry = tk.Entry(search_frame1)
    entry.bind("<Return>", search_songs_enter)
    entry.pack()
    label = tk.Label(treeview_frame, text='검색결과 : ' + str(len(songs)))
    label.pack(side="top")

    search_btn = tk.Button(search_frame1, text='검색', command=lambda: search_songs(entry.get()))
    search_btn.pack()

    search_result_tv = ttk.Treeview(treeview_frame, columns=["id", "title"], displaycolumns=["id", "title"])
    search_result_tv.pack(side="left")

    scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=search_result_tv.yview)
    scrollbar.pack(side="right", fill="y")
    search_result_tv.configure(yscrollcommand=scrollbar.set)

    # treeview["show"] = "headings"
    search_result_tv.column("#0", width=40, anchor="center")
    search_result_tv.column("#1", width=40, anchor="center")
    search_result_tv.column("#2", width=200)
    search_result_tv.heading("#0", text="no", anchor="center")
    search_result_tv.heading("#1", text="id", anchor="center")
    search_result_tv.heading("#2", text="title", anchor="center")
    search_result_tv.bind('<<TreeviewSelect>>', preview_item)

    treeview_frame.pack()

    # buttons
    select_btn = tk.Button(search_frame1, text='선택', command=select_song)
    select_btn.pack()
    add_btn = tk.Button(search_frame1, text='DB 가사 등록', command=open_register_window)
    add_btn.pack()
    add_btn = tk.Button(search_frame1, text='DB 가사 삭제', command=delete_song)
    add_btn.pack()

    # preview
    preview_frame = tk.Frame(search_frame2)
    preview_label = tk.Label(search_frame2, text='Preview')
    preview_label.pack()
    preview_text = ScrolledText(search_frame2)
    preview_text.pack()
    preview_frame.pack()

    entry.focus()


def open_register_window():
    """ 가사등록 윈도우"""
    def register_song():
        title = title_input.get().strip()
        lyrics = lyrics_text.get("1.0", tk.END)
        type = type_combobox.get()
        memo = memo_input.get().strip()

        if not title:
            # messagebox.showerror('error', 'please input title')
            info_lbl.configure(text='please input title')
            title_input.focus()
            return
        if lyrics == '\n' or (not lyrics):
            info_lbl.configure(text='please input lyrics')
            lyrics_text.focus()
            return
        if not type:
            info_lbl.configure(text='please select type')
            type_combobox.focus()
            return

        if messagebox.askyesno('가사 등록', title + ' 곡을 DB에 등록하시겠습니까?', parent=add_window):
            song = [title, lyrics, type, memo]
            insert_song_to_db(song)
        if messagebox.askyesno('가사 등록', title + ' 곡을 현재 목록에 추가 하시겠습니까?', parent=add_window):
            song = ('', title, lyrics, type, memo)
            add_song_list(song)
            messagebox.showinfo('선택', title + ' 곡이 목록에 추가되었습니다.')
            add_window.focus()

    global add_window
    add_window = tk.Toplevel()
    add_window.geometry("300x480+400+200")

    # type
    type_lbl = ttk.Label(add_window, text="type")
    type_lbl.pack()
    type_combobox = ttk.Combobox(add_window, values=song_types, state='readonly')
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
    # register button
    register_btn = tk.Button(add_window, text="등록", command=register_song)
    register_btn.pack()
    # info label
    info_lbl = ttk.Label(add_window, text='', foreground='#d7565d')
    info_lbl.pack()


def add_song_list(song):
    songs.append(song)
    set_treeview_items(songs)


def update_song_list(idx, new_song):
    songs[idx] = new_song


def delete_song_from_list():
    selected = treeview.focus()
    if not selected:
        messagebox.showwarning('삭제', '삭제할 아이템을 먼저 선택해주세요')
        return

    songs.pop(int(selected))
    set_treeview_items(songs)


def set_readonly(flag):
    new_state = 'disabled' if flag else 'normal'
    title_input.configure(state=new_state)
    lyrics_text.configure(state=new_state)
    memo_input.configure(state=new_state)
    type_combobox.configure(state='disabled' if flag else 'readonly')
    save_btn.configure(state=new_state)
    cancel_btn.configure(state=new_state)


def clear_preview_widgets():
    id_lbl_var.set('')
    type_combobox.set('')
    title_input.delete(0, 'end')
    lyrics_text.delete("1.0", tk.END)
    memo_input.delete(0, 'end')
    info_lbl.configure(text='')


def preview_song(e):
    selected = treeview.focus()
    if not selected:
        return

    set_readonly(False)
    clear_preview_widgets()

    selected = int(selected)
    print(selected)

    id = songs[selected][0]
    title = songs[selected][1]
    lyrics = songs[selected][2]
    type = songs[selected][3]
    memo = songs[selected][4]

    id_lbl_var.set(id)
    title_input.insert(0, title)
    lyrics_text.insert(tk.CURRENT, lyrics)
    type_combobox.set(type)
    memo_input.insert(0, memo)

    set_readonly(True)


def clear_song_list():
    if len(songs) <= 0:
        return
    if messagebox.askokcancel('clear', "추가된 곡목록을 초기화 하시겠습니까?"):
        songs.clear()
        treeview.focus('')
        set_treeview_items(songs)


def set_treeview_items(songs):
    treeview.delete(*treeview.get_children())

    for i in range(len(songs)):
        treeview.insert(parent='', index='end', text=i+1, values=(songs[i][1],), iid=i)

    label_var.set('추가된 곡 : ' + str(len(songs)) + '건')


def update_song_btn():
    selected = treeview.focus()
    if not selected:
        messagebox.showwarning('수정', '수정할 아이템을 먼저 선택해주세요')
        return

    set_readonly(False)


def save_song():
    song_id = id_lbl.cget('text')
    title = title_input.get().strip()
    lyrics = lyrics_text.get("1.0", tk.END)
    type = type_combobox.get()
    memo = memo_input.get().strip()

    if not type:
        info_lbl.configure(text='please select type')
        type_combobox.focus()
        return
    if not title:
        info_lbl.configure(text='please input title')
        title_input.focus()
        return
    if lyrics == '\n' or (not lyrics):
        info_lbl.configure(text='please input lyrics')
        lyrics_text.focus()
        return

    selected = treeview.focus()
    if messagebox.askyesno('수정', '수정 내용을 반영 하시겠습니까?'):
        song = (song_id, title, lyrics, type, memo)
        update_song_list(int(selected), song)
    if song_id:
        if messagebox.askyesno('수정', 'DB에 수정된 내용을 반영하시겠습니까?'):
            song = (title, lyrics, type, memo)
            update_song_to_db(song, song_id)


def cancel():
    if messagebox.askyesno('cancel', '수정을 취소하시겠습니까?'):
        preview_song(None)


def generate_ppt():
    if len(songs) <= 0:
        messagebox.showwarning('generate PPT', '곡을 먼저 추가해주세요.')
        return

    # path = filedialog.asksaveasfilename(initialdir="./ppt", title="Select file", filetypes=(("PPTX files", "*.pptx"), ("all files", "*.*")))
    path = filedialog.asksaveasfilename(title="Select file", filetypes=(("PPTX files", "*.pptx"), ("all files", "*.*")))
    path = path.replace('.pptx', '')

    if not path:
        return

    subtitle_maker.generate_ppt(songs, path)
    os.startfile(path + '.pptx')


init_db()
selected_idx = ''   # treeview에서 선택된 인덱스('': 선택안됨)

root = tk.Tk()
root.title("PPT Subtitle Maker")
root.geometry("640x460+100+100")

# fonts
basic_font = font.Font(family="맑은 고딕", size=9)
bold_font = font.Font(family="맑은 고딕", size=9, weight="bold")

frame1 = tk.Frame(root, relief="groove", bd=2)
frame1.pack(side="left", fill="y", padx=4, anchor="n")

frame2 = tk.Frame(root, relief="groove", bd=2)
frame2.pack(side="left", fill="y", padx=4, anchor="n")

lb_bottom = tk.Label(root, bg="#f00")
lb_bottom.pack(side="bottom", fill="x")

# frame title
list_label = tk.Label(frame1, text='List', font=bold_font, bg="white", fg="red")
list_label.pack(fill="x", anchor="center")

# 추가된 곡 건수 label
lb_status = tk.Label(frame1)
lb_status.pack(fill="x")
label_var = tk.StringVar(value='')
lb_list_info = tk.Label(lb_status, font=bold_font, textvariable=label_var)
lb_list_info.pack(side="left")

# clear button
clear_btn = tk.Button(lb_status, text="clear", command=clear_song_list)
clear_btn.pack(side="right", padx=2)

# 추가된 곡 리스트
treeview_frame = tk.Frame(frame1)
treeview_frame.pack(padx=4, pady=4)
treeview = ttk.Treeview(treeview_frame, columns=["title"], displaycolumns=["title"], height=12)
treeview.pack(side="left")
scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=treeview.yview)
scrollbar.pack(side="right", fill="y")
treeview.configure(yscrollcommand=scrollbar.set)

# treeview["show"] = "headings"
treeview.column("#0", width=40, anchor="center")
treeview.heading("#0", text="no", anchor="center")
treeview.column("#1", width=200)
treeview.heading("#1", text="title", anchor="center")
treeview.bind('<<TreeviewSelect>>', preview_song)

# buttons
lb_buttons = tk.Label(frame1)
lb_buttons.pack(fill="x", anchor="e")
update_btn = tk.Button(lb_buttons, text='수정', command=update_song_btn)
update_btn.pack(side="right", padx=2)
remove_btn = tk.Button(lb_buttons, text='제거', font=basic_font, command=delete_song_from_list)
remove_btn.pack(side="right", padx=2)
search_btn = tk.Button(lb_buttons, text='추가', font=basic_font, command=open_search_window)
search_btn.pack(side="right", padx=2)

generate_btn = tk.Button(frame1, text='PPT 생성', width=16, height=2, font=bold_font, bg='#fff', fg='#f00', command=generate_ppt)
generate_btn.pack(side="bottom", fill="x", padx=16, pady=8)

# preview frame

# frame title
preview_label = tk.Label(frame2, text='Preview', font=bold_font, bg="white", fg="red")
preview_label.pack(fill="x", anchor="center")

# type
lb_type = tk.Label(frame2)
lb_type.pack(fill="x")
type_lbl = tk.Label(lb_type, text='구분', font=bold_font)
type_lbl.pack(side="left")
type_combobox = ttk.Combobox(lb_type, values=song_types, width=10, state='readonly')
type_combobox.pack(side="left", padx=4)

# id
id_lbl = tk.Label(lb_type, text='ID', font=bold_font)
id_lbl.pack(side="left")
id_lbl_var = tk.StringVar()
id_lbl = tk.Label(lb_type, textvariable=id_lbl_var)
id_lbl.pack(side="left")

# title
lb_title = tk.Label(frame2)
lb_title.pack(fill="x")
title_lbl = tk.Label(lb_title, text='제목', font=bold_font)
title_lbl.pack(side="left")
title_input = tk.Entry(lb_title, width=20)
title_input.pack(side="left", padx=4, fill="x", expand=True)

# lyrics
lb_lyrics = tk.Label(frame2)
lb_lyrics.pack(fill="x")
lyrics_lbl = tk.Label(lb_lyrics, text='가사', font=bold_font)
lyrics_lbl.pack(side="left", anchor="n")
lyrics_text = ScrolledText(lb_lyrics, font=basic_font, height=20)
lyrics_text.pack(side="left", padx=4, fill="both", expand=True)

# memo
lb_memo = tk.Label(frame2)
lb_memo.pack(fill="x")
memo_lbl = tk.Label(lb_memo, text='메모', font=bold_font)
memo_lbl.pack(side="left")
memo_input = tk.Entry(lb_memo)
memo_input.pack(side="left", padx=4, fill="x", expand=True)

# save, cancel buttons
lb_previewButtons = tk.Label(frame2)
lb_previewButtons.pack(side="bottom", fill="x")
info_lbl = ttk.Label(lb_previewButtons, text='', foreground='#d7565d')
info_lbl.pack(side="top")
cancel_btn = tk.Button(lb_previewButtons, text='cancel', command=cancel, state='disabled')
cancel_btn.pack(side="right", padx=4)
save_btn = tk.Button(lb_previewButtons, text='save', command=save_song, state='disabled')
save_btn.pack(side="right", padx=4)


set_treeview_items(songs)
set_readonly(True)

if __name__ == '__main__':
    root.mainloop()
