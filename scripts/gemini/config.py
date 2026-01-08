"""
Gemini API Configuration
if塾 Instagram ワークフロー設定 v3.0
6カテゴリ × 5シーン構成
時間認識機能（Time-Aware）対応
"""
import os
from datetime import datetime

# ============================================
# 時間認識設定（Time Awareness）
# ============================================
def get_current_time_context():
    """現在の日時コンテキストを取得"""
    now = datetime.now()
    return {
        "current_year": now.year,
        "current_month": now.month,
        "current_month_name": f"{now.month}月",
        "current_day": now.day,
        "today_str": now.strftime("%Y-%m-%d"),
        "timestamp": now.strftime("%Y-%m-%dT%H:%M:%S"),
        "date_id": now.strftime("%Y%m%d"),
        "datetime_obj": now
    }

# 現在時刻のグローバルコンテキスト（インポート時に更新）
TIME_CONTEXT = get_current_time_context()

# API Key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Models
# Gemini 3 Flash Preview + thinking_level=minimal（思考モードオフ）
MODELS = {
    "research": "gemini-3-flash-preview",    # リサーチ・トレンド分析（Google Search対応）
    "content": "gemini-3-flash-preview",     # コンテンツ生成（高速・低コスト）
    "image": "gemini-3-pro-image-preview",   # 画像生成（高品質日本語対応）
}

# ============================================
# 画像生成設定
# ============================================
IMAGE_GENERATION_CONFIG = {
    "model": "gemini-3-pro-image-preview",
    "resolution": "1K",           # 1K解像度
    "aspect_ratio": "4:5",        # Instagram縦長投稿
    "canvas_width": 1080,         # 出力幅
    "canvas_height": 1350,        # 出力高さ（4:5比率）
    "language": "ja",             # 日本語
    "default_style": "japanese_anime",  # デフォルトスタイル
}

# ============================================
# テキストオーバーレイ設定
# ============================================
TEXT_OVERLAY_CONFIG = {
    "enabled": True,              # テキストオーバーレイを有効化
    "canvas_width": 1080,
    "canvas_height": 1350,

    # フォントサイズ（1080x1350用に最適化 v3.0 - インパクト重視）
    "title_font_size": 140,       # メインタイトル（大幅増：72→140）
    "content_font_size": 90,      # コンテンツ（増加：48→90）
    "subtext_font_size": 60,      # サブテキスト（増加：36→60）

    # テキスト位置（キャンバス高さに対する割合）
    "title_position_y": 0.20,     # 上から20%（調整：0.15→0.20）
    "content_position_y": 0.80,   # 上から80%（調整：0.82→0.80）

    # 縁取り設定（強化 v3.0 - 袋文字効果）
    "outline_width": 15,          # 縁取り幅（大幅増：6→15で視認性向上）
    "shadow_offset": 6,           # 影のオフセット（増加：4→6）

    # カテゴリ別カラー（ピンク文字+黒縁取り）
    "category_colors": {
        "default": {"title": "#FF69B4", "sub": "#FF8C00", "outline": "#000000"},
        "announcement": {"title": "#FF3131", "sub": "#FFFFFF", "outline": "#000000"},
        "development": {"title": "#0CC0DF", "sub": "#FFFFFF", "outline": "#000000"},
        "activity": {"title": "#00BF63", "sub": "#FFFFFF", "outline": "#000000"},
        "education": {"title": "#FFDE59", "sub": "#212121", "outline": "#000000"},
        "ai_column": {"title": "#CB6CE6", "sub": "#FFFFFF", "outline": "#000000"},
        "business": {"title": "#FFD700", "sub": "#212121", "outline": "#000000"},
    }
}

