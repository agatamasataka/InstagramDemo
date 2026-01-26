import sqlite3
import datetime
import os
import csv

DB_NAME = "instamanager.db"

class DatabaseManager:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # 0. Clients & Stores Tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS stores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            name TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients (id)
        )
        ''')

        # 1. Images Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT,
            image_blob BLOB,
            memo TEXT,
            tags TEXT,
            client_id INTEGER,
            store_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients (id),
            FOREIGN KEY (store_id) REFERENCES stores (id)
        )
        ''')
        
        # Migration: Add columns to images
        cursor.execute("PRAGMA table_info(images)")
        cols = [info[1] for info in cursor.fetchall()]
        if 'tags' not in cols: cursor.execute("ALTER TABLE images ADD COLUMN tags TEXT")
        if 'client_id' not in cols: cursor.execute("ALTER TABLE images ADD COLUMN client_id INTEGER")
        if 'store_id' not in cols: cursor.execute("ALTER TABLE images ADD COLUMN store_id INTEGER")

        # 2. Texts Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS texts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            genre TEXT,
            client_id INTEGER,
            store_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients (id),
            FOREIGN KEY (store_id) REFERENCES stores (id)
        )
        ''')
        
        # Migration: Add columns to texts
        cursor.execute("PRAGMA table_info(texts)")
        cols = [info[1] for info in cursor.fetchall()]
        if 'client_id' not in cols: cursor.execute("ALTER TABLE texts ADD COLUMN client_id INTEGER")
        if 'store_id' not in cols: cursor.execute("ALTER TABLE texts ADD COLUMN store_id INTEGER")

        # 3. Schedules Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_date DATE,
            post_time TEXT,
            store_name TEXT,
            image_id INTEGER,
            text_id INTEGER,
            post_type TEXT,
            status TEXT,
            client_id INTEGER,
            store_id INTEGER,
            FOREIGN KEY (image_id) REFERENCES images (id),
            FOREIGN KEY (text_id) REFERENCES texts (id),
            FOREIGN KEY (client_id) REFERENCES clients (id),
            FOREIGN KEY (store_id) REFERENCES stores (id)
        )
        ''')
        
        # Migration: Add columns to schedules
        cursor.execute("PRAGMA table_info(schedules)")
        cols = [info[1] for info in cursor.fetchall()]
        if 'post_time' not in cols: cursor.execute("ALTER TABLE schedules ADD COLUMN post_time TEXT")
        if 'post_type' not in cols: cursor.execute("ALTER TABLE schedules ADD COLUMN post_type TEXT")
        if 'client_id' not in cols: cursor.execute("ALTER TABLE schedules ADD COLUMN client_id INTEGER")
        if 'store_id' not in cols: cursor.execute("ALTER TABLE schedules ADD COLUMN store_id INTEGER")
        
<<<<<<< HEAD
=======
        # 4. Settings Table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        ''')

>>>>>>> c5d2c25d7640490051c0d591eb838e91fa43e32b
        conn.commit()
        
        # Ensure Default Client exists
        cursor.execute("SELECT count(*) FROM clients")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO clients (name) VALUES (?)", ("デフォルトクライアント",))
            default_client_id = cursor.lastrowid
            
            # Link existing orphan data to default client
            cursor.execute("UPDATE images SET client_id = ? WHERE client_id IS NULL", (default_client_id,))
            cursor.execute("UPDATE texts SET client_id = ? WHERE client_id IS NULL", (default_client_id,))
            cursor.execute("UPDATE schedules SET client_id = ? WHERE client_id IS NULL", (default_client_id,))
            
        conn.commit()
        conn.close()

    # --- CSV Import Logic ---
    def import_schedules_from_csv(self, file_path, store_name_arg=None):
        """
        Imports schedules from a CSV file.
<<<<<<< HEAD
        Expected CSV format:
        Header: date, time, store_name, type
=======
        Robustly handles metadata rows before the actual header.
        Expected columns: 日付, 投稿時間, 店舗, 種別, テキスト/本文
>>>>>>> c5d2c25d7640490051c0d591eb838e91fa43e32b
        """
        count = 0
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
<<<<<<< HEAD
            with open(file_path, mode='r', encoding='utf-8') as f:
