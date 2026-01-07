# Gemini統合ワークフロー - サブエージェント定義

## 概要

Gemini APIを活用した高品質Instagram投稿ワークフロー。
以下のエージェントが連携して、リサーチ→企画→生成→改善のサイクルを回す。

---

## 使用モデル

| エージェント | モデル | 用途 |
|-------------|--------|------|
| Trend Research | gemini-3-pro-preview | リサーチ・トレンド分析 |
| Content Planning | gemini-2.5-flash | コンテンツ企画 |
| Image Generation | gemini-2.5-flash | 画像生成 |
| Content Improvement | gemini-2.5-flash | 改善分析 |

---

## エージェント詳細

### 1. TrendResearchAgent（トレンドリサーチ）

**機能:**
- Google検索によるグラウンディングで最新トレンド取得
- Instagram ハッシュタグ分析
- 競合アカウント分析
- リアルタイムトレンド監視

**入力:**
- track: "juku" / "business"
- hashtags: 分析対象ハッシュタグ

**出力:**
```json
{
    "trending_topics": [],
    "popular_content_types": [],
    "engagement_insights": "",
    "recommended_hooks": [],
    "best_posting_times": [],
    "competitor_analysis": "",
    "content_recommendations": []
}
```

**使用例:**
```python
from scripts.gemini.client import GeminiClient, TrendResearchAgent

client = GeminiClient()
agent = TrendResearchAgent(client)

# 塾向けトレンドリサーチ
trends = agent.research_instagram_trends("juku")

# リアルタイムトレンド
realtime = agent.get_realtime_trends()
```

---

### 2. ImageGenerationAgent（画像生成）

**機能:**
- Instagram投稿用画像の自動生成
- カルーセル全スライドの一括生成
- リールサムネイル生成
- ブランドガイドラインに沿ったビジュアル

**画像サイズ（2026年推奨）:**
| 形式 | アスペクト比 | サイズ |
|------|-------------|--------|
| フィード（縦長） | 4:5 | 1080x1350px |
| フィード（縦長大） | 3:4 | 1080x1440px |
| リール/ストーリー | 9:16 | 1080x1920px |
| 正方形 | 1:1 | 1080x1080px |

**入力:**
- post_id: 投稿ID
- slides: スライド情報リスト
- size_key: 画像サイズキー

**出力:**
- 生成された画像ファイルパスのリスト

**使用例:**
```python
from scripts.gemini.client import GeminiClient, ImageGenerationAgent

client = GeminiClient()
agent = ImageGenerationAgent(client)

# カルーセル画像生成
slides = [
    {"number": 1, "type": "hook", "headline": "新学期前の声かけ"},
    {"number": 2, "type": "problem", "headline": "こんな悩みありませんか？"},
    ...
]

image_paths = agent.generate_carousel_images(
    "2026-01-08-0900-juku-carousel-01",
    slides,
    "feed_portrait"  # 4:5 推奨
)
```

---

### 3. ContentImprovementAgent（コンテンツ改善）

**機能:**
- 投稿パフォーマンス分析
- エンゲージメント率評価
- 改善提案の自動生成
- 次回投稿へのフィードバック

**入力:**
- post_data: 投稿データ
- metrics: パフォーマンス指標

**出力:**
```json
{
    "performance_score": 0-100,
    "strengths": [],
    "weaknesses": [],
    "improvement_suggestions": [],
    "next_post_recommendations": {
        "hook_suggestions": [],
        "content_angle": "",
        "visual_recommendations": [],
        "caption_tips": []
    }
}
```

**使用例:**
```python
from scripts.gemini.client import GeminiClient, ContentImprovementAgent

client = GeminiClient()
agent = ContentImprovementAgent(client)

# パフォーマンス分析
metrics = {
    "reach": 1000,
    "saves": 50,
    "likes": 100,
    "comments": 10
}

analysis = agent.analyze_post_performance(post_data, metrics)
suggestions = agent.suggest_improvements(post_data)
```

---

## 統合ワークフロー

### Daily Workflow（毎日実行）

```bash
# 環境変数設定
export GEMINI_API_KEY="your-api-key"

# 実行
python -m scripts.gemini.workflow daily --date 2026-01-08
```

**処理フロー:**
1. トレンドリサーチ（塾/企業両方）
2. リアルタイムトレンド取得
3. コンテンツ企画（3投稿）
4. 画像生成（カルーセル/リール）
5. posts.json更新
6. 日次レポート生成

### Research Only（リサーチのみ）

```bash
python -m scripts.gemini.workflow research --track both
```

### Improvement Analysis（改善分析）

```bash
python -m scripts.gemini.workflow improve --post-id 2026-01-08-0900-juku-carousel-01
```

---

## ブランドガイドライン（自動適用）

**ビジュアルスタイル:**
- 日本アニメ風、やわらかい線、安心感
- 白＋淡いブルー/グリーン基調
- 余白多め、テキストオーバーレイ用スペース確保

**カラーパレット:**
- Primary: #4A90A4
- Secondary: #7CB8A8
- Background: #F5F5F5

**禁止事項:**
- 派手すぎるデザイン
- 過度なキラキラ効果
- リアルな人物写真
- 文字のレンダリング（後から追加）

---

## セットアップ

```bash
# 1. 依存パッケージインストール
pip install -r requirements.txt

# 2. 環境変数設定
export GEMINI_API_KEY="your-api-key"

# 3. 動作確認
python -m scripts.gemini.workflow research --track juku
```

---

## 注意事項

1. **APIキー管理**: GEMINI_API_KEYは環境変数で管理
2. **レート制限**: Gemini APIのレート制限に注意
3. **画像生成**: 失敗時はSVGプレースホルダーを自動生成
4. **コンテンツ審査**: 生成されたコンテンツは人間が最終確認