# ============================================
# スタイルプリセット（画像生成用）
# ============================================
STYLE_PRESETS = {
    "japanese_anime": {
        "name": "Japanese Anime Style",
        "description": "高品質な日本のアニメイラスト",
        "prompt_prefix": "Japanese anime style, cel shading, high quality, masterpiece, vivid colors, expressive eyes, clean line art, dynamic composition",
        "visual_quality": "studio quality anime illustration, professional animation aesthetic, emotional depth through art direction",
        "atmosphere": "warm and inviting, hopeful, inspiring"
    },
    "makoto_shinkai": {
        "name": "Makoto Shinkai Style",
        "description": "新海誠風の美しい背景と光の表現",
        "prompt_prefix": "Makoto Shinkai style, beautiful detailed background, volumetric lighting, lens flare, detailed clouds, stunning scenery, anime aesthetic",
        "visual_quality": "cinematic quality, photorealistic backgrounds with anime characters",
        "atmosphere": "nostalgic, dreamy, emotionally evocative"
    },
    "lofi_aesthetic": {
        "name": "Lo-Fi Aesthetic",
        "description": "リラックスした落ち着いた雰囲気",
        "prompt_prefix": "Lo-fi aesthetic, soft pastel colors, cozy atmosphere, relaxed mood, warm lighting, hand-drawn feel, anime style",
        "visual_quality": "gentle illustration, calming visual tone",
        "atmosphere": "peaceful, comfortable, safe space"
    }
}

# ============================================
# ネガティブプロンプト設定（UI/テキスト除去）
# ============================================
NEGATIVE_PROMPTS = {
    "global": [
        "low quality", "blurry", "distorted", "ugly", "watermark",
        "text", "letters", "words", "signature", "deformed", "bad quality",
        "worst quality", "jpeg artifacts"
    ],
    "ui_elements": [
        "instagram frame", "instagram ui", "social media interface",
        "buttons", "icons", "like button", "heart icon", "comment icon",
        "share button", "save button", "username", "profile picture",
        "screenshot", "app interface", "phone screen", "notification",
        "status bar", "navigation bar", "border", "frame"
    ],
    "text_elements": [
        "text overlay", "caption", "hashtag", "watermark text",
        "title text", "subtitle", "logo text", "brand name text",
        "japanese text in image", "english text in image"
    ],
    "date_elements": [
        "calendar", "date numbers", "year text", "month text",
        "day numbers", "clock", "timestamp", "2026", "2025", "2024"
    ],
    "unwanted_styles": [
        "photorealistic", "3d render", "photograph", "real photo",
        "stock photo", "clipart", "icon style", "flat design ui"
    ]
}

# ============================================
# 時間認識リサーチ用検索クエリテンプレート
# ============================================
def get_search_queries(category_id: str) -> list:
    """カテゴリ別の時間認識検索クエリを生成"""
    ctx = get_current_time_context()
    year = ctx["current_year"]
    month = ctx["current_month"]

    queries = {
        "announcement": [
            f"プログラミング教室 トレンド {year}",
            f"オンライン塾 ニュース {year}年{month}月",
            f"IT教育 最新 {year}"
        ],
        "development": [
            f"学生 アプリ開発 事例 {year}",
            f"高校生 プログラミング 作品 {year}",
            f"AIアプリ 開発 中学生 {year}"
        ],
        "activity": [
            f"プログラミング教室 活動 {year}",
            f"ハッカソン 中高生 {year}年{month}月",
            f"子供 プログラミング イベント {year}"
        ],
        "education": [
            f"AI時代 教育 {year}",
            f"プログラミング教育 必修化 {year}",
            f"大学入試 情報I 対策 {year}",
            f"子育て AI {year}年{month}月"
        ],
        "ai_column": [
            f"最新 AIツール 学生向け {year}",
            f"ChatGPT 活用 学習 {year}年{month}月",
            f"Gemini 新機能 {year}",
            f"生成AI 教育 {year}"
        ],
        "business": [
            f"中学生 副業 {year}",
            f"高校生 稼ぐ方法 {year}",
            f"学生 起業 トレンド {year}年{month}月",
            f"LINEスタンプ 販売 {year}"
        ]
    }

    return queries.get(category_id, queries["activity"])

