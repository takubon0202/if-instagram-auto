# if塾 Instagram Workflow v2.0

子どもの可能性を最大限に発揮する - プログラミング教室「if塾」のInstagram投稿自動生成システム。

## Live Demo

**GitHub Pages**: https://takubon0202.github.io/if-instagram-auto/

---

## 概要

**6カテゴリ × 5シーン構成**の自動投稿ワークフロー。

- **Gemini API連携**: リアルタイムトレンドリサーチ・コンテンツ生成・画像生成
- **5シーン構成**: 表紙→内容1→内容2→内容3→サンクス（固定画像）
- **曜日別カテゴリ**: 週次スケジュールで自動カテゴリ選択
- **GitHub Actions**: 毎日3回（9:00, 12:30, 20:00 JST）自動実行
- **Instagram風プレビュー**: 無限スクロール・カテゴリフィルター・Grid/Feed切替

---

## 技術スタック

| レイヤー | 技術 | 用途 |
|---------|------|------|
| **Frontend** | HTML5, CSS3, Vanilla JS | Instagram風UIプレビュー |
| **Backend** | Python 3.11, Pydantic | ワークフロー、データ検証 |
| **AI/LLM** | Google Gemini API (3モデル) | リサーチ、コンテンツ、画像生成 |
| **Data** | JSON (4ファイル) | 投稿、設定、テンプレート、スタッフ |
| **Hosting** | GitHub Pages | 静的サイトデプロイ |
| **CI/CD** | GitHub Actions | 自動投稿スケジューリング |

---

## 使用モデル

| エージェント | モデル | 機能 |
|-------------|--------|------|
| TrendResearchAgent | `gemini-3-flash-preview` | Google Search グラウンディングでリサーチ（thinking=minimal） |
| ContentGenerationAgent | `gemini-3-flash-preview` | 5シーンコンテンツ生成（thinking=minimal） |
| ImageGenerationAgent | `gemini-3-pro-image-preview` | **日本語テキスト込み完成画像**を生成（1K, 4:5） |
| ContentImprovementAgent | `gemini-3-flash-preview` | パフォーマンス分析・改善（thinking=minimal） |

### 画像生成仕様

| 項目 | 値 |
|------|-----|
| モデル | gemini-3-pro-image-preview |
| 解像度 | 1K |
| アスペクト比 | 4:5（Instagram縦長投稿） |
| 言語 | 日本語 |
| ロゴ | if塾ロゴ自動挿入（右下） |

### 画像生成フロー（Image-First Content）

```
1. TrendResearchAgent → トレンドトピック取得
2. ContentGenerationAgent → 5シーンのテキスト生成
3. ImageGenerationAgent → 日本語テキスト + if塾ロゴを画像に埋め込んで生成
   └─ 成功: PNG画像（テキスト込み完成版）
   ※ GEMINI_API_KEY必須（フォールバックなし）
```

### if塾ロゴ

```
┌─────────┐
│  ┌───┐  │
│  │IF │塾 │  ← オレンジ色「IF」+ 黒モニターフレーム
│  └───┘  │
└─────────┘
```

**特徴:**
- 画像がそのまま投稿コンテンツとして完成
- 日本語テキストが画像内にレンダリング
- if塾ブランドロゴが自動挿入
- リトライロジック（最大3回）で安定性向上
- GEMINI_API_KEY必須で高品質画像を保証

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
| announcement | お知らせ | セミナー、募集、休校情報 | #E53935 (赤) |
| development | 開発物 | 生徒作品、技術力証明 | #1E88E5 (青) |
| activity | 活動報告 | 授業風景、イベント | #43A047 (緑) |
| education | 教育コラム | 保護者向け啓蒙 | #FF9800 (橙) |
| ai_column | AIコラム | 最新AI情報、保存促進 | #7B1FA2 (紫) |
| business | ビジネスコラム | 稼ぐ力、差別化 | #FFC107 (金) |

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

**投稿時間**: 09:00, 12:30, 20:00 (JST)

