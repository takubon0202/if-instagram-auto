"""
Text Overlay Module v1.0
if塾 Instagram画像にテキストを重ねる

PIL/Pillowを使用して生成画像にテキストオーバーレイを追加
- アウトライン効果（縁取り）
- 日本語フォント対応
- Instagram 4:5比率（1080x1350）

参考: getabako/InstagramGenerator のCanvas実装をPythonで再現
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import os

# config.pyからの設定を試行
try:
    from .config import TEXT_OVERLAY_CONFIG
    DEFAULT_CONFIG = {
        "canvas_width": TEXT_OVERLAY_CONFIG.get("canvas_width", 1080),
        "canvas_height": TEXT_OVERLAY_CONFIG.get("canvas_height", 1350),
        "aspect_ratio": "4:5",
        "font_path": None,
        "title_font_size": TEXT_OVERLAY_CONFIG.get("title_font_size", 80),
        "content_font_size": TEXT_OVERLAY_CONFIG.get("content_font_size", 60),
        "subtext_font_size": TEXT_OVERLAY_CONFIG.get("subtext_font_size", 40),
        "title_position_y": TEXT_OVERLAY_CONFIG.get("title_position_y", 0.12),
        "content_position_y": TEXT_OVERLAY_CONFIG.get("content_position_y", 0.85),
        "text_colors": {
            "primary": "#FF69B4",
            "secondary": "#FFFFFF",
            "outline": "#000000",
        },
        "outline_width": TEXT_OVERLAY_CONFIG.get("outline_width", 4),
        "shadow_offset": TEXT_OVERLAY_CONFIG.get("shadow_offset", 3),
        "category_colors": TEXT_OVERLAY_CONFIG.get("category_colors", {})
    }
except ImportError:
    # デフォルト設定
    DEFAULT_CONFIG = {
        "canvas_width": 1080,
        "canvas_height": 1350,
        "aspect_ratio": "4:5",

        # フォント設定
        "font_path": None,  # システムフォントを使用
        "title_font_size": 80,
        "content_font_size": 60,
        "subtext_font_size": 40,

        # テキスト位置（キャンバス高さに対する割合）
        "title_position_y": 0.12,     # 上から12%
        "content_position_y": 0.85,   # 上から85%（下部）

        # カラー設定
        "text_colors": {
            "primary": "#FF69B4",     # ピンク（添付画像と同様）
            "secondary": "#FFFFFF",   # 白
            "outline": "#000000",     # 黒の縁取り
        },

        # 縁取り設定
        "outline_width": 4,
        "shadow_offset": 3,
        "category_colors": {}
    }

# 日本語フォントの候補パス
JAPANESE_FONT_PATHS = [
    # Windows
    "C:/Windows/Fonts/meiryo.ttc",
    "C:/Windows/Fonts/msgothic.ttc",
    "C:/Windows/Fonts/YuGothM.ttc",
    "C:/Windows/Fonts/BIZ-UDGothicR.ttc",
    # macOS
    "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    # Linux
    "/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]


class TextOverlayEngine:
    """
    画像にテキストオーバーレイを追加するエンジン

    添付画像のように:
    - メインタイトル（上部、ピンク文字+黒縁取り）
    - サブテキスト（下部、オレンジ文字+黒縁取り）
    """

    def __init__(self, config: dict = None):
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        self.font_path = self._find_japanese_font()

    def _find_japanese_font(self) -> str:
        """日本語フォントを探す"""
        # 設定されたフォントパスがあればそれを使用
        if self.config.get("font_path") and os.path.exists(self.config["font_path"]):
            return self.config["font_path"]

        # 候補から探す
        for font_path in JAPANESE_FONT_PATHS:
            if os.path.exists(font_path):
                print(f"[Font] Found: {font_path}")
                return font_path

        print("[Font] Warning: No Japanese font found, using default")
        return None

    def _get_font(self, size: int) -> ImageFont.FreeTypeFont:
        """指定サイズのフォントを取得"""
        try:
            if self.font_path:
                return ImageFont.truetype(self.font_path, size)
            else:
                # フォールバック: デフォルトフォント
                return ImageFont.load_default()
        except Exception as e:
            print(f"[Font] Error loading font: {e}")
            return ImageFont.load_default()

    def add_text_overlay(
        self,
        image_path: str,
        title_text: str = "",
        subtext: str = "",
        output_path: str = None,
        title_color: str = None,
        subtext_color: str = None
    ) -> str:
        """
        画像にテキストオーバーレイを追加

        Args:
            image_path: 入力画像パス
            title_text: メインタイトル（上部）
            subtext: サブテキスト（下部）
            output_path: 出力パス（Noneの場合は上書き）
            title_color: タイトルの色（例: "#FF69B4"）
            subtext_color: サブテキストの色

        Returns:
            str: 出力画像のパス
        """
        # 画像を開く
        img = Image.open(image_path).convert("RGBA")

        # 4:5にリサイズ（必要な場合）
        img = self._resize_to_aspect_ratio(img)

        # テキストオーバーレイ用のレイヤーを作成
        txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)

        # タイトルを描画（上部）
        if title_text:
            self._draw_outlined_text(
                draw=draw,
                text=title_text,
                position_y=self.config["title_position_y"],
                font_size=self.config["title_font_size"],
                text_color=title_color or self.config["text_colors"]["primary"],
                outline_color=self.config["text_colors"]["outline"],
                canvas_width=img.width,
                canvas_height=img.height
            )

        # サブテキストを描画（下部）
        if subtext:
            self._draw_outlined_text(
                draw=draw,
                text=subtext,
                position_y=self.config["content_position_y"],
                font_size=self.config["subtext_font_size"],
                text_color=subtext_color or "#FF8C00",  # オレンジ
                outline_color=self.config["text_colors"]["outline"],
                canvas_width=img.width,
                canvas_height=img.height
            )

        # レイヤーを合成
        output = Image.alpha_composite(img, txt_layer)
        output = output.convert("RGB")

        # 保存
        save_path = output_path or image_path
        output.save(save_path, "PNG", quality=95)
        print(f"[TextOverlay] Saved: {save_path}")

        return save_path

    def _resize_to_aspect_ratio(self, img: Image.Image) -> Image.Image:
        """画像を4:5にリサイズ（カバーモード）"""
        target_w = self.config["canvas_width"]
        target_h = self.config["canvas_height"]
        target_ratio = target_w / target_h

        src_w, src_h = img.size
        src_ratio = src_w / src_h

        if abs(src_ratio - target_ratio) < 0.01:
            # すでに正しい比率
            return img.resize((target_w, target_h), Image.Resampling.LANCZOS)

        # カバーモード: 短い辺を基準にスケール
        if src_ratio > target_ratio:
            # 横長の画像 → 高さ基準
            new_h = target_h
            new_w = int(src_w * (target_h / src_h))
        else:
            # 縦長の画像 → 幅基準
            new_w = target_w
            new_h = int(src_h * (target_w / src_w))

        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        # 中央でクロップ
        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2
        img = img.crop((left, top, left + target_w, top + target_h))

        return img

    def _draw_outlined_text(
        self,
        draw: ImageDraw.Draw,
        text: str,
        position_y: float,
        font_size: int,
        text_color: str,
        outline_color: str,
        canvas_width: int,
        canvas_height: int
    ):
        """
        縁取り付きテキストを描画

        添付画像のスタイル:
        - ピンク/オレンジの文字
        - 黒の縁取り（ストローク）
        - 中央揃え
        - 複数行対応
        """
        font = self._get_font(font_size)
        lines = text.replace("\\n", "\n").split("\n")

        # 行の高さ
        line_height = font_size * 1.3

        # Y位置を計算（複数行の場合は中央揃え）
        total_height = len(lines) * line_height
        start_y = canvas_height * position_y - total_height / 2

        for i, line in enumerate(lines):
            if not line.strip():
                continue

            # テキストの幅を計算してX位置を決定（中央揃え）
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (canvas_width - text_width) // 2
            y = start_y + i * line_height

            # 縁取りを描画（8方向 + 影）
            outline_width = self.config["outline_width"]

            # 影（オフセット）
            shadow_offset = self.config["shadow_offset"]
            draw.text(
                (x + shadow_offset, y + shadow_offset),
                line,
                font=font,
                fill=(0, 0, 0, 180)  # 半透明の黒
            )

            # 縁取り（8方向）
            for dx in range(-outline_width, outline_width + 1):
                for dy in range(-outline_width, outline_width + 1):
                    if dx != 0 or dy != 0:
                        draw.text(
                            (x + dx, y + dy),
                            line,
                            font=font,
                            fill=outline_color
                        )

            # メインテキスト
            draw.text((x, y), line, font=font, fill=text_color)

    def create_instagram_post(
        self,
        background_image_path: str,
        headline: str,
        subtext: str = "",
        output_path: str = None,
        style: str = "default"
    ) -> str:
        """
        Instagram投稿用画像を作成

        Args:
            background_image_path: 背景画像
            headline: メインヘッドライン
            subtext: サブテキスト
            output_path: 出力パス
            style: スタイル名（default, announcement, ai_column等）

        Returns:
            str: 出力画像パス
        """
        # config.pyからのカテゴリカラーを優先使用
        category_colors = self.config.get("category_colors", {})

        # デフォルトのスタイルカラー
        default_style_colors = {
            "default": {"title": "#FF69B4", "sub": "#FF8C00"},
            "announcement": {"title": "#FF3131", "sub": "#FFFFFF"},
            "development": {"title": "#0CC0DF", "sub": "#FFFFFF"},
            "activity": {"title": "#00BF63", "sub": "#FFFFFF"},
            "education": {"title": "#FFDE59", "sub": "#212121"},
            "ai_column": {"title": "#CB6CE6", "sub": "#FFFFFF"},
            "business": {"title": "#FFD700", "sub": "#212121"},
        }

        # category_colorsに設定があればそちらを使用
        if style in category_colors:
            colors = category_colors[style]
        else:
            colors = default_style_colors.get(style, default_style_colors["default"])

        return self.add_text_overlay(
            image_path=background_image_path,
            title_text=headline,
            subtext=subtext,
            output_path=output_path,
            title_color=colors["title"],
            subtext_color=colors["sub"]
        )


def add_text_to_image(
    image_path: str,
    headline: str,
    subtext: str = "",
    output_path: str = None,
    category: str = "default"
) -> str:
    """
    ヘルパー関数: 画像にテキストを追加

    Args:
        image_path: 入力画像パス
        headline: ヘッドライン
        subtext: サブテキスト
        output_path: 出力パス
        category: カテゴリ（スタイル選択用）

    Returns:
        str: 出力画像パス
    """
    engine = TextOverlayEngine()
    return engine.create_instagram_post(
        background_image_path=image_path,
        headline=headline,
        subtext=subtext,
        output_path=output_path,
        style=category
    )


# テスト用
if __name__ == "__main__":
    print("Text Overlay Module Test")
    engine = TextOverlayEngine()
    print(f"Font path: {engine.font_path}")
    print(f"Config: {engine.config}")
