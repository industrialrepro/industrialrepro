import requests
from datetime import datetime

API_URL = "https://sheet2api.com/v1/XeqEedOPStOM/%25E5%25BE%2585%25E6%258B%259C%25E8%25A8%25AA%25E5%25AE%25A2%25E6%2588%25B6%25E6%25B8%2585%25E5%2596%25AE"
OUTPUT_FILE = "routes.html"

# 分級優先順序
GRADE_ORDER = {"A": 1, "B": 2, "C": 3, "D": 4}

# 取得資料
def fetch_data():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

# 過濾並排序資料
def filter_and_sort(data):
    valid_entries = [
        row for row in data
        if row.get("分級") in GRADE_ORDER and row.get("地址")
    ]
    sorted_entries = sorted(valid_entries, key=lambda x: GRADE_ORDER[x["分級"]])
    return sorted_entries[:6]

# 產生 HTML 內容
def generate_html(entries):
    today = datetime.now().strftime("%Y/%m/%d")
    html = [
        f"<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>",
        f"<title>{today} 拜訪行程</title>",
        f"<style>body{{font-family:'Microsoft JhengHei';padding:20px;line-height:1.6}} .entry{{margin-bottom:30px}} .note{{color:gray}}</style></head><body>",
        f"<h2>{today} 拜訪行程</h2>"
    ]

    if not entries:
        html.append("<p>⚠️今日沒有符合條件的拜訪對象</p>")
    else:
        for i, entry in enumerate(entries, 1):
            html.append("<div class='entry'>")
            html.append(f"<strong>第{i}站</strong><br>")
            if entry.get("公司名稱"):
                html.append(f"公司名稱：{entry['公司名稱']}<br>")
            if entry.get("客戶名稱"):
                html.append(f"客戶名稱：{entry['客戶名稱']}<br>")
            if entry.get("重要資訊"):
                html.append(f"重要資訊：{entry['重要資訊']}<br>")
            if entry.get("主要目的"):
                html.append(f"主要目的：{entry['主要目的']}<br>")
            if entry.get("地址"):
                map_link = f"https://www.google.com/maps/search/?api=1&query={entry['地址']}"
                html.append(f"地址：<a href='{map_link}' target='_blank'>{entry['地址']}</a><br>")
            html.append("</div>")

    html.append("</body></html>")
    return "\n".join(html)

# 主程式
if __name__ == "__main__":
    try:
        raw_data = fetch_data()
        today_entries = filter_and_sort(raw_data)
        html_content = generate_html(today_entries)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(html_content)

        print("✅ routes.html 已成功產出")
    except Exception as e:
        print("❌ 發生錯誤：", str(e))
