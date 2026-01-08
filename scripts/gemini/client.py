"""
Gemini API Client v2.0
if塾 Instagram ワークフロー
6カテゴリ × 5シーン構成対応
"""
import os
import json
import base64
from datetime import datetime
from pathlib import Path

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("Warning: google-genai not installed. Run: pip install google-genai")

from .config import (
    GEMINI_API_KEY, MODELS, IMAGE_SIZES, BRAND_CONFIG,
    CATEGORIES, THANKS_IMAGE, SCENE_STRUCTURE,
    IMAGE_GENERATION_CONFIG, LOGO_CONFIG,
    STYLE_PRESETS, NEGATIVE_PROMPTS, CONCEPT_TO_VISUAL,
    CATEGORY_ANIME_STYLES, SCENE_MATERIAL_TEMPLATES,
    get_current_time_context, get_search_queries, TIME_CONTEXT
)


class GeminiClient:
    """Gemini APIクライアント"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY")
        self.client = None
        self._initialize()

    def _initialize(self):
        """クライアント初期化"""
        if not GENAI_AVAILABLE:
            print("google-genai is not available")
            return

        if not self.api_key:
            print("Warning: GEMINI_API_KEY not set")
            return

        try:
            self.client = genai.Client(api_key=self.api_key)
        except Exception as e:
            print(f"Failed to initialize Gemini client: {e}")

    def is_available(self) -> bool:
        """クライアントが利用可能か確認"""
        return self.client is not None


class TrendResearchAgent:
    """
    トレンドリサーチエージェント v3.0
    Gemini 3 Pro Preview + Google Search でリアルタイムリサーチ
    6カテゴリ対応 + 時間認識機能（Time-Aware）

    【重要】常に現在の年月を認識し、最新情報を検索
    """

    def __init__(self, client: GeminiClient):
        self.client = client
        self.model = MODELS["research"]
        self.time_context = get_current_time_context()

    def research_category_trends(self, category_id: str) -> dict:
        """
        カテゴリ別のInstagramトレンドをリサーチ（時間認識対応）

        Args:
            category_id: カテゴリID (announcement, development, activity, education, ai_column, business)

        【時間認識】現在は {year}年{month}月 のトレンドを検索
        """
        if category_id not in CATEGORIES:
            return {"error": f"Unknown category: {category_id}"}

        # 時間コンテキストを更新
        self.time_context = get_current_time_context()
        year = self.time_context["current_year"]
        month = self.time_context["current_month"]
        month_name = self.time_context["current_month_name"]

        if not self.client.is_available():
            return self._mock_category_trends(category_id)

        category = CATEGORIES[category_id]
        hashtags = " ".join(category["hashtags"][:5])

        # 時間認識検索クエリを取得
        search_queries = get_search_queries(category_id)
        search_queries_str = "\n".join([f"- {q}" for q in search_queries])

        prompt = f"""
あなたはInstagramのトレンドリサーチャーです。

【重要】現在は{year}年{month_name}です。
以下のカテゴリに関連する{year}年の最新トレンドを調査してください。
古い情報（2024年以前）は使用しないでください。

カテゴリ: {category['name']}
目的: {category['purpose']}
関連ハッシュタグ: {hashtags}

検索キーワード例:
{search_queries_str}

