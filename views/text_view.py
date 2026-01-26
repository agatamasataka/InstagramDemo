import customtkinter as ctk
from database import DatabaseManager
from theme import BrandColors, BUTTON_CONFIG, HEADER_LABEL_CONFIG

class TextView(ctk.CTkFrame):
    def __init__(self, master, db: DatabaseManager, client_id):
        super().__init__(master, fg_color=BrandColors.BG_LIGHT_MAIN)
        self.db = db
        self.client_id = client_id
        self.current_store_id = None
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # 1. Header
        self.header_frame = ctk.CTkFrame(self, fg_color=BrandColors.BG_WHITE, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="テキスト管理", **HEADER_LABEL_CONFIG)
        self.title_label.pack(side="left", padx=30, pady=20)
        
        # Store Filter
        self.store_var = ctk.StringVar(value="店舗: フィルタなし")
        self.store_combo = ctk.CTkComboBox(self.header_frame, values=["店舗: フィルタなし"], 
                                           command=self.store_changed, variable=self.store_var, width=150)
        self.store_combo.pack(side="left", padx=10)
        self.load_stores()

        # Add Button
        self.add_btn = ctk.CTkButton(self.header_frame, text="+ 新規作成", command=self.open_add_modal, width=120, **BUTTON_CONFIG)
        self.add_btn.pack(side="right", padx=10)
        
        # Import CSV Button
        self.import_btn = ctk.CTkButton(self.header_frame, text="📄 CSV取込", command=self.import_csv, width=100, 
                                        fg_color="#333", hover_color="black", font=("M PLUS Rounded 1c", 12))
        self.import_btn.pack(side="right", padx=10)
        
        self.refresh_btn = ctk.CTkButton(self.header_frame, text="更新", command=self.load_data, width=80, 
                                         fg_color="transparent", text_color=BrandColors.PRIMARY, hover_color="#EEE", 
                                         font=("M PLUS Rounded 1c", 12, "bold"))
        self.refresh_btn.pack(side="right", padx=10)

        # 2. List Area
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color=BrandColors.BG_LIGHT_MAIN) # Transparent/Light bg for card list
        self.scroll_frame.grid(row=2, column=0, sticky="nsew", padx=30, pady=20)
        
        self.load_data()

    def load_stores(self):
        stores = self.db.fetch_stores(self.client_id)
        self.store_map = {s['name']: s['id'] for s in stores}
        values = ["店舗: フィルタなし"] + list(self.store_map.keys())
        self.store_combo.configure(values=values)

    def store_changed(self, choice):
        if choice in self.store_map:
            self.current_store_id = self.store_map[choice]
        else:
            self.current_store_id = None
        self.load_data()

    def load_data(self):
        for w in self.scroll_frame.winfo_children():
            w.destroy()
            
        texts = self.db.fetch_texts(client_id=self.client_id, store_id=self.current_store_id)
        
        # Display as cards
        cols = 2 # 2 columns for text cards
        
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        self.scroll_frame.grid_columnconfigure(1, weight=1)
        
        for i, item in enumerate(texts):
            r = i // cols
            c = i % cols
            self.create_card(item, r, c)

    def create_card(self, item, r, c):
        card = ctk.CTkFrame(self.scroll_frame, fg_color="white", corner_radius=15, border_width=1, border_color="#E0E0E0")
        card.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
        
        # Header: Genre + ID
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(15, 5))
        
        genre = item['genre'] if item['genre'] else "未分類"
        ctk.CTkLabel(header, text=genre, fg_color="#E0F7FA", text_color=BrandColors.PRIMARY, corner_radius=5, padx=5).pack(side="left")
        ctk.CTkLabel(header, text=f"ID: {item['id']}", text_color="gray").pack(side="right")
        
        # Content
        content_text = item['content']
        # Truncate for display if too long
        display_text = content_text
        if len(display_text) > 150:
            display_text = display_text[:150] + "..."
            
        lbl_content = ctk.CTkLabel(card, text=display_text, anchor="w", justify="left", wraplength=400, font=("M PLUS Rounded 1c", 13), text_color="#333")
        lbl_content.pack(fill="both", expand=True, padx=15, pady=5)
        
        # Actions
        actions = ctk.CTkFrame(card, fg_color="#FAFAFA", corner_radius=10, height=40)
        actions.pack(fill="x", padx=2, pady=2, side="bottom")
        
        # Copy Button
        btn_copy = ctk.CTkButton(actions, text="コピー", width=80, height=28, fg_color="white", text_color="#333", hover_color="#EEE", border_width=1, border_color="#DDD",
                                 command=lambda t=content_text: self.copy_to_clipboard(t))
        btn_copy.pack(side="right", padx=10, pady=5)

    def copy_to_clipboard(self, text):
        self.master.clipboard_clear()
        self.master.clipboard_append(text)
        print("Copied to clipboard")

    def import_csv(self):
        from tkinter import filedialog, messagebox
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            success, msg = self.db.import_texts_from_csv(file_path)
            if success:
                messagebox.showinfo("インポート成功", msg)
                self.load_data()
            else:
                messagebox.showerror("エラー", msg)

    def open_add_modal(self):
        # modal to add text
        top = ctk.CTkToplevel(self)
        top.title("新規テキスト作成")
        top.geometry("500x400")
        top.transient(self)
        top.grab_set()
        top.configure(fg_color="white")
        
        ctk.CTkLabel(top, text="ジャンル", font=("M PLUS Rounded 1c", 12, "bold"), text_color="gray").pack(anchor="w", padx=20, pady=(20, 5))
        entry_genre = ctk.CTkEntry(top, placeholder_text="例: キャンペーン, お知らせ")
        entry_genre.pack(fill="x", padx=20)
        
        ctk.CTkLabel(top, text="投稿本文", font=("M PLUS Rounded 1c", 12, "bold"), text_color="gray").pack(anchor="w", padx=20, pady=(15, 5))
        text_content = ctk.CTkTextbox(top, height=200)
        text_content.pack(fill="both", expand=True, padx=20)
        
        def save():
            genre = entry_genre.get()
            content = text_content.get("0.0", "end").strip()
            if content:
                self.db.add_text(content, genre, client_id=self.client_id, store_id=self.current_store_id)
                self.load_data()
                top.destroy()
                
        ctk.CTkButton(top, text="保存する", command=save, **BUTTON_CONFIG).pack(pady=20)
