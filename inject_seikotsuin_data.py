import sqlite3
import os
import datetime
import random
import glob

DB_NAME = "instamanager.db"

DUMMY_TEXTS = [
    {
        "content": """デスクワーク向け！座ったままできる「肩甲骨はがし」
長時間のパソコン作業で背中がガチガチになっていませんか？
オフィスでも座ったままできる簡単なストレッチをご紹介します✨

1. 両手を肩に置く
2. 肘で大きな円を描くように回す
3. 前回し・後ろ回し 各10回

これだけで血流が良くなり、肩がスッキリします！
ぜひ隙間時間に試してみてくださいね。

#[地域名]整骨院 #[駅名]整骨院 #ストレッチ動画 #肩こり解消 #腰痛ストレッチ #セルフケア #デスクワーク #オフィスストレッチ #健康維持 #体のメンテナンス #柔軟 #整骨院""",
        "genre": "セルフケア"
    },
    {
        "content": """【猫背矯正 ビフォーアフター】
「姿勢が悪いとよく言われる...」とお悩みの患者様。
当院の猫背矯正を受けていただきました！

左：施術前（頭が前に出て、背中が丸まっている）
右：施術後（耳と肩のラインが揃い、背筋が伸びている）

1回の施術でもこれだけの変化が出ます！（※効果には個人差があります）
姿勢が整うと、見た目年齢もマイナス5歳！？✨

#[地域名]整骨院 #[駅名]整骨院 #猫背矯正 #姿勢改善 #骨盤矯正 #ビフォーアフター #姿勢美人 #ストレートネック #スマホ首 #姿勢が良くなる #体の歪み #根本改善""",
        "genre": "ビフォーアフター"
    },
    {
        "content": """なぜ「ギックリ腰」になるの？🤔
重い物を持った時だけでなく、くしゃみや洗顔など、ふとした動作でも起こるギックリ腰。

主な原因は「筋肉疲労の蓄積」と「姿勢の悪さ」です。
限界を迎えた筋肉が、些細なきっかけで炎症を起こしてしまうのです⚡️

「腰に違和感があるな...」と思ったら、それは体が発しているSOS信号です！
痛くなる前に、早めのメンテナンスをおすすめします。

#[地域名]整骨院 #[駅名]整骨院 #腰痛 #ギックリ腰 #頭痛 #肩こり #坐骨神経痛 #ヘルニア #痛みの原因 #健康知識 #体の仕組み #整骨院の先生""",
        "genre": "症状解説"
    },
    {
        "content": """院長の素顔に迫る！治療家になったきっかけ👨‍⚕️
こんにちは、院長の[名前]です。
私が治療家を目指したのは、高校時代の怪我がきっかけでした。

部活で足を痛め、大会出場を諦めかけていた時、親身になって治療してくれた整骨院の先生がいました。
「私も、痛みで苦しむ人を助けたい！」
その時の想いが、今の私の原動力になっています🔥

地域の皆様の健康を全力でサポートします！
お体の悩み、何でもご相談ください。

#[地域名]整骨院 #[駅名]整骨院 #スタッフ紹介 #柔道整復師 #治療家 #整骨院の日常 #アットホームな職場 #笑顔 #地域の皆様に愛される #健康相談 #体の悩み #[地域名]""",
        "genre": "スタッフ紹介"
    },
    {
        "content": """【患者様の声】
「長年の頭痛が改善しました」
嬉しいお言葉をいただきました✨

デスクワークによる慢性的な肩こりと頭痛に悩まされていたA様。
姿勢矯正と鍼治療を組み合わせたメニューで、根本からの改善を目指しました。
「薬を飲む回数が減って、仕事も集中できるようになりました！」と笑顔でお話しいただき、私たちも本当に嬉しいです😊

#[地域名]整骨院 #[駅名]整骨院 #お客様の声 #患者様の声 #口コミ #嬉しい報告 #改善事例 #ありがとうございます #感謝 #地域密着 #選ばれる理由 #評判""",
        "genre": "患者様の声"
    },
    {
        "content": """整骨院と整体院、何が違うの？🤔
よくいただくご質問にお答えします！

【整骨院（接骨院）】
・国家資格（柔道整復師）を持った施術者が在籍
・骨折、脱臼、打撲、捻挫などの怪我には「保険が適用」されます

【整体院】
・民間資格での施術が主
・リラクゼーションや慢性的な痛みのケアが中心（保険適用外）

当院は「整骨院」ですので、急な痛みや怪我の治療はもちろん、交通事故治療なども対応可能です🚑
慢性的な肩こりなどには自費診療もご用意しています。

#[地域名]整骨院 #[駅名]整骨院 #整骨院選び #保険適用 #交通事故治療 #むち打ち #整体 #マッサージ #質問コーナー #初めての方大歓迎 #健康情報 #豆知識""",
        "genre": "Q&A"
    },
    {
        "content": """産後ママ必見！骨盤の歪みチェックリスト✅
出産後、こんなお悩みはありませんか？

□ 産前のズボンが入らない
□ ぽっこりお腹が戻らない
□ 尿漏れがある
□ 腰痛や股関節痛がある
□ 仰向けで寝ると腰が浮く

3つ以上当てはまったら、骨盤が歪んでいる可能性大！😱
産後の骨盤は非常にデリケート。正しいケアでしっかり整えましょう。
当院はキッズスペース完備！お子様連れでも安心して通えます👶

#[地域名]整骨院 #[駅名]整骨院 #産後骨盤矯正 #産後ケア #ママの悩み #子連れOK #赤ちゃんのいる生活 #産後ダイエット #骨盤の歪み #マタニティ #ママの味方 #キッズスペース完備""",
        "genre": "産後ケア"
    },
    {
        "content": """初めての方も安心！ご来院からの流れ🔰
「整骨院って初めてで不安...」という方へ、当院の施術の流れをご紹介します。

1. 受付・カウンセリングシート記入
2. 問診・検査（痛みの原因をしっかり探ります）
3. 施術方針の説明（納得いただいてから施術します）
4. 施術（お一人お一人に合わせたオーダーメイド治療）
5. 今後のアドバイス・お会計

明るく清潔な院内で、リラックスして施術を受けていただけます✨
まずはご予約・お問い合わせをお待ちしております！

#[地域名]整骨院 #[駅名]整骨院 #初診 #院内風景 #清潔感 #コロナ対策 #予約優先 #個室あり #施術風景 #安心安全 #リラックス #メンテナンス""",
        "genre": "院内ツアー"
    },
    {
        "content": """実は腰に悪い！やってはいけない「座り方」ワースト3🙅‍♂️
デスクワークや家でのリラックスタイム、こんな座り方していませんか？

🥉 ワースト3：足組み座り
骨盤がねじれ、腰痛の原因に！
🥈 ワースト2：横座り（お姉さん座り）
股関節への負担大。左右非対称な体になります。
🥇 ワースト1：仙骨座り（ずっこけ座り）
椅子に浅く腰掛け、背もたれに寄りかかる姿勢。腰への負担が最強です😱

正しい座り方は、骨盤を立てて座ること！
意識してみてくださいね。

#[地域名]整骨院 #[駅名]整骨院 #生活習慣 #座り方 #足組み #悪い姿勢 #健康習慣 #予防医学 #体の使い方 #腰に優しい #アドバイス #注意喚起""",
        "genre": "NG習慣"
    },
    {
        "content": """気圧の変化で頭痛がする...「天気痛」かも？☔️
雨の日や台風が近づくと調子が悪い、頭が痛い...。
それは気圧の変化によって自律神経が乱れる「天気痛（気象病）」かもしれません。

対処法としておすすめなのが「耳マッサージ」👂
耳を上下横に引っ張ったり、くるくる回したりするだけで、血流が良くなり自律神経が整いやすくなります。

辛い時は無理せず、当院の頭痛治療や鍼灸治療もご相談ください📍

#[地域名]整骨院 #[駅名]整骨院 #自律神経 #気象病 #天気痛 #冷え性改善 #水分補給 #熱中症対策 #季節の変わり目 #免疫力アップ #五月病 #体調管理""",
        "genre": "季節の不調"
    }
]

