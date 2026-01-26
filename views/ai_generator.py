import customtkinter as ctk
from theme import BrandColors
from tkinter import messagebox
from datetime import datetime

class AIGeneratorModal(ctk.CTkToplevel):
    def __init__(self, master, db, on_save_callback=None, for_selection=False):
        super().__init__(master)
        self.db = db
        self.on_save_callback = on_save_callback
        self.for_selection = for_selection
        
        self.title("AI Content Generator")
        self.geometry("750x850")
        self.after(100, self.lift)
        self.configure(fg_color="#F4F6F8") 
        
        # Header
        header = ctk.CTkFrame(self, fg_color="white", height=60, corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="✨ AI記事生成アシスタント", font=("M PLUS Rounded 1c", 18, "bold"), 
                     text_color=BrandColors.PRIMARY).pack(pady=15)

        # Main Scroll
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 1. Input Section
        self.create_input_section()
        
        # 2. Results Section
        self.results_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.results_frame.pack(fill="x", pady=20)
        
    def create_input_section(self):
        frame = ctk.CTkFrame(self.scroll, fg_color="white", corner_radius=12, border_width=0)
        frame.pack(fill="x", pady=0)
        
        inner = ctk.CTkFrame(frame, fg_color="transparent")
        inner.pack(fill="x", padx=30, pady=30)
        
        # API Key Config (Top Right of inner)
        self.btn_apikey = ctk.CTkButton(inner, text="⚙️ API設定", width=80, height=24, 
                                        fg_color="#F1F3F4", text_color="#555", hover_color="#E0E0E0",
                                        command=self.ask_api_key, font=("M PLUS Rounded 1c", 10))
        self.btn_apikey.pack(anchor="e", pady=(0, 10))

        ctk.CTkLabel(inner, text="STEP 1. シーン・症状を選択", font=("M PLUS Rounded 1c", 13, "bold"), text_color="#555").pack(anchor="w")
        
        self.scene_vars = []
        scenes = ["腰痛・肩こり", "スポーツ障害", "産後骨盤矯正", "姿勢改善(猫背)", "交通事故治療", "鍼灸治療", "メンテナンス", "急な痛み(ぎっくり腰)"]
        
        scene_grid = ctk.CTkFrame(inner, fg_color="#FAFAFA", corner_radius=8)
        scene_grid.pack(fill="x", pady=(10, 20), padx=0)
        
        for i, s in enumerate(scenes):
            var = ctk.StringVar(value="")
            chk = ctk.CTkCheckBox(scene_grid, text=s, variable=var, onvalue=s, offvalue="", 
                                  font=("M PLUS Rounded 1c", 12), text_color="#333",
                                  checkbox_width=20, checkbox_height=20, corner_radius=4,
                                  fg_color=BrandColors.PRIMARY, hover_color=BrandColors.CTA_HOVER)
            chk.grid(row=i//4, column=i%4, padx=15, pady=12, sticky="w")
            self.scene_vars.append(var)
            
        grid_frame = ctk.CTkFrame(inner, fg_color="transparent")
        grid_frame.pack(fill="x")
        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)
        
        f1 = ctk.CTkFrame(grid_frame, fg_color="transparent")
        f1.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(f1, text="STEP 2. キーワード (任意)", font=("M PLUS Rounded 1c", 13, "bold"), text_color="#555").pack(anchor="w")
        self.entry_tags = ctk.CTkEntry(f1, placeholder_text="#ストレッチ, #予約空き...", height=36, border_width=1, border_color="#DDD")
        self.entry_tags.pack(fill="x", pady=(8, 0))
        
        f2 = ctk.CTkFrame(grid_frame, fg_color="transparent")
        f2.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        ctk.CTkLabel(f2, text="STEP 3. 投稿の目的", font=("M PLUS Rounded 1c", 13, "bold"), text_color="#555").pack(anchor="w")
        self.purpose_combo = ctk.CTkComboBox(f2, values=["新規患者様向け", "既存患者様向け", "自費メニュー紹介", "院の雰囲気紹介", "スタッフ紹介"], 
                                             height=36, border_width=1, border_color="#DDD", state="readonly")
        self.purpose_combo.pack(fill="x", pady=(8, 0))
        self.purpose_combo.set("新規患者様向け")
        
        self.btn_gen = ctk.CTkButton(inner, text="✨ AIで記事案を生成", command=self.generate_with_ai, 
                      fg_color="transparent", border_width=2, border_color=BrandColors.PRIMARY, text_color=BrandColors.PRIMARY,
                      hover_color="#E0F2F1", height=45, font=("M PLUS Rounded 1c", 14, "bold"), corner_radius=22)
        self.btn_gen.pack(pady=(30, 0), fill="x")

    def ask_api_key(self):
        curr = self.db.get_setting("openai_api_key") or ""
        dialog = ctk.CTkInputDialog(text="OpenAI API Keyを入力してください:", title="API設定")
        # Pre-filling is not supported by standard InputDialog easily without custom class, but simplest valid way:
        # We just ask. If user cancels, we do nothing.
        
        # Hack: Since CTkInputDialog doesn't support default value easily, we just ask.
        # Ideally we make a custom dialog but for now:
        print(f"Current Key: {curr}") # Debug
        
        new_key = dialog.get_input()
        if new_key is not None and new_key.strip():
            self.db.set_setting("openai_api_key", new_key.strip())
            messagebox.showinfo("保存", "API Keyを保存しました")

    def generate_with_ai(self):
        api_key = self.db.get_setting("openai_api_key")
        if not api_key:
            messagebox.showwarning("設定不足", "OpenAI API Keyが設定されていません。\n右上の「設定」ボタンから入力してください。")
            self.ask_api_key()
            return

        scenes = [v.get() for v in self.scene_vars if v.get()]
        tags = self.entry_tags.get()
        purpose = self.purpose_combo.get()
        
        if not scenes and not tags:
            messagebox.showwarning("入力不足", "シーンまたはキーワードを入力してください")
            return

        self.btn_gen.configure(state="disabled", text="✨ AIが思考中...")
        self.update()
        
        import openai
        import threading
        
        def run_api():
            try:
                client = openai.Client(api_key=api_key)
                
                prompt = f"""
あなたは整骨院・整体院のプロのSNS運用担当者です。
以下の情報を元に、Instagramのフィード投稿用の文章を作成してください。
親しみやすく、かつ専門性も感じるトーンでお願いします。

【ターゲット・目的】
{purpose}

【症状・シーン】
{', '.join(scenes) if scenes else '指定なし'}

【追加キーワード・要素】
{tags if tags else 'なし'}

【出力要件】
- 3つの異なるバリエーションを作成してください。
- 各バリエーションは「タイトル（キャッチーに）」「本文」「ハッシュタグ」を含めます。
- 全体をJSON形式ではなく、見やすいテキスト形式で区切って出力してください。
- 絵文字を適度に使用してください。
"""
                response = client.chat.completions.create(
                    model="gpt-4o", # or gpt-3.5-turbo
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant for SNS marketing."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8
                )
                
                content = response.choices[0].message.content
                
                # Simple parsing logic or just showing raw chunks
                # We will try to split by some separator if AI follows instructions, 
                # but for robustness let's just ask AI to split by "---"
                
                self.after(0, lambda: self._process_ai_result(content))
                
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("APIエラー", str(e)))
                self.after(0, lambda: self.btn_gen.configure(state="normal", text="✨ AIで記事案を生成"))

        threading.Thread(target=run_api, daemon=True).start()

    def _process_ai_result(self, text_content):
        # Allow user to see raw output or try to split
        # We'll rely on visual separation in UI for now
        # But to make it "selectable cards", we should try to split it.
        
        # Let's treat the whole thing as one result if splitting fails, 
        # or split by "パターン" or numbers if possible.
        
        # For this iteration, let's just show the full result in one card for copy-paste, 
        # OR split by newlines blocks.
        
        # Improved Strategy: Split by double newlines or standard markers
        variations = []
        
        # Naive split attempt based on headers
        import re
        parts = re.split(r'パターン\d|案\d', text_content)
        if len(parts) > 1:
            variations = [p.strip() for p in parts if p.strip()]
        else:
            variations = [text_content]
            
        self.btn_gen.configure(state="normal", text="✨ AIで記事案を生成（再生成）")
        self._show_results(variations)

    def _show_results(self, variations):
        for w in self.results_frame.winfo_children(): w.destroy()
        
        ctk.CTkLabel(self.results_frame, text="GENERATED DRAFTS", font=("Arial", 12, "bold"), text_color="#999").pack(anchor="w", padx=5, pady=(0, 10))

        for i, text in enumerate(variations):
            self.create_result_card(i, text)

    def create_result_card(self, idx, content):
        card = ctk.CTkFrame(self.results_frame, fg_color="white", corner_radius=10, border_width=0)
        card.pack(fill="x", pady=8)
        
        card.grid_columnconfigure(1, weight=1)
        
        accent = ctk.CTkFrame(card, fg_color=BrandColors.PRIMARY if idx == 0 else "#DDD", width=6, corner_radius=0)
        accent.grid(row=0, column=0, sticky="ns")
        
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        
        header = ctk.CTkFrame(content_frame, fg_color="transparent")
        header.pack(fill="x")
        
        tag_lbl = f"案 {idx+1}"
        tag_col = BrandColors.PRIMARY if idx == 0 else "gray"
        ctk.CTkLabel(header, text=tag_lbl, font=("M PLUS Rounded 1c", 11, "bold"), text_color=tag_col).pack(side="left")
        
        # Limit height or make scrollable if too long? Textbox usually better for long text
        preview_text = content
        if len(preview_text) > 300: preview_text = preview_text[:300] + "..."
        
        lbl = ctk.CTkLabel(content_frame, text=preview_text, font=("M PLUS Rounded 1c", 13), justify="left", anchor="w", text_color="#333", wraplength=550)
        lbl.pack(fill="x", pady=(5, 10))
        
        btn = ctk.CTkButton(content_frame, text="採用・編集する", command=lambda: self.open_finalize(content), 
                            height=32, width=120, fg_color="#333", hover_color="#000", font=("M PLUS Rounded 1c", 12, "bold"))
        btn.pack(anchor="e", pady=(5, 0))

    def open_finalize(self, content):
        FinalizeModal(self, self.db, content, self.on_save_callback, self.for_selection)

