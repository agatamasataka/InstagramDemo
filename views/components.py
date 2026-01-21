import customtkinter as ctk
from theme import BrandColors, BUTTON_CONFIG, HEADER_LABEL_CONFIG

class SelectionModal(ctk.CTkToplevel):
    def __init__(self, master, items, title="Select Item", on_select=None):
        super().__init__(master)
        self.title(title)
        self.geometry("600x500")
        self.transient(master) # Make it modal-like relative to master
        self.grab_set() # Focus grab
        
        self.on_select = on_select
        self.configure(fg_color="white")
        
        # Header
        ctk.CTkLabel(self, text=title, font=("M PLUS Rounded 1c", 18, "bold"), text_color=BrandColors.PRIMARY).pack(pady=15)
        
        # Filter Entry
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self.filter_items)
        ctk.CTkEntry(self, textvariable=self.search_var, placeholder_text="検索...", width=400).pack(pady=(0, 10))

        # Scrollable Grid
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="#F9F9F9", width=550, height=350)
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.items = items # List of dicts {id, image_path, text_preview, etc}
        self.card_refs = []
        
        self.populate(items)
        
    def populate(self, items):
        for w in self.scroll_frame.winfo_children():
            w.destroy()
            
        cols = 3
        for i, item in enumerate(items):
            r = i // cols
            c = i % cols
            self.create_card(item, r, c)

    def create_card(self, item, r, c):
        # Card Frame
        card = ctk.CTkFrame(self.scroll_frame, fg_color="white", border_width=1, border_color="#EEE")
        card.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
        
        # Click event handler
        def select_handler(event=None):
            if self.on_select:
                self.on_select(item['id'])
            self.destroy()

        card.bind("<Button-1>", select_handler)
        
        # If Image
        if 'file_path' in item:
            try:
                from PIL import Image
                img = Image.open(item['file_path'])
                img.thumbnail((120, 100))
                ctk_img = ctk.CTkImage(img, size=img.size)
                lbl = ctk.CTkLabel(card, image=ctk_img, text="")
                lbl.pack(pady=5)
                lbl.bind("<Button-1>", select_handler)
            except:
                ctk.CTkLabel(card, text="[No Img]").pack(pady=20)

        # If Text
        if 'content' in item:
            preview = item['content'][:40] + "..." if len(item['content']) > 40 else item['content']
            lbl = ctk.CTkLabel(card, text=preview, wraplength=140, font=("M PLUS Rounded 1c", 11), text_color="gray30")
            lbl.pack(pady=5, padx=5)
            lbl.bind("<Button-1>", select_handler)
            
        # ID Badge
        # ctk.CTkLabel(card, text=f"ID: {item['id']}", font=("Arial", 9), text_color="gray").pack(side="bottom", pady=2)

    def filter_items(self, *args):
        query = self.search_var.get().lower()
        if not query:
            self.populate(self.items)
            return
            
        filtered = [item for item in self.items if str(item.get('id','')).lower() in query or item.get('memo','').lower() in query or item.get('content','').lower() in query]
        self.populate(filtered)