# Map specific images to genres if possible, or just random
# We will just register existing images with generic tags first.

def text_factory(content, genre):
    return {"content": content, "genre": genre}

def inject_seikotsuin_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Clear Data
    print("Clearing existing data...")
    cursor.execute("DELETE FROM schedules")
    cursor.execute("DELETE FROM texts")
    cursor.execute("DELETE FROM images")
    
    conn.commit()
    
    # 2. Re-register Images from assets_store with Seikotsuin Tags
    assets_dir = os.path.join(os.getcwd(), "assets_store")
    image_files = glob.glob(os.path.join(assets_dir, "*"))
    
    # Filter for image extensions
    image_files = [f for f in image_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
    
    print(f"Found {len(image_files)} existing images to re-register.")
    
    registered_image_ids = []
    
    tags_pool = ["#院内風景", "#施術の様子", "#スタッフ", "#外観", "#設備紹介"]
    
    for img_path in image_files:
        # Determine tags randomly or generically
        tags = random.choice(tags_pool)
        memo = "Demo Image"
        
        cursor.execute("INSERT INTO images (file_path, memo, tags) VALUES (?, ?, ?)", (img_path, memo, tags))
        registered_image_ids.append(cursor.lastrowid)
        
    print(f"Re-registered {len(registered_image_ids)} images.")

    # 3. Insert Texts and Schedules
    start_date = datetime.date.today()
    
    # Fetch stores to link
    # If no stores exist, create dummy stores.
    # Note: store table might not be cleared. Let's check or just ensure 1 store exists.
    # We didn't delete stores table, so we assume stores exist or we use hardcoded ID.
    # Let's check stores.
    cursor.execute("SELECT id, name FROM stores")
    stores = cursor.fetchall()
    if not stores:
        cursor.execute("INSERT INTO stores (client_id, name) VALUES (?, ?)", (1, "あがた整骨院 本院"))
        stores = [(cursor.lastrowid, "あがた整骨院 本院")]
        
    store_cycle = [s[1] for s in stores]
    store_id_cycle = [s[0] for s in stores]

    print("Inserting Texts and Schedules...")
    
    for i, data in enumerate(DUMMY_TEXTS):
        # Insert Text
        cursor.execute("INSERT INTO texts (content, genre) VALUES (?, ?)", (data["content"], data["genre"]))
        text_id = cursor.lastrowid
        
        # Schedule Date
        target_date = (start_date + datetime.timedelta(days=i)).isoformat()
        
        # Pick Image
        img_id = random.choice(registered_image_ids) if registered_image_ids else None
        
        # Store
        store_idx = i % len(stores)
        store_name = store_cycle[store_idx]
        store_id = store_id_cycle[store_idx]
        
        status = "未完了"
        if img_id: status = "投稿待ち" # Make them look ready
        
        cursor.execute('''
            INSERT INTO schedules (target_date, store_name, image_id, text_id, status, store_id, client_id, post_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (target_date, store_name, img_id, text_id, status, store_id, 1, "フィード"))
        
    conn.commit()
    conn.close()
    print("Seikotsuin data injection complete.")

if __name__ == "__main__":
    inject_seikotsuin_data()