以下の情報をJSON形式で出力してください:
{{
    "research_date": "{self.time_context['today_str']}",
    "trending_topics": ["{year}年のトピック1", "トピック2", "トピック3"],
    "popular_hooks": [
        "{year}年最新！〇〇",
        "{month_name}のニュース：〇〇",
        "今月の注目〇〇"
    ],
    "content_ideas": [
        {{
            "cover": "{year}年版タイトル案",
            "content1": "内容1の要点",
            "content2": "内容2の要点",
            "content3": "内容3の要点"
        }}
    ],
    "news_sources": ["参照したニュースURL1", "ニュースURL2"],
    "best_posting_times": ["09:00", "12:30", "20:00"],
    "engagement_tips": ["ヒント1", "ヒント2"]
}}
"""

        try:
            grounding_tool = types.Tool(
                google_search=types.GoogleSearch()
            )

            response = self.client.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[grounding_tool],
                    response_mime_type="application/json",
                    thinking_config=types.ThinkingConfig(thinking_level="minimal")
                )
            )

            return json.loads(response.text)

        except Exception as e:
            print(f"Research error: {e}")
            return self._mock_category_trends(category_id)

    def _mock_category_trends(self, category_id: str) -> dict:
        """カテゴリ別モックデータ（時間認識対応）"""
        ctx = get_current_time_context()
        year = ctx["current_year"]
        month_name = ctx["current_month_name"]
        today_str = ctx["today_str"]

        mock_data = {
            "announcement": {
                "research_date": today_str,
                "trending_topics": [
                    f"{year}年冬期講習募集開始",
                    "新AIコース開講",
                    "無料体験キャンペーン"
                ],
                "popular_hooks": [
                    f"【{year}年{month_name}】残り3席！",
                    "今だけ限定特典",
                    f"{month_name}スタート！"
                ],
                "content_ideas": [{
                    "cover": f"{year}年、AI学習を始めよう！",
                    "content1": f"この冬、AI×プログラミング合宿を開催",
                    "content2": "3日間でオリジナルAIアプリを完成",
                    "content3": f"日程：{year}年2月開催、オンライン"
                }],
                "news_sources": [],
                "best_posting_times": ["09:00", "12:30", "20:00"],
                "engagement_tips": ["緊急性を出す", "限定感を演出"]
            },
            "development": {
                "research_date": today_str,
                "trending_topics": [
                    f"{year}年版生徒のAIアプリ作品",
                    "Gemini API活用プロジェクト",
                    f"{year}年トレンドのWebサービス"
                ],
                "popular_hooks": [
                    f"【{year}年最新】高校生が作ったAIアプリが凄い",
                    "3時間でこれ作った",
                    f"{year}年の中学生エンジニア"
                ],
                "content_ideas": [{
                    "cover": f"{year}年版：高校生が作ったAIチャットボット",
                    "content1": f"{year}年、勉強の質問に答えてくれるAIが進化",
                    "content2": "Gemini APIを使って自分専用の先生を作成",
                    "content3": "今ではクラス全員が使ってます"
                }],
                "news_sources": [],
                "best_posting_times": ["12:30", "18:00", "21:00"],
                "engagement_tips": ["実際の画面を見せる", "ビフォーアフター"]
            },
            "activity": {
                "research_date": today_str,
                "trending_topics": [
                    f"{month_name}の授業風景レポート",
                    f"{year}年ハッカソン結果",
                    "生徒インタビュー"
                ],
                "popular_hooks": [
                    f"【{month_name}】今日の授業、盛り上がりすぎた",
                    f"{year}年ハッカソン優勝！",
                    "新しい仲間が増えました"
                ],
                "content_ideas": [{
                    "cover": f"{month_name}のハッカソン結果発表！",
                    "content1": "24時間でAIアプリを作るハッカソンを開催",
                    "content2": "参加者8名、熱い議論が交わされました",
                    "content3": "子どもたちの発想力に驚かされた1日でした"
                }],
                "news_sources": [],
                "best_posting_times": ["18:00", "20:00", "21:00"],
                "engagement_tips": ["リアルな写真を使う", "生徒の声を入れる"]
            },
            "education": {
                "research_date": today_str,
                "trending_topics": [
                    f"{year}年のAI時代の教育",
                    f"大学入試「情報I」{year}年対策",
                    f"{year}年に必要な子どものスキル"
                ],
                "popular_hooks": [
                    f"【{year}年版】プログラミングは本当に必要？",
                    f"{year}年、AI時代に消える仕事・残る仕事",
                    "学校の成績より大切なこと"
                ],
                "content_ideas": [{
                    "cover": f"{year}年、勉強はこう変わる",
                    "content1": f"{year}年、コードを書くだけの仕事はAIに代替",
                    "content2": "大切なのは『何を作るか』を考える力",
                    "content3": "若いうちからAIを使う側に回る経験を"
                }],
                "news_sources": [],
                "best_posting_times": ["09:00", "12:30", "20:00"],
                "engagement_tips": ["問いかけで始める", "保存したくなる情報"]
            },
            "ai_column": {
                "research_date": today_str,
                "trending_topics": [
                    f"Gemini {year}年最新機能",
                    f"ChatGPT {year}年活用術",
                    f"{year}年注目の画像生成AI"
                ],
                "popular_hooks": [
                    f"【{year}年{month_name}】ChatGPT、まだ普通に使ってるの？",
                    f"Gemini {year}がヤバすぎる",
                    f"{year}年これ知らないと損するAIツール"
                ],
                "content_ideas": [{
                    "cover": f"{year}年{month_name}のAIニュースまとめ",
                    "content1": f"Googleの最新AI「Gemini」{year}年アップデート",
                    "content2": "宿題の写真を送ると解説してくれる新機能",
                    "content3": "ただし計算ミスもあるので検算必須"
                }],
                "news_sources": [],
                "best_posting_times": ["12:30", "18:00", "21:00"],
                "engagement_tips": ["具体的なツール名を出す", "保存・シェア促進"]
            },
            "business": {
                "research_date": today_str,
                "trending_topics": [
                    f"{year}年中学生の副業術",
                    f"AIスタンプ販売{year}",
                    f"{year}年スキルを売る方法"
                ],
                "popular_hooks": [
                    f"【{year}年版】中学生でも月3万稼ぐ方法",
                    f"{year}年AIでスタンプ作成→販売",
                    f"{year}年高校生が副業で○万円"
                ],
                "content_ideas": [{
                    "cover": f"{year}年版：中学生でも月3万稼げる方法",
                    "content1": f"{year}年、生成AIでイラストを作ってスタンプ販売",
                    "content2": "Gemini画像生成→申請の3ステップ",
                    "content3": "売れるまで改善し続けるPDCAが身につく"
                }],
                "news_sources": [],
                "best_posting_times": ["18:00", "20:00", "21:00"],
                "engagement_tips": ["具体的な金額を出す", "手順を明確に"]
            }
        }

        return mock_data.get(category_id, mock_data["activity"])


class ContentGenerationAgent:
    """
    コンテンツ生成エージェント v3.0
    5シーン構成のコンテンツを生成
    時間認識機能（Time-Aware）対応
    """

    def __init__(self, client: GeminiClient):
        self.client = client
        self.model = MODELS["content"]
        self.time_context = get_current_time_context()

    def generate_5scene_content(self, category_id: str, topic: str) -> dict:
        """5シーン構成のコンテンツを生成（時間認識対応）"""
        if not self.client.is_available():
            return self._mock_content(category_id, topic)

        # 時間コンテキストを更新
        self.time_context = get_current_time_context()
        year = self.time_context["current_year"]
        month_name = self.time_context["current_month_name"]
        today_str = self.time_context["today_str"]

        category = CATEGORIES[category_id]

        prompt = f"""