=======
            # 1. Find the header row index
            header_row_index = 0
            encodings = ['utf-8', 'cp932', 'shift_jis']
            
            found_header = False
            encoding_used = 'utf-8'
            
            # Try to determine encoding and header offset
            for enc in encodings:
                try:
                    with open(file_path, mode='r', encoding=enc) as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            if "日付" in line or "date" in line.lower():
                                header_row_index = i
                                found_header = True
                                encoding_used = enc
                                break
                    if found_header: break
                except UnicodeDecodeError:
                    continue
            
            if not found_header:
                return False, "有効なヘッダー行（'日付' または 'date' を含む行）が見つかりませんでした。"

            # 2. Parse from the header row
            with open(file_path, mode='r', encoding=encoding_used) as f:
                # Skip to header
                for _ in range(header_row_index):
                    next(f)
                
>>>>>>> c5d2c25d7640490051c0d591eb838e91fa43e32b
                reader = csv.DictReader(f)
                
                for row in reader:
                    date_val = None
                    time_val = None
                    store_val = store_name_arg
                    type_val = None
<<<<<<< HEAD
                    
                    for k, v in row.items():
                        if not k: continue
                        k_lower = k.lower()
                        if 'date' in k_lower or '日付' in k_lower:
                            date_val = v.strip()
                        elif 'time' in k_lower or '時間' in k_lower:
                            time_val = v.strip()
                        elif ('store' in k_lower or '店舗' in k_lower) and not store_name_arg:
                            store_val = v.strip()
                        elif 'type' in k_lower or '種別' in k_lower:
                            type_val = v.strip()
                    
                    if date_val:
                        # If store_val is still None, use a default or skip? 
                        # User wants per-store import, so store_val should likely be provided via arg or csv
                        if not store_val: store_val = "Unknown Store"
                        
                        cursor.execute('''
                            INSERT INTO schedules (target_date, post_time, store_name, post_type, status)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (date_val, time_val, store_val, type_val, "未完了"))
=======
                    content_val = None
                    
                    # Fuzzy match keys
                    for k, v in row.items():
                        if not k: continue
                        k_lower = k.lower()
                        v_str = str(v).strip()
                        
                        if 'date' in k_lower or '日付' in k_lower:
                            date_val = v_str
                        elif 'time' in k_lower or '時間' in k_lower:
                            time_val = v_str
                        elif ('store' in k_lower or '店舗' in k_lower) and not store_name_arg:
                            store_val = v_str
                        elif 'type' in k_lower or '種別' in k_lower:
                            type_val = v_str
                        elif any(x in k_lower for x in ['text', 'content', 'caption', '本文', 'キャプション']):
                            content_val = v_str
                    
                    # Validation: Required fields check
                    if date_val:
                        # Fix date format if necessary (e.g., "1月7日" -> "2026-01-07")
                        # Assuming current year or next occurrence?
                        # For now, store exactly as is, or try simple normalize.
                        # If "1月7日" format, append year? 
                        # Let's keep it simple string for now to avoid parsing errors, 
                        # BUT ScheduleView expects YYYY-MM-DD for sorting/display logic sometimes.
                        # Let's try to convert "1月7日" to "2026-01-07" if needed.
                        # The user CSV has "2025/12/24" in metadata but "1月7日" in data.
                        # Assuming "current/next season". Let's guess 2026 based on context or current year.
                        
                        import re
                        m = re.match(r'(\d+)月(\d+)日', date_val)
                        if m:
                            # Naive year assumption: 2026 based on metadata context
                            date_val = f"2026-{int(m.group(1)):02d}-{int(m.group(2)):02d}"
                        
                        m2 = re.match(r'(\d+)/(\d+)/(\d+)', date_val)
                        if m2:
                           date_val = f"{m2.group(1)}-{int(m2.group(2)):02d}-{int(m2.group(3)):02d}"

                        if not store_val: store_val = "Unknown Store"
                        
                        text_id = None
                        if content_val:
                            cursor.execute("INSERT INTO texts (content, genre) VALUES (?, ?)", (content_val, "インポート"))
                            text_id = cursor.lastrowid

                        cursor.execute('''
                            INSERT INTO schedules (target_date, post_time, store_name, post_type, status, text_id)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (date_val, time_val, store_val, type_val, "未確認", text_id))
