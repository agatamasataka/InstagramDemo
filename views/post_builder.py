import customtkinter as ctk
from PIL import Image
from theme import BrandColors, BUTTON_CONFIG

class PostBuilderModal(ctk.CTkToplevel):
    def __init__(self, master, db, schedule_id, current_img_id, current_txt_id, on_save):
        super().__init__(master)
        self.db = db
        self.schedule_id = schedule_id
        self.selected_img_id = current_img_id
        self.selected_txt_id = current_txt_id
        self.on_save = on_save
        
        # Image Cache to prevent GC
        self.image_refs = [] # For list items
        self.preview_image_ref = None # For preview area
        
        self.title("投稿を作成・編集")
        self.geometry("1400x800")
        self.after(100, self.lift)
        self.configure(fg_color=BrandColors.BG_LIGHT_MAIN)
        
        # Grid Layout: | Images (Left) | Texts (Center) | Preview (Right) |
        self.grid_columnconfigure(0, weight=4) # Images
        self.grid_columnconfigure(1, weight=4) # Texts
        self.grid_columnconfigure(2, weight=3) # Preview
        self.grid_rowconfigure(0, weight=1)

        # === 1. IMAGE SELECTION (Left) ===
        self.frame_img = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        self.frame_img.grid(row=0, column=0, sticky="nsew", padx=1, pady=0)
        
        ctk.CTkLabel(self.frame_img, text="📷 画像を選択", font=("M PLUS Rounded 1c", 16, "bold"), text_color=BrandColors.PRIMARY).pack(pady=10)
        
        self.img_tabs = ctk.CTkSegmentedButton(self.frame_img, values=["すべて", "写真", "イラスト"], command=self.filter_images)
        self.img_tabs.set("すべて")
        self.img_tabs.pack(pady=5, padx=10)

        self.scroll_img = ctk.CTkScrollableFrame(self.frame_img, fg_color="transparent")
        self.scroll_img.pack(fill="both", expand=True, padx=10, pady=10)
        
        # === 2. TEXT SELECTION (Center) ===
        self.frame_txt = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        self.frame_txt.grid(row=0, column=1, sticky="nsew", padx=1, pady=0)
        
<<<<<<< HEAD
        ctk.CTkLabel(self.frame_txt, text="📝 テキストを選択", font=("M PLUS Rounded 1c", 16, "bold"), text_color=BrandColors.PRIMARY).pack(pady=10)
        
=======
        ctk.CTkLabel(self.frame_txt, text="📝 テキストを選択", font=("M PLUS Rounded 1c", 16, "bold"), text_color=BrandColors.PRIMARY).pack(pady=(10, 5))
        ctk.CTkButton(self.frame_txt, text="✨ AIで生成する", command=self.open_ai_generator,
                      width=120, height=28, fg_color="#E0F7FA", text_color="#006064", hover_color="#B2EBF2",
                      font=("M PLUS Rounded 1c", 12, "bold")).pack(pady=(0, 10))
                      

>>>>>>> c5d2c25d7640490051c0d591eb838e91fa43e32b
        genres = ["すべて"] + list(set([t['genre'] for t in self.db.fetch_texts() if t['genre']]))
        if len(genres) > 5: genres = genres[:5]
        
        self.txt_tabs = ctk.CTkSegmentedButton(self.frame_txt, values=genres, command=self.filter_texts)
        self.txt_tabs.set("すべて")
        self.txt_tabs.pack(pady=5, padx=10)

        self.scroll_txt = ctk.CTkScrollableFrame(self.frame_txt, fg_color="transparent")
        self.scroll_txt.pack(fill="both", expand=True, padx=10, pady=10)

        # === 3. PREVIEW & ACTIONS (Right) ===
        self.frame_prev = ctk.CTkFrame(self, fg_color="#F9F9F9", corner_radius=0)
        self.frame_prev.grid(row=0, column=2, sticky="nsew", padx=0, pady=0)
        
        ctk.CTkLabel(self.frame_prev, text="投稿プレビュー", font=("M PLUS Rounded 1c", 16, "bold"), text_color="gray").pack(pady=20)
        
        self.phone = ctk.CTkFrame(self.frame_prev, fg_color="white", width=280, height=450, corner_radius=20, border_color="#DDD", border_width=2)
        self.phone.pack(pady=10)
        self.phone.pack_propagate(False)
        
        self.p_img_lbl = ctk.CTkLabel(self.phone, text="NO IMAGE", fg_color="#EEE", width=260, height=260)
        self.p_img_lbl.pack(pady=10)
        
        self.p_txt_box = ctk.CTkTextbox(self.phone, height=150, fg_color="transparent", font=("M PLUS Rounded 1c", 11), text_color="#333", wrap="word")
        self.p_txt_box.pack(fill="both", padx=10)
        
