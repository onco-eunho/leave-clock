import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from service.time_calculator import TimeCalculator, Time, format_timedelta_to_total_hours, DayStatus
from service.cheer_up import get_cheer_message
from PIL import Image, ImageTk
import os, sys

class TimeKeeperApp:
    def __init__(self, master):
        self.master = master
        master.title("퇴근 시간 계산기")
        master.geometry("450x550")
        try:
            # Determine the base path for resources
            if getattr(sys, 'frozen', False):
                # Running in a PyInstaller bundle
                base_path = sys._MEIPASS
            else:
                # Running in a normal Python environment
                script_dir = os.path.dirname(os.path.abspath(__file__))
                # Assuming .ini and icon.png are in the project root, two levels up from adaptor/gui.py
                base_path = os.path.abspath(os.path.join(script_dir, '..', '..'))

            icon_path = os.path.join(base_path, "statics", "icon.png") # Assuming icon.png is in statics/ and added to statics/ of bundle

            icon_image = Image.open(icon_path)
            icon_image.thumbnail((64, 64), Image.LANCZOS) # Resize to 64x64, maintaining aspect ratio
            icon_photo = ImageTk.PhotoImage(icon_image)
            master.iconphoto(True, icon_photo)
        except Exception as e:
            print(f"Error setting icon: {e}")

        # Pass the absolute path to .ini file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Assuming .ini is in the project root, two levels up from adaptor/gui.py
        project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
        config_file_path = os.path.join(project_root, '.ini')
        self.calculator = TimeCalculator(config_path=config_file_path)
        self.config = self.calculator.config # Access config from the calculator instance

        self._create_widgets()

    def _create_widgets(self):
        # --- Main Frame ---
        main_frame = ttk.Frame(self.master, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        # --- Input Fields ---
        ttk.Label(main_frame, text="총 필요 시간 (HH:MM:SS):").pack(fill=X)
        self.entry_required = ttk.Entry(main_frame)
        self.entry_required.pack(fill=X, pady=(0, 5))
        default_required_time = self.config.get('app', 'default_required_time', fallback='40:00:00')
        self.entry_required.insert(0, default_required_time)

        ttk.Label(main_frame, text="현재까지 누적 시간 (HH:MM:SS):").pack(fill=X)
        self.entry_accumulated = ttk.Entry(main_frame)
        self.entry_accumulated.pack(fill=X, pady=(0, 5))

        ttk.Label(main_frame, text="출근 시간 (HH:MM:SS):").pack(fill=X)
        self.entry_current = ttk.Entry(main_frame)
        self.entry_current.pack(fill=X, pady=(0, 10))

        # --- Work Days Configuration ---
        work_days_per_week = self.config.getint('app', 'work_days_per_week', fallback=5)
        day_names = ["월", "화", "수", "목", "금", "토", "일"]

        ttk.Label(main_frame, text="근무일:").pack(fill=X, pady=(10, 0))

        self.day_status_vars = []
        day_options = [status.value for status in DayStatus]

        days_frame = ttk.Frame(main_frame)
        days_frame.pack(fill=X, pady=5)

        for i in range(work_days_per_week):
            day_frame = ttk.Frame(days_frame)
            day_frame.pack(side=LEFT, fill=X, expand=True, padx=5)

            ttk.Label(day_frame, text=day_names[i]).pack()

            day_status_var = ttk.StringVar(value=DayStatus.WORK.value)
            day_status_menu = ttk.Combobox(day_frame, textvariable=day_status_var, values=day_options, state="readonly", font=("Helvetica", 10), justify='center', width=5)
            day_status_menu.pack(pady=2, fill=X)
            self.day_status_vars.append(day_status_var)
            day_status_menu.bind("<<ComboboxSelected>>", lambda event, menu=day_status_menu, var=day_status_var: self._update_day_status_style(menu, var))
            self._update_day_status_style(day_status_menu, day_status_var)

        # --- Calculate Button ---
        calculate_button = ttk.Button(main_frame, text="퇴근 시간 계산", command=self.on_calculate, bootstyle=SUCCESS)
        calculate_button.pack(fill=X, pady=15, ipady=5)

        # --- Result Display ---
        self.result_var = ttk.StringVar()
        result_label = ttk.Label(main_frame, textvariable=self.result_var, font=("Helvetica", 14))
        result_label.pack(pady=5)

        self.avg_time_var = ttk.StringVar()
        avg_time_label = ttk.Label(main_frame, textvariable=self.avg_time_var, font=("Helvetica", 12), bootstyle=PRIMARY)
        avg_time_label.pack(pady=5)

        self.cheer_var = ttk.StringVar()
        cheer_label = ttk.Label(main_frame, textvariable=self.cheer_var, font=("Helvetica", 12), bootstyle=INFO)
        cheer_label.pack(pady=5)

        self.today_end_time_var = ttk.StringVar()
        today_end_time_label = ttk.Label(main_frame, textvariable=self.today_end_time_var, font=("Helvetica", 12), bootstyle=WARNING)
        today_end_time_label.pack(pady=5)

    def on_calculate(self):
        required_time = self.entry_required.get()
        accumulated_time = self.entry_accumulated.get()
        current_time = self.entry_current.get()

        print(f"--- Calculation Start ---")
        print(f"Input: Required={required_time}, Accumulated={accumulated_time}, Current={current_time}")

        if not all([required_time, accumulated_time, current_time]):
            messagebox.showerror("오류", "모든 시간 값을 입력해야 합니다.")
            print(f"Error: Missing input values.")
            return

        # --- Day Status Calculation ---
        total_vacation_hours = 0
        excluded_days = 0
        completed_days = 0
        for status_var in self.day_status_vars:
            status = status_var.get()
            
            if status == DayStatus.COMPLETED.value:
                completed_days += 1
                continue

            if status == DayStatus.ANNUAL_LEAVE.value:
                total_vacation_hours += 8
                excluded_days += 1
            elif status == DayStatus.HALF_DAY_LEAVE.value:
                total_vacation_hours += 4
            elif status == DayStatus.REMOTE.value:
                excluded_days += 1

        work_days_per_week = self.config.getint('app', 'work_days_per_week', fallback=5)
        remaining_days_to_work = (work_days_per_week - completed_days) - excluded_days
        print(f"Day Status: Completed={completed_days}, Excluded={excluded_days}, VacationHours={total_vacation_hours}")
        print(f"Work Days: PerWeek={work_days_per_week}, Remaining={remaining_days_to_work}")

        # --- End Time Calculation ---
        end_time_result, rest_time_result = None, None
        if remaining_days_to_work == 1:
            print(f"Scenario: Last workday (remaining_days_to_work = 1)")
            end_time_result, rest_time_result = self.calculator.calculate_end_time(required_time, accumulated_time, current_time, vacation_hours=total_vacation_hours)
            if isinstance(end_time_result, str): # Error case
                messagebox.showerror("입력 오류", end_time_result)
                self.result_var.set("")
                self.cheer_var.set("")
                print(f"Error in calculate_end_time: {end_time_result}")
            else:
                end_time_str = format_timedelta_to_total_hours(end_time_result)
                rest_time_str = format_timedelta_to_total_hours(rest_time_result)
                self.result_var.set(f"🎉 예상 완료 시간: {end_time_str}\n⏳ 남은 시간: {rest_time_str}")
                cheer_message = get_cheer_message(rest_time_result, self.config)
                self.cheer_var.set(cheer_message)
                print(f"Last Day Result: EndTime={end_time_str}, RestTime={rest_time_str}")
        else:
            self.result_var.set("")
            self.cheer_var.set("")
            print(f"Not last workday, clearing result and cheer messages.")

        # --- Average Time Calculation ---
        print(f"Calculating average time per day...")
        error_msg, avg_time_result = self.calculator.calculate_average_time_per_day(required_time, accumulated_time, completed_days, excluded_days, vacation_hours=total_vacation_hours)

        if error_msg:
            self.avg_time_var.set(error_msg)
            self.today_end_time_var.set("") # Clear today's end time if there's an error
            print(f"Error in calculate_average_time_per_day: {error_msg}")
        elif avg_time_result is not None:
            avg_time_str = format_timedelta_to_total_hours(avg_time_result)
            self.avg_time_var.set(f"🗓️ 남은 날, 하루 평균: {avg_time_str}")
            print(f"Average Time Result: {avg_time_str}")

            # Calculate today's estimated end time if not the last workday
            if remaining_days_to_work > 1:
                print(f"Scenario: More than one workday remaining (remaining_days_to_work > 1)")
                try:
                    current_time_td = Time(*map(int, current_time.split(':'))).to_timedelta()
                    today_estimated_end_time = current_time_td + avg_time_result
                    today_end_time_str = format_timedelta_to_total_hours(today_estimated_end_time)
                    self.today_end_time_var.set(f"⏰ 오늘 예상 퇴근 시간: {today_end_time_str}")
                    print(f"Today's Estimated End Time: CurrentTime={current_time}, AvgTime={avg_time_str}, EstimatedEndTime={today_end_time_str}")
                except ValueError:
                    self.today_end_time_var.set("출근 시간 형식 오류")
                    print(f"Error: Current time format error for today's end time calculation.")
            else:
                self.today_end_time_var.set("") # Clear if it's the last workday
                print(f"Not calculating today's end time: remaining_days_to_work is not > 1.")
        else:
            self.avg_time_var.set("")
            self.today_end_time_var.set("") # Clear today's end time if avg time is not available
            print(f"Average time result is None, clearing average and today's end time messages.")
        print(f"--- Calculation End ---")

    def _bind_paste_event(self, entry_widget):
        # Bind Ctrl+v (Windows/Linux) and Cmd+v (macOS) for paste functionality
        entry_widget.bind("<Control-v>", lambda e: entry_widget.event_generate("<<Paste>>"))
        entry_widget.bind("<Command-v>", lambda e: entry_widget.event_generate("<<Paste>>"))

    def _update_day_status_style(self, combobox, status_var):
        status = status_var.get()
        style_map = {
            DayStatus.WORK.value: "primary",
            DayStatus.REMOTE.value: "info",
            DayStatus.ANNUAL_LEAVE.value: "danger",
            DayStatus.HALF_DAY_LEAVE.value: "warning",
            DayStatus.COMPLETED.value: "success"
        }
        combobox.config(bootstyle=style_map.get(status, "default"))


if __name__ == "__main__":
    root = ttk.Window(themename="litera")
    app = TimeKeeperApp(root)
    root.mainloop()
