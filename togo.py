import pandas as pd
import re
import unicodedata

def extract_features(name):
    # 空白・改行・タブを削除（全角・半角ともに）
    name_clean = re.sub(r'[\s\u3000]', '', name)  # \u3000 は全角スペース

    hira_count = sum(1 for ch in name_clean if 'ぁ' <= ch <= 'ん')
    kata_count = sum(1 for ch in name_clean if ('ァ' <= ch <= 'ヶ') or ch == 'ー')  # 長音「ー」もカタカナに含める
    kanji_count = sum(1 for ch in name_clean if unicodedata.name(ch, '').startswith('CJK UNIFIED'))
    number_count = sum(1 for ch in name_clean if ch.isdigit())

    total_chars = len(name_clean)
    other_count = total_chars - hira_count - kata_count - kanji_count - number_count

    def ratio(count):
        return count / total_chars if total_chars > 0 else 0

    has_number = int(number_count > 0)

    types = []
    if hira_count > 0:
        types.append('ひ')
    if kata_count > 0:
        types.append('カ')
    if kanji_count > 0:
        types.append('漢')
    if other_count > 0:
        types.append('記')

    return {
        '文字数': total_chars,
        'ひらがな比率': ratio(hira_count),
        'カタカナ比率': ratio(kata_count),
        '漢字比率': ratio(kanji_count),
        '記号等比率': ratio(other_count),
        '数字を含む': has_number,
        '構成タイプ': '+'.join(types)
    }

# データ読み込みと処理
df = pd.read_csv('1~22.csv')
features = df['商品名'].apply(extract_features)
features_df = pd.DataFrame(features.tolist())
result_df = pd.concat([df, features_df], axis=1)

# 保存
result_df.to_csv('ice_特徴.csv', index=False, encoding='utf-8-sig')
print("✅ 空白除去＆特徴抽出済 → ice_product_features_cleaned.csv")