def get_cheer_message(rest_time, config):
    if rest_time.total_seconds() > 14400:
        return config.get('messages', 'more_than_4_hours_left', fallback="아직 네 시간 넘게 남았네요... 여유를 가지세요!🫠")
    elif rest_time.total_seconds() > 7200:
        return config.get('messages', 'more_than_2_hours_left', fallback="아직 두 시간 넘게 남았네요... 일 좀 더 하셔야겠어요!🥹")
    elif rest_time.total_seconds() > 0:
        return config.get('messages', 'less_than_1_hour_left', fallback="이제 한 시간도 안 남았네요! 힘내세요!🏃")
    elif rest_time.total_seconds() <= 0:
        return config.get('messages', 'work_done', fallback="수고하셨습니다! 퇴근 하세요!✌️")
    else:
        return config.get('messages', 'invalid_start_time', fallback="출근한지 얼마 안 된 것 같은데요? 출근 시간부터 다시 확인해 주세요!😅")
