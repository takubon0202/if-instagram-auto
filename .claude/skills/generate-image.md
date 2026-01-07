# /generate-image

Gemini 3 Pro Image Preview を使用してif塾のInstagram投稿画像を生成するスキル。

## Material vs Context 分離

このスキルは「Material vs Context」分離アプローチを採用:

| 項目 | 担当 |
|------|------|
| 画像 | 純粋なアニメイラスト素材（テキスト・UI要素なし） |
| テキスト | フロントエンド（CSSオーバーレイ） |
| ロゴ | フロントエンド（HTML/CSS） |

## 使用方法

```
/generate-image [カテゴリ] [テキスト]
```

## 処理フロー

1. **カテゴリ解析**: 指定カテゴリのスタイル設定を取得
2. **概念→視覚変換**: 抽象的なテキストを具体的な視覚描写に変換
3. **プロンプト生成**: 英語プロンプト作成（Instagram参照なし）
4. **画像生成**: Gemini 3 Pro Image Preview APIで純粋なアニメイラスト生成
5. **保存**: assets/img/posts/に画像を保存

## オプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| --category | カテゴリID | activity |
| --scene | シーン番号（1-4） | 1 |
| --headline | メインテキスト | 必須 |
| --subtext | サブテキスト | 空 |
| --style | スタイルプリセット | japanese_anime |
| --output | 出力ファイル名 | 自動生成 |

## カテゴリ

| ID | 名前 | カラー | アニメスタイル |
|----|------|--------|---------------|
| announcement | お知らせ | 赤系 | energetic |
| development | 開発物 | 青系 | innovative |
| activity | 活動報告 | 緑系 | engaged |
| education | 教育コラム | 橙系 | focused |
| ai_column | AIコラム | 紫系 | futuristic |
| business | ビジネスコラム | 金系 | professional |

## スタイルプリセット

| ID | 説明 |
|----|------|
| japanese_anime | 高品質な日本のアニメイラスト（デフォルト） |
| makoto_shinkai | 新海誠風の美しい背景 |
| lofi_aesthetic | Lo-Fi風リラックス |

## 例

### 基本使用
```
/generate-image ai_column "Gemini 3.0がヤバい"
```

### オプション指定
```
/generate-image --category development --scene 2 --headline "高校生が作ったAIアプリ" --subtext "3時間で完成"
```

### スタイル指定
```
/generate-image --category business --style makoto_shinkai --headline "AIで業務効率10倍"
```

### 複数シーン生成
```
/generate-image --category ai_column --all --headline "AIで変わる学習体験"
```

## 画像仕様

```
モデル: gemini-3-pro-image-preview
解像度: 1K
アスペクト比: 4:5（Instagram縦長投稿）
プロンプト言語: 英語
出力: 純粋なアニメイラスト（テキストなし）
```

## ネガティブプロンプト（自動除外）

以下の要素は自動的に除外されます:
- Instagram UI（フレーム、ボタン、いいね）
- テキスト・文字
- ウォーターマーク
- 低品質要素
- 写真調スタイル

## 出力例

```
[INFO] 画像生成開始...
[INFO] カテゴリ: ai_column (futuristic style)
[INFO] スタイル: japanese_anime
[INFO] シーン: 1/5 (表紙)
[INFO] 概念→視覚変換: "AI学習" → "glowing holographic interface, student with sparkling eyes"
[OK] シーン1: 純粋なアニメイラスト生成完了
[INFO] 保存先: assets/img/posts/2026-01-07-ai_column-01.png
[INFO] overlay_text: "Gemini 3.0がヤバい" (フロントエンドで表示)
```

## JSON出力構造

```json
{
  "scene_id": 1,
  "image_url": "assets/img/posts/...",
  "overlay_text": "Gemini 3.0がヤバい",
  "subtext": "最新AIトレンド"
}
```

## エラー時

```
[ERROR] 画像生成失敗
[RETRY] 2/3 回目を試行中...
[FALLBACK] SVGプレースホルダーを生成しました
```

## 関連

- 12_image_generator エージェント
- `/figma-to-code` - Figmaデザインからコード生成
- `scripts/gemini/config.py` - スタイル設定
