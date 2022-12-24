# PPT Subtitle Maker

txt 가사파일을 두줄 씩 불러와서 PPT로 만들어주는 앱

## USAGE

1. install [python 3.9.12](https://www.python.org/downloads/release/python-3912/)
   - error occurs on python over 3.10
2. install python-pptx library
   - `pip install python-pptx`
3. 곡명.txt 파일을 만들고 그 안에 만들고 싶은 자막의 가사를 작성한다.
   - 한줄 씩 엔터로 구분해서 작성
   - e.g. `sample.txt`
4. run `python subtitle-maker [곡명]
   - e.g. `python subtitle-maker sample`
5. 생성된 `곡명.pptx ` ppt 파일을 확인한다.

## todo

- manage lyrics with DB
- try catch
- GUI mode
- 여러 곡 한번에 저장해서 콘티 만들기
