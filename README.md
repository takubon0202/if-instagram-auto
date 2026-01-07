# if塾 Instagram Workflow v2.0

子どもの可能性を最大限に発揮する - プログラミング教室「if塾」のInstagram投稿自動生成システム。

## 概要

**6カテゴリ × 5シーン構成**の自動投稿ワークフロー。

- **Gemini API連携**: リアルタイムトレンドリサーチ・画像生成・改善分析
- **5シーン構成**: 表紙→内容1→内容2→内容3→サンクス（固定画像）
- **曜日別カテゴリ**: 週次スケジュールで自動カテゴリ選択

---

## 5シーン構成

全投稿で統一された構成:

| シーン | ラベル | 目的 |
|--------|--------|------|
| 1 | 表紙 | インパクト重視のタイトル |
| 2 | 内容1 | 概要・課題提示 |
| 3 | 内容2 | メリット・解決策 |
| 4 | 内容3 | 詳細・提案 |
| 5 | サンクス | アクション誘導（固定画像） |

**サンクス画像**: `assets/img/posts/ifjukuthanks.png`（必ず最後に使用）

---

## 6カテゴリ

| ID | カテゴリ | 目的 | テーマカラー |
|----|----------|------|--------------|
| announcement | お知らせ | セミナー、募集、休校情報 | 赤・ピンク系 |
| development | 開発物 | 生徒作品、技術力証明 | 青・ネオン系 |
| activity | 活動報告 | 授業風景、イベント | 緑系 |
| education | 教育コラム | 保護者向け啓蒙 | オレンジ系 |
| ai_column | AIコラム | 最新AI情報、保存促進 | 紫系 |
| business | ビジネスコラム | 稼ぐ力、差別化 | 金・黄色系 |

---

## 曜日別スケジュール

| 曜日 | カテゴリ | 理由 |
|------|----------|------|
| 月 | お知らせ | 週の始まり |
| 火 | 教育コラム | 保護者向け |
| 水 | 開発物 | 成果物紹介 |
| 木 | AIコラム | テック情報 |
| 金 | ビジネスコラム | 週末に試してもらう |
| 土 | 活動報告 | イベント報告 |
| 日 | 活動報告 | イベント報告 |

---

## セットアップ

```bash
# 1. 依存パッケージインストール
pip install -r requirements.txt

# 2. 環境変数設定
# Windows (PowerShell)
$env:GEMINI_API_KEY = "your-api-key"

# macOS/Linux
export GEMINI_API_KEY="your-api-key"
```

---

## ワークフローコマンド

```bash
# デイリーワークフロー（曜日に応じたカテゴリで5シーン投稿を生成）
python -m scripts.gemini.workflow daily --date 2026-01-08

# リサーチのみ（全カテゴリ or 指定カテゴリ）
python -m scripts.gemini.workflow research
python -m scripts.gemini.workflow research --category ai_column

# カスタム生成（指定カテゴリ・トピック）
python -m scripts.gemini.workflow generate --category development --topic "AIチャットボット"
```

---

## 使用モデル

| エージェント | モデル | 機能 |
|-------------|--------|------|
| TrendResearchAgent | gemini-3-pro-preview | Google Search グラウンディングでリサーチ |
| ContentGenerationAgent | gemini-2.5-flash | 5シーンコンテンツ生成 |
| ImageGenerationAgent | gemini-2.5-flash | Instagram画像生成（4:5） |
| ContentImprovementAgent | gemini-2.5-flash | パフォーマンス分析・改善 |

---

## ディレクトリ構成

```
ifjuku-ig-prototype/
├── index.html                    # プレビューサイト
├── requirements.txt              # Python依存パッケージ
├── assets/
│   ├── css/style.css
│   ├── js/app.js
│   └── img/
│       └── posts/
│           └── ifjukuthanks.png  # サンクス画像（固定）
├── data/
│   ├── config.json
│   ├── posts.json
│   ├── topics.json               # 6カテゴリ設定
│   ├── stories.json
│   └── highlights.json
└── scripts/
    ├── validate_data.js
    ├── agents/                   # サブエージェント定義
    ├── gemini/                   # Gemini API統合
    │   ├── config.py             # 6カテゴリ・5シーン設定
    │   ├── client.py             # 4エージェント実装
    │   └── workflow.py           # ワークフローv2.0
    └── daily_reports/
```

---

## カテゴリ別テンプレート

### お知らせ（announcement）
- **表紙**: インパクト重視のタイトル（例：「【緊急募集】残り3席！」）
- **内容1**: 何が起きるのか？
- **内容2**: 参加するとどうなる？
- **内容3**: いつ・どこで？

### 開発物（development）
- **表紙**: 成果物＋キャッチコピー（例：「高校生が作ったAIアプリが凄すぎる」）
- **内容1**: どんな悩みを解決？（Before）
- **内容2**: どうやって動く？（Process）
- **内容3**: 使った結果は？（After）