以下の条件で、Instagram投稿用の5シーンコンテンツを生成してください。

【重要】現在は{year}年{month_name}です。
この時期に保護者や学生が気にするトピックを意識して、{year}年の最新情報を反映してください。

カテゴリ: {category['name']}
トピック: {topic}
投稿日: {today_str}

5シーン構成（マガジン形式）:
1. 表紙（Hook）: {category['cover_format']} - 「{year}年最新版」「{month_name}のニュース」など日付要素を含める
2. 内容1（Problem/課題）: {category['content1_format']} - 読者の現状や悩み
3. 内容2（Solution/ニュース）: {category['content2_format']} - 具体的な{year}年の情報やツール
4. 内容3（Deep Dive/活用法）: {category['content3_format']} - if塾の視点での活用法
5. サンクス（CTA/誘導）: アクション誘導（固定画像使用）

ブランド: {BRAND_CONFIG['name']}
トーン: {BRAND_CONFIG['style']['tone']}

JSON形式で出力:
{{
    "generated_at": "{self.time_context['timestamp']}",
    "cover": {{
        "headline": "{year}年版タイトル（短く、インパクト重視）",
        "subtext": "{month_name}の最新情報"
    }},
    "content1": {{
        "headline": "内容1のメインテキスト",
        "subtext": "補足テキスト"
    }},
    "content2": {{
        "headline": "内容2のメインテキスト",
        "subtext": "補足テキスト"
    }},
    "content3": {{
        "headline": "内容3のメインテキスト",
        "subtext": "補足テキスト"
    }},
    "caption": "【{year}年{month_name}】で始まるInstagramキャプション（改行入り）",
    "hashtags": ["#if塾", "#{year}年", "ハッシュタグ"]
}}
"""

        try:
            response = self.client.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    thinking_config=types.ThinkingConfig(thinking_level="minimal")
                )
            )

            return json.loads(response.text)

        except Exception as e:
            print(f"Content generation error: {e}")
            return self._mock_content(category_id, topic)

    def _mock_content(self, category_id: str, topic: str) -> dict:
        """モックコンテンツ（時間認識対応）"""
        ctx = get_current_time_context()
        year = ctx["current_year"]
        month_name = ctx["current_month_name"]
        timestamp = ctx["timestamp"]

        return {
            "generated_at": timestamp,
            "cover": {
                "headline": f"{year}年版：{topic[:15]}",
                "subtext": f"{month_name}の最新情報"
            },
            "content1": {
                "headline": "こんな悩みありませんか？",
                "subtext": f"{year}年の課題"
            },
            "content2": {
                "headline": f"{year}年の解決策をご紹介",
                "subtext": "最新ツールで解決"
            },
            "content3": {
                "headline": "今すぐ始めよう",
                "subtext": "if塾で学ぶ"
            },
            "caption": f"【{year}年{month_name}】{topic}\n\nif塾からお届けします。\n\n詳細はプロフィール欄から！",
            "hashtags": ["#if塾", f"#{year}年"] + CATEGORIES[category_id]["hashtags"][:8]
        }


class ImageGenerationAgent:
    """
    画像生成エージェント v5.0
    Gemini 3 Pro Image Preview + テキストオーバーレイ

    【統合アプローチ v5.0】
    - 画像: Gemini APIでImage-to-Image生成（キャラクター参照画像付き）
    - スタイル: if塾オリジナルちびキャラスタイルを維持
    - テキスト: Pillowでオーバーレイを追加（BIZ UD Gothic Bold）
    - 出力: テキスト付きの完成画像（1080x1350 / 4:5比率）
    """

    def __init__(self, client: GeminiClient):
        self.client = client
        self.model = MODELS["image"]  # gemini-3-pro-image-preview
        self.output_dir = Path(__file__).parent.parent.parent / "assets" / "img" / "posts"
        self.characters_dir = Path(__file__).parent.parent.parent / "assets" / "img" / "characters"
        self.max_retries = 3
        self.image_config = IMAGE_GENERATION_CONFIG
        self.style_presets = STYLE_PRESETS
        self.negative_prompts = NEGATIVE_PROMPTS
        self.concept_to_visual = CONCEPT_TO_VISUAL
        self.category_anime_styles = CATEGORY_ANIME_STYLES
        self.scene_templates = SCENE_MATERIAL_TEMPLATES

        # キャラクター参照画像をロード
        self.character_images = self._load_character_images()

        # テキストオーバーレイエンジンを初期化
        try:
            from .text_overlay import TextOverlayEngine
            self.text_overlay_engine = TextOverlayEngine()
            self.enable_text_overlay = True
            print("      [TextOverlay] Engine initialized (v2.0 with BIZ UD Gothic)")
        except ImportError as e:
            print(f"      [TextOverlay] Not available: {e}")
            self.text_overlay_engine = None
            self.enable_text_overlay = False

    def _load_character_images(self) -> dict:
        """
        if塾キャラクター参照画像をロード
        Image-to-Image生成でスタイル維持に使用
        """
        try:
            from PIL import Image as PILImage
        except ImportError:
            print("      [Characters] PIL not available")
            return {}

        characters = {}
        character_files = {
            "girl_happy": "girl_happy.png",
            "girl_surprised": "girl_surprised.png",
            "girl_excited": "girl_excited.png",
            "boy_green_happy": "boy_green_happy.png",
            "boy_green_thinking": "boy_green_thinking.png",
            "boy_green_smile": "boy_green_smile.png",
            "boy_black_energetic": "boy_black_energetic.png",
            "child_sad": "child_sad.png",
        }

        for char_name, filename in character_files.items():
            char_path = self.characters_dir / filename
            if char_path.exists():
                try:
                    characters[char_name] = PILImage.open(str(char_path)).convert("RGBA")
                    print(f"      [Characters] Loaded: {char_name}")
                except Exception as e:
                    print(f"      [Characters] Failed to load {char_name}: {e}")

        return characters

    def _select_character_for_scene(self, scene_id: int, category_id: str) -> str:
        """
        シーンとカテゴリに適したキャラクターを選択

        Returns:
            str: キャラクターキー（例: "girl_happy"）
        """
        # カテゴリ別のデフォルトキャラクター
        category_characters = {
            "announcement": ["girl_excited", "boy_green_happy"],
            "development": ["boy_green_smile", "boy_green_thinking"],
            "activity": ["girl_happy", "boy_black_energetic"],
            "education": ["girl_surprised", "boy_green_thinking"],
            "ai_column": ["boy_green_smile", "girl_happy"],
            "business": ["boy_green_happy", "girl_excited"],
        }

        # シーン別の感情マッピング
        scene_emotions = {
            1: "excited",   # cover: 興味を引く
            2: "thinking",  # content1: 課題提示
            3: "happy",     # content2: 解決策
            4: "smile",     # content3: アクション
        }

        chars = category_characters.get(category_id, ["girl_happy", "boy_green_happy"])
        emotion = scene_emotions.get(scene_id, "happy")

        # 感情に合ったキャラクターを優先
        for char in chars:
            if emotion in char:
                return char

        return chars[scene_id % len(chars)]

    def generate_scene_image(
        self,
        post_id: str,
        scene: dict,
        category: dict,
        size: dict = None,
        use_reference_image: bool = True
    ) -> str:
        """
        シーン用画像を生成（Image-to-Image with Character References）

        v5.0: キャラクター参照画像を使用したImage-to-Image生成
        純粋なアニメイラスト素材を生成（テキスト・UI要素なし）

        Args:
            post_id: 投稿ID
            scene: シーン情報（headline, subtext含む）
            category: カテゴリ情報
            size: 画像サイズ（未使用、ImageConfigで制御）
            use_reference_image: キャラクター参照画像を使用するか

        Returns:
            str: 生成された画像のパス
        """
        if not self.client.is_available():
            raise Exception("Gemini client not available")

        scene_id = scene.get('scene_id', 1)
        category_id = category.get('id', 'activity')

        # 概念からビジュアル記述への変換
        visual_scene = self._convert_concept_to_visual(scene, category_id)

        # スタイルプリセットの取得
        style_key = self.category_anime_styles.get(category_id, {}).get('recommended_style', 'japanese_anime')
        style = self.style_presets.get(style_key, self.style_presets['japanese_anime'])

        # カテゴリ別アニメスタイルの取得
        anime_style = self.category_anime_styles.get(category_id, self.category_anime_styles['activity'])

        # シーン別素材テンプレートの取得
        scene_template = self.scene_templates.get(scene_id, self.scene_templates[1])

        # Image-to-Image用プロンプトを構築（キャラクタースタイル維持）
        prompt = self._build_image_to_image_prompt(
            visual_scene=visual_scene,
            style=style,
            anime_style=anime_style,
            scene_template=scene_template,
            category=category,
            scene_id=scene_id
        )

        # ネガティブプロンプトを構築
        negative_prompt = self._build_negative_prompt()

        print(f"      [Prompt] {prompt[:100]}...")

        # 参照キャラクター画像を選択
        char_key = self._select_character_for_scene(scene_id, category_id)
        reference_image = self.character_images.get(char_key) if use_reference_image else None

        if reference_image:
            print(f"      [Reference] Using character: {char_key}")

        # リトライロジック付きで画像生成
        last_error = None
        for attempt in range(self.max_retries):
            try:
                # コンテンツを構築（Image-to-Image）
                if reference_image and use_reference_image:
                    # Image-to-Image: 参照画像 + プロンプト
                    contents = [
                        f"""Create an illustration in the EXACT same chibi/cute anime art style as this reference character image.