>>>>>>> c5d2c25d7640490051c0d591eb838e91fa43e32b
                        count += 1
            
            conn.commit()
            conn.close()
            return True, f"{count} 件のスケジュール枠を取り込みました。"
        except Exception as e:
            return False, f"エラーが発生しました: {str(e)}"

    def import_texts_from_csv(self, file_path):
        """
        Imports texts from a CSV file.
        Format: content, genre
        """
        count = 0
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            with open(file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    content_val = None
                    genre_val = "未分類"
                    
                    for k, v in row.items():
                        if not k: continue
                        k_lower = k.lower()
                        if 'content' in k_lower or '本文' in k_lower or 'text' in k_lower:
                            content_val = v.strip()
                        elif 'genre' in k_lower or 'ジャンル' in k_lower:
                            genre_val = v.strip()
                            
                    if content_val:
                        cursor.execute('INSERT INTO texts (content, genre) VALUES (?, ?)', (content_val, genre_val))
                        count += 1
                        
            conn.commit()
            conn.close()
            return True, f"{count} 件のテキストを取り込みました。"
        except Exception as e:
            return False, f"エラー: {str(e)}"

<<<<<<< HEAD
=======
    def add_text(self, content, genre="AI生成"):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO texts (content, genre) VALUES (?, ?)", (content, genre))
        conn.commit()
        conn.close()

>>>>>>> c5d2c25d7640490051c0d591eb838e91fa43e32b
    def add_schedule(self, target_date, post_time, store_name, post_type, client_id=None, store_id=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO schedules (target_date, post_time, store_name, post_type, status, client_id, store_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
<<<<<<< HEAD
        ''', (target_date, post_time, store_name, post_type, "未完了", client_id, store_id))
=======
        ''', (target_date, post_time, store_name, post_type, "未対応", client_id, store_id))
        conn.commit()
        conn.close()

    def update_status(self, schedule_id, status):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE schedules SET status = ? WHERE id = ?", (status, schedule_id))
>>>>>>> c5d2c25d7640490051c0d591eb838e91fa43e32b
        conn.commit()
        conn.close()

    def fetch_schedules(self, store_filter=None, client_id=None):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = '''
        SELECT 
            s.id,
            s.target_date,
            s.post_time,
            s.store_name,
            s.post_type,
            s.status,
            s.image_id,
            i.file_path,
            i.memo as image_memo,
            i.tags as image_tags,
            s.text_id,
            t.content as text_content
        FROM schedules s
        LEFT JOIN images i ON s.image_id = i.id
        LEFT JOIN texts t ON s.text_id = t.id
        WHERE 1=1
        '''
        
        params = []
        if client_id is not None:
            query += ' AND s.client_id = ?'
            params.append(client_id)
            
        if store_filter and store_filter != "全店舗データのサマリ":
            query += ' AND s.store_name = ?'
            params.append(store_filter)
            
        query += ' ORDER BY s.target_date ASC, s.post_time ASC'
        
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        
        result = []
        for row in rows:
            result.append(dict(row))
        conn.close()
        return result

    def get_all_stores(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT store_name FROM schedules WHERE store_name IS NOT NULL ORDER BY store_name")
        rows = cursor.fetchall()
        conn.close()
        return [r[0] for r in rows]

    def update_schedule_link(self, schedule_id, image_id=None, text_id=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if image_id == "": image_id = None
        if text_id == "": text_id = None
        
        cursor.execute('''
            UPDATE schedules 
            SET image_id = ?, text_id = ? 
            WHERE id = ?
        ''', (image_id, text_id, schedule_id))
        
        # Now check status
        status = "未完了"
        if image_id and text_id:
            status = "完了"
            
        cursor.execute('UPDATE schedules SET status = ? WHERE id = ?', (status, schedule_id))
        
        conn.commit()
        conn.close()
        return status

    def add_image(self, file_path, memo=None, tags=None, client_id=None, store_id=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        filename = os.path.basename(file_path)
        if memo is None:
            memo = filename
            
        cursor.execute('INSERT INTO images (file_path, memo, tags, client_id, store_id) VALUES (?, ?, ?, ?, ?)', 
                       (file_path, memo, tags, client_id, store_id))
        new_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        return new_id
        
    def update_image_tags(self, image_id, tags):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE images SET tags = ? WHERE id = ?', (tags, image_id))
        conn.commit()
        conn.close()

    def add_text(self, content, genre, client_id=None, store_id=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO texts (content, genre, client_id, store_id) VALUES (?, ?, ?, ?)', 
                       (content, genre, client_id, store_id))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return new_id

    def fetch_images(self, tag_filter=None, client_id=None, store_id=None):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = 'SELECT * FROM images WHERE 1=1'
        params = []
        
        if client_id is not None:
             query += ' AND (client_id = ? OR client_id IS NULL)'
             params.append(client_id)
        if store_id is not None:
             query += ' AND (store_id = ? OR store_id IS NULL)'
             params.append(store_id)
        
        if tag_filter:
            query += ' AND tags LIKE ?'
            params.append(f"%{tag_filter}%")
            
        query += ' ORDER BY id DESC'
        
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall() 
        result = []
        for row in rows:
            result.append(dict(row))
        conn.close()
        return result

    def fetch_texts(self, client_id=None, store_id=None):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = 'SELECT * FROM texts WHERE 1=1'
        params = []
        
        if client_id is not None:
             query += ' AND (client_id = ? OR client_id IS NULL)'
             params.append(client_id)
        if store_id is not None:
             query += ' AND (store_id = ? OR store_id IS NULL)'
             params.append(store_id)
             
        query += ' ORDER BY id DESC'
        
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(dict(row))
        conn.close()
        return result

    def get_status_check(self, image_id, text_id):
        if image_id and text_id:
            return "OK"
        return "未"

    # --- Client & Store Management ---
    def fetch_clients(self):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients ORDER BY id")
        rows = cursor.fetchall()
        d = [dict(row) for row in rows]
        conn.close()
        return d

    def add_client(self, name):
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clients (name) VALUES (?)", (name,))
            client_id = cursor.lastrowid
            
            # Add default stores
            cursor.execute("INSERT INTO stores (client_id, name) VALUES (?, ?)", (client_id, "店舗A"))
            cursor.execute("INSERT INTO stores (client_id, name) VALUES (?, ?)", (client_id, "店舗B"))
            
            conn.commit()
            return True, "Registered successfully"
        except sqlite3.IntegrityError:
            return False, "Name already exists"
        finally:
            conn.close()

    def fetch_stores(self, client_id):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stores WHERE client_id = ? ORDER BY name", (client_id,))
        rows = cursor.fetchall()
        d = [dict(row) for row in rows]
        conn.close()
        return d

    def add_store(self, client_id, name):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO stores (client_id, name) VALUES (?, ?)", (client_id, name))
        nid = cursor.lastrowid
        conn.commit()
        conn.close()
        return nid

    def delete_store(self, store_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM stores WHERE id = ?", (store_id,))
        conn.commit()
        conn.close()
<<<<<<< HEAD
=======

    def get_setting(self, key):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        res = cursor.fetchone()
        conn.close()
        return res[0] if res else None

    def set_setting(self, key, value):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
        conn.commit()
        conn.close()
>>>>>>> c5d2c25d7640490051c0d591eb838e91fa43e32b