# ============================================
# 概念→視覚変換テンプレート
# ============================================
CONCEPT_TO_VISUAL = {
    # 感情・雰囲気の変換
    "安心感": "warm soft lighting, cozy room, comfortable furniture, gentle smile, relaxed posture",
    "達成感": "sparkling eyes, proud expression, raised fist, bright sunlight, confetti",
    "成長": "seedling growing into tree, before-after comparison, level up visual, ascending stairs",
    "可能性": "open door with bright light, endless sky, floating islands, multiple paths",
    "集中": "focused eyes on screen, headphones on, organized desk, soft ambient glow",
    "楽しさ": "bright colors, playful expression, dynamic pose, sparkle effects",
    "挑戦": "character facing mountain, determined expression, clenched fist, sunrise background",
    "つながり": "multiple characters together, hands reaching out, network visualization",

    # テーマの変換
    "不登校支援": "cozy home learning setup, gentle anime character at desk, warm room lighting, supportive atmosphere",
    "プログラミング学習": "anime student at computer, code visualization floating in air, glowing screen, futuristic classroom",
    "AI活用": "friendly robot assistant, holographic interface, collaboration scene, bright tech aesthetic",
    "ビジネススキル": "young entrepreneur character, startup office, vision board, growth chart visualization",
    "創造性": "artist character with floating ideas, colorful imagination clouds, creative workspace",
    "コミュニティ": "diverse anime characters in circle, collaboration scene, shared workspace"
}

# ============================================
# カテゴリ別アニメスタイル設定
# ============================================
CATEGORY_ANIME_STYLES = {
    "announcement": {
        "character_mood": "excited, energetic, welcoming",
        "setting": "bright classroom entrance, open door with light",
        "color_palette": "warm reds and oranges, inviting tones",
        "illustration_focus": "anime character making announcement gesture",
        "recommended_style": "japanese_anime"
    },
    "development": {
        "character_mood": "proud, accomplished, creative",
        "setting": "modern tech workspace, multiple monitors, code floating",
        "color_palette": "cool blues and cyans, tech glow",
        "illustration_focus": "student showing completed project on screen",
        "recommended_style": "japanese_anime"
    },
    "activity": {
        "character_mood": "happy, engaged, collaborative",
        "setting": "classroom with students working together",
        "color_palette": "fresh greens, natural tones",
        "illustration_focus": "group learning scene, hands-on activity",
        "recommended_style": "lofi_aesthetic"
    },
    "education": {
        "character_mood": "thoughtful, curious, inspired",
        "setting": "library or study room with warm lighting",
        "color_palette": "warm oranges, sunset tones",
        "illustration_focus": "parent and child or teacher explaining concept",
        "recommended_style": "makoto_shinkai"
    },
    "ai_column": {
        "character_mood": "amazed, curious, tech-savvy",
        "setting": "futuristic space with AI visualization",
        "color_palette": "purples and magentas, neon accents",
        "illustration_focus": "character interacting with AI hologram",
        "recommended_style": "japanese_anime"
    },
    "business": {
        "character_mood": "confident, entrepreneurial, motivated",
        "setting": "modern startup office, vision board background",
        "color_palette": "gold and yellow, success tones",
        "illustration_focus": "young entrepreneur with business ideas floating",
        "recommended_style": "japanese_anime"
    }
}

# ============================================
# シーン別素材テンプレート
# ============================================
SCENE_MATERIAL_TEMPLATES = {
    1: {  # 表紙
        "role": "hook_attention",
        "material_focus": "character_emotion_highlight",
        "composition": "centered character, dynamic background, eye-catching pose",
        "visual_weight": "80% character, 20% background elements"
    },
    2: {  # 内容1
        "role": "problem_presentation",
        "material_focus": "situation_illustration",
        "composition": "character in context, showing challenge or question",
        "visual_weight": "60% character, 40% environment"
    },
    3: {  # 内容2
        "role": "solution_showcase",
        "material_focus": "transformation_visual",
        "composition": "character with solution elements, positive atmosphere",
        "visual_weight": "50% character, 50% solution visualization"
    },
    4: {  # 内容3
        "role": "action_inspiration",
        "material_focus": "future_vision",
        "composition": "character moving forward, path or door metaphor",
        "visual_weight": "70% character, 30% directional elements"
    }
}

# if塾ロゴ設定
LOGO_CONFIG = {
    "brand_name": "if塾",
    "logo_text": "IF",
    "logo_colors": {
        "primary": "#FF6B00",     # オレンジ
        "outline": "#000000",     # 黒の縁取り
        "background": "#FFFFFF"   # 白背景
    },
    "logo_style": "モニターフレーム内にオレンジ色の「IF」ロゴ、立体的な縁取り",
    "placement": "bottom-right",  # 右下配置
    "size": "small",              # 控えめなサイズ
    "include_in_image": False     # 画像には含めず、フロントエンドで重ねる
}

