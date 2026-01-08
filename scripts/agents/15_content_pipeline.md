# 15 - Content Pipeline（コンテンツパイプラインエージェント）

## 役割
投稿コンテンツの生成から公開までの完全なパイプラインを管理する。
DailyInstagramのアーキテクチャを参考に、モジュラー設計で実装。

## パイプライン概要

```
[トピック選択] → [コンテンツ生成] → [画像生成] → [テキスト合成] → [投稿/保存]
     ↓              ↓              ↓             ↓            ↓
14_topic     01_trend      12_image     text_overlay    data/posts.json
selector     scout         generator
```

## パイプラインステージ

### Stage 1: トピック選択
```python
def select_topic() -> dict:
    """
    今日の投稿トピックを選択

    1. 曜日からカテゴリを決定
    2. 重複チェック（過去30日）
    3. 最も使用回数が少ないトピックを選択
    """
```

### Stage 2: コンテンツ生成
```python
def generate_content(topic: dict) -> dict:
    """
    トピックからスライドコンテンツを生成

    1. トレンドリサーチ（オプション）
    2. ヘッドライン・ポイント生成
    3. キャプション・ハッシュタグ生成
    """
```

### Stage 3: 画像生成
```python
def generate_images(content: dict) -> list:
    """
    各スライドの背景画像を生成

    1. Gemini APIで背景画像生成
    2. 4:5比率（1080x1350）
    3. リトライ・フォールバック処理
    """
```

### Stage 4: テキスト合成
```python
def compose_final_images(images: list, content: dict) -> list:
    """
    背景画像にテキストオーバーレイを追加

    1. Pillowでテキスト描画
    2. 縁取り効果
    3. カテゴリ別カラー適用
    """
```

### Stage 5: 保存・公開
```python
def save_and_publish(final_images: list, content: dict) -> dict:
    """
    最終画像を保存し、posts.jsonを更新

    1. 画像をassets/img/posts/に保存
    2. posts.jsonに投稿データを追加
    3. 投稿履歴を記録
    """
```

## スケジュール設定

### 朝投稿（9:00 JST）
- タイプ: カルーセル
- スライド数: 5-7枚
- カテゴリ: 曜日ベース

### 夕方投稿（20:00 JST）
- タイプ: リール
- 長さ: 15-30秒
- カテゴリ: 同日の朝と同じ

## 設定ファイル

```json
{
  "pipeline": {
    "morning": {
      "time": "09:00",
      "type": "carousel",
      "slides": 5
    },
    "evening": {
      "time": "20:00",
      "type": "reel",
      "duration": 15
    }
  },
  "retry": {
    "max_attempts": 3,
    "delay_seconds": 5
  },
  "output": {
    "image_dir": "assets/img/posts",
    "posts_file": "data/posts.json"
  }
}
```

## 使用例

```python
from scripts.pipeline.runner import ContentPipeline

pipeline = ContentPipeline()

# 朝の投稿を生成
result = pipeline.run_morning_post()

print(f"Generated: {result['post_id']}")
print(f"Images: {len(result['images'])}")
print(f"Category: {result['category']}")

# 結果
# Generated: 2026-01-08-0900-ai_column-carousel-01
# Images: 5
# Category: ai_column
```

## エラーハンドリング

```python
try:
    result = pipeline.run_morning_post()
except TopicSelectionError:
    # 全トピックが最近使用済み
    result = pipeline.run_with_fallback_topic()
except ImageGenerationError:
    # 画像生成失敗
    result = pipeline.run_with_placeholder_images()
except Exception as e:
    # その他のエラー
    logging.error(f"Pipeline failed: {e}")
    pipeline.save_error_report(e)
```

## 関連ファイル

- `scripts/pipeline/runner.py` - パイプライン実装
- `13_post_history_manager.md` - 重複チェック
- `14_topic_selector.md` - トピック選択
- `12_image_generator.md` - 画像生成
- `.github/workflows/daily-post.yml` - 自動実行
