# 13 - Post History Manager（投稿履歴管理エージェント）

## 役割
投稿の重複を防ぎ、コンテンツのローテーションを管理する。
DailyInstagramの`postHistory.ts`を参考に実装。

## 設計思想

| 機能 | 説明 |
|------|------|
| 重複チェック | 過去30日間の投稿を確認 |
| 類似度判定 | 60-80%のキーワード類似度で判定 |
| 履歴保存 | posts-history.json に記録 |

## データ構造

```json
{
  "history": [
    {
      "id": "2026-01-08-0900-ai_column-carousel-01",
      "timestamp": "2026-01-08T09:00:00+09:00",
      "category": "ai_column",
      "title": "Gemini 3.0がヤバい",
      "keywords": ["Gemini", "AI", "最新"],
      "content_hash": "abc123..."
    }
  ],
  "settings": {
    "dedup_window_days": 30,
    "similarity_threshold": 0.7
  }
}
```

## 主要機能

### 1. 重複チェック
```python
def check_duplicate(title: str, keywords: list) -> bool:
    """
    過去30日間の投稿と比較して重複をチェック

    Returns:
        True: 重複あり（投稿をスキップすべき）
        False: 重複なし（投稿OK）
    """
```

### 2. 類似度計算
```python
def calculate_similarity(keywords_a: list, keywords_b: list) -> float:
    """
    キーワードリストの類似度を計算（Jaccard係数）

    Returns:
        0.0-1.0: 類似度スコア
    """
    intersection = set(keywords_a) & set(keywords_b)
    union = set(keywords_a) | set(keywords_b)
    return len(intersection) / len(union) if union else 0.0
```

### 3. 履歴記録
```python
def record_post(post_data: dict) -> None:
    """
    投稿を履歴に記録
    古い記録（30日以上前）は自動削除
    """
```

## 使用例

```python
from scripts.history.manager import PostHistoryManager

manager = PostHistoryManager()

# 重複チェック
is_duplicate = manager.check_duplicate(
    title="Gemini 3.0がヤバい",
    keywords=["Gemini", "AI", "最新"]
)

if is_duplicate:
    print("[SKIP] 類似投稿が過去30日以内に存在")
else:
    # 投稿処理
    ...
    # 履歴記録
    manager.record_post({
        "id": post_id,
        "category": "ai_column",
        "title": "Gemini 3.0がヤバい",
        "keywords": ["Gemini", "AI", "最新"]
    })
```

## 関連ファイル

- `data/posts-history.json` - 履歴データ
- `scripts/history/manager.py` - 実装ファイル
- `14_topic_selector.md` - トピック選択エージェント
