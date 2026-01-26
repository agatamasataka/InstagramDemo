import customtkinter as ctk
from tkinterdnd2 import DND_FILES
from database import DatabaseManager
from PIL import Image
import os
import shutil
from theme import BrandColors, BUTTON_CONFIG, HEADER_LABEL_CONFIG
from views.text_view import TextView

class MaterialView(ctk.CTkFrame):
    def __init__(self, master, db: DatabaseManager, client_id):
        super().__init__(master, fg_color=BrandColors.BG_LIGHT_MAIN)
        self.db = db
        self.client_id = client_id
        self.images_cache = []
        self.current_store_id = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. Mode Switcher (Top)
        self.mode_frame = ctk.CTkFrame(self, fg_color=BrandColors.BG_WHITE, height=50, corner_radius=0)
        self.mode_frame.grid(row=0, column=0, sticky="ew")
        
        self.mode_label = ctk.CTkLabel(self.mode_frame, text="素材管理", **HEADER_LABEL_CONFIG)
        self.mode_label.pack(side="left", padx=30, pady=10)

        self.seg_btn = ctk.CTkSegmentedButton(self.mode_frame, values=["画像素材", "テキスト素材"],
                                              command=self.switch_mode, width=200)
        self.seg_btn.set("画像素材")
        self.seg_btn.pack(side="left", padx=20, pady=10)

        # 2. Content Area
        self.content_area = ctk.CTkFrame(self, fg_color="transparent")
        self.content_area.grid(row=1, column=0, sticky="nsew")
        self.content_area.grid_columnconfigure(0, weight=1)
        self.content_area.grid_rowconfigure(0, weight=1)

        # --- Image View Container ---
        self.frame_images = ctk.CTkFrame(self.content_area, fg_color="transparent")
        
        # Image Header (Store Filter etc)
        self.img_header = ctk.CTkFrame(self.frame_images, fg_color="transparent")
        self.img_header.pack(fill="x", padx=0, pady=0)
        
        self.store_var = ctk.StringVar(value="店舗: フィルタなし")
        self.store_combo = ctk.CTkComboBox(self.img_header, values=["店舗: フィルタなし"], 
                                           command=self.store_changed, variable=self.store_var, width=150)
        self.store_combo.pack(side="left", padx=30, pady=10)
        
        self.tag_entry = ctk.CTkEntry(self.img_header, placeholder_text="タグで検索...", width=150)
        self.tag_entry.pack(side="right", padx=(5, 30), pady=10)
        self.tag_entry.bind("<Return>", lambda e: self.search_tags())
        
        self.search_btn = ctk.CTkButton(self.img_header, text="🔍", width=40, command=self.search_tags, 
                                        fg_color="#333", hover_color="black")
        self.search_btn.pack(side="right", padx=5, pady=10)

        # Drop Zone
        self.drop_frame = ctk.CTkFrame(self.frame_images, fg_color="#F0F8FF", corner_radius=15, border_width=2, border_color=BrandColors.PRIMARY)
        self.drop_frame.pack(fill="x", padx=30, pady=(10, 10))
        self.drop_frame.pack_propagate(False)
        self.drop_frame.configure(height=100)

        self.lbl_drop = ctk.CTkLabel(self.drop_frame, text="📂 画像をドラッグ＆ドロップ または クリックして追加", 
                                     font=("M PLUS Rounded 1c", 14, "bold"), text_color=BrandColors.PRIMARY)
        self.lbl_drop.pack(expand=True, fill="both")

        try:
           self.drop_frame.drop_target_register(DND_FILES)
           self.drop_frame.dnd_bind('<<Drop>>', self.on_drop)
        except:
            pass
<<<<<<< HEAD
        self.lbl_drop.bind("<Button-1>", self.open_file_dialog)
        self.drop_frame.bind("<Button-1>", self.open_file_dialog)

=======
        self.drop_frame.bind("<Button-1>", self.open_file_dialog)

        # Import Folder Button
        self.btn_import_folder = ctk.CTkButton(self.frame_images, text="☁️ Google Drive等のフォルダから一括取り込み", 
                                               command=self.open_folder_import,
                                               height=36,
                                               fg_color="#FFF", border_width=1, border_color="#DDD",
                                               text_color="#333", hover_color="#F5F5F5",
                                               font=("M PLUS Rounded 1c", 12, "bold"))
        self.btn_import_folder.pack(fill="x", padx=30, pady=(5, 10))

>>>>>>> c5d2c25d7640490051c0d591eb838e91fa43e32b
        # Gallery
        self.scroll_frame = ctk.CTkScrollableFrame(self.frame_images, fg_color=BrandColors.BG_WHITE, corner_radius=15)
        self.scroll_frame.pack(fill="both", expand=True, padx=30, pady=10)

        # --- Text View Container ---
        # Instantiate TextView. It expects (master, db, client_id)
        # We pass self.content_area as master. But we want to control visibility manually.
        # Actually, let's instantiate it but only pack it when needed.
        self.text_view_instance = TextView(self.content_area, db, client_id)
        
        # Allow TextView to manage its own layout inside content_area.
        # But wait, TextView is a frame.

        # Initial Load
        self.load_stores()
        self.load_images()
        self.switch_mode("画像素材")

    def switch_mode(self, mode):
        if mode == "画像素材":
<<<<<<< HEAD
            self.text_view_instance.pack_forget()
=======
            self.text_view_instance.grid_forget()
