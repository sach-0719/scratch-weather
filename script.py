import os
import requests
import scratchattach as sa

def main():
    print("========================================================")
    print("🚀 Scratch Weather Bot - 処理を開始します")
    print("========================================================")

    # 🔐 1. 環境変数の読み込み（セッションIDではなくパスワードを使用）
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    username = os.environ.get("SCRATCH_USERNAME")
    password = os.environ.get("SCRATCH_PASSWORD") # 👈 パスワードを追加
    project_id = os.environ.get("SCRATCH_PROJECT_ID")

    missing_secrets = []
    if not api_key: missing_secrets.append("OPENWEATHER_API_KEY")
    if not username: missing_secrets.append("SCRATCH_USERNAME")
    if not password: missing_secrets.append("SCRATCH_PASSWORD")
    if not project_id: missing_secrets.append("SCRATCH_PROJECT_ID")

    if missing_secrets:
        print(f"❌【設定エラー】環境変数が不足しています: {', '.join(missing_secrets)}")
        return

    # 🌤️ 2. OpenWeatherMapから天気データの取得
    city_name = "Tokyo"
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric",
        "lang": "ja"
    }

    try:
        print(f"📡 OpenWeatherMapから {city_name} の天気を取得中...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        weather_id = int(data["weather"][0]["id"])
        temp = int(round(data["main"]["temp"]))
        weather_desc = data["weather"][0]["description"]
        
        print(f"✨【天気取得成功】")
        print(f"   ・現在の天気: {weather_desc} (天気ID: {weather_id})")
        print(f"   ・現在の気温: {temp} ℃")
        
    except Exception as e:
        print(f"❌【エラー】OpenWeatherMapからの天気取得に失敗しました: {e}")
        return

    # 🐱 3. パスワード認証でScratchにログイン＆書き込み
    try:
        print(f"🔑 パスワードを使って Scratch アカウント（{username}）にログイン中...")
        # sa.login_by_id の代わりに sa.login を使用します
        session = sa.login(username, password)
        
        print(f"☁️ Scratchプロジェクト（ID: {project_id}）のクラウドに接続中...")
        cloud = session.connect_cloud(project_id)
        
        print("📤 データを送信中...")
        cloud.set_var("weather_id", str(weather_id))
        print(f"   ➡️ weather_id を 【{weather_id}】 に更新")
        
        cloud.set_var("temperature", str(temp))
        print(f"   ➡️ temperature を 【{temp}】 に更新")
        
        print("🎉【すべての処理が正常に完了しました！】")
        
    except Exception as e:
        print(f"❌【エラー】Scratchへの接続・書き込みに失敗しました: {e}")

if __name__ == "__main__":
    main()
