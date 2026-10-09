import os
import requests
import scratchattach as sa

def main():
    print("========================================================")
    print("🚀 Scratch Weather Bot - 処理を開始します")
    print("========================================================")

    # ========================================================
    # 🔐 1. 全ての設定を環境変数から安全に読み込む（完全な隠蔽）
    # ========================================================
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    username = os.environ.get("SCRATCH_USERNAME")
    session_id = os.environ.get("SCRATCH_SESSION_ID")
    project_id = os.environ.get("SCRATCH_PROJECT_ID")

    # 必須の設定が揃っているか厳重にチェック
    missing_secrets = []
    if not api_key: missing_secrets.append("OPENWEATHER_API_KEY")
    if not username: missing_secrets.append("SCRATCH_USERNAME")
    if not session_id: missing_secrets.append("SCRATCH_SESSION_ID")
    if not project_id: missing_secrets.append("SCRATCH_PROJECT_ID")

    if missing_secrets:
        print(f"❌【設定エラー】GitHubのSecretsに必要な設定が足りません: {', '.join(missing_secrets)}")
        return

    # ========================================================
    # 🌤️ 2. OpenWeatherMapから「東京」の天気を取得
    # ========================================================
    city_name = "Tokyo"
    # 👇 ここを以下の形に書き換えます（f-stringを使わず、間違いを防ぐ形にします）
    url = "https://openweathermap.org"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric",  # 👈 ここがバグの原因です（最初の " が抜けています）
        "lang": "ja"
    }

    try:
        print(f"📡 OpenWeatherMapから {city_name} の天気を取得中...")
        response = requests.get(url, params=params) # 👈 params=params を追加
        response.raise_for_status()
        data = response.json()

        # 3桁の天気IDと、整数にした気温を取得
        weather_id = data["weather"][0]["id"] # 配列の1番目から正確に取得
        temp = int(data["main"]["temp"])       
        weather_desc = data["weather"][0]["description"]
        
        print(f"✨【天気取得成功】")
        print(f"  ・現在の天気: {weather_desc} (天気ID: {weather_id})")
        print(f"  ・現在の気温: {temp} ℃")
        
    except Exception as e:
        print(f"❌【エラー】OpenWeatherMapからの天気取得に失敗しました: {e}")
        return

    # ========================================================
    # 🐱 3. セッションIDを使ってScratchのクラウド変数に送信
    # ========================================================
    try:
        print(f"🔑 セッションIDを使ってScratchアカウント（{username}）に認証中...")
        session = sa.login_by_id(session_id, username=username)
        
        print(f"☁️ Scratchプロジェクト（ID: {project_id}）のクラウド変数に接続中...")
        cloud = session.connect_cloud(project_id)
        
        # Scratchのクラウド変数を更新
        print("📤 データを送信中...")
        cloud.set_var("weather_id", weather_id)
        print(f"  ➡️ ☁ weather_id を 【{weather_id}】 に書き換えました")
        
        cloud.set_var("temperature", temp)
        print(f"  ➡️ ☁ temperature を 【{temp}】 に書き換えました")
        
        print("🎉【すべての処理が正常に完了しました！】")
        
    except Exception as e:
        print(f"❌【エラー】Scratchへの書き込みに失敗しました: {e}")
        print("💡 対策: scratchsessionsidの有効期限が切れていないか、アカウントが『Scratcher』権限を持っているか確認してください。")

if __name__ == "__main__":
    main()