### 活動報告（activity）
- **表紙**: 授業風景・イベント（例：「今日の授業、盛り上がりすぎた」）
- **内容1**: 今日何をした？
- **内容2**: 生徒の反応は？
- **内容3**: 指導者の視点

### 教育コラム（education）
- **表紙**: 問いかけ・逆説（例：「『プログラミングは不要』は本当か？」）
- **内容1**: 世の中の流れ
- **内容2**: if塾の考え
- **内容3**: 今やるべきこと

### AIコラム（ai_column）
- **表紙**: ツール名・衝撃的事実（例：「ChatGPT、まだ普通に使ってるの？」）
- **内容1**: これは何？
- **内容2**: どう使う？
- **内容3**: プロの視点

### ビジネスコラム（business）
- **表紙**: 金額・稼ぎ方（例：「中学生でも月3万稼ぐ方法」）
- **内容1**: 何を使う？
- **内容2**: 具体的なツール
- **内容3**: マインドセット

---

## デザインルール

### 配色（カテゴリ別）

| カテゴリ | Primary | Secondary |
|----------|---------|-----------|
| お知らせ | #E53935 | #FF6F61 |
| 開発物 | #1E88E5 | #00BCD4 |
| 活動報告 | #43A047 | #66BB6A |
| 教育コラム | #FF9800 | #FFB74D |
| AIコラム | #7B1FA2 | #AB47BC |
| ビジネス | #FFC107 | #FFD54F |

### フォント・スタイル
- **極太ゴシック体＋袋文字（縁取り）** で視認性最大化
- 余白多め、テキストオーバーレイ用スペース確保

---

## API未設定時の動作

GEMINI_API_KEYが未設定の場合、モックデータで動作:
- **リサーチ**: カテゴリ別サンプルトレンドデータ
- **画像生成**: カテゴリ色のSVGプレースホルダー
- **分析**: サンプル改善提案

---

## 出力ファイル

| ファイル | 説明 |
|----------|------|
| `scripts/research_results.json` | カテゴリ別リサーチ結果 |
| `scripts/daily_reports/YYYY-MM-DD.md` | 日次レポート |
| `assets/img/posts/*.svg` | 生成プレースホルダー |
| `assets/img/posts/ifjukuthanks.png` | サンクス画像（固定） |

---

## スタッフ画像システム

### スタッフ一覧

| ID | 名前 | 役割 | 対応カテゴリ |
|----|------|------|--------------|
| inoue_haruto | 井上陽斗 | 講師 | activity, development, education |
| kagaya_yuma | 加賀屋結眞 | 講師 | activity, development, ai_column |
| yamazaki_takumi | 山﨑琢己 | 講師 | activity, development, education |
| watanabe_yuzuki | 渡辺柚気 | 講師 | activity, development, business |
| fujimoto_hinata | 藤本陽向 | 講師 | activity, development, education |
| takasaki_shota | 高崎翔太 | 代表・講師 | 全カテゴリ |

### 画像タイプ

| タイプ | 用途 | 推奨シーン |
|--------|------|------------|
| profile | プロフィール写真 | cover, announcement |
| teaching | 授業風景 | content1, content2, development |
| casual | カジュアル写真 | content3, activity |
| business | ビジネス写真 | announcement, business |

### カテゴリ別選択ルール

| カテゴリ | 優先スタッフ | 画像タイプ |
|----------|-------------|------------|
| お知らせ | 高崎翔太 | business |
| 開発物 | 全員からランダム | teaching |
| 活動報告 | 全員からランダム | casual |
| 教育コラム | 高崎翔太 | profile |
| AIコラム | 高崎翔太, 加賀屋結眞 | casual |
| ビジネスコラム | 高崎翔太 | business |

### セットアップ

```bash
# スタッフディレクトリを作成
python -m scripts.gemini.staff setup

# 画像の状態をチェック
python -m scripts.gemini.staff check
```

### 画像配置

Google Drive からスタッフ画像をダウンロードして配置：
- ソース: https://drive.google.com/drive/folders/1CYGZroIXSF6Mkh1ARfM_BPcTSa9FWapV

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

---

## 運用フロー

### Daily Run（毎日実行）
1. 曜日に応じたカテゴリを自動選択
2. Gemini APIでトレンドリサーチ
3. 5シーン構成で投稿企画
4. 画像生成（4枚 + サンクス画像）
5. posts.json更新
6. 日次レポート生成
7. 人間が最終確認
8. Instagramへ投稿

---

## ローカル開発

```bash
# プレビューサイト起動
python -m http.server 8000

# データ検証
node scripts/validate_data.js

# ワークフローテスト
python -m scripts.gemini.workflow daily --date 2026-01-08
```

---

## GitHub Pages

1. Settings → Pages → Source: `main`
2. `https://<username>.github.io/<repo>/` で公開

---

## ライセンス

Copyright (c) if塾. All rights reserved.