{prompt}

IMPORTANT STYLE REQUIREMENTS:
- Match the cute chibi proportions (big head, small body)
- Match the thick black outline style
- Match the simple, clean coloring style
- Match the soft shading and highlights
- Create a new scene with similar character design, NOT a copy

Negative: {negative_prompt}""",
                        reference_image
                    ]
                else:
                    # Text-to-Image（参照画像なし）
                    contents = f"{prompt}\n\nNegative: {negative_prompt}"

                # Gemini API を使用
                response = self.client.client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        response_modalities=['IMAGE'],
                        image_config=types.ImageConfig(
                            aspect_ratio=self.image_config["aspect_ratio"],  # "4:5"
                        )
                    )
                )

                # レスポンスから画像を抽出
                for part in response.parts:
                    if part.text is not None:
                        continue
                    elif part.inline_data is not None:
                        image = part.as_image()

                        filename = f"{post_id}-{scene_id:02d}.png"
                        output_path = self.output_dir / filename
                        output_path.parent.mkdir(parents=True, exist_ok=True)

                        # 4:5にリサイズして保存（1080x1350）
                        from PIL import Image as PILImage
                        if image.size != (1080, 1350):
                            image = self._resize_to_instagram(image)

                        image.save(str(output_path), "PNG")
                        print(f"      [OK] Scene {scene_id}: Base image saved ({image.size})")

                        # テキストオーバーレイを追加
                        if self.enable_text_overlay and self.text_overlay_engine:
                            headline = scene.get('headline', '')
                            subtext = scene.get('subtext', '')

                            if headline:  # テキストがある場合のみオーバーレイ
                                try:
                                    self.text_overlay_engine.create_instagram_post(
                                        background_image_path=str(output_path),
                                        headline=headline,
                                        subtext=subtext,
                                        output_path=str(output_path),
                                        style=category_id
                                    )
                                    print(f"      [OK] Scene {scene_id}: Text overlay added")
                                except Exception as overlay_error:
                                    print(f"      [WARN] Text overlay failed: {overlay_error}")

                        return f"assets/img/posts/{filename}"

                raise Exception("No image data in response")

            except Exception as e:
                last_error = e
                print(f"      [Retry {attempt + 1}/{self.max_retries}] {e}")
                if attempt < self.max_retries - 1:
                    import time
                    time.sleep(2)

        raise Exception(f"Image generation failed after {self.max_retries} attempts: {last_error}")

    def _resize_to_instagram(self, img) -> 'PILImage':
        """
        画像をInstagram 4:5比率（1080x1350）にリサイズ

        Args:
            img: PIL Image

        Returns:
            PIL Image: リサイズ後の画像
        """
        from PIL import Image as PILImage

        target_w, target_h = 1080, 1350
        target_ratio = target_w / target_h

        src_w, src_h = img.size
        src_ratio = src_w / src_h

        if abs(src_ratio - target_ratio) < 0.01:
            # すでに正しい比率
            return img.resize((target_w, target_h), PILImage.Resampling.LANCZOS)

        # カバーモード: 短い辺を基準にスケール
        if src_ratio > target_ratio:
            # 横長の画像 → 高さ基準
            new_h = target_h
            new_w = int(src_w * (target_h / src_h))
        else:
            # 縦長の画像 → 幅基準
            new_w = target_w
            new_h = int(src_h * (target_w / src_w))

        img = img.resize((new_w, new_h), PILImage.Resampling.LANCZOS)

        # 中央でクロップ
        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2
        img = img.crop((left, top, left + target_w, top + target_h))

        return img

    def _build_image_to_image_prompt(
        self,
        visual_scene: str,
        style: dict,
        anime_style: dict,
        scene_template: dict,
        category: dict,
        scene_id: int
    ) -> str:
        """
        Image-to-Image用のプロンプトを構築

        キャラクタースタイルを維持しながら新しいシーンを生成
        """
        # スタイルプレフィックス
        style_prefix = "Cute chibi anime style, thick black outlines, simple clean coloring"

        # キャラクターと設定
        character_mood = anime_style.get('character_mood', 'happy, engaged')
        setting = anime_style.get('setting', 'modern classroom')
        color_palette = anime_style.get('color_palette', 'vibrant colors')

        # シーン構成
        composition = scene_template.get('composition', 'centered character')

        # カテゴリカラー
        primary_color = category.get('colors', {}).get('primary', '#4A90A4')

        prompt = f"""
{style_prefix},