---

## GitHub Actions 自動投稿

### スケジュール実行

毎日3回、GitHub Actionsが自動でワークフローを実行:

- **09:00 JST** (UTC 0:00) - 朝の通勤・通学時間
- **12:30 JST** (UTC 3:30) - 昼休み
- **20:00 JST** (UTC 11:00) - 夜のリラックスタイム

### 手動実行

GitHub Actions → workflow_dispatch で手動実行可能:

- **カテゴリ指定**: 特定カテゴリで生成
- **ドライラン**: コミットせずにテスト

### ワークフロー設定

`.github/workflows/daily-post.yml`:

```yaml
on:
  schedule:
    - cron: '0 0 * * *'   # JST 9:00
    - cron: '30 3 * * *'  # JST 12:30
    - cron: '0 11 * * *'  # JST 20:00
  workflow_dispatch:
    inputs:
      category: ...
      dry_run: ...
```

---

## フロントエンド機能

### Instagram風プレビューUI

- **無限スクロール**: 12投稿ずつ自動読み込み
- **Grid/Feed表示切替**: 3カラムグリッド or 縦長フィード
- **カテゴリフィルター**: 7カテゴリ（すべて含む）で絞り込み
- **投稿モーダル**: カルーセル画像・キャプション・ハッシュタグ表示
- **ストーリービューア**: フルスクリーン・自動進行・プログレスバー
- **ダークテーマ**: Instagram 2025準拠のデザイン

### 操作方法

| 操作 | アクション |
|------|----------|
| 投稿クリック | モーダル表示 |
| 左右スワイプ | カルーセル操作 |
| ←→キー | 画像切替 |
| Escキー | モーダル閉じる |
| ストーリー左/右タップ | 前後移動 |
| 下スクロール | 追加読み込み |

---

## セットアップ

### 1. 依存パッケージインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数設定

```bash
# Windows (PowerShell)
$env:GEMINI_API_KEY = "your-api-key"

# macOS/Linux
export GEMINI_API_KEY="your-api-key"
```

### 3. GitHub Secrets設定

GitHub リポジトリ → Settings → Secrets → Actions:

- `GEMINI_API_KEY`: Google Gemini APIキー

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

## ディレクトリ構成

```
ifjuku-ig-prototype/
├── index.html                    # Instagram風プレビューサイト
├── README.md                     # このファイル
├── CLAUDE.md                     # Claude Code設定
├── requirements.txt              # Python依存パッケージ
│
├── .github/
│   └── workflows/
│       └── daily-post.yml        # GitHub Actions (毎日3回自動実行)
│
├── assets/
│   ├── css/
│   │   └── style.css             # Instagram 2025ダークテーマ
│   ├── js/
│   │   └── app.js                # Vanilla JS (フレームワーク不使用)
│   └── img/
│       ├── posts/                # 投稿画像
│       │   └── ifjukuthanks.png  # サンクス画像（固定）
│       ├── staff/                # スタッフ画像 (6名)
│       └── stories/              # ストーリー用画像
│
├── data/
│   ├── config.json               # サイト設定
│   ├── posts.json                # 投稿データベース（累積）
│   ├── topics.json               # 6カテゴリテンプレート
│   ├── stories.json              # ストーリー設定
│   ├── highlights.json           # ハイライト設定
│   └── staff.json                # スタッフ情報
│
├── scripts/
│   ├── gemini/                   # Gemini API統合
│   │   ├── config.py             # 6カテゴリ・5シーン・モデル設定
│   │   ├── client.py             # 4エージェント実装
│   │   ├── workflow.py           # ワークフローv2.0
│   │   └── staff.py              # スタッフ画像選択
│   ├── agents/                   # サブエージェント定義 (11種)
│   ├── daily_reports/            # 日次レポート
│   └── validate_data.js          # JSONバリデーション
│
└── docs/
    └── architecture.md           # システムアーキテクチャ
```

---

## データ構造

### posts.json（累積型）

