import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import tkinter.font as font
import sqlite3
import os
import ppt_maker


# song_id, title, lyrics, type, memo
# songs = [
#    (1, '꽃 들도2', '꽃들도2 테수투\n입니당\n\n깔깔\n', 'CCM', '굳굳'),
#    (2, '꽃들도3', '꽃들도 세번째\n테수투 쿠쿠\n', 'CCM', '베리굿'),
#    (3, '꽃들도5', '꽃들도5입니닫ㅇ\n', '찬송가', ''),
#    (4, '꽃들도6', '하하동\n', 'CCM', '오오')
# ]
songs = []
song_types = ['찬송가', 'CCM', '기타']

# 가사등록 윈도우
global register_window
register_window = None

# 선택된 곡의 id
global selected_id
selected_id = None

# 선택된 treeview
global selected_tv
selected_tv = None


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
    conn = None
    try:
        conn = sqlite3.connect("./jeil.db", isolation_level=None)
        cur = conn.cursor()
        sql = "SELECT * FROM song WHERE REPLACE(title, ' ', '') like '%' || REPLACE(?, ' ', '') || '%' "
        cur.execute(sql, (title,))
        data = cur.fetchall()
        return data
    except Exception as e:
        messagebox.showerror('insert', 'error :' + e)
    finally:
        conn.close()


def select_song_by_id(song_id):
    conn = None
    try:
        conn = sqlite3.connect("./jeil.db", isolation_level=None)
        cur = conn.cursor()
        sql = "SELECT * FROM song WHERE song_id=? "
        cur.execute(sql, (song_id,))
        data = cur.fetchone()
        return data
    except Exception as e:
        messagebox.showerror('insert', 'error :' + e)
    finally:
        conn.close()


def insert_song_to_db(song):
    conn = None
    try:
        conn = sqlite3.connect("./jeil.db", isolation_level=None)
        cur = conn.cursor()
        sql = "INSERT INTO song(title, lyrics, type, memo) VALUES(?,?,?,?)"
        result = cur.execute(sql, song)
        messagebox.showinfo('success', 'insert success')
        return result.lastrowid
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
        messagebox.showinfo('delete', 'success')
        search_songs(search_entry.get())
    except Exception as e:
        messagebox.showerror('delete', 'error : ' + e)
    finally:
        conn.close()


def auto_format_lyrics(target):
    lyrics = target.strip().split('\n')
    lyrics = list(filter(lambda x: x != '' and x != ' ' and x != '  ', lyrics))

    # 긴 가사 둘로 나누기
    for idx, line in enumerate(lyrics):
        if len(line) > 24:
            splited_line = line.split(' ')
            half = len(splited_line) // 2
            lyrics[idx] = ' '.join(splited_line[:half])
            lyrics.insert(idx+1, ' '.join(splited_line[half:]))

    # 두줄 씩 나누기
    new_lyrics = ''
    for i, line in enumerate(lyrics):
        new_lyrics += (line + '\n')
        if i % 2 == 1:
            new_lyrics += '\n'

    new_lyrics = new_lyrics.strip()
    return new_lyrics


def on_click_auto_format():
    target = lyrics_text.get("1.0", tk.END).strip()
    new_lyrics = auto_format_lyrics(target)
    lyrics_text.delete("1.0", tk.END)
    lyrics_text.insert(tk.CURRENT, new_lyrics)