Create a new illustration scene:
- Scene: {visual_scene}
- Character mood: {character_mood}
- Setting: {setting} with {color_palette}
- Composition: {composition}
- Main accent color: {primary_color}

Technical requirements:
- Cute chibi proportions (large head, small body like the reference)
- Thick black outlines around all elements
- Simple, clean cell-shaded coloring
- Soft highlights and minimal shading
- No text, no UI elements, no borders
- Leave clear space at top and bottom for text overlay
- Vertical composition optimized for 4:5 aspect ratio
- High quality illustration suitable for Instagram post
"""
        return prompt.strip()

    def _convert_concept_to_visual(self, scene: dict, category_id: str) -> str:
        """
        概念的な内容を具体的な視覚描写に変換

        例: "安心感" → "warm soft lighting, cozy room, gentle smile"
        """
        headline = scene.get('headline', '') or scene.get('label', '')
        subtext = scene.get('subtext', '')

        # 概念辞書から変換を試みる
        visual_elements = []

        for concept, visual in self.concept_to_visual.items():
            if concept in headline or concept in subtext:
                visual_elements.append(visual)

        # カテゴリに基づくデフォルトビジュアル
        anime_style = self.category_anime_styles.get(category_id, {})
        if anime_style:
            visual_elements.append(anime_style.get('setting', ''))
            visual_elements.append(anime_style.get('illustration_focus', ''))

        # 変換結果がない場合はプログラミング学習のデフォルト
        if not visual_elements:
            visual_elements.append(
                "anime student at computer, focused expression, coding on screen, "
                "modern classroom background, warm lighting"
            )

        return ", ".join(filter(None, visual_elements))

    def _build_material_prompt(
        self,
        visual_scene: str,
        style: dict,
        anime_style: dict,
        scene_template: dict,
        category: dict
    ) -> str:
        """
        Material（素材）フォーカスのプロンプトを構築

        【重要】「Instagram」や「投稿」という言葉を使用しない
        純粋なアニメイラスト素材として生成
        """
        # スタイルプレフィックス
        style_prefix = style.get('prompt_prefix', 'Japanese anime style, high quality')
        visual_quality = style.get('visual_quality', 'studio quality anime illustration')
        atmosphere = style.get('atmosphere', 'warm and inviting')

        # キャラクターと設定
        character_mood = anime_style.get('character_mood', 'happy, engaged')
        setting = anime_style.get('setting', 'modern classroom')
        color_palette = anime_style.get('color_palette', 'vibrant colors')

        # シーン構成
        composition = scene_template.get('composition', 'centered character')

        # カテゴリカラー
        primary_color = category.get('colors', {}).get('primary', '#4A90A4')
        secondary_color = category.get('colors', {}).get('secondary', '#7CB8A8')

        prompt = f"""
{style_prefix},
{visual_quality},

