# read lyrics file
f = open("test.txt", 'r', encoding='UTF-8')
lines = f.readlines()
lines = list(filter(lambda s: s != ('\u200b\n' and '\n'), lines))  # remove emptyline
lyrics = []
for i in range(0, len(lines), 2):
    lyrics.append(''.join(lines[i:i+2]))

print(lyrics)
lyrics = list(map(lambda s: s.strip(), lyrics))

print(lyrics)
exit()


mylist = ['hello\n', '안녕\n', 'world\n', '세상\n', 'lorem\n', '로렘\n', 'ipsum\n', '입숨\n']
for i in range(0, len(mylist), 2):
    print(mylist[i:i+2])
# f = open("test.txt", 'r', encoding='UTF-8')
# lines = f.readlines()
# result = []
# for i in range(0, len(lines), 2):
#     result.append(''.join(lines[i:i+2]))

# print(result)


# mylist = ['hello\n', '안녕\n', 'world\n', '세상\n', 'lorem\n', '로렘\n', 'ipsum\n', '입숨\n']
# result = []
# for i in range(0, len(mylist), 2):
#     temp = []
#     temp = ''.join(mylist[i:i+2])
#     result.append(temp)
# print(result)

exit()

lyrics = []
for idx, line in enumerate(lines):
    if idx % 2 == 0:
        lyrics.append(line)
    else:
        lyrics[idx]

f2 = open("write-test.txt", "w", encoding='UTF-8')
for line in lines:
    f2.write(line)

f2.close

for idx, line in enumerate(lines):
    line = line.strip()
    # print(idx, idx % 2, line)


f.close()