# Instagram Image Sizes (2026 Recommended)
IMAGE_SIZES = {
    "feed_portrait": {
        "width": 1080,
        "height": 1350,
        "ratio": "4:5",
        "use_case": "フィード投稿（縦長推奨）"
    },
    "feed_portrait_large": {
        "width": 1080,
        "height": 1440,
        "ratio": "3:4",
        "use_case": "フィード投稿（縦長大）"
    },
    "reel_story": {
        "width": 1080,
        "height": 1920,
        "ratio": "9:16",
        "use_case": "リール・ストーリー"
    },
    "square": {
        "width": 1080,
        "height": 1080,
        "ratio": "1:1",
        "use_case": "正方形投稿"
    }
}

# ============================================
# 5シーン構成（全投稿共通）
# ============================================
SCENE_STRUCTURE = {
    "total_scenes": 5,
    "scenes": [
        {"id": 1, "name": "cover", "label": "表紙", "purpose": "インパクト重視のタイトル"},
        {"id": 2, "name": "content1", "label": "内容1", "purpose": "概要・課題提示"},
        {"id": 3, "name": "content2", "label": "内容2", "purpose": "メリット・解決策"},
        {"id": 4, "name": "content3", "label": "内容3", "purpose": "詳細・提案"},
        {"id": 5, "name": "thanks", "label": "サンクス", "purpose": "アクション誘導", "fixed": True}
    ]
}

# サンクス画像（最後のスライドに必ず使用）
THANKS_IMAGE = "assets/img/posts/ifjukuthanks.png"