Scene description: {visual_scene},

Character: anime style student character, {character_mood}, expressive eyes,
Setting: {setting},
Color palette: {color_palette}, accent colors {primary_color} and {secondary_color},
Atmosphere: {atmosphere},
Composition: {composition},

Technical requirements:
- Pure illustration with no text, no UI elements, no borders
- Clean background suitable for text overlay
- High quality anime art style
- Professional illustration quality
- No watermarks or signatures
- Leave space for text overlay (especially top and bottom areas)
"""
        return prompt.strip()

    def _build_negative_prompt(self) -> str:
        """
        ネガティブプロンプトを構築
        UI要素、テキスト、日付要素、低品質要素を除外
        """
        all_negatives = []
        all_negatives.extend(self.negative_prompts.get('global', []))
        all_negatives.extend(self.negative_prompts.get('ui_elements', []))
        all_negatives.extend(self.negative_prompts.get('text_elements', []))
        all_negatives.extend(self.negative_prompts.get('date_elements', []))  # 日付要素も除外
        all_negatives.extend(self.negative_prompts.get('unwanted_styles', []))

        return ", ".join(all_negatives)

    def _get_scene_material_direction(self, scene_id: int, category_id: str) -> str:
        """
        シーン別の素材方向性を取得（UIではなくイラスト素材として）
        """
        anime_style = self.category_anime_styles.get(category_id, {})
        scene_template = self.scene_templates.get(scene_id, self.scene_templates[1])

        directions = {
            1: f"""
