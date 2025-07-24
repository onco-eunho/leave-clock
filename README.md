# 퇴근 시간 계산기

<img src="app.png" alt="Leave Clock App">

- gemini cli와 Vibe 코딩 해보기(~~vibe coding이 느좋코딩 이래요~~)
- 해당 코드는 퇴근 시간을 계산하는 프로그램입니다. 사용자는 총 필요 시간, 누적 시간, 출근 시간을 입력하여 퇴근 시간을 계산할 수 있습니다.
- 또한, 잔여 근무 시간을 기반으로 남은 근무일의 평균 퇴근 시간을 예측하고, 격려 메시지를 제공합니다.

## 개발 환경

<img src="https://img.shields.io/badge/Python-3.13-blue.svg" alt="Python Version">

## 사용법

### 설치

1. 이 저장소를 클론합니다.
2. (선택) 가상 환경을 설정합니다. 예: `python -m venv .venv`
3. `pip install -r requirements.txt`를 사용해 필요한 패키지를 설치합니다.
4. (선택) `.ini`파일을 수정하여 커스터마이징을 진행합니다.
5. (선택) `install.sh`(MacOS) 또는 `install.bat`(Windows)를 실행하여 실행 파일을 설치합니다.

### 실행

- python 사용 시: `python main.py`를 실행하여 프로그램을 시작합니다.
- 실행 파일 사용 시: `leave-clock` 명령어를 사용하거나 `leave-clock.app` 파일을 실행합니다.(실행 파일로 실행할 경우 지연 시간이 발생할 수 있습니다.)

### 커스터마이징

- `.ini` 파일을 수정하여 메시지, 시간 단위 등을 변경할 수 있습니다.
  ```ini
  [messages]
  more_than_4_hours_left = "아직 네 시간 넘게 남았네요... 여유를 가지세요!🫠"
  more_than_2_hours_left = "아직 두 시간 넘게 남았네요... 일 좀 더 하셔야겠어요!🥹"
  less_than_1_hour_left = "이제 한 시간도 안 남았네요! 힘내세요!🏃"
  work_done = "수고하셨습니다! 퇴근 하세요!✌️"
  invalid_start_time = "출근한지 얼마 안 된 것 같은데요? 출근 시간부터 다시 확인해 주세요!😅"
  ```
- `service/cheer_up.py` 파일에서 조건문을 추가/수정/삭제 해서 격려 메시지가 출력되는 조건을 커스터마이징 할 수 있습니다.
  ```python
  def get_cheer_message(rest_time, config):
    if rest_time.total_seconds() > 60 * 60 * 4:
        return config.get('messages', 'more_than_4_hours_left', fallback="아직 네 시간 넘게 남았네요... 여유를 가지세요!🫠")
    elif rest_time.total_seconds() > 60 * 60 * 2:
        return config.get('messages', 'more_than_2_hours_left', fallback="아직 두 시간 넘게 남았네요... 일 좀 더 하셔야겠어요!🥹")
    elif rest_time.total_seconds() > 0:
        return config.get('messages', 'less_than_1_hour_left', fallback="이제 한 시간도 안 남았네요! 힘내세요!🏃")
    elif rest_time.total_seconds() <= 0:
        return config.get('messages', 'work_done', fallback="수고하셨습니다! 퇴근 하세요!✌️")
    else:
        return config.get('messages', 'invalid_start_time', fallback="출근한지 얼마 안 된 것 같은데요? 출근 시간부터 다시 확인해 주세요!😅")
  ```

### 버그

- python으로 실행 시 앱 아이콘이 표시되지 않는 버그가 있습니다. 이는 Python의 `tkinter` 라이브러리에서 발생하는 문제로, 실행 파일로 실행할 경우에는 정상적으로 표시됩니다.
