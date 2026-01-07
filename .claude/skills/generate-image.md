# /generate-image

Gemini 3 Pro Image Preview を使用してif塾のInstagram投稿画像を生成するスキル。

## 使用方法

```
/generate-image [カテゴリ] [テキスト]
```

## 処理フロー

1. **カテゴリ解析**: 指定カテゴリのスタイル設定を取得
2. **プロンプト生成**: 日本語テキストとif塾ロゴを含むプロンプト作成
3. **画像生成**: Gemini 3 Pro Image Preview APIで画像生成
4. **保存**: assets/img/posts/に画像を保存

## オプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| --category | カテゴリID | activity |
| --scene | シーン番号（1-4） | 1 |
| --headline | メインテキスト | 必須 |
| --subtext | サブテキスト | 空 |
| --output | 出力ファイル名 | 自動生成 |

## カテゴリ

| ID | 名前 | カラー |
|----|------|--------|
| announcement | お知らせ | 赤系 |
| development | 開発物 | 青系 |
| activity | 活動報告 | 緑系 |
| education | 教育コラム | 橙系 |
| ai_column | AIコラム | 紫系 |
| business | ビジネスコラム | 金系 |

## 例

### 基本使用
```
/generate-image ai_column "Gemini 3.0がヤバい"
```

### オプション指定
```
/generate-image --category development --scene 2 --headline "高校生が作ったAIアプリ" --subtext "3時間で完成"
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
言語: 日本語
ロゴ: if塾ロゴ（右下）
```

## if塾ロゴ

生成画像には自動的にif塾ロゴが含まれます：

```
┌─────────────────┐
│  ┌───┐          │
│  │IF │ 塾       │
│  └───┘          │
│ (モニターフレーム)│
└─────────────────┘
```

- オレンジ色の「IF」文字
- 黒いモニターフレーム
- 立体的な縁取り

## 出力例

```
[INFO] 画像生成開始...
[INFO] カテゴリ: ai_column
[INFO] シーン: 1/5 (表紙)
[OK] シーン1: Gemini 3.0がヤバい...
[INFO] 保存先: assets/img/posts/2026-01-07-ai_column-01.png
```

## エラー時

```
[ERROR] 画像生成失敗
[RETRY] 2/3 回目を試行中...
[FALLBACK] SVGプレースホルダーを生成しました
```

## 関連

- `/figma-to-code` - Figmaデザインからコード生成
- エージェント: 12_image_generator
