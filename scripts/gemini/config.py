"""
Gemini API 設定ファイル
環境変数 GEMINI_API_KEY を設定してください
"""
import os

# API設定
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# モデル設定
MODELS = {
    "research": "gemini-3-pro-preview",      # リサーチ・トレンド分析用
    "content": "gemini-2.5-flash",            # コンテンツ生成用
    "image": "gemini-2.5-flash",              # 画像生成用
}

# Instagram画像サイズ設定（2026年最新）
IMAGE_SIZES = {
    "feed_square": {"width": 1080, "height": 1080, "ratio": "1:1"},
    "feed_portrait": {"width": 1080, "height": 1350, "ratio": "4:5"},    # 推奨
    "feed_portrait_tall": {"width": 1080, "height": 1440, "ratio": "3:4"},
    "feed_landscape": {"width": 1080, "height": 566, "ratio": "1.91:1"},
    "reel_story": {"width": 1080, "height": 1920, "ratio": "9:16"},      # リール・ストーリー
    "carousel": {"width": 1080, "height": 1350, "ratio": "4:5"},         # カルーセル推奨
}

# デフォルト設定
DEFAULT_FEED_SIZE = "feed_portrait"  # 4:5が推奨
DEFAULT_REEL_SIZE = "reel_story"     # 9:16

# if(塾) ブランド設定
BRAND_CONFIG = {
    "name": "if(塾)",
    "tagline": "AIで支援 / 個別最適 / 第三の居場所",
    "url": "https://if-juku.net/",
    "target_audiences": [
        "不登校/発達特性のある子ども（当事者）",
        "不登校/発達特性のある子どもを持つ保護者",
        "支援団体・自治体",
        "AI導入をしたい企業",
    ],
    "posting_schedule": ["09:00", "12:30", "20:00"],
    "posting_ratio": {"juku": 2, "business": 1},
    "prohibited_words": ["診断", "治療", "治る", "必ず", "絶対", "確実"],
    "required_elements": [
        "配慮の一文",
        "CTA（if-juku.net）",
        "専門家相談推奨（必要に応じて）",
    ],
    "style": {
        "tone": "やさしい、安心、押し付けない",
        "colors": ["#4A90A4", "#7CB8A8", "#F5F5F5"],
        "visual": "日本アニメ風、余白多め、柔らかい光",
    }
}

# リサーチ設定
RESEARCH_CONFIG = {
    "instagram_hashtags": {
        "juku": [
            "#不登校", "#発達特性", "#オンライン塾", "#居場所づくり",
            "#個別指導", "#プログラミング教育", "#小学生", "#中学生", "#高校生",
            "#子育て", "#保護者", "#学習支援"
        ],
        "business": [
            "#生成AI", "#AI研修", "#DX推進", "#業務効率化",
            "#ChatGPT", "#プロンプト", "#企業研修", "#中小企業DX"
        ]
    },
    "competitor_analysis": True,
    "trend_sources": [
        "Instagram Explore",
        "Google Trends",
        "Twitter/X トレンド",
        "教育系メディア",
    ]
}