def open_register_window():
    """ 가사등록 윈도우"""
    def register_song():
        title = title_input.get().strip()
        lyrics = lyrics_text.get("1.0", tk.END).strip()
        type = type_combobox.get()
        memo = memo_input.get().strip()

        if not title:
            info_lbl.configure(text='제목을 입력해주세요.')
            title_input.focus()
            return
        if lyrics == '\n' or (not lyrics):
            info_lbl.configure(text='가사를 입력해주세요.')
            lyrics_text.focus()
            return
        if not type:
            info_lbl.configure(text='타입을 선택해 주세요.')
            type_combobox.focus()
            return

        if messagebox.askyesno('가사 등록', title + ' 곡을 DB에 등록 하시겠습니까?', parent=register_window):
            new_song = [title, lyrics, type, memo]
            new_song_id = insert_song_to_db(new_song)
        if messagebox.askyesno('가사 등록', title + ' 곡을 현재 목록에 추가 하시겠습니까?', parent=register_window):
            new_song = (new_song_id, title, lyrics, type, memo)
            songs.append(new_song)
            set_treeview_items(songs)

            messagebox.showinfo('가사 등록', title + ' 곡이 목록에 추가되었습니다.')
            register_window.focus()

    def on_click_auto_format():
        target = lyrics_text.get("1.0", tk.END).strip()
        new_lyrics = auto_format_lyrics(target)
        lyrics_text.delete("1.0", tk.END)
        lyrics_text.insert(tk.CURRENT, new_lyrics)

    global register_window
    if register_window != None and register_window.winfo_exists():
        register_window.focus()
        return

    register_window = tk.Toplevel()
    register_window.title("New Lyrics")
    register_window.geometry("280x516+300+100")

    # type
    lb_1 = tk.Label(register_window)
    lb_1.pack(fill="x")
    type_lbl = ttk.Label(lb_1, font=bold_font, text="타입")
    type_lbl.pack(side="left", padx=2)
    type_combobox = ttk.Combobox(lb_1, font=basic_font, values=song_types, state='readonly', width=8)
    type_combobox.pack(side="left", padx=2)
    # title
    lb_2 = tk.Label(register_window)
    lb_2.pack(fill="x")
    title_lbl = ttk.Label(lb_2, font=bold_font, text="제목")
    title_lbl.pack(side="left", padx=2)
    title_input = tk.Entry(lb_2, font=basic_font)
    title_input.pack(side="left", fill="x", expand=True, padx=2)
    # lyrics
    lyrics_lbl = ttk.Label(register_window, font=bold_font, text="가사")
    lyrics_lbl.pack()
    lyrics_text = tk.Text(register_window, font=basic_font)
    lyrics_text.pack()
    # memo
    lb_4 = tk.Label(register_window)
    lb_4.pack(fill="x")
    memo_lbl = ttk.Label(lb_4, font=bold_font, text="메모")
    memo_lbl.pack(side="left", padx=2)
    memo_input = tk.Entry(lb_4, font=basic_font)
    memo_input.pack(side="left", fill="x", expand=True, padx=2)

    # info label
    info_lbl = ttk.Label(register_window, font=bold_font, text='', foreground='#d7565d')
    info_lbl.pack(anchor="center")

    # 가사 자동정렬 button
    auto_format_btn = tk.Button(register_window, font=basic_font, text="가사 자동정렬 ", command=on_click_auto_format)
    auto_format_btn.pack(side="left", padx=4, pady=4)

    # register button
    register_btn = tk.Button(register_window, font=basic_font, text="등록", command=register_song)
    register_btn.pack(side="right", padx=4, pady=4)

    title_input.focus()


def search_songs(title):
    if not title.strip():
        return

    search_tv.delete(*search_tv.get_children())   # clear tv

    global results
    results = select_songs_from_db(title)
    label.configure(text='검색 결과 : ' + str(len(results)) + '건')
    if len(results) <= 0:
        messagebox.showwarning('검색', '검색 결과가 없습니다.')
        search_entry.focus()
        return

    for i in range(len(results)):
        search_tv.insert(parent='', index='end', text=i+1, values=results[i], iid=i)


def search_songs_enter(e):
    search_songs(search_entry.get())


def set_readonly(flag):
    new_state = 'disabled' if flag else 'normal'
    title_input.configure(state=new_state)
    lyrics_text.configure(state=new_state)
    memo_input.configure(state=new_state)
    type_combobox.configure(state='disabled' if flag else 'readonly')
    auto_format_btn.configure(state=new_state)
    save_btn.configure(state=new_state)
    cancel_btn.configure(state=new_state)


def clear_preview():
    set_readonly(False)
    type_combobox.set('')
    id_lbl_var.set('')
    title_input.delete(0, 'end')
    lyrics_text.delete("1.0", tk.END)
    memo_input.delete(0, 'end')
    info_lbl.configure(text='')
    set_readonly(True)


def preview_song_by_id(song_id):
    song = select_song_by_id(song_id)

    id = song[0]
    title = song[1]
    lyrics = song[2]
    type = song[3]
    memo = song[4]

    set_readonly(False)
    type_combobox.set(type)
    id_lbl_var.set(id)
    title_input.delete(0, 'end')
    title_input.insert(0, title)
    lyrics_text.delete("1.0", tk.END)
    lyrics_text.insert(tk.CURRENT, lyrics)
    memo_input.delete(0, 'end')
    memo_input.insert(0, memo)
    info_lbl.configure(text='')
    set_readonly(True)


