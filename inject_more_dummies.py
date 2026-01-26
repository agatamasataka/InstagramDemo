import sqlite3
import datetime
import random

DB_NAME = "instamanager.db"

STORES = ["渋谷店", "新宿店", "オンライン", "全店舗共通", "大阪店", "名古屋店", "福岡店"]

DUMMY_CONTENTS = [
    {
        "genre": "休日案内",
        "content": """【臨時休業のお知らせ】
誠に勝手ながら、設備点検のため下記日程は臨時休業とさせていただきます。

休業日：2月15日（月）

ご不便をおかけしますが、何卒よろしくお願い申し上げます。
翌日からは通常通り営業いたします🙇‍♂️
#臨時休業 #お知らせ #リフレッシュ"""
    },
    {
        "genre": "スタッフ紹介",
        "content": """＼ 今月のMVPスタッフ！ ／
笑顔が素敵な佐藤さんを紹介します✨
「お客様に最高の体験を！」をモットーに頑張っています。

見かけたらぜひ声をかけてくださいね！
おすすめのメニューも詳しく教えてくれますよ☕️
#スタッフ紹介 #MVP #接客 #ロカオプ"""
    },
    {
        "genre": "キャンペーン",
        "content": """🎁 フォロー＆いいね キャンペーン実施中！
抽選で10名様に「特製ギフトセット」をプレゼント！

＜応募方法＞
1. @locaop_official をフォロー
2. この投稿にいいね❤️
3. コメントで当選確率アップ！？

期間は今月末まで！たくさんのご応募お待ちしております！
#プレゼントキャンペーン #懸賞 #ギフト #フォローキャンペーン"""
    },
    {
        "genre": "日替わりメニュー",
        "content": """今日のランチはこれ！🍛
「彩り野菜のキーマカレー」

たっぷりの野菜とスパイスが食欲をそそります。
数量限定ですのでお早めに！
テイクアウトも可能です🍱
#ランチ #キーマカレー #日替わり #野菜たっぷり"""
    },
    {
        "genre": "新商品",
        "content": """新色登場！🎨
大人気のトートバッグに、春らしい「パステルピンク」が仲間入りしました。

ちょっとしたお出かけにぴったりのサイズ感。
オンラインストアでも販売開始しました✨
プロフィールのリンクからチェックしてください！
#新商品 #トートバッグ #春コーデ #パステルカラー"""
    },
     {
        "genre": "Q&A",
        "content": """Q. 予約は必要ですか？
A. 平日は予約なしでも比較的スムーズにご案内できますが、土日は混雑するため事前予約をおすすめしております📱

Web予約なら24時間受付中！
詳しくはハイライトの「予約」をご覧ください。
#よくある質問 #予約 #Web予約 #混雑状況"""
    },
    {
        "genre": "雨の日特典",
        "content": """☔️ 雨の日サービス実施中
本日は雨のため、ご来店のお客様に「トッピング1品無料」サービスを行います！

足元にお気をつけてお越しください。
温かいスープもご用意してお待ちしております🥣
#雨の日 #雨の日特典 #サービス #トッピング無料"""
    },
    {
        "genre": "裏メニュー",
        "content": """【常連様限定！？】
メニューには載っていない「抹茶アフォガート」🍵
実はスタッフにこっそり注文すると作れるんです...！

この投稿を見た方限定でオーダー解禁します🤫
「インスタ見た」と伝えてくださいね。
#裏メニュー #抹茶スイーツ #アフォガート #秘密"""
    },
    {
        "genre": "採用情報",
        "content": """一緒に働く仲間を募集中！🤝
ロカオプカフェでは、新しいスタッフを募集しています。

・週2日〜OK
・未経験歓迎
・美味しい賄い付き🍛

興味のある方はDMまたはHPからご連絡ください！
#求人 #アルバイト募集 #カフェスタッフ #採用"""
    },
    {
        "genre": "季節の挨拶",
        "content": """もうすぐバレンタインですね🍫
皆様は誰にチョコを渡しますか？

ロカオプではバレンタイン限定の特別なラッピングをご用意しております。
大切な人への贈り物に、ぜひご利用ください🎁
#バレンタイン #ギフトラッピング #贈り物 #季節のイベント"""
    }
]

def inject_more_dummies():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    start_date = datetime.date.today() + datetime.timedelta(days=7) # Start from next week
    
    for i, data in enumerate(DUMMY_CONTENTS):
        # 1. Add Text
        cursor.execute("INSERT INTO texts (content, genre) VALUES (?, ?)", (data["content"], data["genre"]))
        text_id = cursor.lastrowid
        
        # 2. Add Schedule
        # No image linked by default, just empty slots waiting for assignment
        target_date = (start_date + datetime.timedelta(days=i)).isoformat()
        store = random.choice(STORES)
        
        cursor.execute('''
            INSERT INTO schedules (target_date, store_name, image_id, text_id, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (target_date, store, None, text_id, "未完了"))
        
        # Note: We linked the text_id so user doesn't have to pick it, 
        # but in "Materials" view logic we often pick image then text.
        # But here we simulate populated schedule lines that need Images.
        # So text is pre-filled (Status: 未完了 because no image).
        
        print(f"Added Dummy Schedule: {target_date} [{data['genre']}]")

    conn.commit()
    conn.close()
    print("10 more dummy entries injected.")

if __name__ == "__main__":
    inject_more_dummies()
