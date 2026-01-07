"""
Gemini API Configuration
if塾 Instagram ワークフロー設定 v2.0
6カテゴリ × 5シーン構成
"""
import os

# API Key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Models
MODELS = {
    "research": "gemini-3-pro-preview",   # リサーチ・トレンド分析
    "content": "gemini-2.5-flash",         # コンテンツ生成
    "image": "gemini-2.5-flash",           # 画像生成
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
