import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from main import calculate_end_time, format_timedelta_to_total_hours, config, get_current_time, calculate_average_time_per_day
from cheer_up import get_cheer_message

def on_calculate():
    required_time = entry_required.get()
    accumulated_time = entry_accumulated.get()
    current_time = entry_current.get()

    if not all([required_time, accumulated_time, current_time]):
        messagebox.showerror("오류", "모든 시간 값을 입력해야 합니다.")
        return

    # --- Day Status Calculation ---
    total_vacation_hours = 0
    excluded_days = 0
    for i, status_var in enumerate(day_status_vars):
        status = status_var.get()
        # 완료된 날은 계산에서 제외
        if completed_vars[i].get():
            continue

        if status == "연차":
            total_vacation_hours += 8
            excluded_days += 1
        elif status == "반차":
            total_vacation_hours += 4
        elif status == "재택":
            excluded_days += 1

    completed_days = sum(var.get() for var in completed_vars)
    work_days_per_week = config.getint('app', 'work_days_per_week', fallback=5)
    remaining_days_to_work = (work_days_per_week - completed_days) - excluded_days

    # --- End Time Calculation (only if it's the last workday) ---
    if remaining_days_to_work == 1:
        end_time_result, rest_time_result = calculate_end_time(required_time, accumulated_time, current_time, vacation_hours=total_vacation_hours)
        if isinstance(end_time_result, str): # Error case
            messagebox.showerror("입력 오류", end_time_result)
            result_var.set("")
            cheer_var.set("")
        else:
            end_time_str = format_timedelta_to_total_hours(end_time_result)
            rest_time_str = format_timedelta_to_total_hours(rest_time_result)
            result_var.set(f"🎉 예상 완료 시간: {end_time_str}\n⏳ 남은 시간: {rest_time_str}")
            cheer_message = get_cheer_message(rest_time_result, config)
            cheer_var.set(cheer_message)
    else:
        result_var.set("")
        cheer_var.set("")

    # --- Average Time Calculation ---
    error_msg, avg_time_result = calculate_average_time_per_day(required_time, accumulated_time, completed_days, excluded_days, vacation_hours=total_vacation_hours)

    if error_msg:
        avg_time_var.set(error_msg)
    elif avg_time_result is not None:
        avg_time_str = format_timedelta_to_total_hours(avg_time_result)
        avg_time_var.set(f"🗓️ 남은 날, 하루 평균: {avg_time_str}")
    else:
        avg_time_var.set("")


# --- GUI Setup ---
window = ttk.Window(themename="litera")
window.title("퇴근 시간 계산기")
window.geometry("450x650")

# --- Main Frame ---
main_frame = ttk.Frame(window, padding=20)
main_frame.pack(fill=BOTH, expand=YES)

# --- Input Fields ---
ttk.Label(main_frame, text="총 필요 시간 (HH:MM:SS):").pack(fill=X)
entry_required = ttk.Entry(main_frame)
entry_required.pack(fill=X, pady=(0, 5))
default_required_time = config.get('app', 'default_required_time', fallback='40:00:00')
entry_required.insert(0, default_required_time)

ttk.Label(main_frame, text="현재까지 누적 시간 (HH:MM:SS):").pack(fill=X)
entry_accumulated = ttk.Entry(main_frame)
entry_accumulated.pack(fill=X, pady=(0, 5))

ttk.Label(main_frame, text="출근 시간 (HH:MM:SS):").pack(fill=X)
entry_current = ttk.Entry(main_frame)
entry_current.pack(fill=X, pady=(0, 10))

# --- Work Days Configuration ---
work_days_per_week = config.getint('app', 'work_days_per_week', fallback=5)
day_names = ["월", "화", "수", "목", "금", "토", "일"]

ttk.Label(main_frame, text="근무일:").pack(fill=X, pady=(10, 0))

completed_vars = []
day_status_vars = []
day_options = ["근무", "재택", "연차", "반차"]


days_frame = ttk.Frame(main_frame)
days_frame.pack(fill=X, pady=5)

for i in range(work_days_per_week):
    day_frame = ttk.Frame(days_frame)
    day_frame.pack(side=LEFT, fill=X, expand=True, padx=5)

    ttk.Label(day_frame, text=day_names[i]).pack()

    completed_var = ttk.BooleanVar()
    completed_chk = ttk.Checkbutton(day_frame, text="완료", variable=completed_var, bootstyle="success-round-toggle")
    completed_chk.pack(pady=2)
    completed_vars.append(completed_var)

    day_status_var = ttk.StringVar(value=day_options[0])
    day_status_menu = ttk.Combobox(day_frame, textvariable=day_status_var, values=day_options, state="readonly", font=("Helvetica", 10), justify='center', width=5)
    day_status_menu.pack(pady=2, fill=X)
    day_status_vars.append(day_status_var)


# --- Calculate Button ---
calculate_button = ttk.Button(main_frame, text="퇴근 시간 계산", command=on_calculate, bootstyle=SUCCESS)
calculate_button.pack(fill=X, pady=15, ipady=5)

# --- Result Display ---
result_var = ttk.StringVar()
result_label = ttk.Label(main_frame, textvariable=result_var, font=("Helvetica", 14))
result_label.pack(pady=5)

avg_time_var = ttk.StringVar()
avg_time_label = ttk.Label(main_frame, textvariable=avg_time_var, font=("Helvetica", 12), bootstyle=PRIMARY)
avg_time_label.pack(pady=5)

cheer_var = ttk.StringVar()
cheer_label = ttk.Label(main_frame, textvariable=cheer_var, font=("Helvetica", 12), bootstyle=INFO)
cheer_label.pack(pady=5)


window.mainloop()