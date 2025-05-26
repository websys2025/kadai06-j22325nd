import requests
import pandas as pd

# ------------------------------------------------------------
# kadai6-1.py
#
# 使用するオープンデータ:
#   - 総務省統計局 e-Stat API の「労働力調査（基本集計）」
#
# エンドポイント概要:
#   - API種別: e-Stat 統計データ提供API v3.0
#   - URL: https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData
#   - データID : 0003102935（労働力調査（基本集計））
#   - 内容: 年齢・性別などに分かれた就業者数、失業者数、労働力人口などの統計
#
# 使い方:
#   - スクリプトを実行すると、労働力調査のデータをJSONで取得し、
#     pandas の DataFrame に整形して表示する。
#   - 出力データには地域、分類、年齢階級などの人が読める分類名称も含まれる。
#
# ------------------------------------------------------------

# アプリケーションID
APP_ID = "8f8c4c81413355f9f7b0de584a68958a4d64bc36"

# APIエンドポイント
API_URL = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

# APIリクエストパラメータ（労働力調査（基本集計））
params = {
    "appId": APP_ID,
    "statsDataId": "0003102935",  # 労働力調査（基本集計）
    "metaGetFlg": "Y",
    "cntGetFlg": "N",
    "explanationGetFlg": "Y",
    "annotationGetFlg": "Y",
    "sectionHeaderFlg": "1",
    "replaceSpChars": "0",
    "lang": "J"
}

# APIへリクエスト送信
response = requests.get(API_URL, params=params)
data = response.json()

# 統計データの VALUE 部分を取り出して DataFrame に変換
values = data['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']
df = pd.DataFrame(values)

# メタ情報の取得と名称への変換
meta_info = data['GET_STATS_DATA']['STATISTICAL_DATA']['CLASS_INF']['CLASS_OBJ']
for class_obj in meta_info:
    column_name = '@' + class_obj['@id']
    id_to_name_dict = {}

    if isinstance(class_obj['CLASS'], list):
        for obj in class_obj['CLASS']:
            id_to_name_dict[obj['@code']] = obj['@name']
    else:
        id_to_name_dict[class_obj['CLASS']['@code']] = class_obj['CLASS']['@name']

    df[column_name] = df[column_name].replace(id_to_name_dict)

# 列名変換の辞書を作成して適用
col_replace_dict = {'@unit': '単位', '$': '値'}
for class_obj in meta_info:
    org_col = '@' + class_obj['@id']
    new_col = class_obj['@name']
    col_replace_dict[org_col] = new_col

df.columns = [col_replace_dict.get(col, col) for col in df.columns]

# 結果出力
print(df)
