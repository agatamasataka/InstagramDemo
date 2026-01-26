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
        # Configure Main Grid
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=0) # Preview Fixed
        self.main_container.grid_rowconfigure(1, weight=1)

        # Header -> Row 0, Col 0
        header = ctk.CTkFrame(self.main_container, height=40, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 0))
        
        ctk.CTkButton(header, text="⬅ クライアント選択に戻る", command=self.show_client_view, 
                      fg_color="transparent", text_color="gray", width=100, anchor="w").pack(side="left")
        
        # PREVIEW CONTAINER -> Row 0-2, Col 1 (Spans Header and Body)
        self.preview_container = ctk.CTkFrame(self.main_container, width=350, fg_color="white", corner_radius=0)
        self.preview_container.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=0, pady=0)
        self.preview_container.pack_propagate(False)

        # TABS -> Row 1, Col 0
        self.tab_view = ctk.CTkTabview(self.main_container, anchor="nw", corner_radius=15, 
                                       fg_color=BrandColors.BG_LIGHT_MAIN, 
                                       segmented_button_selected_color=BrandColors.PRIMARY,
                                       segmented_button_selected_hover_color=BrandColors.CTA_HOVER,
                                       segmented_button_unselected_color="white",
                                       text_color="gray30",
                                       command=self.on_tab_changed)
        self.tab_view.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        
        # Tab 1: 進行管理 (Schedule)
        tab_schedule = self.tab_view.add("進行管理コックピット")
        # Pass client info to views, AND PREVIEW FRAME
        self.schedule_view = ScheduleView(tab_schedule, self.db, client_id=self.current_client['id'], preview_frame=self.preview_container)
        self.schedule_view.pack(fill="both", expand=True)
        
        # Tab 2: 素材管理 (Materials)
        tab_material = self.tab_view.add("素材管理")
        self.material_view = MaterialView(tab_material, self.db, client_id=self.current_client['id'])
        self.material_view.pack(fill="both", expand=True)

        # Footer for Client Name -> Row 2, Col 0
        footer = ctk.CTkFrame(self.main_container, height=30, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))
        ctk.CTkLabel(footer, text=f"Client: {self.current_client['name']}", font=("M PLUS Rounded 1c", 12, "bold"), text_color="gray").pack(side="left")

    def on_tab_changed(self):
        selected = self.tab_view.get()
        if selected == "進行管理コックピット":
             self.preview_container.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=0, pady=0)
        else:
             self.preview_container.grid_remove()

if __name__ == "__main__":
    app = InstaManagerApp()
    app.mainloop()
