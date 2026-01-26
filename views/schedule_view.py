import customtkinter as ctk
from database import DatabaseManager
from datetime import datetime
from theme import BrandColors, BUTTON_CONFIG, HEADER_LABEL_CONFIG, SUBHEADER_CONFIG
from views.components import SelectionModal
from views.post_builder import PostBuilderModal

from views.date_picker import DatePickerButton, TimePickerButton
from PIL import Image, ImageOps
from tkinter import filedialog, messagebox
import os
import sys

class ScheduleView(ctk.CTkFrame):
    def __init__(self, master, db: DatabaseManager, client_id, preview_frame=None):
        super().__init__(master, fg_color=BrandColors.BG_LIGHT_MAIN)
        self.db = db
        self.client_id = client_id
        self.current_preview_image = None
        self.btn_images = [] 
        self.thumbnail_cache = {} # Cache for list thumbnails 
        
        # Grid Configuration
        self.grid_columnconfigure(0, weight=1) 
        self.grid_rowconfigure(1, weight=1)

        # === LEFT COLUMN: LIST ===
        self.left_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.left_panel.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))
        self.left_panel.grid_columnconfigure(0, weight=1)
        self.left_panel.grid_rowconfigure(2, weight=1)

        # 1. Header Area
        self.header_frame = ctk.CTkFrame(self.left_panel, fg_color=BrandColors.BG_WHITE, corner_radius=0, height=60)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.header_frame.pack_propagate(False) # Fixed height header
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="進行管理", font=("M PLUS Rounded 1c", 18, "bold"), text_color="#333")
        self.title_label.pack(side="left", padx=(20, 20), pady=10)
        
        # Store Filter (Compact)
        self.store_filter_var = ctk.StringVar(value="全店舗データのサマリ")
        self.store_combo = ctk.CTkComboBox(self.header_frame, 
                                           values=["全店舗データのサマリ"],
                                           command=self.filter_changed,
                                           variable=self.store_filter_var,
                                           width=180, height=28, font=("M PLUS Rounded 1c", 12),
                                           state="readonly")
        self.store_combo.pack(side="left", padx=5, pady=10)

        # Store Config Button
        self.config_btn = ctk.CTkButton(self.header_frame, text="⚙️ 店舗", command=self.open_store_management, width=60, height=28,
                                        fg_color="transparent", border_width=1, border_color="#CCC", text_color="#555", hover_color="#EEE",
                                        font=("M PLUS Rounded 1c", 11))
        self.config_btn.pack(side="left", padx=5)

        # Import Button
        self.import_btn = ctk.CTkButton(self.header_frame, text="📥 CSV取込", command=self.import_csv, width=80, height=28,
                                        fg_color="transparent", border_width=1, border_color="#CCC", text_color="#333", hover_color="#EEE",
                                        font=("M PLUS Rounded 1c", 11, "bold"))
        self.import_btn.pack(side="left", padx=5)

        # Actions (Right aligned)
        self.add_btn = ctk.CTkButton(self.header_frame, text="＋ 追加", command=self.open_add_schedule_modal, width=80, height=28,
                                        fg_color="#333", hover_color="black", font=("M PLUS Rounded 1c", 12, "bold"))
        self.add_btn.pack(side="right", padx=(5, 20), pady=10)

        self.ai_btn = ctk.CTkButton(self.header_frame, text="✨ AI作成", command=self.open_ai_generator, 
                                    width=110, height=32,
                                    fg_color="#6C35DE", text_color="white", hover_color="#5E2CBF",
                                    font=("M PLUS Rounded 1c", 13, "bold"))
        self.ai_btn.pack(side="right", padx=10, pady=10)

        self.refresh_btn = ctk.CTkButton(self.header_frame, text="⟳", command=self.reload_all, width=30, height=28, 
                                         fg_color="transparent", hover_color="#EEE", text_color="#333", font=("Arial", 16))
        self.refresh_btn.pack(side="right", padx=5)

        self.restart_btn = ctk.CTkButton(self.header_frame, text="App更新", command=self.restart_app, width=60, height=28,
                                         fg_color="#F57C00", hover_color="#EF6C00", font=("M PLUS Rounded 1c", 11, "bold"))
        self.restart_btn.pack(side="right", padx=5)

        # 2. View Headers (Table Header)
        # Combine Header and List into a container for "Table Look"
        self.table_container = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.table_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))
        self.table_container.grid_rowconfigure(1, weight=1)
        self.table_container.grid_columnconfigure(0, weight=1)

        self.col_header_frame = ctk.CTkFrame(self.table_container, fg_color="#F1F3F4", corner_radius=5, height=35)
        self.col_header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 0))
        self.col_header_frame.pack_propagate(False)
        
        headers = ["日付", "時間", "店舗", "コンテンツ (サムネイル+本文)", "種別", "ステータス", "確認"]
        widths = [120, 50, 80, 300, 60, 90, 40] 
        
        # Re-doing header with grid to match rows perfectly
        for w in self.col_header_frame.winfo_children(): w.destroy()
        
        for i, header in enumerate(headers):
             label = ctk.CTkLabel(self.col_header_frame, text=header, width=widths[i], anchor="w", 
                                 font=("M PLUS Rounded 1c", 11, "bold"), text_color="#5F6368")
             label.grid(row=0, column=i, padx=5, pady=5, sticky="w")
             
        self.col_header_frame.grid_columnconfigure(3, weight=1) # Content expands

        # 3. List
        self.scroll_frame = ctk.CTkScrollableFrame(self.table_container, fg_color="white", corner_radius=0)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.scroll_frame.grid_columnconfigure(3, weight=1) 
        
        # === RIGHT COLUMN: PREVIEW ===
        if preview_frame:
            self.right_panel = preview_frame
            # Clean up preview frame just in case
            for w in self.right_panel.winfo_children(): w.destroy()
        else:
            self.grid_columnconfigure(1, weight=1)
            self.right_panel = ctk.CTkFrame(self, fg_color=BrandColors.BG_WHITE, corner_radius=0, width=350)
            self.right_panel.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=0, pady=0)
            self.right_panel.pack_propagate(False)

        # Custom "Right Upper Full" Layout
        self.right_panel.grid_rowconfigure(0, weight=0) # Text
        self.right_panel.grid_rowconfigure(1, weight=1) # Phone
        
        # Title very top
        lbl = ctk.CTkLabel(self.right_panel, text="即時プレビュー", font=("M PLUS Rounded 1c", 14, "bold"), text_color=BrandColors.PRIMARY, height=20)
        lbl.pack(pady=(5, 0))
        
        # Phone Frame (Max Height, packed tight)
        self.phone_frame = ctk.CTkFrame(self.right_panel, fg_color="white", width=300, height=740, 
                                        border_width=6, border_color="#333", corner_radius=35)
        self.phone_frame.pack(pady=(5, 10), padx=15)
        self.phone_frame.pack_propagate(False)
        
        # Notch
        notch = ctk.CTkFrame(self.phone_frame, fg_color="#333", width=100, height=20, corner_radius=10)
        notch.place(relx=0.5, y=10, anchor="n")
        
        # Content Container
        self.p_content_area = ctk.CTkFrame(self.phone_frame, fg_color="transparent")
        self.p_content_area.pack(fill="both", expand=True, padx=10, pady=(40, 20)) 
        
        # User Header
        self.p_user_frame = ctk.CTkFrame(self.p_content_area, fg_color="white", height=40)
        self.p_user_frame.pack(fill="x", padx=0, pady=(0, 5))
        
        self.p_icon = ctk.CTkFrame(self.p_user_frame, width=30, height=30, corner_radius=15, fg_color="#DDD")
        self.p_icon.pack(side="left")
        self.p_store_name = ctk.CTkLabel(self.p_user_frame, text="Store_Name", font=("Arial", 12, "bold"))
        self.p_store_name.pack(side="left", padx=10)
        
        # Image
        self.p_image_label = ctk.CTkLabel(self.p_content_area, text="NO IMAGE", fg_color="#F0F0F0", width=265, height=265, corner_radius=0)
        self.p_image_label.pack(fill="x")
        
        # Bottom controls
        ctrl_frame = ctk.CTkFrame(self.p_content_area, fg_color="white", height=30)
        ctrl_frame.pack(fill="x", padx=0, pady=5)
        ctk.CTkLabel(ctrl_frame, text="♡ 💬 ➤", font=("Arial", 16), text_color="#333").pack(anchor="w")
        
        # Caption (Maximize text area)
        self.p_caption = ctk.CTkTextbox(self.p_content_area, font=("M PLUS Rounded 1c", 12), text_color="#333", fg_color="transparent", wrap="word", height=280)
        self.p_caption.pack(fill="both", padx=0, pady=0)
        self.p_caption.insert("0.0", "リストを選択すると、ここにプレビューが表示されます。")
        self.p_caption.configure(state="disabled")
        
        # Home Bar
        home_bar = ctk.CTkFrame(self.phone_frame, fg_color="#333", width=100, height=5, corner_radius=2)
        home_bar.place(relx=0.5, rely=0.98, anchor="s")

        self.reload_all()

    def open_ai_generator(self):
        def on_done():
            self.reload_all()
        from views.ai_generator import AIGeneratorModal
        AIGeneratorModal(self, self.db, on_save_callback=on_done, for_selection=False)

    def import_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not filename: return
        
        # Ask for store assignment override or use CSV value
        current_store_filter = self.store_filter_var.get()
        target_store = None
        if current_store_filter != "全店舗データのサマリ":
             if messagebox.askyesno("確認", f"現在選択中の店舗 '{current_store_filter}' として取り込みますか？\n(いいえを選択すると、CSV内の店舗名を使用します)"):
                 target_store = current_store_filter
        
        success, msg = self.db.import_schedules_from_csv(filename, store_name_arg=target_store)
        if success:
            messagebox.showinfo("成功", msg)
            self.reload_all()
        else:
            messagebox.showerror("エラー", msg)

    def open_store_management(self):
        top = ctk.CTkToplevel(self)
        top.title("店舗管理")
        top.geometry("400x500")
        
        # List
        ctk.CTkLabel(top, text="登録済み店舗一覧", font=("M PLUS Rounded 1c", 14, "bold")).pack(pady=10)
        
        list_frame = ctk.CTkScrollableFrame(top, height=200)
        list_frame.pack(fill="x", padx=20)
        
        self.store_vars = {} # map id to var (if needed) or just widgets
        
        def refresh_list():
            for w in list_frame.winfo_children(): w.destroy()
            stores = self.db.fetch_stores(self.client_id)
            for s in stores:
                row = ctk.CTkFrame(list_frame, fg_color="transparent")
                row.pack(fill="x", pady=2)
                ctk.CTkLabel(row, text=s['name'], anchor="w").pack(side="left", padx=5)
                
                def delete_action(sid=s['id'], sname=s['name']):
                    self.confirm_delete_store(sid, sname, top, refresh_list)
                    
                ctk.CTkButton(row, text="削除", width=60, fg_color="#FFCDD2", text_color="#C62828", 
                              hover_color="#EF9A9A", command=delete_action).pack(side="right", padx=5)

        refresh_list()
        
        # Add New
        ctk.CTkLabel(top, text="新規店舗追加", font=("M PLUS Rounded 1c", 12, "bold")).pack(pady=(20, 5))
        entry_new = ctk.CTkEntry(top, placeholder_text="店舗名を入力")
        entry_new.pack(pady=5)
        
        def add_action():
            name = entry_new.get().strip()
            if name:
                self.db.add_store(self.client_id, name)
                entry_new.delete(0, "end")
                refresh_list()
                self.reload_all()
        
        ctk.CTkButton(top, text="追加", command=add_action, **BUTTON_CONFIG).pack(pady=10)
        ctk.CTkButton(top, text="閉じる", width=100, fg_color="transparent", border_width=1, border_color="#CCC", text_color="#333", hover_color="#EEE", command=top.destroy).pack(pady=(0, 20))

    def confirm_delete_store(self, store_id, store_name, parent, refresh_cb):
        dialog = ctk.CTkInputDialog(text=f"店舗 '{store_name}' を削除しますか？\n確認のため「削除」と入力してください。", title="削除確認")
        res = dialog.get_input()
        if res == "削除":
            self.db.delete_store(store_id)
            refresh_cb()
            self.reload_all()
        elif res is not None:
             messagebox.showerror("エラー", "入力が正しくありません")

    def reload_all(self):
        # Update combo values first
        stores_data = self.db.fetch_stores(self.client_id)
        store_names = [s['name'] for s in stores_data]
        
        current = self.store_filter_var.get()
        values = ["全店舗データのサマリ"] + store_names
        self.store_combo.configure(values=values)
        if current not in values:
            self.store_filter_var.set("全店舗データのサマリ")
            
        self.load_data()

    def filter_changed(self, choice):
        self.load_data()

    def open_add_schedule_modal(self):
        top = ctk.CTkToplevel(self)
        top.title("スケジュール手動追加")
        top.geometry("400x500")
        
        # 1. Date
        ctk.CTkLabel(top, text="投稿日").pack(pady=(20, 5))
        btn_date = DatePickerButton(top, width=200)
        btn_date.pack(pady=5)
        
        # 2. Time
        ctk.CTkLabel(top, text="投稿時間").pack(pady=5)
        btn_time = TimePickerButton(top, width=200)
        btn_time.pack(pady=5)
        
        # 3. Store
        ctk.CTkLabel(top, text="店舗").pack(pady=5)
        stores = self.db.fetch_stores(self.client_id)
        store_map = {s['name']: s['id'] for s in stores}
        store_names = list(store_map.keys())
        store_combo = ctk.CTkComboBox(top, values=store_names)
        if store_names: store_combo.set(store_names[0])
        store_combo.pack(pady=5)

        # 4. Type
        ctk.CTkLabel(top, text="投稿種別").pack(pady=5)
        type_combo = ctk.CTkComboBox(top, values=["フィード", "リール"])
        type_combo.pack(pady=5)
        
        def save():
            date_val = btn_date.get_date()
            time_val = btn_time.get_time()
            store_name = store_combo.get()
            post_type = type_combo.get()
            
            store_id = store_map.get(store_name)
            
            if not date_val:
                messagebox.showerror("エラー", "日付を選択してください")
                return
            
            if not time_val: time_val = ""

            # Call DB
            self.db.add_schedule(target_date=date_val, post_time=time_val, 
                                 store_name=store_name, post_type=post_type, 
                                 client_id=self.client_id, store_id=store_id)
            
            self.reload_all()
            top.destroy()

        btn_frame = ctk.CTkFrame(top, fg_color="transparent")
        btn_frame.pack(pady=30)
        ctk.CTkButton(btn_frame, text="追加", command=save, **BUTTON_CONFIG).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="キャンセル", width=100, fg_color="transparent", border_width=1, border_color="#CCC", text_color="#333", hover_color="#EEE", command=top.destroy).pack(side="left", padx=10)

    def load_data(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.btn_images.clear() 

        filter_val = self.store_filter_var.get()
        schedules = self.db.fetch_schedules(store_filter=filter_val, client_id=self.client_id)
        
        for idx, row in enumerate(schedules):
            self.create_row(idx, row)
            
        if schedules:
            self.update_preview(schedules[0])

    def create_row(self, idx, row):
        # Determine status value mapping
        raw_status = row['status'] if row.get('status') else "未対応"
        
        # Migration mapping
        status_map = {
            "未完了": "未対応",
            "未確認": "未対応",
            "OK": "投稿完了" 
        }
        status_val = status_map.get(raw_status, raw_status)

        # Background color logic (Subtle pastel colors)
        bg_colors = {
            "投稿完了": "#E6F4EA", # Subtle Green
            "投稿待ち": "#E1F5FE", # Subtle Blue
            "承認待ち": "#FFF3E0", # Subtle Orange
            "下書き": "#FFF8E1",   # Subtle Yellow
            "未対応": "transparent" 
        }
        bg_color = bg_colors.get(status_val, "transparent")
            
        row_frame = ctk.CTkFrame(self.scroll_frame, fg_color=bg_color, corner_radius=0)
        row_frame.pack(fill="x", pady=1, padx=0)
        
        # 0:Date(80), 1:Time(50), 2:Store(80), 3:Content(Exp), 4:Type(60), 5:Status(90), 6:Preview(40)
        row_frame.grid_columnconfigure(3, weight=1)
        
        def on_click(e=None):
            self.update_preview(row)
        
        row_frame.bind("<Button-1>", on_click)
        txt_font_main = ("M PLUS Rounded 1c", 12)
        txt_font_sub = ("M PLUS Rounded 1c", 11)
        
        # 1. Date
        # 1. Date
        try:
             dt = datetime.strptime(str(row['target_date']), "%Y-%m-%d")
             date_display = f"{dt.year}年{dt.month}月{dt.day}日"
        except ValueError:
             date_display = str(row['target_date'])
             
        ctk.CTkLabel(row_frame, text=date_display, width=120, anchor="w", 
                     font=txt_font_main, text_color="#333").grid(row=0, column=0, padx=5, sticky="w")
        
        # 2. Time
        post_time = row['post_time'] if row['post_time'] else "-"
        ctk.CTkLabel(row_frame, text=post_time, width=50, anchor="w", 
                     font=txt_font_sub, text_color="#555").grid(row=0, column=1, padx=5, sticky="w")
        
        # 3. Store
        store_display = str(row['store_name'])
        if len(store_display) > 8: store_display = store_display[:8] + "..."
        ctk.CTkLabel(row_frame, text=store_display, width=80, anchor="w", 
                     font=txt_font_sub, text_color="#555").grid(row=0, column=2, padx=5, sticky="w")
        
        # 4. Content (Image + Text)
        content_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        content_frame.grid(row=0, column=3, padx=5, sticky="ew")
        
        btn_fg = "transparent"
        text_col = "#999"
        display_text = "＋ 素材を追加"
        button_image = None
        
        has_content = (row['image_id'] or row['text_id'])
        
        try:
            placeholder = Image.new('RGBA', (30, 30), (0, 0, 0, 0))
            ctk_placeholder = ctk.CTkImage(placeholder, size=(30, 30))
            self.btn_images.append(ctk_placeholder)
        except:
            ctk_placeholder = None
        
        if has_content:
            text_col = "#333"
            
            txt_part = "(テキスト未設定)"
            if row['text_content']:
                 raw = row['text_content'].replace('\n', ' ')
                 if len(raw) > 40: raw = raw[:40] + "..."
                 txt_part = raw
            
            if row['file_path']:
                fpath = row['file_path']
                if fpath in self.thumbnail_cache:
                    button_image = self.thumbnail_cache[fpath]
                    display_text = f"  {txt_part}"
                else:
                    try:
                        img = Image.open(fpath).convert("RGBA")
                        img = ImageOps.pad(img, (80, 80), method=Image.Resampling.LANCZOS, color=(255, 255, 255, 0))
                        ctk_thumb = ctk.CTkImage(img, size=(30, 30))
                        self.thumbnail_cache[fpath] = ctk_thumb
                        button_image = ctk_thumb
                        display_text = f"  {txt_part}" 
                    except:
                        button_image = ctk_placeholder
                        display_text = f"📷(Error) {txt_part}"
            else:
                 button_image = ctk_placeholder
                 display_text = f"  {txt_part}"
        else:
             button_image = ctk_placeholder

        btn_edit = ctk.CTkButton(content_frame, text=display_text, 
                                 image=button_image, compound="left",
                                 font=txt_font_main,
                                 fg_color="transparent", hover_color="#F1F3F4",
                                 text_color=text_col,
                                 height=36, corner_radius=5,
                                 anchor="w", 
                                 command=lambda r=row: self.open_builder(r))
        btn_edit.pack(fill="both") 
        
        # 5. Type
        post_type = row['post_type'] if row['post_type'] else "-"
        ctk.CTkLabel(row_frame, text=post_type, width=60, anchor="w", 
                     font=txt_font_sub, text_color="#777").grid(row=0, column=4, padx=5, sticky="w")
        
        # 6. Status
        def toggle_status():
            curr = status_val
            flow = ["未対応", "下書き", "承認待ち", "投稿待ち", "投稿完了"]
            try:
                idx = flow.index(curr)
                nex = flow[(idx + 1) % len(flow)]
            except ValueError:
                nex = "未対応" 
            
            self.db.update_status(row['id'], nex)
            self.reload_all()

        st_fg = "#EEE"
        st_text_col = "#333"
        
        status_colors = {
            "投稿完了": "#43A047", 
            "投稿待ち": "#039BE5", 
            "承認待ち": "#FB8C00", 
            "下書き": "#FDD835",
            "未対応": "#EEEEEE"
        }
        st_bg = status_colors.get(status_val, "#EEE")
        if status_val in ["投稿完了", "投稿待ち", "承認待ち"]: st_text_col = "white"
        if status_val == "未対応": st_text_col = "#777"

        btn_status = ctk.CTkButton(row_frame, text=status_val, width=80, height=24,
                                   fg_color=st_bg, hover_color=st_bg,
                                   text_color=st_text_col,
                                   font=("M PLUS Rounded 1c", 10, "bold"),
                                   command=toggle_status)
        btn_status.grid(row=0, column=5, padx=5)

        # 7. Preview Button
        ctk.CTkButton(row_frame, text="👁", width=30, height=24,
                                    fg_color="#F1F3F4", hover_color="#E0E0E0", text_color="#555",
                                    command=lambda r=row: self.update_preview(r)).grid(row=0, column=6, padx=5)

    def open_builder(self, row):
        def on_save(img_id, txt_id):
            self.db.update_schedule_link(row['id'], image_id=img_id, text_id=txt_id)
            self.load_data()
            
        PostBuilderModal(self, self.db, row['id'], row['image_id'], row['text_id'], on_save)
            
    def update_preview(self, row):
        self.p_store_name.configure(text=row['store_name'])
        
        if row['file_path'] and row['image_id']:
            try:
                img = Image.open(row['file_path'])
                w, h = img.size
                min_dim = min(w, h)
                img = img.crop(((w-min_dim)/2, (h-min_dim)/2, (w+min_dim)/2, (h+min_dim)/2))
                img.thumbnail((280, 280))
                self.current_preview_image = ctk.CTkImage(img, size=(280, 280))
                self.p_image_label.configure(image=self.current_preview_image, text="")
            except:
                 self.p_image_label.configure(image=None, text="Error")
        else:
             self.p_image_label.configure(image=None, text="NO IMAGE")

        self.p_caption.configure(state="normal")
        self.p_caption.delete("0.0", "end")
        if row['text_content']:
            self.p_caption.insert("0.0", f"{row['text_content']}")
        else:
             self.p_caption.insert("0.0", "（テキスト未設定）")
        self.p_caption.configure(state="disabled")

    def restart_app(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