<<<<<<< HEAD
        self.btn_save = ctk.CTkButton(self.frame_prev, text="この内容で決定", font=("M PLUS Rounded 1c", 16, "bold"), 
                                      height=50, fg_color=BrandColors.PRIMARY, hover_color=BrandColors.CTA_HOVER,
                                      command=self.save_and_close)
        self.btn_save.pack(side="bottom", fill="x", padx=20, pady=30)
=======
        # Actions
        action_frame = ctk.CTkFrame(self.frame_prev, fg_color="transparent")
        action_frame.pack(side="bottom", fill="x", padx=20, pady=30)
        
        self.btn_save = ctk.CTkButton(action_frame, text="この内容で決定", font=("M PLUS Rounded 1c", 16, "bold"), 
                                      height=50, fg_color=BrandColors.PRIMARY, hover_color=BrandColors.CTA_HOVER,
                                      command=self.save_and_close)
        self.btn_save.pack(side="top", fill="x", pady=(0, 10))
        
        ctk.CTkButton(action_frame, text="キャンセル", font=("M PLUS Rounded 1c", 14), 
                      height=40, fg_color="transparent", border_width=1, border_color="#CCC", 
                      text_color="#555", hover_color="#EEE",
                      command=self.destroy).pack(side="top", fill="x")
