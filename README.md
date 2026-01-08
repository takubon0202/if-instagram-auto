# if塾 Instagram Workflow v3.0

子どもの可能性を最大限に発揮する - プログラミング教室「if塾」のInstagram投稿自動生成システム。

## Live Demo

**GitHub Pages**: https://takubon0202.github.io/if-instagram-auto/

---

## v3.0 新機能

- **時間認識機能（Time-Aware）**: 常に現在の年月を認識し、最新トレンドを検索
- **キャラクター参照画像**: Image-to-Image生成でif塾オリジナルスタイルを維持
- **テキストオーバーレイエンジン**: Pillowで日本語テキストを美しく描画
- **日本語フォント自動ダウンロード**: Noto Sans JP を自動取得
- **フォールバック画像生成**: APIエラー時もスタッフ画像やグラデーション背景で継続
- **システム評価エージェント**: 95%以上の合格率でシステム品質を保証

---

## 概要

**6カテゴリ × 5シーン構成**の自動投稿ワークフロー。

- **Gemini API連携**: リアルタイムトレンドリサーチ・コンテンツ生成・画像生成
- **5シーン構成**: 表紙→内容1→内容2→内容3→サンクス（固定画像）
- **曜日別カテゴリ**: 週次スケジュールで自動カテゴリ選択
- **GitHub Actions**: 毎日自動実行（JST 16:55）
- **Instagram風プレビュー**: 無限スクロール・カテゴリフィルター・Grid/Feed切替

---

## 技術スタック

| レイヤー | 技術 | 用途 |
|---------|------|------|
| **Frontend** | HTML5, CSS3, Vanilla JS | Instagram風UIプレビュー |
| **Backend** | Python 3.11, Pillow, Pydantic | ワークフロー、画像処理、データ検証 |
| **AI/LLM** | Google Gemini API (3モデル) | リサーチ、コンテンツ、画像生成 |
| **Text Overlay** | Pillow + Noto Sans JP | 日本語テキスト描画 |
| **Data** | JSON (6ファイル) | 投稿、設定、テンプレート、スタッフ |
| **Hosting** | GitHub Pages | 静的サイトデプロイ |
| **CI/CD** | GitHub Actions | 自動投稿スケジューリング |

---

## 使用モデル

| エージェント | モデル | 機能 |
|-------------|--------|------|
| TrendResearchAgent | `gemini-3-flash-preview` | Google Search グラウンディングでリサーチ（thinking=minimal） |
| ContentGenerationAgent | `gemini-3-flash-preview` | 5シーンコンテンツ生成（thinking=minimal） |
| ImageGenerationAgent | `gemini-3-pro-image-preview` | キャラクター参照画像を使ったImage-to-Image生成（1K, 4:5） |
| TextOverlayEngine | Pillow + Noto Sans JP | 日本語テキストオーバーレイ |
| ContentImprovementAgent | `gemini-3-flash-preview` | パフォーマンス分析・改善（thinking=minimal） |

---

## 画像生成フロー（v3.0）

```
1. TrendResearchAgent → 時間認識でトレンドトピック取得
2. ContentGenerationAgent → 5シーンのテキスト生成
3. ImageGenerationAgent → キャラクター参照画像でImage-to-Image生成
   ├─ 成功: PNG画像（アニメ風イラスト）
   └─ 失敗: フォールバック画像生成
4. TextOverlayEngine → 日本語テキストをオーバーレイ
   ├─ タイトル: 画面上部20%
   └─ サブテキスト: 画面下部80%
5. 完成画像として保存 (1080x1350)
```

### 画像生成仕様

| 項目 | 値 |
|------|-----|
| モデル | gemini-3-pro-image-preview |
| 解像度 | 1K (1080x1350) |
| アスペクト比 | 4:5（Instagram縦長投稿） |
| スタイル | Cute chibi anime style |
| フォント | Noto Sans CJK JP Bold |

### フォールバック動作

GEMINI_API_KEYが未設定またはAPIエラー時:

1. **スタッフ画像優先**: シーンに紐づくスタッフ画像を背景に使用
2. **グラデーション背景**: スタッフ画像がない場合はカテゴリ色でグラデーション生成
3. **テキストオーバーレイ**: タイトルとサブテキストのみ描画（不要な要素なし）

---

## テキストオーバーレイ設定

| 項目 | 値 | 説明 |
|------|-----|------|
| title_font_size | 100 | タイトルフォントサイズ |
| content_font_size | 60 | コンテンツフォントサイズ |
| subtext_font_size | 40 | サブテキストフォントサイズ |
| padding_ratio | 0.10 | 左右余白（各10%） |
| line_height_ratio | 1.5 | 行間比率 |
| outline_width | 12 | 縁取り幅 |
| shadow_offset | 5 | 影のオフセット |

---

## キャラクター参照画像

Image-to-Image生成でif塾オリジナルスタイルを維持:

| キャラクター | 用途 |
|-------------|------|
| girl_happy | 表紙、ポジティブシーン |
| girl_surprised | 驚き、発見シーン |
| girl_excited | 興奮、お知らせシーン |
| boy_green_happy | 解決策、成功シーン |
| boy_green_thinking | 課題提示、考察シーン |
| boy_green_smile | AIコラム、テックシーン |
| boy_black_energetic | 活動報告、イベント |
| child_sad | 問題提起シーン |

