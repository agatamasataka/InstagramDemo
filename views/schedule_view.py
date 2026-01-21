import customtkinter as ctk
from database import DatabaseManager
from theme import BrandColors, BUTTON_CONFIG, HEADER_LABEL_CONFIG, SUBHEADER_CONFIG
from views.components import SelectionModal
from views.post_builder import PostBuilderModal
from PIL import Image
from tkinter import filedialog, messagebox

class ScheduleView(ctk.CTkFrame):
    def __init__(self, master, db: DatabaseManager, client_id):
        super().__init__(master, fg_color=BrandColors.BG_LIGHT_MAIN)
        self.db = db
        self.client_id = client_id
        self.current_preview_image = None
        self.btn_images = [] 
        
        # Grid Configuration
        self.grid_columnconfigure(0, weight=3) # List Area
        self.grid_columnconfigure(1, weight=1) # Preview Area
        self.grid_rowconfigure(1, weight=1)

        # === LEFT COLUMN: LIST ===
        self.left_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.left_panel.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))
        self.left_panel.grid_columnconfigure(0, weight=1)
        self.left_panel.grid_rowconfigure(2, weight=1)

        # 1. Header Area
        self.header_frame = ctk.CTkFrame(self.left_panel, fg_color=BrandColors.BG_WHITE, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="進行管理ダッシュボード", **HEADER_LABEL_CONFIG)
        self.title_label.pack(side="left", padx=30, pady=20)
        
        # Store Filter (New!)
        self.store_filter_var = ctk.StringVar(value="全店舗データのサマリ")
        self.store_combo = ctk.CTkComboBox(self.header_frame, 
                                           values=["全店舗データのサマリ"],
                                           command=self.filter_changed,
                                           variable=self.store_filter_var,
                                           width=200, font=("M PLUS Rounded 1c", 13))
        self.store_combo.pack(side="left", padx=10, pady=20)

        # Store Config Button
        self.config_btn = ctk.CTkButton(self.header_frame, text="⚙️ 店舗管理", command=self.open_store_management, width=100,
                                        fg_color="transparent", border_width=1, border_color="#CCC", text_color="#333", hover_color="#EEE",
                                        font=("M PLUS Rounded 1c", 12))
        self.config_btn.pack(side="left", padx=5)

        # Add Schedule Button
        self.add_btn = ctk.CTkButton(self.header_frame, text="➕ スケジュール追加", command=self.open_add_schedule_modal, width=160, 
                                        fg_color="#333", hover_color="black", font=("M PLUS Rounded 1c", 12, "bold"), height=32)
        self.add_btn.pack(side="right", padx=(5, 30), pady=20)

        self.refresh_btn = ctk.CTkButton(self.header_frame, text="更新", command=self.reload_all, width=80, **BUTTON_CONFIG)
        self.refresh_btn.configure(fg_color=BrandColors.PRIMARY)
        self.refresh_btn.pack(side="right", padx=5, pady=20)

        # 2. View Headers
        self.col_header_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.col_header_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=(20, 5))
        
        headers = ["日付", "投稿時間", "店舗名", "投稿内容 (サムネイル+本文)", "種別", "ステータス"]
        widths = [90, 60, 80, 400, 80, 60] 
        
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(self.col_header_frame, text=header, width=widths[i], anchor="w", 
                                 font=("M PLUS Rounded 1c", 11, "bold"), text_color="gray60")
            label.grid(row=0, column=i, padx=5, sticky="w")
            
        self.col_header_frame.grid_columnconfigure(3, weight=1)

        # 3. List
        self.scroll_frame = ctk.CTkScrollableFrame(self.left_panel, fg_color=BrandColors.BG_WHITE, corner_radius=15)
        self.scroll_frame.grid(row=2, column=0, sticky="nsew", padx=30, pady=(0, 30))
        self.scroll_frame.grid_columnconfigure(2, weight=1) # Content column expands

        # === RIGHT COLUMN: PREVIEW ===
        self.right_panel = ctk.CTkFrame(self, fg_color=BrandColors.BG_WHITE, corner_radius=0, width=350)
        self.right_panel.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=0, pady=0)
        self.right_panel.pack_propagate(False) 
        
        ctk.CTkLabel(self.right_panel, text="即時プレビュー", font=("M PLUS Rounded 1c", 16, "bold"), text_color=BrandColors.PRIMARY).pack(pady=(30, 10))
        
        self.phone_frame = ctk.CTkFrame(self.right_panel, fg_color="white", width=300, height=550, border_width=2, border_color="#EEE", corner_radius=20)
        self.phone_frame.pack(pady=10, padx=20)
        self.phone_frame.pack_propagate(False)
        
        self.p_user_frame = ctk.CTkFrame(self.phone_frame, fg_color="white", height=50)
        self.p_user_frame.pack(fill="x", padx=10, pady=10)
        
        self.p_icon = ctk.CTkFrame(self.p_user_frame, width=30, height=30, corner_radius=15, fg_color="#DDD")
        self.p_icon.pack(side="left")
        self.p_store_name = ctk.CTkLabel(self.p_user_frame, text="Store_Name", font=("Arial", 12, "bold"))
        self.p_store_name.pack(side="left", padx=10)
        
        self.p_image_label = ctk.CTkLabel(self.phone_frame, text="NO IMAGE", fg_color="#F0F0F0", width=280, height=280, corner_radius=0)
        self.p_image_label.pack(fill="x")
        
        self.p_caption = ctk.CTkTextbox(self.phone_frame, font=("M PLUS Rounded 1c", 12), text_color="#333", fg_color="transparent", wrap="word", height=150)
        self.p_caption.pack(fill="both", padx=10, pady=5)
        self.p_caption.insert("0.0", "リストを選択すると、ここにプレビューが表示されます。")
        self.p_caption.configure(state="disabled")

        self.reload_all()

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
        top.geometry("400x450")
        
        # 1. Date
        ctk.CTkLabel(top, text="投稿日 (YYYY-MM-DD)").pack(pady=(20, 5))
        entry_date = ctk.CTkEntry(top)
        entry_date.pack(pady=5)
        
        # 2. Time
        ctk.CTkLabel(top, text="投稿時間 (HH:MM)").pack(pady=5)
        entry_time = ctk.CTkEntry(top)
        entry_time.pack(pady=5)
        
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
        type_combo = ctk.CTkComboBox(top, values=["フィード", "リール", "ストーリーズ"])
        type_combo.pack(pady=5)
        
        def save():
            date_val = entry_date.get().strip()
            time_val = entry_time.get().strip()
            store_name = store_combo.get()
            post_type = type_combo.get()
            
            store_id = store_map.get(store_name)
            
            if not date_val:
                messagebox.showerror("エラー", "日付を入力してください")
                return

            # Call DB
            self.db.add_schedule(target_date=date_val, post_time=time_val, 
                                 store_name=store_name, post_type=post_type, 
                                 client_id=self.client_id, store_id=store_id)
            
            self.reload_all()
            top.destroy()

        ctk.CTkButton(top, text="追加", command=save, **BUTTON_CONFIG).pack(pady=30)

    def load_data(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.btn_images.clear() 

        filter_val = self.store_filter_var.get()
        schedules = self.db.fetch_schedules(store_filter=filter_val, client_id=self.client_id)
        
        for idx, row in enumerate(schedules):
            self.create_row(idx, row)

    def create_row(self, idx, row):
        status_check = self.db.get_status_check(row['image_id'], row['text_id'])
        bg_color = "#E0F7FA" if status_check == "OK" else "transparent"
            
        row_frame = ctk.CTkFrame(self.scroll_frame, fg_color=bg_color, corner_radius=8)
        row_frame.pack(fill="x", pady=4, padx=5)
        
        # Grid layout for row items
        # 0: Date, 1: Time, 2: Store, 3: Content (Image+Text), 4: Type, 5: Status
        row_frame.grid_columnconfigure(3, weight=1)
        
        def on_click(e=None):
            self.update_preview(row)
        
        row_frame.bind("<Button-1>", on_click)
        txt_font = ("M PLUS Rounded 1c", 13)
        
        # 1. Date
        l_date = ctk.CTkLabel(row_frame, text=str(row['target_date']), width=90, anchor="w", font=txt_font)
        l_date.grid(row=0, column=0, padx=5)
        l_date.bind("<Button-1>", on_click)
        
        # 2. Time
        post_time = row['post_time'] if row['post_time'] else ""
        l_time = ctk.CTkLabel(row_frame, text=post_time, width=60, anchor="center", font=txt_font)
        l_time.grid(row=0, column=1, padx=5)
        l_time.bind("<Button-1>", on_click)

        # 3. Store
        store_display = str(row['store_name'])
        if len(store_display) > 10: store_display = store_display[:10] + "..."
        l_store = ctk.CTkLabel(row_frame, text=store_display, width=80, anchor="w", font=txt_font)
        l_store.grid(row=0, column=2, padx=5)
        l_store.bind("<Button-1>", on_click)
        
        # 4. Content (Image + Text)
        content_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        content_frame.grid(row=0, column=3, padx=10, sticky="ew")
        
        btn_fg = "#F0F0F0"
        text_col = "gray"
        display_text = "＋ 素材を追加して投稿を作成"
        button_image = None
        
        has_content = (row['image_id'] or row['text_id'])

        # Placeholder for alignment
        try:
            placeholder = Image.new('RGBA', (35, 35), (0, 0, 0, 0))
            ctk_placeholder = ctk.CTkImage(placeholder, size=(35, 35))
            self.btn_images.append(ctk_placeholder)
        except:
            ctk_placeholder = None
        
        if has_content:
            btn_fg = "white"
            text_col = "#333" if status_check == "OK" else "#555"
            
            txt_part = "(テキスト未設定)"
            if row['text_content']:
                 raw = row['text_content'].replace('\n', ' ')
                 if len(raw) > 25: raw = raw[:25] + "..."
                 txt_part = f"📝 {raw}"
            
            if row['file_path']:
                try:
                    img = Image.open(row['file_path'])
                    img.thumbnail((50, 50)) 
                    ctk_thumb = ctk.CTkImage(img, size=(35, 35))
                    self.btn_images.append(ctk_thumb) 
                    button_image = ctk_thumb
                    display_text = f"  {txt_part}" 
                except:
                     # Error case
                    button_image = ctk_placeholder
                    display_text = f"📷(Error)  {txt_part}"
            else:
                 # Text only -> use placeholder for alignment
                 button_image = ctk_placeholder
                 display_text = f"  {txt_part}"

        btn_edit = ctk.CTkButton(content_frame, text=display_text, 
                                 image=button_image, compound="left",
                                 font=("M PLUS Rounded 1c", 12, "normal"),
                                 fg_color=btn_fg, hover_color="#E0E0E0",
                                 text_color=text_col,
                                 height=45, corner_radius=10,
                                 anchor="w", 
                                 command=lambda: self.open_builder(row))
        btn_edit.pack(fill="both") 

        # 5. Type
        post_type = row['post_type'] if row['post_type'] else "-"
        l_type = ctk.CTkLabel(row_frame, text=post_type, width=80, anchor="center", font=txt_font, text_color="gray")
        l_type.grid(row=0, column=4, padx=5)
        
        # 6. Status
        status_text = "OK" if status_check == "OK" else "ー"
        status_color = BrandColors.PRIMARY if status_check == "OK" else "#F0F0F0"
        
        ctk.CTkLabel(row_frame, text=status_text, width=60, corner_radius=10, 
                     fg_color=status_color, text_color="white" if status_check=="OK" else "gray"
                     ).grid(row=0, column=5, padx=10)

        # 7. Preview Button (New)
        btn_preview = ctk.CTkButton(row_frame, text="👁️", width=40, height=30,
                                    fg_color="#EEE", hover_color="#DDD", text_color="#333",
                                    command=lambda: self.update_preview(row))
        btn_preview.grid(row=0, column=6, padx=10)




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
