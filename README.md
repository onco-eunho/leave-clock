# 퇴근 시간 계산기

- 해당 코드는 퇴근 시간을 계산하는 프로그램입니다. 사용자는 총 필요 시간, 누적 시간, 출근 시간을 입력하여 퇴근 시간을 계산할 수 있습니다. 또한, 잔여 시간에 따라 격려 메시지를 출력합니다.

## 개발 환경

- Python 3.12 이상

## 사용법

```bash
python main.py -r <필요 시간> -a <누적 시간> -c <출근 시간>
```

## 예시

```bash
python main.py -a 32:17:29 -c 10:23:37

완료 시간: 18:06:08, 잔여 시간: 0:30:35
이제 한 시간도 안 남았네요! 힘내세요!🏃
```

## .ini 파일 설정 및 커스터마이징

- `.ini` 파일을 사용하여 기본 필요 시간을 설정할 수 있습니다. 예를 들어, `default_required_time`을 `40:00:00`으로 설정하면, 필요 시간을 입력하지 않았을 때 기본값으로 사용됩니다.
- [messages] 섹션을 사용하여 격려 메시지를 커스터마이즈할 수 있습니다.

```ini
[app]
default_required_time = 40:00:00

[messages]
more_than_4_hours_left = 아직 네 시간 넘게 남았네요... 여유를 가지세요!🫠
more_than_2_hours_left = 아직 두 시간 넘게 남았네요... 일 좀 더 하셔야겠어요!🥹
less_than_1_hour_left  = 이제 한 시간도 안 남았네요! 힘내세요!🏃
work_done              = 수고하셨습니다! 퇴근 하세요!✌️
invalid_start_time     = 출근한지 얼마 안 된 것 같은데요? 출근 시간부터 다시 확인해 주세요!😅
```

- 추가로 cheer_up.py 파일 내용을 수정하면 좀 더 다양한 격려 메시지를 추가할 수 있습니다.

```python
def get_cheer_message(rest_time, config):
    ...
    elif rest_time.total_seconds() > 28800:
        return "여덟시간이라니... 여덟시간이라니!!!"
    ...
```
