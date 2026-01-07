# /figma-to-code

FigmaデザインからReact/HTML/CSSコードを生成するスキル。

## 使用方法

```
/figma-to-code [FigmaURL]
```

## 処理フロー

1. **デザイン取得**: Framelink MCPを使用してFigmaからデザイン情報を取得
2. **解析**: レイアウト、スタイル、コンポーネント構造を解析
3. **コード生成**: 指定フレームワークでコンポーネントを生成
4. **最適化**: if塾ブランドガイドラインに沿ってスタイル調整

## オプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| --react | Reactコンポーネントとして生成 | ○ |
| --html | HTML/CSSとして生成 | - |
| --tailwind | Tailwind CSSを使用 | ○ |
| --css-vars | CSS変数を使用 | - |
| --responsive | レスポンシブ対応 | ○ |

## 例

### 基本使用
```
/figma-to-code https://www.figma.com/design/xxxxx
```

### HTML/CSS出力
```
/figma-to-code https://www.figma.com/design/xxxxx --html --css-vars
```

## 出力

### Reactコンポーネント（デフォルト）
```tsx
// components/ComponentName.tsx
import React from 'react';

export const ComponentName: React.FC = () => {
  return (
    <div className="...">
      {/* 生成されたコンポーネント */}
    </div>
  );
};
```

### HTML/CSS
```html
<!-- component.html -->
<div class="component">...</div>

/* component.css */
.component { ... }
```

## if塾ブランド自動適用

生成時に以下のブランドカラーを自動適用：

```css
:root {
  --bg-primary: #0f172a;
  --bg-secondary: #1a1f2e;
  --accent-blue: #3b82f6;
  --accent-purple: #9333ea;
  --accent-gold: #fbbf24;
}
```
