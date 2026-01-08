# 14 - Topic Selector（トピック選択エージェント）

## 役割
投稿トピックの選択ロジックを管理し、カテゴリとスケジュールに基づいてコンテンツを選択する。
DailyInstagramの`topicSelector.ts`を参考に実装。

## ローテーションモード

| モード | 説明 | 使用場面 |
|--------|------|----------|
| weekday | 曜日ベースでカテゴリを割り当て | デフォルト |
| sequential | 順番に選択（lastUsedIndex + 1） | テスト用 |
| random | ランダム選択 | バリエーション重視 |

## 曜日カテゴリマッピング

| 曜日 | カテゴリ | 理由 |
|------|----------|------|
| 月曜 | announcement | 週初めのお知らせ |
| 火曜 | education | 教育コンテンツ |
| 水曜 | ai_column | AIトレンド |
| 木曜 | development | 開発物紹介 |
| 金曜 | activity | 活動報告 |
| 土曜 | business | ビジネス向け |
| 日曜 | education | 教育コンテンツ |

## トピック選択ロジック

### 1. 曜日モード (weekday)
```python
def select_by_weekday(day_of_week: int) -> str:
    """
    曜日に基づいてカテゴリを選択

    Args:
        day_of_week: 0=月曜, 6=日曜

    Returns:
        カテゴリID
    """
    mapping = {
        0: "announcement",
        1: "education",
        2: "ai_column",
        3: "development",
        4: "activity",
        5: "business",
        6: "education"
    }
    return mapping.get(day_of_week, "activity")
```

### 2. 使用回数ベース選択
```python
def select_least_used(category: str) -> dict:
    """
    指定カテゴリ内で最も使用回数が少ないトピックを選択

    Returns:
        トピックデータ
    """
    topics = get_topics_by_category(category)
    return min(topics, key=lambda t: t.get("usedCount", 0))
```

### 3. トピックローテーション
```python
def rotate_topic(topic_id: str) -> None:
    """
    トピックの使用回数をインクリメント
    """
    topics_data = load_topics()
    for topic in topics_data["topics"]:
        if topic["id"] == topic_id:
            topic["usedCount"] = topic.get("usedCount", 0) + 1
            break
    save_topics(topics_data)
```

## トピックデータ構造

```json
{
  "categories": {
    "ai_column": {
      "color": "#7B1FA2",
      "gradient": "linear-gradient(...)",
      "days": [2]
    }
  },
  "topics": [
    {
      "id": "gemini-3-intro",
      "category": "ai_column",
      "title": "Gemini 3.0がヤバい",
      "slides": [
        {"type": "cover", "headline": "...", "subtext": "..."},
        {"type": "content", "headline": "...", "points": ["...", "..."]}
      ],
      "caption": "投稿キャプション #ハッシュタグ",
      "usedCount": 0
    }
  ],
  "settings": {
    "rotationMode": "weekday"
  }
}
```

## 使用例

```python
from scripts.topics.selector import TopicSelector
from datetime import datetime

selector = TopicSelector()

# 今日のカテゴリを取得
today = datetime.now().weekday()
category = selector.select_by_weekday(today)

# そのカテゴリで最も使用回数が少ないトピックを取得
topic = selector.select_least_used(category)

print(f"Today: {category}, Topic: {topic['title']}")

# 投稿後にローテーション
selector.rotate_topic(topic["id"])
```

## 関連ファイル

- `data/topics.json` - トピックデータ
- `scripts/topics/selector.py` - 実装ファイル
- `13_post_history_manager.md` - 重複チェック
