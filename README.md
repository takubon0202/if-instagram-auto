# if(塾) Instagram Workflow Prototype

不登校・発達特性のある子どもたちのためのオンラインプログラミング塾「if(塾)」のInstagram投稿自動生成ワークフロー。

## 概要

このプロジェクトは以下の機能を提供します：

1. **Instagram風プレビューサイト** - GitHub Pagesで投稿を事前確認
2. **Gemini API連携** - AIによるトレンドリサーチ・画像生成・改善分析
3. **サブエージェントワークフロー** - 8つの専門エージェントによるコンテンツ生成

---

## ディレクトリ構成

```
ifjuku-ig-prototype/
├── index.html                    # メインHTML（IG風UI）
├── requirements.txt              # Python依存パッケージ
├── assets/
│   ├── css/
│   │   └── style.css            # スタイルシート
│   ├── js/
│   │   └── app.js               # フロントエンドJS
│   └── img/
│       ├── posts/               # 投稿画像（SVG/PNG）
│       └── stories/             # ストーリー画像
├── data/
│   ├── config.json              # サイト設定
│   ├── posts.json               # 投稿データ
│   ├── stories.json             # ストーリーデータ
│   └── highlights.json          # ハイライト設定
└── scripts/
    ├── validate_data.js         # データ検証スクリプト
    ├── workflow_runner.js       # ワークフロー自動化
    ├── agents/                  # サブエージェント定義
    │   ├── 00_gemini_workflow.md
    │   ├── 01_trend_scout.md
    │   ├── 02_planner.md
    │   ├── 03_carousel_builder.md
    │   ├── 04_reel_scriptwriter.md
    │   ├── 05_jp_copywriter.md
    │   ├── 06_anime_visual_prompt.md
    │   ├── 07_safety_qa.md
    │   └── 08_data_engineer.md
    ├── gemini/                  # Gemini API統合
    │   ├── __init__.py
    │   ├── config.py
    │   ├── client.py
    │   └── workflow.py
    └── daily_reports/           # 日次レポート
```

---

## 機能詳細

### 1. Instagram風プレビューサイト

| 機能 | 説明 |
|------|------|
| グリッド表示 | 3列グリッドで投稿一覧を表示 |
| 投稿モーダル | クリックで詳細表示（キャプション・ハッシュタグ） |
| カルーセル | 横スワイプ対応のスライド表示 |
| ストーリービューア | 自動再生・タップで次へ |
| ハイライト | カテゴリ別フィルタリング |

### 2. 投稿スケジュール

| 時刻 | トラック | 形式 | 内容 |
|------|----------|------|------|
| 09:00 | 塾向け | カルーセル | 保護者・本人向けコンテンツ |
| 12:30 | 企業向け | カルーセル | B2B AI研修・DX推進 |
| 20:00 | 塾向け | リール | 共感・安心を伝える短尺動画 |

### 3. 週次テーマ

**塾向け（juku）:**
| 曜日 | テーマ |
|------|--------|
| 月 | 安心・居場所 |
| 火 | 学習のハードルを下げる |
| 水 | 保護者向け（声かけ） |
| 木 | AI/ITスキル |
| 金 | 無料体験の背中押し |
| 土 | FAQ |
| 日 | まとめ |

**企業向け（business）:**
| 曜日 | テーマ |
|------|--------|
| 月 | 研修の失敗パターン |
| 水 | ワークフロー設計 |
| 金 | LP改善チェック |

---

## Gemini API 連携

### セットアップ

```bash
# 1. 依存パッケージインストール
pip install -r requirements.txt

# 2. 環境変数設定
# Windows (PowerShell)
$env:GEMINI_API_KEY = "your-api-key"

# macOS/Linux
export GEMINI_API_KEY="your-api-key"
```

### ワークフローコマンド

```bash
# デイリーワークフロー（リサーチ→企画→画像生成→データ更新→レポート）
python -m scripts.gemini.workflow daily --date 2026-01-09

# リサーチのみ実行
python -m scripts.gemini.workflow research --track both

# 投稿改善分析
python -m scripts.gemini.workflow improve --post-id 2026-01-08-0900-juku-carousel-01
```

### 使用モデル

| エージェント | モデル | 機能 |
|-------------|--------|------|
| TrendResearchAgent | gemini-3-pro-preview | Google Search グラウンディングでリアルタイムリサーチ |
| ImageGenerationAgent | gemini-2.5-flash | Instagram投稿用画像生成 |
| ContentImprovementAgent | gemini-2.5-flash | パフォーマンス分析・改善提案 |

### 画像サイズ（2026年推奨）

| 形式 | アスペクト比 | サイズ |
|------|-------------|--------|
| フィード（縦長） | 4:5 | 1080x1350px |
| フィード（縦長大） | 3:4 | 1080x1440px |
| リール/ストーリー | 9:16 | 1080x1920px |
| 正方形 | 1:1 | 1080x1080px |

### API未設定時の動作