>>>>>>> c5d2c25d7640490051c0d591eb838e91fa43e32b
            self.frame_images.grid(row=0, column=0, sticky="nsew")
        else:
            self.frame_images.grid_forget()
            self.text_view_instance.grid(row=0, column=0, sticky="nsew")

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
        self.load_images()

    def search_tags(self):
        query = self.tag_entry.get().strip()
        self.load_images(tag_filter=query)

    def on_drop(self, event):
        files = self.parse_drop_files(event.data)
        for f in files:
            self.register_image(f)
        self.load_images()

    def parse_drop_files(self, data):
        if isinstance(data, list): return data
        if "{" in data:
            import re
            return [f for f in re.findall(r'\{k(.*?)?\}', data)]
        return data.split()

    def open_file_dialog(self, event=None):
        from tkinter import filedialog
<<<<<<< HEAD
        file_paths = filedialog.askopenfilenames(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.gif")])
=======
        file_paths = filedialog.askopenfilenames(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.gif;*.webp")])
>>>>>>> c5d2c25d7640490051c0d591eb838e91fa43e32b
        if file_paths:
            for f in file_paths:
                self.register_image(f)
            self.load_images()

<<<<<<< HEAD
=======
    def open_folder_import(self):
        from tkinter import filedialog, messagebox
        folder_path = filedialog.askdirectory(title="取り込むフォルダ（Google Drive等）を選択")
        if not folder_path: return
        
        # Valid extensions
        exts = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
        
        files_to_import = []
        for root, dirs, files in os.walk(folder_path):
            for f in files:
                if os.path.splitext(f)[1].lower() in exts:
                    files_to_import.append(os.path.join(root, f))
        
        if not files_to_import:
            messagebox.showinfo("インポート", "画像ファイルが見つかりませんでした。")
            return
            
        if len(files_to_import) > 10:
            if not messagebox.askyesno("確認", f"{len(files_to_import)} 件の画像が見つかりました。\n取り込みますか？\n（ファイルのコピーに時間がかかる場合があります）"):
                return
        
        imported_count = 0
        for fpath in files_to_import:
            try:
                self.register_image(fpath)
                imported_count += 1
            except Exception as e:
                print(f"Skipped {fpath}: {e}")
                
        self.load_images()
        messagebox.showinfo("完了", f"{imported_count} 件の画像を取り込みました。")

>>>>>>> c5d2c25d7640490051c0d591eb838e91fa43e32b
    def register_image(self, file_path):
        file_path = file_path.strip('{}')
        if not os.path.exists(file_path): return

        assets_dir = os.path.join(os.getcwd(), "assets_store")
        os.makedirs(assets_dir, exist_ok=True)
        
        filename = os.path.basename(file_path)
        dest_path = os.path.join(assets_dir, filename)
        
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(dest_path):
            dest_path = os.path.join(assets_dir, f"{base}_{counter}{ext}")
            counter += 1
            
        shutil.copy2(file_path, dest_path)
        self.db.add_image(dest_path, client_id=self.client_id, store_id=self.current_store_id)

    def load_images(self, tag_filter=None):
        for w in self.scroll_frame.winfo_children():
            w.destroy()
        self.images_cache.clear()

        rows = self.db.fetch_images(tag_filter=tag_filter, client_id=self.client_id, store_id=self.current_store_id)
        cols = 5
        
        for i, row in enumerate(rows):
            r = i // cols
            c = i % cols
            self.create_image_card(row, r, c)

    def create_image_card(self, row, r, c):
        frame = ctk.CTkFrame(self.scroll_frame, fg_color=BrandColors.BG_LIGHT_MAIN, corner_radius=10)
        frame.grid(row=r, column=c, padx=10, pady=10)
        
        # ID Badge
        id_badge = ctk.CTkLabel(frame, text=f"ID: {row['id']}", font=("Arial", 12, "bold"), 
                                fg_color=BrandColors.PRIMARY, text_color="white", corner_radius=5)
        id_badge.pack(pady=5, padx=5, anchor="w")
        
        # Image
        try:
            pil_img = Image.open(row['file_path'])
            pil_img.thumbnail((120, 120))
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=pil_img.size)
            self.images_cache.append(ctk_img)
            
            lbl = ctk.CTkLabel(frame, text="", image=ctk_img)
            lbl.pack(padx=10, pady=5)
        except:
            ctk.CTkLabel(frame, text="[IMG ERR]").pack(padx=10)
            
        # Filename
        fname = os.path.basename(row['file_path'])
        if len(fname) > 12: fname = fname[:9] + "..."
        ctk.CTkLabel(frame, text=fname, font=("Arial", 10), text_color="gray").pack(pady=(0,2))
        
        # Tags
        tags = row['tags'] if row['tags'] else "（タグなし）"
        if len(tags) > 10: tags = tags[:10] + "..."
        
        btn_tags = ctk.CTkButton(frame, text=f"🏷 {tags}", height=20, width=100, 
                                 fg_color="transparent", text_color=BrandColors.PRIMARY, 
                                 font=("M PLUS Rounded 1c", 10), hover_color="#E0E0E0",
                                 command=lambda: self.edit_tags(row))
        btn_tags.pack(pady=(0, 5))

    def edit_tags(self, row):
        dialog = ctk.CTkInputDialog(text=f"タグを編集 (ID: {row['id']}):\nカンマ区切りで入力", title="タグ編集")
        new_tags = dialog.get_input()
        if new_tags is not None:
            self.db.update_image_tags(row['id'], new_tags)
            self.load_images()