def preview_song(e, obj):
    global selected_tv
    if obj == 'search':  # search_tv item누른 경우
        selected_tv = search_tv
    elif obj == 'list':  # list_tv item누른 경우
        selected_tv = list_tv

    idx = selected_tv.focus()
    if not idx:
        return

    global selected_id
    selected_id = selected_tv.item(idx)['values'][0]
    preview_song_by_id(selected_id)


def delete_song():
    selected = search_tv.focus()
    if not selected:
        messagebox.showwarning('삭제', '삭제할 곡을 먼저 선택해 주세요.')
        return

    selected_song = results[int(selected)]
    if messagebox.askokcancel('삭제', selected_song[1] + " 곡을 DB에서 삭제하시겠습니까?"):
        delete_song_from_db(selected_song[0])
        search_songs(search_entry.get())


def add_to_list():
    idx = search_tv.focus()
    if not idx:
        return

    selected_song = results[int(idx)]
    songs.append(selected_song)
    set_treeview_items(songs)


def update_song_btn():
    print('edit id: ', selected_id)

    if not selected_id:
        messagebox.showwarning('수정', '수정할 아이템을 먼저 선택해주세요')
        return

    set_readonly(False)


def save_edited():
    song_id = id_lbl.cget('text')
    title = title_input.get().strip()
    lyrics = lyrics_text.get("1.0", tk.END).strip()
    type = type_combobox.get()
    memo = memo_input.get().strip()

    if not song_id:
        info_lbl.configure(text='no song id exists.')
        return
    if not type:
        info_lbl.configure(text='please select type.')
        type_combobox.focus()
        return
    if not title:
        info_lbl.configure(text='please input title.')
        title_input.focus()
        return
    if lyrics == '\n' or (not lyrics):
        info_lbl.configure(text='please input lyrics.')
        lyrics_text.focus()
        return

    if messagebox.askyesno('수정', 'DB에 수정된 내용을 저장 하시겠습니까?'):
        # update db
        song = (title, lyrics, type, memo)
        update_song_to_db(song, song_id)

        # update list_tv
        for idx, song in enumerate(songs):
            if song[0] == song_id:
                songs[idx] = (song_id, title, lyrics, type, memo)
                set_treeview_items(songs)

        # update search_tv
        if selected_tv == search_tv:
            search_songs(search_entry.get())

        set_readonly(True)


def cancel_edited():
    if messagebox.askyesno('cancel', '수정을 취소하시겠습니까?'):
        song = select_song_by_id(selected_id)
        preview_song(None, song)
        set_readonly(True)


def set_treeview_items(songs):
    list_tv.delete(*list_tv.get_children())  # clear tv

    for i in range(len(songs)):
        list_tv.insert(parent='', index='end', text=i+1, values=songs[i], iid=i)

    label_var.set('추가된 곡 : ' + str(len(songs)) + '건')


def clear_song_list():
    if len(songs) <= 0:
        return
    if messagebox.askokcancel('clear', "추가된 곡 목록을 초기화 하시겠습니까?"):
        songs.clear()
        set_treeview_items(songs)
        list_tv.focus('')
        search_tv.focus('')
        clear_preview()


def delete_song_from_list():
    selected = list_tv.focus()
    if not selected:
        messagebox.showwarning('제거', '목록에서 제거할 아이템을 먼저 선택해주세요')
        return

    songs.pop(int(selected))
    set_treeview_items(songs)


def list_up():
    selected = list_tv.focus()
    if not selected:
        messagebox.showwarning('수정', '수정할 아이템을 먼저 선택해주세요')
        return

    if int(selected) == 0:
        return

    target = songs[int(selected)]
    songs.pop(int(selected))
    songs.insert(int(selected)-1, target)
    set_treeview_items(songs)


def list_down():
    selected = list_tv.focus()
    if not selected:
        messagebox.showwarning('수정', '수정할 아이템을 먼저 선택해주세요')
        return

    if int(selected) == len(songs)-1:
        return

    target = songs[int(selected)]
    songs.pop(int(selected))
    songs.insert(int(selected)+1, target)
    set_treeview_items(songs)


def generate_ppt():
    if len(songs) <= 0:
        messagebox.showwarning('generate PPT', '곡을 먼저 추가해주세요.')
        return

    # path = filedialog.asksaveasfilename(initialdir="./ppt", title="Select file", filetypes=(("PPTX files", "*.pptx"), ("all files", "*.*")))
    path = filedialog.asksaveasfilename(title="Select file", filetypes=(("PPTX files", "*.pptx"), ("all files", "*.*")))
    path = path.replace('.pptx', '')

    if not path:
        return

    ppt_maker.generate_ppt(songs, path)
    os.startfile(path + '.pptx')


