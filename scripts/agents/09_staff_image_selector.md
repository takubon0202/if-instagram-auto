# 09 - Staff Image Selector（スタッフ画像選択エージェント）

## 役割
投稿のカテゴリ・シーンに最適なスタッフ画像を選択・提案する。

## 入力
- カテゴリID（announcement, development, activity, education, ai_column, business）
- シーン名（cover, content1, content2, content3）
- 投稿トピック（オプション）

## 出力
- 推奨スタッフ
- 画像タイプ
- 画像パス
- 選択理由

## スタッフ一覧

| ID | 名前 | 役割 | 対応カテゴリ |
|----|------|------|--------------|
| inoue_haruto | 井上陽斗 | 講師 | activity, development, education |
| kagaya_yuma | 加賀屋結眞 | 講師 | activity, development, ai_column |
| yamazaki_takumi | 山﨑琢己 | 講師 | activity, development, education |
| watanabe_yuzuki | 渡辺柚気 | 講師 | activity, development, business |
| fujimoto_hinata | 藤本陽向 | 講師 | activity, development, education |
| takasaki_shota | 高崎翔太 | 代表・講師 | 全カテゴリ |

## 画像タイプ

| タイプ | 用途 | 推奨シーン |
|--------|------|------------|
| profile | プロフィール写真 | cover, announcement |
| teaching | 授業風景 | content1, content2, development |
| casual | カジュアル写真 | content3, activity |
| business | ビジネス写真 | announcement, business |

## カテゴリ別選択ルール

### お知らせ（announcement）
- 優先スタッフ: 高崎翔太
- 画像タイプ: business

### 開発物（development）
- 優先スタッフ: 全員からランダム
- 画像タイプ: teaching

### 活動報告（activity）
- 優先スタッフ: 全員からランダム
- 画像タイプ: casual

### 教育コラム（education）
- 優先スタッフ: 高崎翔太
- 画像タイプ: profile

### AIコラム（ai_column）
- 優先スタッフ: 高崎翔太, 加賀屋結眞
- 画像タイプ: casual

### ビジネスコラム（business）
- 優先スタッフ: 高崎翔太
- 画像タイプ: business

## 使用例

```python
from scripts.gemini.staff import StaffImageAgent

agent = StaffImageAgent()

# カテゴリに基づいてスタッフを提案
suggestion = agent.suggest_staff_for_post("ai_column", "Gemini 2.5の使い方")
print(suggestion)
# {
#   "suggested_staff": {"id": "takasaki_shota", "name": "高崎翔太", ...},
#   "image_type": "casual",
#   "image_path": "assets/img/staff/takasaki_shota/casual.png",
#   "reason": "ai_columnカテゴリの優先ルールに基づいて選択"
# }

# シーンに適した画像を取得
image_path = agent.get_image_for_scene("development", "content1")
```

## 画像配置手順

1. Google Driveからスタッフ画像をダウンロード
   - ソース: https://drive.google.com/drive/folders/1CYGZroIXSF6Mkh1ARfM_BPcTSa9FWapV

2. 各スタッフのフォルダに配置
   ```
   assets/img/staff/
   ├── inoue_haruto/
   │   ├── profile.png
   │   ├── teaching.png
   │   └── casual.png
   ├── kagaya_yuma/
   │   └── ...
   └── takasaki_shota/
       ├── profile.png
       ├── teaching.png
       ├── casual.png
       └── business.png
   ```

3. 画像チェック
   ```bash
   python -m scripts.gemini.staff check
   ```

## 注意事項

- 画像が存在しない場合はフォールバック処理
- プライバシーに配慮した画像を使用
- 本人の許可を得た画像のみ使用
