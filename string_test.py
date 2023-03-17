print(len('만백성들아 기뻐하라 우리의 왕이 나셨다'))
print(len('내가 원하는 한 가지 주님의 기쁨이 되는 것'))
print(len('당신은 하나님의 언약안에있는 축복의 통로'))
print(len('당신을 통하여서 열방이 주께 돌아오게되리'))
print(len('교회를 교회되게 예배를 예배되게 우릴 사용하소서'))
print(len('성령 안에 예배하리라 자유의 마음으로'))
print(len('마음으로 사랑으로 사역하리라 교회는 생명이니'))
print(len('당신은 하나님의 언약안에있는 축복의 통로'))


lyrics = '우리에겐 소원이 하나 있네\n주님 다시 오실 그날 까지\n교회를 교회되게 예배를 예배되게 우릴 사용하소서'
lyrics = lyrics.strip().split('\n')
lyrics = list(filter(lambda x: x != '' and x != ' ' and x != '  ', lyrics))


# print(lyrics[0].split(' '))
for idx, line in enumerate(lyrics):
    if len(line) > 24:
        splited_line = line.split(' ')
        half = len(splited_line) // 2
        lyrics[idx] = ' '.join(splited_line[:half])
        lyrics.insert(idx+1, ' '.join(splited_line[half:]))

print(lyrics)

# new_lyrics = ''
# for i, line in enumerate(lyrics):
#     new_lyrics += (line + '\n')
#     if i % 2 == 1:
#         new_lyrics += '\n'
#     # print(i, line)

# new_lyrics = new_lyrics.strip()
# print(new_lyrics)


# sample_list = ['   ', 'a dd', '', 'abc', 'qdsf']
# sample_list = ' '.join(sample_list).split()
# print(sample_list)