>>>>>>> c5d2c25d7640490051c0d591eb838e91fa43e32b

        self.all_images = self.db.fetch_images()
        self.all_texts = self.db.fetch_texts()
        
        self.populate_images()
        self.populate_texts()
        self.update_preview()

    def filter_images(self, value):
        self.populate_images()

    def filter_texts(self, value):
        self.populate_texts(filter_genre=None if value=="すべて" else value)

    def populate_images(self):
        for w in self.scroll_img.winfo_children(): w.destroy()
        self.image_refs.clear() # Clear specific list cache
        
        cols = 3
        for i, item in enumerate(self.all_images):
            r = i // cols
            c = i % cols
            self.create_img_card(item, r, c)

    def create_img_card(self, item, r, c):
        is_selected = (item['id'] == self.selected_img_id)
        border_col = BrandColors.PRIMARY if is_selected else "#EEE"
        bg_col = "#E0F7FA" if is_selected else "white"
        
        card = ctk.CTkFrame(self.scroll_img, fg_color=bg_col, border_width=2, border_color=border_col)
        card.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
        
        def select():
            self.selected_img_id = item['id']
            self.populate_images() 
            self.update_preview()
            
        card.bind("<Button-1>", lambda e: select())
        
        try:
            img = Image.open(item['file_path'])
            img.thumbnail((100, 100))
            ctk_img = ctk.CTkImage(img, size=img.size)
            self.image_refs.append(ctk_img) # KEEP REF
            
            l = ctk.CTkLabel(card, image=ctk_img, text="")
            l.pack(pady=5)
            l.bind("<Button-1>", lambda e: select())
        except:
            l = ctk.CTkLabel(card, text="No Img")
            l.pack(pady=20)
            l.bind("<Button-1>", lambda e: select())
            
        if is_selected:
            ctk.CTkLabel(card, text="✔ 選択中", font=("M PLUS Rounded 1c", 10, "bold"), text_color=BrandColors.PRIMARY).pack(pady=2)

    def populate_texts(self, filter_genre=None):
        for w in self.scroll_txt.winfo_children(): w.destroy()
        
        items = self.all_texts
        if filter_genre:
            items = [t for t in items if t['genre'] == filter_genre]
            
        for i, item in enumerate(items):
            self.create_txt_card(item, i)

    def create_txt_card(self, item, idx):
        is_selected = (item['id'] == self.selected_txt_id)
        border_col = BrandColors.PRIMARY if is_selected else "#EEE"
        bg_col = "#E0F7FA" if is_selected else "white"
        
        card = ctk.CTkFrame(self.scroll_txt, fg_color=bg_col, border_width=2, border_color=border_col, height=80)
        card.pack(fill="x", padx=5, pady=5)
        
        def select():
            self.selected_txt_id = item['id']
            self.populate_texts(self.txt_tabs.get() if self.txt_tabs.get() != "すべて" else None)
            self.update_preview()

        card.bind("<Button-1>", lambda e: select())
        
        genre = item['genre'] if item['genre'] else "未分類"
        ctk.CTkLabel(card, text=f"【{genre}】", font=("M PLUS Rounded 1c", 11, "bold"), text_color="gray").pack(anchor="w", padx=10, pady=(5,0))
        
        content = item['content'][:60].replace("\n", " ") + "..."
        l = ctk.CTkLabel(card, text=content, anchor="w", justify="left", font=("M PLUS Rounded 1c", 12))
        l.pack(fill="x", padx=10, pady=5)
        l.bind("<Button-1>", lambda e: select())

        if is_selected:
            ctk.CTkLabel(card, text="✔ 選択中", font=("M PLUS Rounded 1c", 10, "bold"), text_color=BrandColors.PRIMARY).pack(anchor="e", padx=10)

    def update_preview(self):
        sel_img = next((i for i in self.all_images if i['id'] == self.selected_img_id), None)
        sel_txt = next((t for t in self.all_texts if t['id'] == self.selected_txt_id), None)
        
        if sel_img:
            try:
                img = Image.open(sel_img['file_path'])
                img.thumbnail((260, 260))
                ctk_img = ctk.CTkImage(img, size=img.size)
                self.preview_image_ref = ctk_img # KEEP REF
                
                self.p_img_lbl.configure(image=ctk_img, text="")
            except:
                self.p_img_lbl.configure(image=None, text="Error")
        else:
             self.p_img_lbl.configure(image=None, text="NO IMAGE")
             
        self.p_txt_box.configure(state="normal")
        self.p_txt_box.delete("0.0", "end")
        if sel_txt:
            self.p_txt_box.insert("0.0", sel_txt['content'])
        self.p_txt_box.configure(state="disabled")

    def save_and_close(self):
        if self.on_save:
            self.on_save(self.selected_img_id, self.selected_txt_id)
        self.destroy()
<<<<<<< HEAD
=======

    def open_ai_generator(self):
        def on_generated():
             # Reload texts
             self.all_texts = self.db.fetch_texts()
             self.populate_texts()
             
             # Select the latest text (Auto-apply)
             try:
                 cursor = self.db.conn.cursor()
                 latest = cursor.execute("SELECT id, content FROM texts ORDER BY id DESC LIMIT 1").fetchone()
                 if latest:
                     self.selected_txt_id = latest[0]
                     self.populate_texts(self.txt_tabs.get() if self.txt_tabs.get() != "すべて" else None)
                     self.update_preview()
             except:
                 pass

        from views.ai_generator import AIGeneratorModal
        AIGeneratorModal(self, self.db, on_save_callback=on_generated, for_selection=True)
>>>>>>> c5d2c25d7640490051c0d591eb838e91fa43e32b