```json
{
  "metadata": {
    "version": "3.0",
    "total_posts": 12,
    "last_updated": "2026-01-07T17:59:55"
  },
  "posts": [
    {
      "id": "2026-01-08-0900-announcement-carousel-01",
      "datetime": "2026-01-08T09:00:00+09:00",
      "type": "carousel",
      "category": "announcement",
      "title": "投稿タイトル",
      "caption": "投稿本文...",
      "hashtags": ["#if塾", "#プログラミング塾"],
      "media": [
        { "kind": "image", "src": "assets/img/posts/...", "alt": "説明" }
      ],
      "highlight": "お知らせ",
      "staff": { "name": "高崎翔太", "role": "代表・講師" },
      "status": "published"
    }
  ]
}
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

## デザインシステム

### Instagram 2025準拠

- **テーマ**: ダークモード (#121212)
- **画像サイズ**: 1080×1350px (4:5 縦長)
- **グラデーション**: Instagramストーリーリング風
- **フォント**: 極太ゴシック体＋袋文字（縁取り）

### カテゴリ配色

| カテゴリ | Primary | Secondary |
|----------|---------|-----------|
| お知らせ | #E53935 | #FF6F61 |
| 開発物 | #1E88E5 | #00BCD4 |
| 活動報告 | #43A047 | #66BB6A |
| 教育コラム | #FF9800 | #FFB74D |
| AIコラム | #7B1FA2 | #AB47BC |
| ビジネス | #FFC107 | #FFD54F |

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
| `data/posts.json` | 投稿データ（累積・上書きしない） |
| `scripts/research_results.json` | カテゴリ別リサーチ結果 |
| `scripts/daily_reports/YYYY-MM-DD.md` | 日次レポート |
| `assets/img/posts/*.png` | 生成画像 |
| `assets/img/posts/*.svg` | プレースホルダー |

---

## 運用フロー

### 自動実行（毎日3回）

1. **GitHub Actions** がスケジュール実行
2. 曜日に応じた**カテゴリを自動選択**
3. **Gemini 3 Pro + Google Search** でトレンドリサーチ
4. **5シーン構成**で投稿コンテンツ生成
5. **Gemini 2.5 Flash Image** で画像生成（4枚 + サンクス）
6. `posts.json` に**追加保存**（上書きしない）
7. **Git commit & push** → GitHub Pages自動デプロイ
8. 日次レポート生成

### 手動確認

生成されたコンテンツを確認後、Instagramへ手動投稿。

---

## ローカル開発

```bash
# プレビューサイト起動
python -m http.server 8000
# → http://localhost:8000 でアクセス

# データ検証
node scripts/validate_data.js

# ワークフローテスト
python -m scripts.gemini.workflow daily --date 2026-01-08

# スタッフディレクトリ作成
python -m scripts.gemini.staff setup
```

---

## デプロイ

### GitHub Pages

1. Settings → Pages → Source: `main` branch
2. 自動デプロイ: https://takubon0202.github.io/if-instagram-auto/

### GitHub Actions権限

Settings → Actions → General:
- Workflow permissions: **Read and write permissions**
- Allow GitHub Actions to create and approve pull requests: **有効**

---

## トラブルシューティング

### 投稿が表示されない

1. ブラウザのキャッシュをクリア（Ctrl+Shift+R）
2. DevTools (F12) → Console で `[if塾]` ログを確認
3. Network タブで `data/posts.json` が200を返しているか確認

### GitHub Actions が失敗する

1. Settings → Secrets → `GEMINI_API_KEY` が設定されているか確認
2. Actions → workflow_dispatch → dry_run: true でテスト
3. ログで Python エラーを確認

### 画像生成エラー

- `gemini-3-pro-image-preview` モデルを使用しているか確認
- `GEMINI_API_KEY` が設定されているか確認（必須）
- APIクォータを確認
- 画像生成に失敗するとワークフローがエラー終了

---

## ライセンス

Copyright (c) if塾. All rights reserved.