init_db()

root = tk.Tk()
root.title("PPT Subtitle Maker")
root.geometry("990x490+100+100")

# fonts
basic_font = font.Font(family="맑은 고딕", size=9)
bold_font = font.Font(family="맑은 고딕", size=9, weight="bold")

# frames
frame1 = tk.Frame(root, relief="groove", bd=2, bg="#E5E9F0")
frame2 = tk.Frame(root, relief="groove", bd=2)
frame3 = tk.Frame(root, relief="groove", bd=2)
frame1.pack(side="left", fill="y", padx=4, pady=2, anchor="n")
frame2.pack(side="left", fill="y", padx=4, pady=2, anchor="n")
frame3.pack(side="left", fill="y", padx=4, pady=2, anchor="n")

"""
frame1 - Search
"""

lb_frame1_title = tk.Label(frame1, text='Search', font=bold_font, bg="white", fg="#BF616A")
lb_frame1_title.pack(fill="x", anchor="center")

# combobox
lb_search = tk.Label(frame1, bg="#E5E9F0")
lb_search.pack(fill="x")
# values = ['전체', '제목', '가사']
values = ['제목']
combobox = ttk.Combobox(lb_search, values=values, font=basic_font, width="8", state='readonly')
combobox.current(0)
combobox.pack(side="left")

# search search_entry
search_entry = tk.Entry(lb_search, font=basic_font)
search_entry.bind("<Return>", search_songs_enter)
search_entry.pack(side="left", fill="x", padx=4, expand=True)

# search button
search_btn = tk.Button(lb_search, text='검색', font=basic_font, fg="#2E3440", command=lambda: search_songs(search_entry.get()))
search_btn.pack(side="left", padx=2)

# search result
label = tk.Label(frame1, text='검색 결과 : ' + str(len(songs)), font=bold_font, bg="#E5E9F0")
label.pack(side="top", pady=4, fill="x")

# treeview - 검색 결과
treeview_frame = tk.Frame(frame1, bg="#E5E9F0")
treeview_frame.pack(padx=4, pady=4)
search_tv = ttk.Treeview(treeview_frame, columns=["id", "title"], displaycolumns=["id", "title"], height=14)
search_tv.pack(side="left")

# treeview["show"] = "headings"
search_tv.heading("#0", text="no")
search_tv.heading("#1", text="id")
search_tv.heading("#2", text="title")
search_tv.column("#0", width=40, anchor="center")
search_tv.column("#1", width=40, anchor="center")
search_tv.column("#2", width=220)
search_tv.bind('<<TreeviewSelect>>', lambda e, obj='search': preview_song(e, obj))

scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=search_tv.yview)
scrollbar.pack(side="right", fill="y")
search_tv.configure(yscrollcommand=scrollbar.set)


# buttons
lb_search2 = tk.Label(frame1, bg="#E5E9F0")
lb_search2.pack(fill="x")
add_btn = tk.Button(lb_search2, text='새 가사 등록', font=basic_font, command=open_register_window)
add_btn.pack(side="right", padx=2)
add_btn = tk.Button(lb_search2, text='가사 삭제', font=basic_font, command=delete_song)
add_btn.pack(side="right", padx=2)
add_to_list_btn = tk.Button(frame1, text='목록에 추가', width=16, height=2, font=bold_font, bg='#fff', fg='#2E3440', command=add_to_list)
add_to_list_btn.pack(side="bottom", fill="x", padx=8, pady=8)

"""
frame 2 - Preview
"""

# frame title
lb_frame2_title = tk.Label(frame2, text='Preview', font=bold_font, bg="white", fg="red")
lb_frame2_title.pack(fill="x")

# ID
id_lbl_var = tk.StringVar(value='')
id_lbl = tk.Label(frame2, textvariable=id_lbl_var)
id_lbl.pack(anchor="e", padx=4)

# type
lb_type = tk.Label(frame2)
lb_type.pack(fill="x")
type_lbl = tk.Label(lb_type, text='구분', font=bold_font)
type_lbl.pack(side="left")
type_combobox = ttk.Combobox(lb_type, values=song_types, width=10, state='readonly')
type_combobox.pack(side="left", padx=4)

