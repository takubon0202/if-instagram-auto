# 12 - Image Generator（画像生成エージェント）

## 役割
Gemini 3 Pro Image Preview を使用して、if塾のInstagram投稿用画像を生成する。

## 設計思想: Material vs Context 分離

**重要**: 画像生成において「素材（Material）」と「文脈（Context）」を明確に分離する。

| 項目 | 担当 | 説明 |
|------|------|------|
| 画像素材 | Gemini API | 純粋なアニメイラスト（テキスト・UI要素なし） |
| テキスト表示 | フロントエンド | CSSオーバーレイまたは画像合成 |
| ロゴ表示 | フロントエンド | HTML/CSSで重ね表示 |

### なぜ分離するのか？
- **問題**: Instagramという文脈をプロンプトに含めると、モデルがInstagramのUI（いいねボタン、枠など）を描画してしまう
- **解決**: 「純粋なアニメイラスト」として生成し、テキスト・UIは後処理で追加

## モデル
`gemini-3-pro-image-preview`

## 入力
- カテゴリID（announcement, development, activity, education, ai_column, business）
- シーン情報（scene_id, headline, subtext）
- 投稿ID

## 出力
- PNG画像（1K解像度、4:5比率）
- **純粋なアニメイラスト素材**（テキスト・UI要素を含まない）
- 画像パス: `assets/img/posts/{post_id}-{scene_id:02d}.png`

## 画像仕様

| 項目 | 値 |
|------|-----|
| モデル | gemini-3-pro-image-preview |
| 解像度 | 1K |
| アスペクト比 | 4:5（Instagram縦長投稿） |
| プロンプト言語 | 英語（精度向上のため） |
| 出力スタイル | 日本のアニメ風イラスト |
| リトライ | 最大3回 |

## スタイルプリセット

利用可能なスタイルプリセット:

| プリセット | 説明 | 使用場面 |
|-----------|------|---------|
| japanese_anime | 高品質な日本のアニメイラスト | デフォルト |
| makoto_shinkai | 新海誠風の美しい背景 | B2B向け |
| lofi_aesthetic | Lo-Fi風リラックス | 不登校支援 |

## ネガティブプロンプト（除外要素）

以下の要素は自動的に除外されます:

- **UI要素**: instagram frame, social media interface, buttons, icons
- **テキスト**: text overlay, caption, hashtag, watermark, letters
- **品質低下**: low quality, blurry, distorted, ugly
- **不要スタイル**: photorealistic, 3d render, photograph

## 概念→視覚変換

抽象的な概念を具体的な視覚描写に自動変換:

| 概念 | 視覚変換 |
|------|---------|
| 安心感 | warm soft lighting, cozy room, gentle smile |
| 達成感 | sparkling eyes, proud expression, confetti |
| 集中 | focused eyes, clean desk, soft background |
| 成長 | morning light, sprouting plant, hopeful sky |

## カテゴリ別アニメスタイル

各カテゴリに最適化されたアニメスタイル設定:

| カテゴリ | キャラクターの雰囲気 | 背景 | カラーパレット |
|----------|---------------------|------|---------------|
| announcement | excited, energetic | bright classroom | warm reds |
| development | curious, innovative | modern workspace | tech blues |
| activity | happy, engaged | outdoor/workshop | vibrant greens |
| education | studious, focused | library/study | warm oranges |
| ai_column | futuristic, intelligent | cyber/holographic | purples |
| business | professional, confident | modern office | golden tones |

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

# 生成される画像は純粋なアニメイラスト素材
# テキストは含まれない（フロントエンドでオーバーレイ）
image_path = agent.generate_scene_image(
    post_id="2026-01-07-0900-ai_column-carousel-01",
    scene=scene,
    category=category
)
```

## JSON出力構造（Material vs Context対応）

```json
{
  "post_id": "2026-01-07-0900-ai_column-carousel-01",
  "type": "carousel",
  "pages": [
    {
      "scene_id": 1,
      "scene_name": "cover",
      "label": "表紙",
      "image_url": "assets/img/posts/...",
      "overlay_text": "AIで変わる学習体験",
      "subtext": "if塾からお届け"
    }
  ]
}
```

## API設定

```python
# Gemini 3 Pro Image Preview の呼び出し
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=english_prompt,  # 英語プロンプト
    config=types.GenerateContentConfig(
        image_config=types.ImageConfig(
            aspect_ratio="4:5",
            image_size="1K"
        )
    )
)
```

## プロンプト構造（内部処理）

```
[スタイルプリセット]
Japanese anime style, cel shading, high quality, masterpiece...

[シーン視覚描写]
A cheerful junior high school student with sparkling eyes...

[構図指示]
centered composition, aspect ratio 4:5...

[除外指示]
Avoid: text, ui, instagram frame, watermark...
```

## エラーハンドリング

1. **リトライロジック**: 最大3回まで自動リトライ
2. **フォールバック**: API失敗時はSVGプレースホルダーを生成
3. **ログ出力**: 各シーンの生成状況を詳細に出力

## 注意事項

- GEMINI_API_KEY 環境変数が必要
- ネットワーク接続が必要
- 1画像あたり約2-5秒の生成時間
- **重要**: 生成画像にはテキストを含めない（フロントエンドで処理）

## 関連ファイル

- `scripts/gemini/config.py` - スタイルプリセット、ネガティブプロンプト設定
- `scripts/gemini/client.py` - ImageGenerationAgentクラス
- `.claude/skills/generate-image.md` - スキル定義
