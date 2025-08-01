import configparser
import os

def load_config(base_path):
    config = configparser.ConfigParser()
    config_file_path = os.path.join(base_path, '.ini')
    if not os.path.exists(config_file_path):
        # Create a default .ini file if it doesn't exist
        config['app'] = {
            'default_required_time': '40:00:00',
            'work_days_per_week': '5'
        }
        config['messages'] = {
            'more_than_4_hours_left': '아직 네 시간 넘게 남았네요... 여유를 가지세요!🫠',
            'more_than_2_hours_left': '아직 두 시간 넘게 남았네요... 일 좀 더 하셔야겠어요!🥹',
            'less_than_1_hour_left': '이제 한 시간도 안 남았네요! 힘내세요!🏃',
            'work_done': '수고하셨습니다! 퇴근 하세요!✌️',
            'invalid_start_time': '출근한지 얼마 안 된 것 같은데요? 출근 시간부터 다시 확인해 주세요!😅'
        }
        with open(config_file_path, 'w') as configfile:
            config.write(configfile)
    else:
        config.read(config_file_path)
    return config