class FinalizeModal(ctk.CTkToplevel):
    def __init__(self, master, db, content, on_save_callback, for_selection=False):
        super().__init__(master)
        self.db = db
        self.content = content
        self.on_save_callback = on_save_callback
        self.for_selection = for_selection
        
        self.title("投稿内容の確定")
        self.geometry("500x700")
        self.configure(fg_color="#F4F6F8")
        self.after(100, self.lift)

        # Layout
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=0, pady=0)

        # 1. Content Edit
        ctk.CTkLabel(self.scroll, text="投稿内容の編集・タグ付け", font=("M PLUS Rounded 1c", 14, "bold"), text_color="#333").pack(pady=(20, 5), padx=20, anchor="w")
        
        self.txt_edit = ctk.CTkTextbox(self.scroll, height=150, font=("M PLUS Rounded 1c", 13), border_width=1, border_color="#DDD")
        self.txt_edit.pack(fill="x", padx=20, pady=5)
        self.txt_edit.insert("0.0", content)
        
        # Tags
        ctk.CTkLabel(self.scroll, text="タグを選択・追加", font=("M PLUS Rounded 1c", 12, "bold"), text_color="#555").pack(pady=(15, 5), padx=20, anchor="w")
        
        tag_cloud = ctk.CTkFrame(self.scroll, fg_color="transparent")
        tag_cloud.pack(fill="x", padx=20, pady=5)
        
        suggested = ["#整骨院", "#腰痛改善", "#肩こり解消", "#スポーツ外傷", "#産後骨盤矯正", "#交通事故治療", "#姿勢改善", "#鍼灸", "#リハビリ", "#夜20時まで"]
        for i, t in enumerate(suggested):
            btn = ctk.CTkButton(tag_cloud, text=t, width=60, height=24, fg_color="#E0E0E0", text_color="#333", 
                                hover_color="#D5D5D5", font=("M PLUS Rounded 1c", 11),
                                command=lambda tag=t: self.toggle_tag(tag))
            btn.grid(row=i//5, column=i%5, padx=3, pady=3, sticky="ew")
        for i in range(5): tag_cloud.grid_columnconfigure(i, weight=1)

        self.entry_tags = ctk.CTkEntry(self.scroll, height=36, placeholder_text="#手入力タグ")
        self.entry_tags.pack(fill="x", padx=20, pady=5)
        
        # 2. Action Choice
        ctk.CTkLabel(self.scroll, text="保存オプション", font=("M PLUS Rounded 1c", 14, "bold"), text_color="#333").pack(pady=(20, 10), padx=20, anchor="w")
        
        self.action_var = ctk.StringVar(value="material")
        
        # Option A
        frame_A = ctk.CTkFrame(self.scroll, fg_color="white", corner_radius=8)
        frame_A.pack(fill="x", padx=20, pady=5)
        
        opt_a_text = "この投稿に適用（素材として保存）" if self.for_selection else "素材として保存のみ"
        
        rb1 = ctk.CTkRadioButton(frame_A, text=opt_a_text, variable=self.action_var, value="material", command=self.toggle_inputs,
                                 font=("M PLUS Rounded 1c", 13))
        rb1.pack(anchor="w", padx=15, pady=15)
        
        # Option B (Hide if for_selection)
        if not self.for_selection:
            frame_B = ctk.CTkFrame(self.scroll, fg_color="white", corner_radius=8)
            frame_B.pack(fill="x", padx=20, pady=5)
            rb2 = ctk.CTkRadioButton(frame_B, text="スケジュールを作成", variable=self.action_var, value="schedule_new", command=self.toggle_inputs,
                                     font=("M PLUS Rounded 1c", 13))
            rb2.pack(anchor="w", padx=15, pady=15)
            
            self.date_frame = ctk.CTkFrame(frame_B, fg_color="transparent")
            self.date_frame.pack(fill="x", padx=40, pady=(0, 15))
            
            ctk.CTkLabel(self.date_frame, text="日付 (YYYY-MM-DD):", font=("M PLUS Rounded 1c", 12), text_color="#555").pack(side="left")
            self.date_entry = ctk.CTkEntry(self.date_frame, width=120)
            self.date_entry.pack(side="left", padx=10)
            today = datetime.now().strftime("%Y-%m-%d")
            self.date_entry.insert(0, today)
        else:
            self.date_entry = None

        # Footer (Fixed)
        self.footer = ctk.CTkFrame(self, fg_color="white", height=80, corner_radius=0)
        self.footer.pack(fill="x", side="bottom")
        
        # Execute
        btn_text = "適用して戻る" if self.for_selection else "確定して保存"
        ctk.CTkButton(self.footer, text=btn_text, command=self.execute, 
                      fg_color=BrandColors.PRIMARY, height=45, font=("M PLUS Rounded 1c", 14, "bold")).pack(pady=15, padx=20, fill="x")
        
        self.toggle_inputs()

    def toggle_tag(self, tag):
        current_text = self.entry_tags.get()
        if tag in current_text:
            new_text = current_text.replace(tag, "").strip()
            new_text = " ".join(new_text.split())
        else:
            if current_text:
                new_text = current_text.strip() + " " + tag
            else:
                new_text = tag
        self.entry_tags.delete(0, "end")
        self.entry_tags.insert(0, new_text)
    
    def toggle_inputs(self):
        if self.date_entry:
            if self.action_var.get() == "schedule_new":
                self.date_entry.configure(state="normal", fg_color="white", text_color="black")
            else:
                self.date_entry.configure(state="disabled", fg_color="#F0F0F0", text_color="gray")

    def execute(self):
        final_content = self.txt_edit.get("0.0", "end").strip()
        final_tags = self.entry_tags.get()
        
        # Save as material
        self.db.add_text(final_content, genre="AI生成")
        
        if not self.for_selection and self.action_var.get() == "schedule_new" and self.date_entry:
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT MAX(id) FROM texts")
            res = cursor.fetchone()
            if res:
                text_id = res[0]
                date_str = self.date_entry.get()
                self.db.add_schedule(date_str, "12:00", store_id=1, status="下書き")
                cursor.execute("SELECT MAX(id) FROM schedules")
                sched_res = cursor.fetchone()
                if sched_res:
                    self.db.update_schedule_link(sched_res[0], 'text', text_id)

        if self.on_save_callback: self.on_save_callback()
        messagebox.showinfo("完了", "保存しました")
        self.master.destroy()