# ============================================
# 6カテゴリ設定
# ============================================
CATEGORIES = {
    "announcement": {
        "id": "announcement",
        "name": "お知らせ",
        "purpose": "セミナー開催、新コース募集、休校情報など即時性の高い情報",
        "colors": {
            "primary": "#E53935",
            "secondary": "#FF6F61",
            "accent": "#FFCDD2",
            "text": "#FFFFFF"
        },
        "visual_style": "教室の明るい写真 or 拡声器やベルを持った3Dキャラクター",
        "cover_format": "インパクト重視のタイトル",
        "content1_format": "何が起きるのか？（概要）",
        "content2_format": "参加するとどうなる？（メリット）",
        "content3_format": "いつ・どこで？（詳細）",
        "hashtags": ["#if塾", "#プログラミング塾", "#お知らせ", "#新コース", "#生徒募集", "#オンライン授業"]
    },
    "development": {
        "id": "development",
        "name": "開発物",
        "purpose": "技術力の証明、生徒の成果物自慢",
        "colors": {
            "primary": "#1E88E5",
            "secondary": "#00BCD4",
            "accent": "#B3E5FC",
            "text": "#FFFFFF"
        },
        "visual_style": "実際のアプリ画面のスクショ or PCに向かってガッツポーズする人物",
        "cover_format": "成果物の完成画像＋キャッチコピー",
        "content1_format": "どんな悩みを解決？（Before/課題）",
        "content2_format": "どうやって動く？（Process/機能）",
        "content3_format": "使った結果は？（After/結果）",
        "hashtags": ["#if塾", "#プログラミング", "#アプリ開発", "#生徒作品", "#Python", "#JavaScript", "#AIアプリ"]
    },
    "activity": {
        "id": "activity",
        "name": "活動報告",
        "purpose": "教室の雰囲気、信頼感の醸成、「楽しそう」と思わせる",
        "colors": {
            "primary": "#43A047",
            "secondary": "#66BB6A",
            "accent": "#C8E6C9",
            "text": "#FFFFFF"
        },
        "visual_style": "授業風景・イベント写真（プライバシー加工済み）",
        "cover_format": "笑顔の集合写真 or 授業風景",
        "content1_format": "今日何をした？（出来事）",
        "content2_format": "生徒の反応は？（様子）",
        "content3_format": "指導者の視点（気付き）",
        "hashtags": ["#if塾", "#プログラミング教室", "#授業風景", "#ハッカソン", "#生徒の成長", "#楽しい授業"]
    },
    "education": {
        "id": "education",
        "name": "教育コラム",
        "purpose": "保護者への啓蒙、教育方針の提示",
        "colors": {
            "primary": "#FF9800",
            "secondary": "#FFB74D",
            "accent": "#FFE0B2",
            "text": "#212121"
        },
        "visual_style": "考える人物のイラスト or 未来的な教室のイメージ",
        "cover_format": "問いかけ・逆説",
        "content1_format": "世の中の流れ（現状の課題）",
        "content2_format": "if塾の考え（解決策・視点）",
        "content3_format": "今やるべきこと（提案）",
        "hashtags": ["#if塾", "#教育", "#プログラミング教育", "#AI時代", "#子育て", "#保護者向け", "#将来のスキル"]
    },
    "ai_column": {
        "id": "ai_column",
        "name": "AIコラム",
        "purpose": "情報感度の高さのアピール、リーチ獲得（保存されやすい）",
        "colors": {
            "primary": "#7B1FA2",
            "secondary": "#AB47BC",
            "accent": "#E1BEE7",
            "text": "#FFFFFF"
        },
        "visual_style": "サイバーパンク風のAIイメージ画像 or ツールロゴのコラージュ",
        "cover_format": "ツール名 or 衝撃的な事実",
        "content1_format": "これは何？（ツール紹介）",
        "content2_format": "どう使う？（活用例）",
        "content3_format": "プロの視点（コツ・注意点）",
        "hashtags": ["#if塾", "#AI", "#ChatGPT", "#Gemini", "#生成AI", "#AIツール", "#最新テック"]
    },
    "business": {
        "id": "business",
        "name": "ビジネスコラム",
        "purpose": "子供の自立心刺激、実益への期待（差別化ポイント）",
        "colors": {
            "primary": "#FFC107",
            "secondary": "#FFD54F",
            "accent": "#212121",
            "text": "#212121"
        },
        "visual_style": "コインやグラフのイラスト or PCと通帳（比喩）の画像",
        "cover_format": "金額 or 稼ぎ方",
        "content1_format": "何を使う？（手段）",
        "content2_format": "具体的なツール（手順）",
        "content3_format": "マインドセット（成功の秘訣）",
        "hashtags": ["#if塾", "#副業", "#中学生", "#高校生", "#お金の教育", "#LINEスタンプ", "#稼ぐ力"]
    }
}

# ============================================
# 曜日別スケジュール
# ============================================
WEEKLY_SCHEDULE = {
    0: "announcement",   # 月曜：お知らせ（週の始まり）
    1: "education",      # 火曜：教育コラム
    2: "development",    # 水曜：開発物紹介
    3: "ai_column",      # 木曜：AIコラム
    4: "business",       # 金曜：ビジネスコラム（週末に試してもらう）
    5: "activity",       # 土曜：活動報告
    6: "activity"        # 日曜：活動報告
}

# 投稿時間
POSTING_TIMES = [
    {"time": "09:00", "target": "朝の通勤・通学時間"},
    {"time": "12:30", "target": "昼休み"},
    {"time": "20:00", "target": "夜のリラックスタイム"}
]

# ============================================
# ブランド設定
# ============================================
BRAND_CONFIG = {
    "name": "if塾",
    "tagline": "子どもの可能性を最大限に発揮する",
    "website": "if-juku.net",
    "url": "https://if-juku.net/",
    "style": {
        "visual": "テック感のある明るいデザイン、極太ゴシック体＋袋文字（縁取り）で視認性最大化",
        "tone": "親しみやすく、専門的、信頼感",
        "colors": ["#FF6B35", "#4A90A4", "#7CB8A8"]
    },
    "prohibited_words": [
        "診断", "治療", "治る", "障害", "必ず", "絶対", "確実"
    ],
    "required_elements": {
        "thanks_image": True,
        "cta": "詳細はプロフィール欄から",
        "hashtag_count": {"min": 5, "max": 15}
    }
}