Cover illustration: Eye-catching hero image
- {anime_style.get('character_mood', 'energetic')} anime character
- {anime_style.get('setting', 'classroom')} background
- Dynamic pose, looking at viewer
- Space at top for title text overlay
- {scene_template.get('composition', 'centered')}""",
            2: f"""
Problem/Context illustration: Storytelling scene
- Character showing curiosity or concern
- {anime_style.get('setting', 'study environment')}
- Thought bubble or question mark visual metaphor
- Clear space for explanatory text
- {scene_template.get('composition', 'character in context')}""",
            3: f"""
Solution illustration: Positive transformation
- Character with confident, happy expression
- Visual metaphor of growth or achievement
- Bright, optimistic color tones
- Space for solution text overlay
- {scene_template.get('composition', 'transformation visual')}""",
            4: f"""
Call-to-action illustration: Forward momentum
- Character moving forward or gesturing invitation
- Open door or path visual metaphor
- Encouraging, welcoming atmosphere
- Space for CTA text overlay
- {scene_template.get('composition', 'directional elements')}"""
        }

        return directions.get(scene_id, directions[1])

    def generate_complete_post_images(
        self,
        post_id: str,
        content: dict,
        category: dict,
        size: dict = None
    ) -> list:
        """
        コンテンツから4シーンの純粋なイラスト素材を一括生成

        【注意】テキストは画像に含めず、別途overlay_textとして保持

        Args:
            post_id: 投稿ID
            content: ContentGenerationAgentからのコンテンツ
            category: カテゴリ情報
            size: 画像サイズ（未使用、ImageConfigで制御）

        Returns:
            list: 生成された画像パスのリスト（4シーン分）
        """
        scenes = [
            {"scene_id": 1, "scene_name": "cover", "label": "表紙",
             "headline": content.get("cover", {}).get("headline", ""),
             "subtext": content.get("cover", {}).get("subtext", ""),
             "purpose": "hook_attention"},
            {"scene_id": 2, "scene_name": "content1", "label": "内容1",
             "headline": content.get("content1", {}).get("headline", ""),
             "subtext": content.get("content1", {}).get("subtext", ""),
             "purpose": "problem_presentation"},
            {"scene_id": 3, "scene_name": "content2", "label": "内容2",
             "headline": content.get("content2", {}).get("headline", ""),
             "subtext": content.get("content2", {}).get("subtext", ""),
             "purpose": "solution_showcase"},
            {"scene_id": 4, "scene_name": "content3", "label": "内容3",
             "headline": content.get("content3", {}).get("headline", ""),
             "subtext": content.get("content3", {}).get("subtext", ""),
             "purpose": "action_inspiration"},
        ]

        image_paths = []
        for scene in scenes:
            try:
                path = self.generate_scene_image(post_id, scene, category)
                image_paths.append(path)
            except Exception as e:
                print(f"    Scene {scene['scene_id']} generation failed: {e}")
                raise

        return image_paths


class ContentImprovementAgent:
    """
    コンテンツ改善エージェント
    投稿後のパフォーマンス分析と改善提案
    """

    def __init__(self, client: GeminiClient):
        self.client = client
        self.model = MODELS["content"]

    def analyze_post_performance(self, post_data: dict, metrics: dict) -> dict:
        """投稿パフォーマンスを分析"""
        if not self.client.is_available():
            return self._mock_analysis(post_data, metrics)

        prompt = f"""
