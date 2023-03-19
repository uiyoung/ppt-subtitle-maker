# PPT Subtitle Maker
<image src="./resources/hymns.png" width=200>

가사를 DB로 관리하고 콘티를 만들어서 PPT 자막 파일로 만들어 주는 앱


## Features

- 가사 DB 관리 : 등록, 검색, 수정, 삭제
- 콘티를 만들어서 한개의 PPT 자막 파일 생성

## Requirements

1. install [python 3.9.12](https://www.python.org/downloads/release/python-3912/)
   - 😮 error occurs on python over 3.10
2. install python-pptx library
   - `pip install python-pptx`

## How to Use

### GUI mode

1. `start.bat` 파일을 실행하여 시작
2. 추가할 곡을 검색한다.
   - 검색결과가 있는 경우 : 목록에서 원하는 곡을 고르고 `목록에 추가` 버튼을 누른다.
   - 검색결과가 없는 경우 : `새 가사 등록` 버튼을 눌러 새로운 가사를 등록한다.
3. 원하는 곡을 모두 선택했으면 메인 윈도우의 `PPT 생성` 버튼을 눌러 PPT 파일을 생성한다.

### CLI mode
txt 가사파일을 두줄 씩 불러와서 PPT로 만들어주는 앱

1. `/txt` 디렉토리에 `곡명.txt` 파일을 만들고 그 안에 만들고 싶은 자막의 가사를 작성한다.
   - 두줄 씩 엔터로 구분해서 작성
   - e.g. `/txt/sample.txt`
2. run `python subtitle_maker ["곡명"]
   - e.g. `python cli_subtitle_maker sample`
3. 생성된 `./ppt/곡명.pptx ` ppt 파일을 확인한다.

## todo

- [x] manage lyrics with DB
- [x] GUI mode
- [x] merger
- [x] 여러 곡 한번에 저장해서 콘티 만들기
- [ ] 콘티 관리(DB 저장, 불러오기)
- [ ] 종료시 콘티 저장, 다시 실행시 불러오기
- [ ] try catch 처리
- [ ] local db -> cloud db with api

## Copyright Information
- <a href="https://www.flaticon.com/free-icons/hymns" title="hymns icons">Hymns icons created by Flat Icons - Flaticon</a>