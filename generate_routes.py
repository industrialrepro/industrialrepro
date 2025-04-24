
import requests
from datetime import datetime
from pytz import timezone

# 讀取 Sheet2API 名單資料
url = "https://sheet2api.com/v1/XeqEedOPStOM/%25E5%25BE%2585%25E6%258B%259C%25E8%25A8%25AA%25E5%25AE%25A2%25E6%2588%25B6%25E6%25B8%2585%25E5%2596%25AE"
res = requests.get(url)
data = res.json()

# 過濾資料，排除未填寫完整的資料列
def is_valid(row):
    return all(row.get(k, "").strip() for k in ["公司名稱", "地址", "主要目的"])

filtered = list(filter(is_valid, data))
sorted_data = sorted(filtered, key=lambda r: r.get("分級", "Z"))[:6]

# 產出行程區塊
now = datetime.now(timezone("Asia/Taipei")).strftime("%Y-%m-%d %H:%M:%S")
cards = ""
for row in sorted_data:
    addr = row.get("地址", "")
    maps_url = f"https://www.google.com/maps/search/?api=1&query={addr}"
    cards += f"""
    <div class='card'>
      <p><strong>公司名稱：</strong>{row.get("公司名稱", "")}</p>
      <p><strong>客戶名稱：</strong>{row.get("客戶名稱", "")}</p>
      <p><strong>重要資訊：</strong>{row.get("重要資訊", "")}</p>
      <p><strong>主要目的：</strong>{row.get("主要目的", "")}</p>
      <p><strong>地址：</strong><a href='{maps_url}' target='_blank'>{addr}</a></p>
    </div>
    """

if not cards:
    cards = "<p style='text-align:center;color:gray'>⚠️ 今日沒有符合條件的拜訪對象</p>"

# 包裝 HTML 完整頁面
html = f"""
<!DOCTYPE html>
<html lang='zh-Hant'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>今日拜訪行程</title>
  <style>
    body {{ font-family: 'Microsoft JhengHei'; padding: 1em; background: #f7f7f7; }}
    h1 {{ text-align: center; }}
    .desc {{ text-align: center; font-size: 0.9em; color: gray; margin-bottom: 1em; }}
    .card {{ background: white; border-radius: 12px; padding: 1em; margin: 1em auto; max-width: 600px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }}
    a {{ color: #3367d6; text-decoration: none; }}
  </style>
</head>
<body>
  <h1>今日拜訪行程</h1>
  <p class='desc'>本頁面由睦聚工業地產自動產出，產生時間：{now}</p>
  {cards}
</body>
</html>
"""

# 儲存 HTML 頁面
with open("routes.html", "w", encoding="utf-8") as f:
    f.write(html)
