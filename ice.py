import requests
from bs4 import BeautifulSoup
import pandas as pd

# 対象のURL
url = 'https://www.ksp-sp.com/open_data/ranking/2025/202521.html'  # ← 14週などに変更可
res = requests.get(url)
res.encoding = 'shift_jis'  # 明示的に文字コード指定（文字化け対策）

soup = BeautifulSoup(res.text, 'html.parser')

# アイスクリーム・デザート類セクションを探す
ice_section = None
for tag in soup.find_all(['h2', 'h3', 'h4', 'h5']):
    if tag.text and 'アイスクリーム' in tag.text:
        ice_section = tag
        break

if not ice_section:
    raise ValueError("❌ アイスクリームのセクションが見つかりません")

# アイスクリーム表を取得
ice_table = ice_section.find_next('table')

# データ抽出
data = []
rows = ice_table.find_all('tr')[1:]
for row in rows:
    name_td = row.find('td', class_='col7')
    pi_td = row.find('td', class_='col5')
    if name_td and pi_td:
        name = name_td.text.strip()
        pi = pi_td.text.strip().replace(',', '')
        data.append({
            '商品名': name,
            '金額PI': pi
        })

# 保存
df = pd.DataFrame(data)
df.to_csv('21.csv', index=False, encoding='utf-8-sig')
print("✅ icecream_week14.csv を出力しました")
