import requests
import pandas as pd

# ------------------------------------------------------------
# kadai6-2.py
#
# 使用するオープンデータ:
#   - 気象庁が公開している天気予報JSONデータ
#   - URL: https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json
#
# 使用方法:
#   1. 本スクリプトを実行すると、東京都の天気予報データを取得。
#   2. 地域名・予報時刻・天気内容を整形して pandas のDataFrameとして表示。
#
# エンドポイント概要:
#   - API形式: JSON 
#   - 地域コード: 130000（東京都）
#   - 提供内容: 複数のエリアの、時刻ごとの天気、降水確率、気温などの予報情報
#
# ------------------------------------------------------------

# APIエンドポイント（東京の天気予報）
API_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json"

# APIへGETリクエスト送信
response = requests.get(API_URL)
data = response.json()

# 最初のエリア（東京地方）の天気予報データを取得
tokyo_area = data[0]
time_series = tokyo_area["timeSeries"][0]  # 時系列データ（天気予報）
areas = time_series["areas"]

# エリアごとの予報をDataFrameに変換
records = []
for area in areas:
    area_name = area["area"]["name"]
    weathers = area["weathers"]
    times = time_series["timeDefines"]

    for time, weather in zip(times, weathers):
        records.append({
            "地域": area_name,
            "予報時刻": time,
            "天気": weather
        })

df = pd.DataFrame(records)

# 結果出力
print(df)
