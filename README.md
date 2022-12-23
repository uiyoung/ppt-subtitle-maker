# PPT Subtitle Maker

txt 가사파일을 두줄 씩 불러와서 PPT로 만들어주는 앱

## USAGE

1. install python 3.9
2. python-pptx 라이브러리 설치
   - `pip install python-pptx`
3. 곡명.txt 파일을 만들어서 가사를 해당 txt 파일에 저장한다.
   - e.g. `sample.txt`
4. `python song-subtitle-maker [곡명]` 으로 실행한다
   - e.g. `python subtitle-maker sample`
5. 생성된 `곡명.pptx ` ppt 파일을 확인한다.

## todo

- DB 연결
- try catch
- GUI
