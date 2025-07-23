import argparse
import configparser
from datetime import datetime, timedelta
from cheer_up import get_cheer_message

config = configparser.ConfigParser()
config.read('.ini')

class Time:
    def __init__(self, hours=0, minutes=0, seconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def __str__(self):
        return f"{self.hours:02}:{self.minutes:02}:{self.seconds:02}"
    
    def to_timedelta(self):
        return timedelta(hours=self.hours, minutes=self.minutes, seconds=self.seconds)


def format_timedelta_to_total_hours(td):
    if not isinstance(td, timedelta):
        return td
    total_seconds = td.total_seconds()
    sign = "-" if total_seconds < 0 else ""
    total_seconds = abs(total_seconds)
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return f"{sign}{hours:02}:{minutes:02}:{seconds:02}"


def get_current_time():
    now = datetime.now()
    return Time(now.hour, now.minute, now.second)

def calculate_end_time(required_time_str, accumulated_time_str, current_time_str, vacation_hours=0):
    try:
        time_delimiter = ':'
        
        required_time = Time(*map(int, required_time_str.split(time_delimiter))).to_timedelta()
        accumulated_time = Time(*map(int, accumulated_time_str.split(time_delimiter))).to_timedelta()
        current_time = Time(*map(int, current_time_str.split(time_delimiter))).to_timedelta()

        vacation_time = timedelta(hours=vacation_hours)
        adjusted_required_time = required_time - vacation_time

        remaining_delta = adjusted_required_time - accumulated_time
        end_time = current_time + remaining_delta
        rest_time = end_time - get_current_time().to_timedelta()

        return end_time, rest_time

    except ValueError:
        return "잘못된 시간 형식입니다. HH:MM:SS 형식으로 입력해 주세요.", None

def calculate_average_time_per_day(required_time_str, accumulated_time_str, completed_days, excluded_days=0, vacation_hours=0):
    try:
        time_delimiter = ':'
        
        required_time = Time(*map(int, required_time_str.split(time_delimiter))).to_timedelta()
        accumulated_time = Time(*map(int, accumulated_time_str.split(time_delimiter))).to_timedelta()

        vacation_time = timedelta(hours=vacation_hours)
        adjusted_required_time = required_time - vacation_time

        work_days_per_week = config.getint('app', 'work_days_per_week', fallback=5)
        
        # First, check if all work days are already marked as completed
        if (work_days_per_week - completed_days) <= 0:
            return "모든 근무일을 완료했습니다! 🎉", timedelta(0)

        # Calculate remaining work time
        remaining_work_time = adjusted_required_time - accumulated_time
        if remaining_work_time.total_seconds() <= 0:
             return "목표 근무 시간을 모두 채웠습니다! 🎉", timedelta(0)

        # Calculate the actual number of days left to work
        remaining_days_to_work = (work_days_per_week - completed_days) - excluded_days

        if remaining_days_to_work <= 0:
            return "남은 근무일이 없거나 제외할 날이 너무 많습니다.", None

        average_seconds_per_day = remaining_work_time.total_seconds() / remaining_days_to_work
        
        avg_td = timedelta(seconds=average_seconds_per_day)

        return None, avg_td

    except (ValueError, configparser.NoOptionError) as e:
        return f"계산 오류: {e}", None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="금요일의 퇴근 시간을 계산합니다. 필요 시간, 누적 시간, 출근 시간을 입력하세요.")
    parser.add_argument("-r", "--required", dest="required_time", required=False, help="총 필요 시간입니다. HH:MM:SS 형식으로 입력하세요. (e.g., '08:00:00').", default=config.get('app', 'default_required_time', fallback='40:00:00'))
    parser.add_argument("-a", "--accumulated", dest="accumulated_time", required=True, help="누적 시간입니다. HH:MM:SS 형식으로 입력하세요. (e.g., '01:30:00').")
    parser.add_argument("-c", "--current", dest="current_time", required=True, help="출근 시간입니다. HH:MM:SS 형식으로 입력하세요. (e.g., '14:00:00').")
    
    args = parser.parse_args()

    end_time_result, rest_time_result = calculate_end_time(args.required_time, args.accumulated_time, args.current_time)

    print(f"완료 시간: {format_timedelta_to_total_hours(end_time_result)}, 잔여 시간: {format_timedelta_to_total_hours(rest_time_result)}")
    print(get_cheer_message(rest_time_result, config))