# title
lb_title = tk.Label(frame2)
lb_title.pack(fill="x")
title_lbl = tk.Label(lb_title, text='제목', font=bold_font)
title_lbl.pack(side="left")
title_input = tk.Entry(lb_title, font=basic_font, width=20)
title_input.pack()
title_input.pack(side="left", padx=4, fill="x", expand=True)

# lyrics
lb_lyrics = tk.Label(frame2)
lb_lyrics.pack(fill="x")
lyrics_lbl = tk.Label(lb_lyrics, text='가사', font=bold_font)
lyrics_lbl.pack(side="left", anchor="n")
lyrics_text = ScrolledText(lb_lyrics, font=basic_font, height=20, width=34)
lyrics_text.pack(side="left", padx=4, fill="both")

# memo
lb_memo = tk.Label(frame2)
lb_memo.pack(fill="x")
memo_lbl = tk.Label(lb_memo, text='메모', font=bold_font)
memo_lbl.pack(side="left")
memo_input = tk.Entry(lb_memo, font=basic_font)
memo_input.pack(side="left", padx=4, fill="x", expand=True)

# save, cancel buttons
lb_previewButtons = tk.Label(frame2)
lb_previewButtons.pack(side="bottom", fill="x", pady=4)
cancel_btn = tk.Button(lb_previewButtons, text='취소', command=cancel_edited, state='disabled')
cancel_btn.pack(side="right", padx=2)
save_btn = tk.Button(lb_previewButtons, text='저장', command=save_edited, state='disabled')
save_btn.pack(side="right", padx=2)
auto_format_btn = tk.Button(lb_previewButtons, text='가사 자동정렬', font=basic_font, command=on_click_auto_format)
auto_format_btn.pack(side="right", padx=2)
update_btn = tk.Button(lb_previewButtons, text='수정', font=basic_font, command=update_song_btn)
update_btn.pack(side="right", padx=2)

# info
info_lbl = tk.Label(frame2, text='', fg='#d7565d')
info_lbl.pack(side="bottom")


"""
frame3 - List
"""

# frame title
list_label = tk.Label(frame3, text='List', font=bold_font, bg="#fffffe", fg="#ff8ba7")
list_label.pack(fill="x", anchor="center")

# clear button
clear_btn = tk.Button(list_label, text="clear", command=clear_song_list)
clear_btn.pack(side="right", padx=2)

# 추가된 곡 건수 label
lb_status = tk.Label(frame3)
lb_status.pack(fill="x")
label_var = tk.StringVar(value='추가된 곡 : 0건')
lb_list_info = tk.Label(lb_status, font=bold_font, textvariable=label_var)
lb_list_info.pack(pady=4)

# treeview - 추가된 곡 리스트
treeview_frame = tk.Frame(frame3)
treeview_frame.pack(padx=4)
list_tv = ttk.Treeview(treeview_frame, columns=["id", "title"], displaycolumns=["id", "title"], height=14)
list_tv.pack(side="left")

# list_tv["show"] = "headings"
list_tv.heading("#0", text="no")
list_tv.heading("#1", text="id")
list_tv.heading("#2", text="title")
list_tv.column("#0", width=40, anchor="center")
list_tv.column("#1", width=40, anchor="center")
list_tv.column("#2", width=220)
list_tv.bind('<<TreeviewSelect>>', lambda e, obj='list': preview_song(e, obj))

scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=list_tv.yview)
scrollbar.pack(side="right", fill="y")
list_tv.configure(yscrollcommand=scrollbar.set)

# buttons
lb_buttons = tk.Label(frame3)
lb_buttons.pack(fill="x", anchor="e")
update_btn = tk.Button(lb_buttons, text=' ↑ ', font=basic_font, command=list_up)
update_btn.pack(side="left", padx=2, pady=2)
update_btn = tk.Button(lb_buttons, text=' ↓ ', font=basic_font, command=list_down)
update_btn.pack(side="left", padx=2, pady=2)
remove_btn = tk.Button(lb_buttons, text='제거', font=basic_font, command=delete_song_from_list)
remove_btn.pack(side="right", padx=2, pady=2)

generate_btn = tk.Button(frame3, text='PPT 생성', width=16, height=2, font=bold_font, bg='#fff', fg='#f00', command=generate_ppt)
generate_btn.pack(side="bottom", fill="x", padx=16, pady=8)

# set_treeview_items(songs)
set_readonly(True)
search_entry.focus()

if __name__ == '__main__':
    root.mainloop()
