name: 每日自動更新拜訪行程頁

on:
  schedule:
    - cron: '0 2 * * *'  # 台灣時間 10:00（UTC+8 → UTC 2:00）
  workflow_dispatch:

jobs:
  generate:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests pytz

    - name: Generate routes.html
      run: python generate_routes.py

    - name: Commit changes
      run: |
        git config --global user.name "github-actions"
        git config --global user.email "github-actions@users.noreply.github.com"
        git pull --rebase origin main || true
        git add routes.html
        git commit -m "每日自動更新拜訪行程頁" || echo "No changes to commit"

    - name: Push updates
      run: |
        git push origin main || echo "Push failed"