GEMINI_API_KEYが未設定の場合、モックデータで動作します：
- トレンドリサーチ: サンプルトレンドデータを返却
- 画像生成: SVGプレースホルダーを自動生成
- 改善分析: サンプル分析結果を返却

---

## サブエージェント構成

### 8つの専門エージェント

| # | エージェント | 役割 |
|---|-------------|------|
| 01 | Trend Scout | トレンド調査・競合分析 |
| 02 | Planner | 投稿スケジュール・テーマ設計 |
| 03 | Carousel Builder | カルーセル構成・スライド設計 |
| 04 | Reel Scriptwriter | リール台本・テロップ作成 |
| 05 | JP Copywriter | 日本語キャプション・ハッシュタグ |
| 06 | Anime Visual Prompt | 画像生成プロンプト作成 |
| 07 | Safety QA | 配慮文・禁止ワードチェック |
| 08 | Data Engineer | JSON整形・バリデーション |

---

## ブランドガイドライン

### ビジュアルスタイル

- 日本アニメ風、やわらかい線、安心感
- 白＋淡いブルー/グリーン基調
- 余白多め、テキストオーバーレイ用スペース確保

### カラーパレット

| 用途 | カラー |
|------|--------|
| Primary | #4A90A4 |
| Secondary | #7CB8A8 |
| Background | #F5F5F5 |

### 禁止事項

**ビジュアル:**
- 派手すぎるデザイン
- 過度なキラキラ効果
- リアルな人物写真
- 文字のレンダリング（後から追加）

**コンテンツ:**
- 未成年（生徒）の写真・動画
- 発達・不登校に関する断定表現

**禁止ワード:**
- 診断
- 治療
- 治る
- 障害（→「特性」を使用）
- 普通の子（→「多くのお子さま」を使用）

### 必須要素

- 配慮文: 「お子さまの状況は一人ひとり異なります。必要に応じて専門家へのご相談もご検討ください。」
- CTA: 常に `if-juku.net` へ誘導

---

## データスキーマ

### posts.json

```json
{
  "id": "2026-01-07-0900-juku-carousel-01",
  "datetime": "2026-01-07T09:00:00+09:00",
  "type": "carousel",
  "track": "juku",
  "title": "タイトル",
  "caption": "キャプション本文...",
  "hashtags": ["#不登校", "#オンライン塾"],
  "cta_url": "https://if-juku.net/",
  "media": [
    {"kind": "image", "src": "assets/img/posts/xxx.svg", "alt": "説明"}
  ],
  "highlight": "保護者向け",
  "notes_for_instagram": {
    "cover_text": "カバーテキスト",
    "first_comment": "最初のコメント",
    "reel_script": null
  }
}
```

### type

| 値 | 説明 |
|----|------|
| carousel | カルーセル（複数画像スライド） |
| reel | リール動画 |
| image | 単一画像 |

### track

| 値 | 説明 |
|----|------|
| juku | 塾向け（保護者・本人） |
| business | 企業向け |

---

## ローカル開発

### プレビューサイト起動

**方法1: Live Server（VS Code）**
1. VS Codeで「Live Server」拡張機能をインストール
2. `index.html` を右クリック → 「Open with Live Server」

**方法2: Python**
```bash
cd ifjuku-ig-prototype
python -m http.server 8000
# http://localhost:8000 を開く
```

**方法3: Node.js**
```bash
npx serve ifjuku-ig-prototype
```

### データ検証

```bash
node scripts/validate_data.js
```

---

## 運用フロー

### Daily Run（毎日実行）

1. Gemini APIでトレンドリサーチ
2. 3投稿を自動企画（09:00 / 12:30 / 20:00）
3. 画像生成（またはSVGプレースホルダー）
4. `data/posts.json` 更新
5. Safety QAで配慮文・禁止ワードチェック
6. 日次レポート生成
7. `node scripts/validate_data.js` でエラー確認
8. 人間が内容を最終チェック
9. git push → GitHub Pages 自動反映
10. Instagramへ手動投稿（任意）

### Weekly Review（週1回）

1. 週間パフォーマンス集計
2. 改善分析実行
3. 次週テーマ調整

---

## GitHub Pages での公開

1. GitHubにリポジトリを作成
2. このフォルダの内容をpush
3. Settings → Pages → Source で `main` ブランチを選択
4. 数分後に `https://<username>.github.io/<repo>/` で公開

---

## 出力ファイル

| ファイル | 説明 |
|----------|------|
| `scripts/research_results.json` | リサーチ結果 |
| `scripts/daily_reports/YYYY-MM-DD.md` | 日次レポート |
| `scripts/improvement_*.json` | 改善分析結果 |
| `assets/img/posts/*.svg` | 生成画像/プレースホルダー |

---

## トラブルシューティング

### Windowsでの文字化け

PowerShellで以下を実行：
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

### Gemini APIエラー

1. APIキーが正しく設定されているか確認
2. レート制限に達していないか確認
3. モックモードで動作確認

### 画像生成失敗

APIエラー時はSVGプレースホルダーが自動生成されます。
後から実画像に差し替え可能です。

---

## ライセンス

Copyright (c) if(塾). All rights reserved.
