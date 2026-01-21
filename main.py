import customtkinter as ctk
from tkinterdnd2 import TkinterDnD
from database import DatabaseManager
from views.schedule_view import ScheduleView
from views.material_view import MaterialView
from views.text_view import TextView
from views.client_view import ClientView
from theme import apply_theme, BrandColors

class InstaManagerApp(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        
        apply_theme()
        
        self.TkdndVersion = TkinterDnD._require(self)
        
        self.title("Locaop InstaManager System")
        self.geometry("1100x700")
        self.configure(fg_color=BrandColors.BG_LIGHT_MAIN)
        
        self.db = DatabaseManager()
        self.current_client = None
        
        # Container for swappable views
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        # Start with Client View
        self.show_client_view()

    def show_client_view(self):
        for w in self.main_container.winfo_children():
            w.destroy()
            
        self.client_view = ClientView(self.main_container, self.db, self.on_client_selected)
        # client_view packs itself in __init__
        
    def on_client_selected(self, client):
        self.current_client = client
        self.show_dashboard()
        
    def show_dashboard(self):
        for w in self.main_container.winfo_children():
            w.destroy()
            
        # Navigation / Tabs
        # Header with Breadcrumb or Back button
        header = ctk.CTkFrame(self.main_container, height=40, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(10, 0))
        
        ctk.CTkButton(header, text="⬅ クライアント選択に戻る", command=self.show_client_view, 
                      fg_color="transparent", text_color="gray", width=100, anchor="w").pack(side="left")
        
        ctk.CTkLabel(header, text=f"Client: {self.current_client['name']}", font=("M PLUS Rounded 1c", 14, "bold"), text_color="#333").pack(side="right")

        tab_view = ctk.CTkTabview(self.main_container, anchor="nw", corner_radius=15, 
                                       fg_color=BrandColors.BG_LIGHT_MAIN, 
                                       segmented_button_selected_color=BrandColors.PRIMARY,
                                       segmented_button_selected_hover_color=BrandColors.CTA_HOVER,
                                       segmented_button_unselected_color="white",
                                       text_color="gray30")
        tab_view.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Tab 1: 進行管理 (Schedule)
        tab_schedule = tab_view.add("進行管理コックピット")
        # Pass client info to views
        self.schedule_view = ScheduleView(tab_schedule, self.db, client_id=self.current_client['id'])
        self.schedule_view.pack(fill="both", expand=True)
        
        # Tab 2: 素材管理 (Materials)
        tab_material = tab_view.add("素材管理 (画像)")
        self.material_view = MaterialView(tab_material, self.db, client_id=self.current_client['id'])
        self.material_view.pack(fill="both", expand=True)
        
        # Tab 3: テキスト管理 (Implemented)
        tab_text = tab_view.add("テキスト管理")
        self.text_view = TextView(tab_text, self.db, client_id=self.current_client['id'])
        self.text_view.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = InstaManagerApp()
    app.mainloop()
