import os
import requests
import scratchattach as sa

def main():
    # ========================================================
    # 🔐 1. 環境変数から安全に各キーやIDを読み込む
    # ========================================================
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    username = os.environ.get("SCRATCH_USERNAME")
    session_id = os.environ.get("SCRATCH_SESSION_ID") # 👈 セッションID
    
    # ⚠️ ここにご自身のScratchのプロジェクトID（URLの数字）を入れてください
    project_id = "123456789" 

    if not api_key or not username or not session_id:
        print("【エラー】GitHubのSecretsに必要な設定が見つかりません。")
        return

    # ========================================================
    # 🌤️ 2. OpenWeatherMapから「東京」の天気を取得
    # ========================================================
    city_name = "Tokyo"
    url = f"https://openweathermap.org{city_name}&appid={api_key}&units=metric&lang=ja"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # 3桁の天気IDと、整数にした気温を取得
        weather_id = data["weather"][0]["id"] 
        temp = int(data["main"]["temp"])       
        weather_desc = data["weather"][0]["description"]
        
        print(f"【天気取得成功】都市: {city_name}")
        print(f"天気ID: {weather_id} ({weather_desc}) / 気温: {temp}℃")
        
    except Exception as e:
        print(f"【エラー】OpenWeatherMapからの天気取得に失敗しました: {e}")
        return

    # ========================================================
    # 🐱 3. セッションIDを使ってScratchのクラウド変数に送信
    # ========================================================
    try:
        print("セッションIDを使ってScratchに認証中...")
        # 🔑 パスワード認証の代わりに、セッションIDとユーザー名でログインします
        session = sa.login_by_id(session_id, username=username)
        cloud = session.connect_cloud(project_id)
        
        # ☁ Scratchのクラウド変数を更新
        cloud.set_var("weather_id", weather_id)
        cloud.set_var("temperature", temp)
        
        print("【Scratch連携成功】クラウド変数を正常に更新しました！")
        
    except Exception as e:
        print(f"【エラー】Scratchへの書き込みに失敗しました: {e}")
        print("※セッションIDの有効期限が切れていないか確認してください。")

if __name__ == "__main__":
    main()
