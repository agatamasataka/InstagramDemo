import sqlite3
import datetime

DB_NAME = "instamanager.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Images Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_path TEXT,
        image_blob BLOB,
        memo TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 2. Texts Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS texts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT,
        genre TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 3. Schedules Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target_date DATE,
        store_name TEXT,
        image_id INTEGER,
        text_id INTEGER,
        status TEXT,
        FOREIGN KEY (image_id) REFERENCES images (id),
        FOREIGN KEY (text_id) REFERENCES texts (id)
    )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database '{DB_NAME}' initialized.")

def insert_dummy_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if data exists
    cursor.execute("SELECT count(*) FROM images")
    if cursor.fetchone()[0] > 0:
        print("Data already exists. Skipping insertion.")
        conn.close()
        return

    # Dummy Images
    images_data = [
        ('/path/to/img1.jpg', None, 'Summer Sale Banner'),
        ('/path/to/img2.jpg', None, 'New Menu Item'),
        ('/path/to/img3.jpg', None, 'Interior Shot'),
    ]
    cursor.executemany("INSERT INTO images (file_path, image_blob, memo) VALUES (?, ?, ?)", images_data)

    # Dummy Texts
    texts_data = [
        ('Amazing summer sale! #summer #sale', 'Promotion'),
        ('Try our new delicious burger! #food #burger', 'Menu'),
        ('Cozy atmosphere waiting for you. #cafe', 'Brand'),
    ]
    cursor.executemany("INSERT INTO texts (content, genre) VALUES (?, ?)", texts_data)

    # Dummy Schedules
    # Linking image_id 1 with text_id 1, etc.
    # Schedule 3 has missing image/text to test status check
    schedules_data = [
        ('2023-10-25', 'Store A', 1, 1, '未完了'),
        ('2023-10-26', 'Store B', 2, 2, '完了'),
        ('2023-10-27', 'Store C', None, 3, '未完了'), # Missing image
        ('2023-10-28', 'Store A', 3, None, '未完了'), # Missing text
    ]
    cursor.executemany("INSERT INTO schedules (target_date, store_name, image_id, text_id, status) VALUES (?, ?, ?, ?, ?)", schedules_data)

    conn.commit()
    conn.close()
    print("Dummy data inserted.")

def check_status(image_id, text_id):
    """
    Simulates the computed property logic.
    Returns "OK" if both IDs are present, otherwise "未".
    """
    if image_id is not None and text_id is not None:
        return "OK"
    else:
        return "未"

def fetch_and_display_data():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Access columns by name
    cursor = conn.cursor()

    # Join Query
    query = '''
    SELECT 
        s.id as schedule_id,
        s.target_date,
        s.store_name,
        s.status as db_status,
        s.image_id,
        i.file_path,
        i.memo as image_memo,
        s.text_id,
        t.content as text_content
    FROM schedules s
    LEFT JOIN images i ON s.image_id = i.id
    LEFT JOIN texts t ON s.text_id = t.id
    '''

    cursor.execute(query)
    rows = cursor.fetchall()

    print("\n--- Schedule List (Console Dashboard) ---")
    print(f"{'ID':<4} | {'Date':<12} | {'Store':<10} | {'ImgID':<5} | {'TxtID':<5} | {'Check':<5} | {'Content Preview':<30}")
    print("-" * 90)

    for row in rows:
        # Computed Logic
        computed_status = check_status(row['image_id'], row['text_id'])
        
        # Formatting for display
        img_id_display = str(row['image_id']) if row['image_id'] else "None"
        txt_id_display = str(row['text_id']) if row['text_id'] else "None"
        content_preview = (row['text_content'][:27] + '...') if row['text_content'] else "---"

        print(f"{row['schedule_id']:<4} | {row['target_date']:<12} | {row['store_name']:<10} | {img_id_display:<5} | {txt_id_display:<5} | {computed_status:<5} | {content_preview:<30}")

    conn.close()

if __name__ == "__main__":
    init_db()
    insert_dummy_data()
    fetch_and_display_data()
