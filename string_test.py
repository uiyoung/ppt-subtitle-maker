str = ' 우리에겐 소원이 하나 있네\n주님 다시 오실 그날 까지\n\n우리 가슴에 새긴 주의 십자가 사랑\n나의 교회를 사랑케 하네\n\n주의 교회를 향한 우리 마음\n희생과 포기와 가난과 고난\n\n하물며 죽음조차 우릴 막을 수 없네\n우리 교회는 이 땅의 희망\n\n \n\n교회를 교회되게 예밸 예배 되게\n\n우릴 사용하소서\n\n진정한 부흥의 날 오늘 임하도록\n\n우릴 사용하소서\n\n \n\n성령안에 예배 하리라\n\n자유의 마음으로\n\n사랑으로 사역하리라\n\n교회는 생명이니\n\n \n\n교회를 교회되게 예밸 예배 되게\n\n우릴 사용하소서\n\n진정한 부흥의 날 오늘 임하도록\n\n우릴 사용하소서'
str = str.strip().split('\n')
str = list(filter(lambda x: x != '' and x != ' ' and x != '  ', str))
print(str)

new_str = ''
for i, line in enumerate(str):
    new_str += (line + '\n')
    if i % 2 == 1:
        new_str += '\n'
    # print(i, line)

new_str = new_str.strip()
print(new_str)


# sample_list = ['   ', 'a dd', '', 'abc', 'qdsf']
# sample_list = ' '.join(sample_list).split()
# print(sample_list)
