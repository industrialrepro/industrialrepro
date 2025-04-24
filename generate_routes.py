
import requests
import os
from datetime import datetime
from pytz import timezone

# 建立資料夾
os.makedirs("Dou", exist_ok=True)

# 設定今天日期（台灣時間）
tz = timezone('Asia/Taipei')
now = datetime.now(tz)
today = now.strftime("%Y/%m/%d")

# 讀取 API
res = requests.get("https://sheet2api.com/v1/XeqEedOPStOM/%25E5%25BE%2585%25E6%258B%259C%25E8%25A8%25AA%25E5%25AE%25A2%25E6%2588%25B6%25E6%25B8%2585%25E5%2596%25AE")
data = res.json()

# 過濾符合條件資料（今天要拜訪 或 是否優先 = 是），完成日期為空
rows = []
for row in data:
    if not isinstance(row, dict):
        continue
    if row.get("完成日期"):
        continue
    if row.get("指定拜訪日") == today or row.get("是否優先") == "是":
        rows.append(row)

# 分級排序
grade_order = {"A": 1, "B": 2, "C": 3, "D": 4}
rows.sort(key=lambda x: grade_order.get(x.get("分級", "").strip().upper(), 99))

# 分組（每組3人，每日最多2組）
groups = [rows[i:i+3] for i in range(0, min(len(rows), 6), 3)]

# HTML 產出
html = '''
<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="UTF-8">
<title>睦聚工業地產 - 今日拜訪行程</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {font-family: sans-serif; background: #f9f9f9; color: #333;}
.card {background: white; border-radius: 8px; margin: 1em auto; padding: 1em; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 500px;}
.card h3 {margin-top: 0; color: #0066cc;}
a {color: #0066cc;} h1 {text-align:center;}
footer {text-align:center; padding:1em; color:#999;}
</style></head><body>
<h1>今日拜訪行程</h1>
'''

if not groups:
    html += "<p style='text-align:center; color: #666;'>今日尚無需拜訪客戶，請查看名單是否已更新。</p>"

for idx, group in enumerate(groups, start=1):
    html += f'<h2>第{idx}組</h2>'
    for row in group:
        html += f'''
        <div class="card">
          <h3>{row.get("公司名稱", "")}</h3>
          <p><strong>客戶名稱：</strong>{row.get("客戶名稱", "")}</p>
          <p><strong>地址：</strong>{row.get("住址", "")}</p>
          <p><strong>目的：</strong>{row.get("主要目的", "（尚未填寫）")}</p>
          <p><strong>重要資訊：</strong>{row.get("重要資訊", "（無）")}</p>
          <a href="https://www.google.com/maps/search/?api=1&query={row.get("住址", "")}" target="_blank">打開地圖導航</a>
        </div>
        '''

html += f'<footer>本頁面由睦聚工業地產自動產出，產生時間：{now.strftime("%Y-%m-%d %H:%M:%S")}</footer></body></html>'

# 儲存
with open("Dou/routes.html", "w", encoding="utf-8") as f:
    f.write(html)