# ============================================
# リサーチ設定
# ============================================
RESEARCH_CONFIG = {
    "instagram_hashtags": {
        "general": ["#プログラミング教室", "#子供プログラミング", "#オンライン塾", "#IT教育"],
        "ai": ["#ChatGPT", "#生成AI", "#Gemini", "#AIツール", "#Claude"],
        "education": ["#教育", "#子育て", "#学習", "#プログラミング教育"],
        "business": ["#副業", "#稼ぐ", "#スキルアップ", "#中学生起業"]
    },
    "competitors": [
        "テックキッズ", "N高", "Life is Tech", "TechAcademyジュニア"
    ],
    "trend_sources": [
        "Instagram Explore",
        "Google Trends",
        "X (Twitter) トレンド",
        "教育系メディア"
    ]
}

# ============================================
# デザインテンプレート設定
# ============================================
DESIGN_CONFIG = {
    "font": {
        "primary": "ヒラギノ角ゴ Pro W6, Hiragino Kaku Gothic Pro, sans-serif",
        "fallback": "Arial, sans-serif",
        "style": "極太ゴシック体＋袋文字（縁取り）"
    },
    "text_overlay": {
        "position": "center",
        "max_chars_per_line": 12,
        "stroke_width": 3,
        "shadow": True
    },
    "animation": {
        "cover": "bounce",
        "content": "fade_in",
        "thanks": "pulse"
    }
}

# ============================================
# Webサイト用デザイン設定 (if Business準拠)
# ============================================
WEB_DESIGN_CONFIG = {
    "theme": "dark",
    "colors": {
        "bg_primary": "#0f172a",
        "bg_secondary": "#1a1f2e",
        "bg_card": "rgba(255, 255, 255, 0.05)",
        "accent_blue": "#3b82f6",
        "accent_blue_light": "#60a5fa",
        "accent_purple": "#9333ea",
        "accent_purple_light": "#a855f7",
        "accent_gold": "#fbbf24",
        "accent_green": "#10b981",
        "accent_orange": "#f97316",
        "text_primary": "#ffffff",
        "text_secondary": "rgba(255, 255, 255, 0.8)",
        "text_muted": "rgba(255, 255, 255, 0.5)",
        "border": "rgba(255, 255, 255, 0.1)"
    },
    "gradients": {
        "blue": "linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%)",
        "purple": "linear-gradient(135deg, #9333ea 0%, #a855f7 100%)",
        "gold": "linear-gradient(135deg, #fbbf24 0%, #f97316 100%)",
        "story": "linear-gradient(45deg, #3b82f6, #9333ea, #f97316)"
    },
    "shadows": {
        "glow_blue": "0 0 40px rgba(59, 130, 246, 0.3)",
        "glow_purple": "0 0 40px rgba(147, 51, 234, 0.3)"
    },
    "reference": "https://service.if-juku.net/"
}

# ============================================
# サービスプラン設定 (if Business)
# ============================================
SERVICE_PLANS = {
    "ai_advisor": {
        "name": "AIパーソナル顧問プラン",
        "price": 55000,
        "price_text": "¥55,000/月",
        "target": "AI導入を検討中の企業",
        "features": [
            "48時間以内チャットレスポンス",
            "月1回60分ミーティング",
            "最適なAIツール選定サポート"
        ]
    },
    "ai_training": {
        "name": "AI人材育成プラン",
        "price": 33000,
        "price_text": "¥33,000/月/人",
        "target": "社内AI人材を育成したい組織",
        "features": [
            "月1回個別トレーニング",
            "毎日のQ&Aサポート",
            "トレーニング後フォローアップ"
        ]
    },
    "ai_development": {
        "name": "AI開発支援プラン",
        "price": 110000,
        "price_text": "¥110,000~/月",
        "target": "カスタムAIシステムが必要な企業",
        "features": [
            "Web・アプリ開発+AI統合",
            "自動化システム構築",
            "月次レビューミーティング"
        ]
    },
    "ai_course": {
        "name": "AI講座プログラム",
        "price": 11000,
        "price_text": "¥11,000/月",
        "target": "自主学習したい方",
        "features": [
            "動画コンテンツ見放題",
            "画像生成・データ分析・コーディング",
            "コミュニティ参加"
        ]
    }
}
