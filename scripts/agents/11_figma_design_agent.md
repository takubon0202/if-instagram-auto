# 11 - Figma Design Agent（Figmaデザインエージェント）

## 役割
Figmaデザインからコードを生成し、UIコンポーネントを実装する。

## 使用MCP
- **Framelink Figma MCP** (figma-developer-mcp)
- 完全無料・無制限

## 入力
- FigmaファイルURL または フレームURL
- 出力形式（React/HTML/CSS）
- スタイルフレームワーク（Tailwind/CSS Variables）

## 出力
- 生成されたコンポーネントコード
- CSS/スタイル定義
- レスポンシブ対応コード

## 利用可能なMCPツール

### get_figma_data
Figmaファイルまたはフレームからデザイン情報を取得。

```
使用例:
「このFigmaリンクのデザイン情報を取得して」
https://www.figma.com/design/xxxxx/ファイル名?node-id=1234
```

### 取得可能な情報
- レイアウト構造（フレーム、グループ、コンポーネント）
- スタイル情報（色、フォント、間隔、シャドウ）
- コンポーネントプロパティ
- Auto Layout設定
- 制約・レスポンシブ設定

## 使用例

### 1. デザインからReactコンポーネント生成

```
このFigmaリンクからReactコンポーネントを生成して：
https://www.figma.com/design/xxxxx

要件：
- TypeScript
- Tailwind CSS
- レスポンシブ対応
```

### 2. カラーパレット抽出

```
このFigmaファイルからCSS変数を生成して：
https://www.figma.com/design/xxxxx

出力形式：
:root {
  --color-primary: #xxx;
  ...
}
```

### 3. コンポーネントライブラリ生成

```
このFigmaファイルの全ボタンコンポーネントを
統一されたReactコンポーネントとして実装して
```

## if塾ブランド連携

### デザイントークン（自動適用）

```css
/* if(Business)テーマ */
--bg-primary: #0f172a;
--accent-blue: #3b82f6;
--gradient-blue: linear-gradient(135deg, #3b82f6, #60a5fa);
```

### カテゴリ別カラー

| カテゴリ | Primary | Secondary |
|----------|---------|-----------|
| お知らせ | #E53935 | #FF6F61 |
| 開発物 | #1E88E5 | #00BCD4 |
| 活動報告 | #43A047 | #66BB6A |
| 教育コラム | #FF9800 | #FFB74D |
| AIコラム | #7B1FA2 | #AB47BC |
| ビジネス | #FFC107 | #FFD54F |

## セットアップ状態

```
MCP: framelink-figma
Status: ✓ Connected
Limit: 無制限（無料）
```

## 注意事項

- Figmaファイルへの閲覧権限が必要
- 大きなファイルは処理に時間がかかる場合あり
- node-idを指定すると特定フレームのみ取得可能

## トラブルシューティング

### 接続エラーの場合
```bash
claude mcp list  # 接続状態確認
claude mcp remove framelink-figma  # 削除
claude mcp add framelink-figma -- npx -y figma-developer-mcp --stdio --figma-api-key=YOUR_KEY
```

### ファイルアクセスエラーの場合
- Figmaファイルの共有設定を確認
- APIトークンの権限を確認
