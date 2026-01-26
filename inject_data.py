import sqlite3
import shutil
import os
import datetime

DB_NAME = "instamanager.db"

# Input Data 2
source_image_path = "/Users/masatakaagata/.gemini/antigravity/brain/da2e63e5-0fdf-4a04-8f73-50f34be1cf12/uploaded_image_1768895971357.jpg"
text_content = """無料オンラインセミナー開催】店舗集客トレンド総集編2025 — 来年に向けて成果を出すためのAI・Google活用ポイント —
＜主なトピック＞
■ AI進化によって何が変わったのか
■ MEO単体ではなぜ限界があるのか
■ Google全体をどう活用すべきか
■ AIで置いていかれないための準備とは
■ どんな企業規模でも参考になる店舗集客のポイントとは

今年話題になった情報を“いま必要な形”に整理できる、知識アップデートに最適な1時間です。
ーーーーーーーーーーーーーーーーー
★セミナー概要★
開催日：2025/12/3（水）
時間：16:00-17:00
主催：株式会社インティメート・マージャー&株式会社ロカオプ
料金：無料
開催方法：Zoom
ーーーーーーーーーーーーーーーーー
参加申し込みはこちら↓↓↓
https://us06web.zoom.us/webinar/register/2317636268782/WN_xjU2Llo0RvG-qRds8Xvjuw#/registration
#セミナー　#店舗集客　#社長　#経営者"""
target_genre = "Seminar 2025"

def inject_data_2():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Handle Image
    assets_dir = os.path.join(os.getcwd(), "assets_store")
    os.makedirs(assets_dir, exist_ok=True)
    
    # Destination filename (unique)
    filename = "seminar_trend_2025.jpg"
    dest_path = os.path.join(assets_dir, filename)
    
    # Copy file
    if os.path.exists(source_image_path):
        shutil.copy2(source_image_path, dest_path)
        print(f"Image copied to {dest_path}")
    else:
        print(f"Warning: Source image not found at {source_image_path}")
        return

    # Insert Image to DB
    cursor.execute('INSERT INTO images (file_path, memo) VALUES (?, ?)', (dest_path, "Store Attraction Trend 2025"))
    new_image_id = cursor.lastrowid
    print(f"Inserted Image ID: {new_image_id}")

    # 2. Handle Text
    cursor.execute('INSERT INTO texts (content, genre) VALUES (?, ?)', (text_content, target_genre))
    new_text_id = cursor.lastrowid
    print(f"Inserted Text ID: {new_text_id}")

    # 3. Create Schedule (Linked)
    # Next day or just another entry for today
    target_date = datetime.date.today().isoformat()
    store_name = "Locaop Co-Host"
    
    cursor.execute('''
        INSERT INTO schedules (target_date, store_name, image_id, text_id, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (target_date, store_name, new_image_id, new_text_id, "完了"))
    new_schedule_id = cursor.lastrowid
    print(f"Inserted Schedule ID: {new_schedule_id}")
    
    conn.commit()
    conn.close()
    print("Dummy data injection 2 complete.")

if __name__ == "__main__":
    inject_data_2()
