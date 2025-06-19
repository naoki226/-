import pandas as pd
import unicodedata
from collections import defaultdict

# CSVファイルとして読み込む
df_excel = pd.read_csv("ice_特徴.csv", usecols=[0], nrows=1100, encoding="utf-8")
product_names = df_excel.iloc[:, 0].dropna().astype(str).tolist()

# 行判定関数（小文字・促音・拗音・清濁半濁対応）
def get_row(ch):
    table = {
        'ア': 'あ行', 'イ': 'あ行', 'ウ': 'あ行', 'エ': 'あ行', 'オ': 'あ行',
        'カ': 'か行', 'キ': 'か行', 'ク': 'か行', 'ケ': 'か行', 'コ': 'か行',
        'ガ': 'が行', 'ギ': 'が行', 'グ': 'が行', 'ゲ': 'が行', 'ゴ': 'が行',
        'サ': 'さ行', 'シ': 'さ行', 'ス': 'さ行', 'セ': 'さ行', 'ソ': 'さ行',
        'ザ': 'ざ行', 'ジ': 'ざ行', 'ズ': 'ざ行', 'ゼ': 'ざ行', 'ゾ': 'ざ行',
        'タ': 'た行', 'チ': 'た行', 'ツ': 'た行', 'テ': 'た行', 'ト': 'た行',
        'ダ': 'だ行', 'ヂ': 'だ行', 'ヅ': 'だ行', 'デ': 'だ行', 'ド': 'だ行',
        'ナ': 'な行', 'ニ': 'な行', 'ヌ': 'な行', 'ネ': 'な行', 'ノ': 'な行',
        'ハ': 'は行', 'ヒ': 'は行', 'フ': 'は行', 'ヘ': 'は行', 'ホ': 'は行',
        'バ': 'ば行', 'ビ': 'ば行', 'ブ': 'ば行', 'ベ': 'ば行', 'ボ': 'ば行',
        'パ': 'ぱ行', 'ピ': 'ぱ行', 'プ': 'ぱ行', 'ペ': 'ぱ行', 'ポ': 'ぱ行',
        'マ': 'ま行', 'ミ': 'ま行', 'ム': 'ま行', 'メ': 'ま行', 'モ': 'ま行',
        'ヤ': 'や行', 'ユ': 'や行', 'ヨ': 'や行',
        'ラ': 'ら行', 'リ': 'ら行', 'ル': 'ら行', 'レ': 'ら行', 'ロ': 'ら行',
        'ワ': 'わ行', 'ヲ': 'わ行', 'ン': 'ん',
        'ァ': 'あ行', 'ィ': 'あ行', 'ゥ': 'あ行', 'ェ': 'あ行', 'ォ': 'あ行',
        'ャ': 'や行', 'ュ': 'や行', 'ョ': 'や行',
        'ッ': 'た行',
        'ヴ': 'ゔ行'
    }
    return table.get(unicodedata.normalize('NFKC', ch))

# 割合計算
results = []
for name in product_names:
    counts = defaultdict(int)
    total = 0
    for ch in name:
        row = get_row(ch)
        if row:
            counts[row] += 1
            total += 1
    result = {row: round(cnt / total * 100, 1) for row, cnt in counts.items()}
    result['商品名'] = name
    results.append(result)

# DataFrameに整形
order = ['あ行', 'か行', 'さ行', 'た行', 'な行', 'は行', 'ま行', 'や行', 'ら行', 'わ行',
         'が行', 'ざ行', 'だ行', 'ば行', 'ぱ行', 'ん', 'ゔ行']
df = pd.DataFrame(results).fillna(0)
df = df[['商品名'] + [col for col in order if col in df.columns]]

# CSVに出力
df.to_csv("product_kana_ratio.csv", index=False, encoding="utf-8-sig")
print("✅ product_kana_ratio.csv に保存しました。")
