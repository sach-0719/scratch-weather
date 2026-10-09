import os
import requests
import scratchattach as sa

def main():
    # ========================================================
    # 🔐 1. 環境変数から安全に秘密のキーやパスワードを読み込む
    # ========================================================
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    username = os.environ.get("SCRATCH_USERNAME")
    password = os.environ.get("SCRATCH_PASSWORD")
    
    # ⚠️ ここに先ほど作成したScratchのプロジェクトID（URLの数字）を入れてください
    project_id = "123456789" 

    # 環境変数が正しく設定されているかチェック
    if not api_key or not username or not password:
        print("【エラー】GitHubのSecretsに必要な設定（APIキーやパスワードなど）が見つかりません。")
        return

    # ========================================================
    # 🌤️ 2. OpenWeatherMapから「東京」の天気を取得
    # ========================================================
    city_name = "Tokyo"
    url = f"https://openweathermap.org{city_name}&appid={api_key}&units=metric&lang=ja"

    try:
        response = requests.get(url)
        response.raise_for_status() # エラーがあれば例外を発生させる
        data = response.json()
        
        weather_id = data["weather"][0]["id"] # 3桁の天気ID（例: 800=晴れ、500=雨）
        temp = int(data["main"]["temp"])       # 気温（小数点以下を切り捨てて整数にする）
        weather_desc = data["weather"][0]["description"] # 日本語の天気説明
        
        print(f"【天気取得成功】都市: {city_name}")
        print(f"天気ID: {weather_id} ({weather_desc}) / 気温: {temp}℃")
        
    except Exception as e:
        print(f"【エラー】OpenWeatherMapからの天気取得に失敗しました: {e}")
        return

    # ========================================================
    # 🐱 3. scratchattachを使ってScratchのクラウド変数に送信
    # ========================================================
    try:
        print("Scratchへのログインを試みています...")
        session = sa.login(username, password)
        cloud = session.connect_cloud(project_id)
        
        # ☁ Scratchのクラウド変数「weather_id」に、3桁の天気IDを書き込む
        cloud.set_var("weather_id", weather_id)
        print(f"-> クラウド変数『weather_id』を 【{weather_id}】 に更新しました。")
        
        # ☁ Scratchのクラウド変数「temperature」に、気温を書き込む
        cloud.set_var("temperature", temp)
        print(f"-> クラウド変数『temperature』を 【{temp}】 に更新しました。")
        
        print("【Scratch連携成功】すべてのクラウド変数を正常に更新しました！")
        
    except Exception as e:
        print(f"【エラー】Scratchへの書き込みに失敗しました: {e}")
        print("※アカウントが『Scratcher』の権限を持っているか、プロジェクトIDが正しいか確認してください。")

if __name__ == "__main__":
    main()
