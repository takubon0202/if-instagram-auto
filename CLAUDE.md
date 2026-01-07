# Claude Code プロジェクト設定

## MCP サーバー

### Framelink Figma MCP（無料・無制限）

FigmaデザインからUI情報を取得するMCPサーバー。

```
Name: framelink-figma
Status: Connected
Limit: 無制限
Cost: 無料
```

#### 使用方法

FigmaのURLを共有するだけでデザイン情報を取得：

```
このFigmaデザインからReactコンポーネントを生成して：
https://www.figma.com/design/xxxxx/ファイル名?node-id=1234
```

#### 取得可能な情報
- フレーム・レイヤー構造
- スタイル（色、フォント、間隔）
- Auto Layout設定
- コンポーネントプロパティ

---

## サブエージェント

### 09 - Staff Image Selector
スタッフ画像の選択・提案

### 10 - Design Agent
UIデザインの改善・生成

### 11 - Figma Design Agent
Figmaからコード生成

### 12 - Image Generator
Instagram投稿画像の生成（Gemini 3 Pro Image Preview）

---

## スキル

### /figma-to-code
FigmaデザインからReact/HTML/CSSコードを生成

```
/figma-to-code [FigmaURL]
```

### /generate-image
if塾Instagram投稿画像を生成

```
/generate-image [カテゴリ] [テキスト]
/generate-image --category ai_column --headline "Gemini 3.0がヤバい"
```

**仕様:**
- モデル: gemini-3-pro-image-preview
- 解像度: 1K
- アスペクト比: 4:5（Instagram縦長）
- ロゴ: if塾ロゴ自動挿入

---

## ブランドガイドライン

### カラーパレット（if Business準拠）

```css
:root {
  --bg-primary: #0f172a;
  --bg-secondary: #1a1f2e;
  --accent-blue: #3b82f6;
  --accent-blue-light: #60a5fa;
  --accent-purple: #9333ea;
  --accent-gold: #fbbf24;
  --accent-green: #10b981;
}
```

### グラデーション

```css
--gradient-blue: linear-gradient(135deg, #3b82f6, #60a5fa);
--gradient-purple: linear-gradient(135deg, #9333ea, #a855f7);
--gradient-story: linear-gradient(45deg, #3b82f6, #9333ea, #f97316);
```

---

## カテゴリカラー

| カテゴリ | Primary | Secondary |
|----------|---------|-----------|
| announcement | #E53935 | #FF6F61 |
| development | #1E88E5 | #00BCD4 |
| activity | #43A047 | #66BB6A |
| education | #FF9800 | #FFB74D |
| ai_column | #7B1FA2 | #AB47BC |
| business | #FFC107 | #FFD54F |

---

## 禁止事項

- APIキー・トークンをコードにハードコード禁止
- 個人情報の外部送信禁止
- 生徒の顔写真の無断使用禁止
