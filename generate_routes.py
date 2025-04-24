import requests

# 從 Sheet2API 讀取資料
import json

res = requests.get("https://sheet2api.com/v1/XeqEedOPStOM/%25E5%25BE%2585%25E6%258B%259C%25E8%25A8%25AA%25E5%25AE%25A2%25E6%2588%25B6%25E6%25B8%2585%25E5%2596%25AE")

# 印出 API 回傳內容
print("API 回傳內容：")
print(res.text)
exit()


rows = [row for row in data if not row.get("完成日期")]

# 排序並分組
rows = sorted(rows, key=lambda x: x.get("分級", "Z"))
groups = [rows[i:i+3] for i in range(0, min(len(rows), 6), 3)]

# 開始產出 HTML
html = '''
<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="UTF-8">
<title>睦聚工業地產 - 今日拜訪行程</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {font-family: sans-serif; background: #f9f9f9; color: #333;}
.card {background: white; border-radius: 8px; margin: 1em; padding: 1em; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
.card h3 {margin-top: 0;} a {color: #0066cc;}
</style></head><body>
<h1 style="text-align:center;">今日拜訪行程</h1>
'''

for idx, group in enumerate(groups, start=1):
    html += f'<h2>第{idx}組</h2>'
    for row in group:
        html += f'''
        <div class="card">
          <h3>{row.get("公司名稱", "")}</h3>
          <p><strong>地址：</strong>{row.get("住址", "")}</p>
          <p><strong>目的：</strong>{row.get("主要目的", "（尚未填寫）")}</p>
          <a href="https://www.google.com/maps/search/?api=1&query={row.get("住址", "")}" target="_blank">打開地圖導航</a>
        </div>
        '''

html += '<footer style="text-align:center; padding:1em; color:#999;">本頁面由睦聚工業地產自動產出</footer></body></html>'

# 儲存到 Dou/routes.html
with open("Dou/routes.html", "w", encoding="utf-8") as f:
    f.write(html)
