
import requests
from datetime import datetime
from pytz import timezone

url = "https://sheet2api.com/v1/XeqEedOPStOM/%E5%BE%85%E6%8B%9C%E8%A8%AA%E5%AE%A2%E6%88%B6%E6%B8%85%E5%96%AE"
response = requests.get(url)
data = response.json()

# 過濾未完成資料（今天尚未完成拜訪）
today = datetime.now(timezone('Asia/Taipei')).date().isoformat()
pending = [row for row in data if not row.get("完成日期")]

# 分級排序 + 是否優先
grade_order = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6}
pending.sort(key=lambda row: (
    grade_order.get(row.get("分級", "Z"), 99),
    0 if row.get("是否優先") == "是" else 1
))

# 每日拜訪數量
num_per_day = 3
today_tasks = pending[:num_per_day]

html = f"""
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>今日拜訪行程</title>
    <style>
        body {{ font-family: '微軟正黑體', sans-serif; padding: 2em; background: #f5f5f5; }}
        h1 {{ text-align: center; color: #333; }}
        .card {{
            background: white;
            padding: 1em;
            margin: 1em auto;
            border-radius: 12px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            max-width: 600px;
        }}
        .card p {{ margin: 0.3em 0; }}
        .footer {{ text-align: center; margin-top: 2em; color: #888; font-size: 0.9em; }}
        a.address-link {{ color: #0645AD; text-decoration: none; }}
    </style>
</head>
<body>
    <h1>今日拜訪行程</h1>
    <div class="footer">本頁面由睦聚工業地產自動產出，產生時間：{datetime.now(timezone('Asia/Taipei')).strftime('%Y-%m-%d %H:%M:%S')}</div>
"""

for row in today_tasks:
    company = row.get("公司名稱", "")
    client = row.get("客戶名稱", "")
    info = row.get("重要資訊", "")
    purpose = row.get("主要目的", "")
    address = row.get("住址", "")
    maps_link = f"https://www.google.com/maps/search/?api=1&query={address}"

    html += f"""
    <div class="card">
        <p><strong>公司名稱：</strong>{company}</p>
        <p><strong>客戶名稱：</strong>{client}</p>
        <p><strong>重要資訊：</strong>{info}</p>
        <p><strong>主要目的：</strong>{purpose}</p>
        <p><strong>地址：</strong><a class="address-link" href="{maps_link}" target="_blank">{address}</a></p>
    </div>
    """

html += "</body></html>"

# 輸出至路徑
with open("Dou/routes.html", "w", encoding="utf-8") as f:
    f.write(html)
