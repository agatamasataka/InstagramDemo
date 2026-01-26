import customtkinter as ctk
from theme import BrandColors, BUTTON_CONFIG, HEADER_LABEL_CONFIG

class ClientView(ctk.CTkFrame):
    def __init__(self, master, db, on_client_selected):
        super().__init__(master, fg_color=BrandColors.BG_LIGHT_MAIN)
        self.db = db
        self.on_client_selected = on_client_selected
        
        self.pack(fill="both", expand=True)
        
        # Center Container
        self.center_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=20, width=600, height=500)
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.center_frame.pack_propagate(False)
        
        # Header
        ctk.CTkLabel(self.center_frame, text="クライアント選択", font=("M PLUS Rounded 1c", 24, "bold"), 
                     text_color=BrandColors.PRIMARY).pack(pady=(40, 30))
        
        # Action Bar (Add Client)
        self.action_frame = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        self.action_frame.pack(fill="x", padx=50, pady=10)
        
        self.entry_new = ctk.CTkEntry(self.action_frame, placeholder_text="新しいクライアント名", width=300)
        self.entry_new.pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(self.action_frame, text="+ 追加", width=80, command=self.add_client, **BUTTON_CONFIG).pack(side="left")
        
        # List of Clients
        self.scroll_list = ctk.CTkScrollableFrame(self.center_frame, fg_color="#F9F9F9", width=500, height=250)
        self.scroll_list.pack(pady=20)
        
        self.load_clients()
        
    def load_clients(self):
        for w in self.scroll_list.winfo_children():
            w.destroy()
            
        clients = self.db.fetch_clients()
        
        if not clients:
            ctk.CTkLabel(self.scroll_list, text="クライアントが登録されていません", text_color="gray").pack(pady=20)
            return

        for client in clients:
            self.create_client_row(client)
            
    def create_client_row(self, client):
        row = ctk.CTkFrame(self.scroll_list, fg_color="white", corner_radius=10, height=60)
        row.pack(fill="x", pady=5, padx=10)
        row.pack_propagate(False)
        
        name_lbl = ctk.CTkLabel(row, text=client['name'], font=("M PLUS Rounded 1c", 16, "bold"), text_color="#333")
        name_lbl.pack(side="left", padx=20)
        
        # Enter Button
        ctk.CTkButton(row, text="管理画面へ", width=100, fg_color=BrandColors.PRIMARY, hover_color=BrandColors.CTA_HOVER,
                      command=lambda: self.enter_client(client)).pack(side="right", padx=15)

    def add_client(self):
        name = self.entry_new.get().strip()
        if not name: return
        
        success, msg = self.db.add_client(name)
        if success:
            self.entry_new.delete(0, "end")
            self.load_clients()
        else:
            print(msg) # Could allow messagebox here if passed reference

    def enter_client(self, client):
        self.on_client_selected(client)
