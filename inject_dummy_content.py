import sqlite3
import shutil
import os
import datetime
import random

DB_NAME = "instamanager.db"
CHARACTER_IMAGE = "/Users/masatakaagata/.gemini/antigravity/brain/da2e63e5-0fdf-4a04-8f73-50f34be1cf12/uploaded_image_1768896009399.png" # The mascot image

DUMMY_TEXTS = [
    {
        "content": """【年末年始の営業について】
いつもご利用ありがとうございます。
年末年始の営業は以下の通りとなります。

12/30 通常営業
12/31 10:00 - 15:00
1/1 - 1/3 休業
1/4 より通常営業

来年もよろしくお願いいたします🎍
#年末年始 #営業案内 #ロカオプ""",
        "genre": "お知らせ"
    },
    {
        "content": """＼ 新メニュー登場！ ／
春季限定「さくらラテ」がスタートしました🌸
ほんのり甘い桜の香りとミルクの相性が抜群です。

期間限定ですのでお早めにどうぞ✨
#カフェ #新メニュー #さくらラテ #春限定""",
        "genre": "メニュー紹介"
    },
    {
        "content": """【お客様の声】
「初めて利用しましたが、スタッフの対応がとても丁寧で安心しました」
嬉しいお言葉ありがとうございます😊

これからも皆様に愛されるお店作りを心がけてまいります！
#お客様の声 #ロカオプ #口コミ""",
        "genre": "口コミ紹介"
    },
     {
        "content": """知ってましたか？🤔
Googleマップの口コミ返信は、SEO（MEO）対策にも効果的なんです！

丁寧な返信は、来店検討中のお客様へのアピールにもなります。
まだの方はぜひ今日から始めてみましょう💪
#MEO対策 #Googleマップ #集客ノウハウ""",
        "genre": "豆知識"
    },
      {
        "content": """ロカオプの公式キャラクター「ロカモン」です！🌱
みんなの集客を応援するために生まれてきました。

これから色々なところに登場するかも...？
見かけたら可愛がってね！
#ロカオプ #ロカモン #公式キャラクター #ゆるキャラ""",
        "genre": "ブランディング"
    }
]

STORES = ["渋谷店", "新宿店", "オンライン", "全店舗共通", "大阪店"]

def inject_multiple_dummies():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    assets_dir = os.path.join(os.getcwd(), "assets_store")
    os.makedirs(assets_dir, exist_ok=True)

    # 1. Register the Mascot Image once
    mascot_img_id = None
    if os.path.exists(CHARACTER_IMAGE):
        dest_filename = "locamon_mascot.png"
        dest_path = os.path.join(assets_dir, dest_filename)
        if not os.path.exists(dest_path):
             shutil.copy2(CHARACTER_IMAGE, dest_path)
             
        # Insert or Retrieve
        cursor.execute("INSERT INTO images (file_path, memo) VALUES (?, ?)", (dest_path, "Locaop Mascot Character"))
        mascot_img_id = cursor.lastrowid
        print(f"Registered Mascot ID: {mascot_img_id}")
    else:
        print("Mascot image not found.")

    # 2. Insert Dummy Texts and Schedules
    start_date = datetime.date.today()
    
    for i, data in enumerate(DUMMY_TEXTS):
        # Insert Text
        cursor.execute("INSERT INTO texts (content, genre) VALUES (?, ?)", (data["content"], data["genre"]))
        text_id = cursor.lastrowid
        
        # Determine schedule date (incrementing days)
        target_date = (start_date + datetime.timedelta(days=i+1)).isoformat()
        store = random.choice(STORES)
        
        # Link logic: 
        # For the last one (intro), link to mascot image.
        # For others, leave image None or random existing image?
        # Let's link the mascot strictly to the relevant text (last one), 
        # and maybe leave others blank or link to previous images for variety if desired.
        # But user just said "create dummy data", so let's populate schedule rows.
        
        link_img_id = None
        status = "未完了"
        
        if "ロカモン" in data["content"] and mascot_img_id:
            link_img_id = mascot_img_id
            status = "完了"
        
        cursor.execute('''
            INSERT INTO schedules (target_date, store_name, image_id, text_id, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (target_date, store, link_img_id, text_id, status))
        
        print(f"Added Schedule: {target_date} - {data['genre']}")

    conn.commit()
    conn.close()
    print("Multiple dummy texts and schedules injected.")

if __name__ == "__main__":
    inject_multiple_dummies()