以下のInstagram投稿のパフォーマンスを分析してください。

## 投稿情報
タイトル: {post_data.get('title', '')}
カテゴリ: {post_data.get('category', '')}
キャプション: {post_data.get('caption', '')[:200]}...

## パフォーマンス指標
リーチ: {metrics.get('reach', 'N/A')}
いいね: {metrics.get('likes', 'N/A')}
保存: {metrics.get('saves', 'N/A')}
コメント: {metrics.get('comments', 'N/A')}

## 分析項目
1. エンゲージメント率の評価
2. 強みと弱みの特定
3. 改善すべきポイント
4. 次回投稿への提案

JSON形式で出力してください。
"""

        try:
            response = self.client.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    thinking_config=types.ThinkingConfig(thinking_level="minimal")
                )
            )

            return json.loads(response.text)

        except Exception as e:
            print(f"Analysis error: {e}")
            return self._mock_analysis(post_data, metrics)

    def _mock_analysis(self, post_data: dict, metrics: dict) -> dict:
        """モック分析データ"""
        return {
            "performance_score": 70,
            "strengths": [
                "5シーン構成が分かりやすい",
                "CTAが明確",
                "ハッシュタグが適切"
            ],
            "weaknesses": [
                "表紙のインパクトが弱い",
                "投稿時間を最適化できる"
            ],
            "improvement_suggestions": [
                "表紙に数字や問いかけを入れる",
                "ストーリーでも告知する"
            ],
            "next_post_recommendations": {
                "hook_suggestions": [
                    "〇〇を知らないと損する",
                    "たった3分でできる〇〇"
                ],
                "content_angle": "より具体的な事例を入れる",
                "visual_tips": ["コントラストを上げる", "文字を大きく"]
            }
        }
