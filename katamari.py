import pandas as pd
import re
from collections import Counter

# CSV読み込み（A列に商品名がある前提）
df = pd.read_csv("ice_特徴.csv", usecols=[0], nrows=1100)
names = df.iloc[:, 0].dropna().astype(str).tolist()

# カタカナ3文字以上のかたまり抽出用の正規表現
katakana_chunk_re = re.compile(r'[ァ-ヴー]{3,}')

# 全ての商品名からカタカナのかたまりを抽出
chunks = []
for name in names:
    chunks += katakana_chunk_re.findall(name)

# 頻度カウント
counter = Counter(chunks)

# 上位50件を表示
top_chunks = counter.most_common(50)
for chunk, count in top_chunks:
    print(f"{chunk}: {count}")