import customtkinter as ctk
from datetime import datetime
import calendar
from theme import BUTTON_CONFIG

class DatePickerButton(ctk.CTkButton):
    def __init__(self, master, font=("M PLUS Rounded 1c", 12), format_str="%Y-%m-%d", command=None, **kwargs):
        self.format_str = format_str
        self.date_val = None
        self.command_callback = command
        
        # Default styling
        if "text" not in kwargs:
            kwargs["text"] = "日付を選択"
        if "width" not in kwargs:
            kwargs["width"] = 140
            
        super().__init__(master, command=self.open_picker, font=font, **kwargs)

    def get_date(self):
        return self.date_val

    def set_date(self, date_str):
        self.date_val = date_str
        self.configure(text=date_str)

    def open_picker(self):
        picker = DatePickerDialog(self, self.set_date)

class DatePickerDialog(ctk.CTkToplevel):
    def __init__(self, master, on_select):
        super().__init__(master)
        self.title("日付選択")
        self.geometry("300x320")
        self.transient(master)
        self.grab_set()
        
        self.on_select = on_select
        self.current_date = datetime.now()
        self.selected_year = self.current_date.year
        self.selected_month = self.current_date.month
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header (Month/Year Navigation)
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=10)
        
        btn_prev = ctk.CTkButton(header, text="<", width=30, command=self.prev_month)
        btn_prev.pack(side="left")
        
        self.lbl_title = ctk.CTkLabel(header, text=f"{self.selected_year}年 {self.selected_month}月", font=("Arial", 16, "bold"))
        self.lbl_title.pack(side="left", expand=True)
        
        btn_next = ctk.CTkButton(header, text=">", width=30, command=self.next_month)
        btn_next.pack(side="right")
        
        # Calendar Grid
        self.cal_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cal_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.build_calendar()
        
    def build_calendar(self):
        # Clear existing
        for w in self.cal_frame.winfo_children():
            w.destroy()
            
        # Day Headers
        days = ["月", "火", "水", "木", "金", "土", "日"]
        for i, d in enumerate(days):
            fg = "black"
            if i == 5: fg = "blue"
            if i == 6: fg = "red"
            ctk.CTkLabel(self.cal_frame, text=d, text_color=fg).grid(row=0, column=i, sticky="ew", padx=2, pady=2)
            
        # Days
        cal = calendar.monthcalendar(self.selected_year, self.selected_month)
        for r, week in enumerate(cal):
            for c, day in enumerate(week):
                if day != 0:
                    def on_day(d=day):
                        date_str = f"{self.selected_year}-{self.selected_month:02d}-{d:02d}"
                        self.on_select(date_str)
                        self.destroy()
                        
                    btn = ctk.CTkButton(self.cal_frame, text=str(day), width=30, height=30, 
                                        fg_color="transparent", text_color="#333", border_width=1, border_color="#EEE",
                                        hover_color="#EEE", command=on_day)
                    btn.grid(row=r+1, column=c, padx=2, pady=2)

    def prev_month(self):
        self.selected_month -= 1
        if self.selected_month < 1:
            self.selected_month = 12
            self.selected_year -= 1
        self.lbl_title.configure(text=f"{self.selected_year}年 {self.selected_month}月")
        self.build_calendar()

    def next_month(self):
        self.selected_month += 1
        if self.selected_month > 12:
            self.selected_month = 1
            self.selected_year += 1
        self.lbl_title.configure(text=f"{self.selected_year}年 {self.selected_month}月")
        self.build_calendar()

class TimePickerButton(ctk.CTkButton):
    def __init__(self, master, font=("M PLUS Rounded 1c", 12), format_str="%H:%M", command=None, **kwargs):
        self.time_val = None
        
        if "text" not in kwargs:
            kwargs["text"] = "時間を選択"
        if "width" not in kwargs:
            kwargs["width"] = 100
            
        super().__init__(master, command=self.open_picker, font=font, **kwargs)

    def get_time(self):
        return self.time_val

    def set_time(self, time_str):
        self.time_val = time_str
        self.configure(text=time_str)

    def open_picker(self):
        TimePickerDialog(self, self.set_time)

class TimePickerDialog(ctk.CTkToplevel):
    def __init__(self, master, on_select):
        super().__init__(master)
        self.title("時間選択")
        self.geometry("300x400")
        self.transient(master)
        self.grab_set()
        self.on_select = on_select
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Grid: Hours Left, Minutes Right
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(main_frame, text="時").grid(row=0, column=0)
        ctk.CTkLabel(main_frame, text="分").grid(row=0, column=1)
        
        h_frame = ctk.CTkScrollableFrame(main_frame, height=250)
        h_frame.grid(row=1, column=0, sticky="nsew", padx=5)
        
        m_frame = ctk.CTkScrollableFrame(main_frame, height=250)
        m_frame.grid(row=1, column=1, sticky="nsew", padx=5)
        
        self.selected_h = "10"
        self.selected_m = "00"
        self.lbl_preview = ctk.CTkLabel(self, text="10:00", font=("Arial", 20, "bold"))
        self.lbl_preview.pack(pady=5)
        
        def update_preview():
            self.lbl_preview.configure(text=f"{self.selected_h}:{self.selected_m}")

        def set_h(h):
            self.selected_h = h
            update_preview()
            
        def set_m(m):
            self.selected_m = m
            update_preview()
            
        for h in range(0, 24):
            val = f"{h:02d}"
            ctk.CTkButton(h_frame, text=val, width=50, command=lambda v=val: set_h(v), 
                          fg_color="transparent", border_width=1, text_color="black", hover_color="#EEE").pack(pady=2)
                          
        for m in range(0, 60, 5): # 5 min intervals
            val = f"{m:02d}"
            ctk.CTkButton(m_frame, text=val, width=50, command=lambda v=val: set_m(v),
                          fg_color="transparent", border_width=1, text_color="black", hover_color="#EEE").pack(pady=2)
                          
        ctk.CTkButton(self, text="決定", command=self.confirm, **BUTTON_CONFIG).pack(pady=10)
        
    def confirm(self):
        t_str = f"{self.selected_h}:{self.selected_m}"
        self.on_select(t_str)
        self.destroy()