---

## 5シーン構成

全投稿で統一された構成:

| シーン | ラベル | 目的 | 描画要素 |
|--------|--------|------|----------|
| 1 | 表紙 | インパクト重視のタイトル | headline + subtext |
| 2 | 内容1 | 概要・課題提示 | headline + subtext |
| 3 | 内容2 | メリット・解決策 | headline + subtext |
| 4 | 内容3 | 詳細・提案 | headline + subtext |
| 5 | サンクス | アクション誘導 | 固定画像 |

**削除された要素**: ページ番号（1/5等）、if塾ロゴ、カテゴリラベル

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

---

## GitHub Actions 自動投稿

### スケジュール実行

毎日 **16:55 JST** (UTC 7:55) に自動実行。

### ワークフロー設定

`.github/workflows/daily-post.yml`:

```yaml
on:
  schedule:
    - cron: '55 7 * * *'  # JST 16:55
  workflow_dispatch:
    inputs:
      category: ...
      dry_run: ...
```

### 手動実行

GitHub Actions → workflow_dispatch で手動実行可能:

- **カテゴリ指定**: 特定カテゴリで生成
- **ドライラン**: コミットせずにテスト

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

# システム評価（95%以上で合格）
python -m scripts.gemini.evaluate_system
```

---

## システム評価

`evaluate_system.py` で以下を検証:

| テスト項目 | 内容 |
|-----------|------|
| モジュールインポート | PIL, config, client, workflow等 |
| 設定ファイル | フォントサイズ、パディング、カテゴリ数 |
| 画像処理 | リサイズ、グラデーション生成 |
| テキストオーバーレイ | フォント検出、描画出力 |
| フォールバック | パス生成、ファイル生成 |
| クライアントメソッド | メソッド存在、引数確認 |
| ワークフロー統合 | カテゴリ取得、5シーン構成 |
| 不要要素削除 | ページ番号等の削除確認 |

**目標**: 95%以上の合格率

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
│       └── daily-post.yml        # GitHub Actions
│
├── assets/
│   ├── css/
│   │   └── style.css             # Instagram 2025ダークテーマ
│   ├── js/
│   │   └── app.js                # Vanilla JS
│   ├── fonts/
│   │   └── NotoSansCJKjp-Bold.otf # 日本語フォント
│   └── img/
│       ├── posts/                # 投稿画像
│       ├── characters/           # キャラクター参照画像 (8種)
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
│   ├── gemini/
│   │   ├── config.py             # 設定（カテゴリ、フォント、モデル）
│   │   ├── client.py             # 4エージェント + 画像処理
│   │   ├── workflow.py           # ワークフローv3.0
│   │   ├── text_overlay.py       # テキストオーバーレイエンジン
│   │   ├── staff.py              # スタッフ画像選択
│   │   └── evaluate_system.py    # システム評価エージェント
│   ├── agents/                   # サブエージェント定義
│   └── daily_reports/            # 日次レポート・評価結果
│
└── docs/
    └── architecture.md           # システムアーキテクチャ
```

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

### 画像優先順位

1. シーンに紐づくスタッフ画像
2. カテゴリに対応するスタッフのプロフィール画像
3. グラデーション背景（フォールバック）

---

## トラブルシューティング

### 画像生成エラー: 'Image' object has no attribute 'size'

**原因**: Gemini APIレスポンスの処理不正

**解決**: `client.py`で`part.inline_data.data`から直接PIL Imageに変換

```python
image_data = part.inline_data.data
image = PILImage.open(io.BytesIO(image_data)).convert("RGB")
```

### 日本語が文字化け（豆腐）

**原因**: 日本語フォントが見つからない

**解決**: `text_overlay.py`が自動的にNoto Sans JPをダウンロード

### フォールバック画像が単色

**原因**: スタッフ画像が設定されていない

**解決**: `workflow.py`の`_plan_5scene_post`でスタッフ画像を各シーンに設定

### GitHub Actionsが失敗

1. Settings → Secrets → `GEMINI_API_KEY` が設定されているか確認
2. Actions → workflow_dispatch → dry_run: true でテスト
3. ログで Python エラーを確認
4. `partial_success`ステータスでもワークフローは継続

---

## 出力ファイル

| ファイル | 説明 |
|----------|------|
| `data/posts.json` | 投稿データ（累積） |
| `scripts/daily_reports/YYYY-MM-DD.md` | 日次レポート |
| `scripts/daily_reports/evaluation_*.json` | システム評価結果 |
| `assets/img/posts/YYYYMMDD_category-NN.png` | 生成画像 |
| `assets/img/posts/YYYYMMDD_category-NN-fallback.png` | フォールバック画像 |

---

## ローカル開発

```bash
# プレビューサイト起動
python -m http.server 8000
# → http://localhost:8000 でアクセス

# ワークフローテスト
python -m scripts.gemini.workflow daily --date 2026-01-08

# システム評価
python -m scripts.gemini.evaluate_system

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

## ライセンス

Copyright (c) if塾. All rights reserved.
