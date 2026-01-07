# 10 - Design Agent（デザインエージェント）

## 役割
if塾ブランドに基づいたUI/UXデザインの改善・生成を行う。

## 入力
- デザイン要件（色、レイアウト、コンポーネント）
- 参照ページ（if(Business) / if塾本サイト）
- 対象ファイル（CSS / HTML）

## 出力
- 改善されたスタイル定義
- デザイントークン
- コンポーネント構成

## ブランドガイドライン

### if(Business) カラーパレット

| 用途 | カラー | Hex |
|------|--------|-----|
| Primary Dark | ダークネイビー | #0f172a |
| Primary | ネイビー | #1a1f2e |
| Accent Blue | ブルー | #3b82f6 |
| Accent Light Blue | ライトブルー | #60a5fa |
| Purple | パープル | #9333ea |
| Purple Light | ライトパープル | #a855f7 |
| Gold | ゴールド | #fbbf24 |
| Green | グリーン | #10b981 |
| Orange | オレンジ | #f97316 |

### if塾（教育向け）カラーパレット

| 用途 | カラー | Hex |
|------|--------|-----|
| Primary | ティール | #4A90A4 |
| Secondary | セカンダリ | #7CB8A8 |
| Accent | アクセント | #F5F5F5 |
| Text | テキスト | #333333 |

### タイポグラフィ

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
```

### デザイン原則

1. **安心感**: 余白を活かした落ち着いたデザイン
2. **信頼性**: プロフェッショナルな印象
3. **アクセシビリティ**: コントラスト比を確保
4. **モダン**: グラデーション、シャドウの活用

## コンポーネントスタイル

### ボタン

```css
/* Primary Button */
.btn-primary {
  background: linear-gradient(135deg, #3b82f6, #60a5fa);
  color: white;
  border-radius: 8px;
  padding: 12px 24px;
  font-weight: 600;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
}

/* Secondary Button */
.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  border-radius: 8px;
  padding: 12px 24px;
  backdrop-filter: blur(8px);
}
```

### カード

```css
.card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
  backdrop-filter: blur(10px);
}

.card:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
}
```

### グラデーション

```css
/* Hero Gradient */
.gradient-hero {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
}

/* Accent Gradient */
.gradient-accent {
  background: linear-gradient(135deg, #3b82f6 0%, #9333ea 100%);
}
```

## Figma MCP連携

### 使用方法

```bash
# Figma MCPを追加（設定済み）
claude mcp add --transport http figma https://mcp.figma.com/mcp

# 利用可能なツール
- get_file: Figmaファイルからデザイン情報を取得
- get_styles: スタイル定義を取得
- get_components: コンポーネント一覧を取得
```

### 認証方法

1. Figmaデスクトップアプリを開く
2. Dev Modeに切り替え（Shift+D）
3. インスペクトパネルで「Enable desktop MCP server」をクリック
4. または https://mcp.figma.com でブラウザ認証

## 使用例

```python
from scripts.design.agent import DesignAgent

agent = DesignAgent()

# カラースキームを生成
colors = agent.generate_color_scheme("business")
# {
#   "primary": "#0f172a",
#   "accent": "#3b82f6",
#   "gradient": "linear-gradient(135deg, #3b82f6, #60a5fa)"
# }

# CSSを改善
improved_css = agent.improve_css(original_css, "modern_dark")
```

## 注意事項

- if(Business)とif塾で異なるカラースキームを使い分ける
- モバイルファーストで設計
- アニメーションは控えめに
- ダークモードを基本とする（Business向け）
