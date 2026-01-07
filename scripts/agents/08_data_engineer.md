# Data Engineer（JSON更新・検証エージェント）

## 役割
全サブエージェントの出力を統合し、posts.json / stories.json を更新する。

## 入力
- 全サブエージェントの最終出力
- 既存のJSONデータ

## 出力
- 更新されたposts.json
- 更新されたstories.json（必要に応じて）
- 検証レポート

## 処理フロー

```
1. 既存JSONを読み込み
   ↓
2. 新規投稿データを構築
   ↓
3. IDの重複チェック
   ↓
4. スキーマ検証
   ↓
5. JSON追記
   ↓
6. 最終検証（validate_data.js）
   ↓
7. 結果レポート出力
```

## 投稿データ構築

### Post Schema
```json
{
  "id": "YYYY-MM-DD-HHMM-track-type-NN",
  "datetime": "YYYY-MM-DDTHH:MM:SS+09:00",
  "type": "carousel|reel|image",
  "track": "juku|business",
  "title": "投稿タイトル",
  "caption": "キャプション全文",
  "hashtags": ["#tag1", "#tag2"],
  "cta_url": "https://if-juku.net/",
  "media": [
    {
      "kind": "image|video",
      "src": "assets/img/posts/filename.svg",
      "alt": "代替テキスト",
      "thumbnail": "サムネイル（video時のみ）"
    }
  ],
  "highlight": "カテゴリ名",
  "notes_for_instagram": {
    "cover_text": "カバーテキスト",
    "first_comment": "最初のコメント",
    "reel_script": "リール台本（reel時のみ）"
  }
}
```

### ID生成ルール
```
YYYY-MM-DD-HHMM-track-type-NN

例:
- 2026-01-07-0900-juku-carousel-01
- 2026-01-07-1230-biz-carousel-01
- 2026-01-07-2000-juku-reel-01
```

### datetime形式
```
ISO 8601 with timezone
例: 2026-01-07T09:00:00+09:00
```

## Story Schema（必要時）
```json
{
  "id": "story-YYYY-MM-DD-NN",
  "datetime": "YYYY-MM-DDTHH:MM:SS+09:00",
  "type": "image|video",
  "src": "assets/img/stories/filename.svg",
  "alt": "代替テキスト",
  "duration": 4,
  "highlight": "カテゴリ名",
  "link": {
    "url": "https://if-juku.net/",
    "label": "リンクラベル"
  },
  "text_overlay": "オーバーレイテキスト"
}
```

## 検証チェックリスト

### 必須フィールド検証
- [ ] id: 一意、フォーマット準拠
- [ ] datetime: ISO 8601形式
- [ ] type: carousel/reel/image のいずれか
- [ ] track: juku/business のいずれか
- [ ] title: 空でない
- [ ] caption: 空でない
- [ ] cta_url: https://if-juku.net/
- [ ] media: 配列、1件以上

### 整合性検証
- [ ] 同一IDの投稿が存在しない
- [ ] datetimeが過去の投稿より後
- [ ] highlightが定義済みカテゴリ
- [ ] media.srcのパスが正しい形式

## エラー処理

### エラーレベル
| Level | 処理 |
|-------|------|
| ERROR | 追記中止、修正必須 |
| WARNING | 追記実行、レポートに記録 |
| INFO | 情報のみ |

### 一般的なエラー
```
ERROR: Duplicate ID found
ERROR: Invalid datetime format
ERROR: Missing required field: {field}
WARNING: Unknown highlight category
WARNING: Media file path may not exist
```

## 出力レポート形式

```markdown
# Data Update Report - YYYY-MM-DD

## Summary
- Posts added: 3
- Stories added: 0
- Validation: PASSED

## New Posts
1. 2026-01-07-0900-juku-carousel-01 - "朝がつらい日に"
2. 2026-01-07-1230-biz-carousel-01 - "AI研修の失敗3選"
3. 2026-01-07-2000-juku-reel-01 - "普通じゃなくていい"

## Warnings
- None

## Errors
- None

## Next Steps
- [ ] 画像ファイルを生成/配置
- [ ] プレビュー確認
- [ ] git push
```
