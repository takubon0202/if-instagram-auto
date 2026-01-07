# 12 - Image Generator（画像生成エージェント）

## 役割
Gemini 3 Pro Image Preview を使用して、if塾のInstagram投稿用画像を生成する。

## モデル
`gemini-3-pro-image-preview`

## 入力
- カテゴリID（announcement, development, activity, education, ai_column, business）
- シーン情報（scene_id, headline, subtext）
- 投稿ID

## 出力
- PNG画像（1K解像度、4:5比率）
- 画像パス（assets/img/posts/{post_id}-{scene_id:02d}.png）

## 画像仕様

| 項目 | 値 |
|------|-----|
| モデル | gemini-3-pro-image-preview |
| 解像度 | 1K |
| アスペクト比 | 4:5（Instagram縦長投稿） |
| 言語 | 日本語 |
| リトライ | 最大3回 |

## if塾ロゴ

生成される全ての画像には右下にif塾ロゴが配置されます：

```
【ロゴ仕様】
- 黒いモニターフレーム内にオレンジ色の「IF」文字
- 立体的な縁取り
- 控えめなサイズ
- 位置: 右下
```

## シーン別デザイン

| シーン | デザイン方針 |
|--------|-------------|
| 1. 表紙 | 大胆、テキスト40%以上、緊急性 |
| 2. 内容1 | 読みやすい、課題提示 |
| 3. 内容2 | 構造的、解決策提示 |
| 4. 内容3 | CTA、行動喚起 |
| 5. サンクス | 固定画像使用 |

## カテゴリ別カラー

| カテゴリ | Primary | Secondary |
|----------|---------|-----------|
| announcement | #E53935 | #FF6F61 |
| development | #1E88E5 | #00BCD4 |
| activity | #43A047 | #66BB6A |
| education | #FF9800 | #FFB74D |
| ai_column | #7B1FA2 | #AB47BC |
| business | #FFC107 | #FFD54F |

## 使用例

```python
from scripts.gemini.client import GeminiClient, ImageGenerationAgent
from scripts.gemini.config import CATEGORIES

client = GeminiClient()
agent = ImageGenerationAgent(client)

# 単一シーンの画像生成
scene = {
    "scene_id": 1,
    "label": "表紙",
    "headline": "AIで変わる学習体験",
    "subtext": "if塾からお届け"
}
category = CATEGORIES["ai_column"]

image_path = agent.generate_scene_image(
    post_id="2026-01-07-0900-ai_column-carousel-01",
    scene=scene,
    category=category
)
print(image_path)
# assets/img/posts/2026-01-07-0900-ai_column-carousel-01-01.png

# 5シーン一括生成
content = {
    "cover": {"headline": "AIで変わる学習体験", "subtext": "最新トレンド"},
    "content1": {"headline": "こんな悩みありませんか？", "subtext": ""},
    "content2": {"headline": "解決策をご紹介", "subtext": ""},
    "content3": {"headline": "今すぐ始めよう", "subtext": "詳細はプロフィールから"}
}

image_paths = agent.generate_complete_post_images(
    post_id="2026-01-07-0900-ai_column-carousel-01",
    content=content,
    category=category
)
```

## API設定

```python
# Gemini 3 Pro Image Preview の呼び出し
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        image_config=types.ImageConfig(
            aspect_ratio="4:5",  # Instagram縦長
            image_size="1K"      # 1K解像度
        )
    )
)
```

## エラーハンドリング

1. **リトライロジック**: 最大3回まで自動リトライ
2. **フォールバック**: API失敗時はSVGプレースホルダーを生成
3. **ログ出力**: 各シーンの生成状況を詳細に出力

## 注意事項

- GEMINI_API_KEY 環境変数が必要
- ネットワーク接続が必要
- 1画像あたり約2-5秒の生成時間
