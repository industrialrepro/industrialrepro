
import requests
import datetime
from pytz import timezone

# 抓取資料
url = "https://sheet2api.com/v1/XeqEedOPStOM/%25E5%25BE%2585%25E6%258B%259C%25E8%25A8%25AA%25E5%25AE%25A2%25E6%2588%25B6%25E6%25B8%2585%25E5%2596%25AE"
res = requests.get(url)
data = res.json()

# 過濾未完成者，依分級排序 A > B > C...
targets = [row for row in data if not row.get("完成日期")]
sorted_targets = sorted(targets, key=lambda x: x.get("分級", "Z"))
today_targets = sorted_targets[:6]

# 當前台灣時間
now = datetime.datetime.now(timezone("Asia/Taipei")).strftime("%Y-%m-%d %H:%M:%S")

# HTML 區塊
blocks = []
for row in today_targets:
    address = row.get("地址", "").strip()
    if address:
        address_html = f'<a href="https://www.google.com/maps/search/?api=1&query={address}" target="_blank">{address}</a>'
    else:
        address_html = ""
    block = f"""
<div style='background:#fff;border-radius:16px;padding:20px;margin-bottom:20px;box-shadow:0 2px 6px rgba(0,0,0,0.1)'>
    <p><strong>公司名稱:</strong> {row.get("公司名稱", "")}</p>
    <p><strong>客戶名稱:</strong> {row.get("客戶名稱", "")}</p>
    <p><strong>重要資訊:</strong> {row.get("重要資訊", "")}</p>
    <p><strong>主要目的:</strong> {row.get("主要目的", "")}</p>
    <p><strong>地址:</strong> {address_html}</p>
</div>
"""
    blocks.append(block)

html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <title>今日拜訪行程</title>
</head>
<body style="font-family:sans-serif;background:#f9f9f9;margin:0;padding:40px">
    <h1 style="text-align:center;color:#333">今日拜訪行程</h1>
    <p style="text-align:center;color:#888;font-size:14px">本頁面由睦聚工業地產自動產出，產生時間: {now}</p>
    <div style="max-width:600px;margin:40px auto">
        {''.join(blocks)}
    </div>
</body>
</html>
"""

with open("Dou/routes.html", "w", encoding="utf-8") as f:
    f.write(html)
