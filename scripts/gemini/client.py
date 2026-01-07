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
    CATEGORY_ANIME_STYLES, SCENE_MATERIAL_TEMPLATES
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
    トレンドリサーチエージェント
    Gemini 3 Pro Preview + Google Search でリアルタイムリサーチ
    6カテゴリ対応
    """

    def __init__(self, client: GeminiClient):
        self.client = client
        self.model = MODELS["research"]

    def research_category_trends(self, category_id: str) -> dict:
        """
        カテゴリ別のInstagramトレンドをリサーチ

        Args:
            category_id: カテゴリID (announcement, development, activity, education, ai_column, business)
        """
        if category_id not in CATEGORIES:
            return {"error": f"Unknown category: {category_id}"}

        if not self.client.is_available():
            return self._mock_category_trends(category_id)

        category = CATEGORIES[category_id]
        hashtags = " ".join(category["hashtags"][:5])

        prompt = f"""
あなたはInstagramのトレンドリサーチャーです。
以下のカテゴリに関連する最新のInstagramトレンドを調査してください。

カテゴリ: {category['name']}
目的: {category['purpose']}
関連ハッシュタグ: {hashtags}

以下の情報をJSON形式で出力してください:
{{
    "trending_topics": ["トピック1", "トピック2", "トピック3"],
    "popular_hooks": ["フック案1", "フック案2", "フック案3"],
    "content_ideas": [
        {{
            "cover": "表紙のタイトル案",
            "content1": "内容1の要点",
            "content2": "内容2の要点",
            "content3": "内容3の要点"
        }}
    ],
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
                    response_mime_type="application/json"
                )
            )

            return json.loads(response.text)

        except Exception as e:
            print(f"Research error: {e}")
            return self._mock_category_trends(category_id)

    def _mock_category_trends(self, category_id: str) -> dict:
        """カテゴリ別モックデータ"""
        mock_data = {
            "announcement": {
                "trending_topics": [
                    "夏期講習募集開始",
                    "新コース開講",
                    "無料体験キャンペーン"
                ],
                "popular_hooks": [
                    "【緊急募集】残り3席！",
                    "今だけ限定特典",
                    "来週スタート！"
                ],
                "content_ideas": [{
                    "cover": "夏期講習、始まります！",
                    "content1": "この夏、AI×プログラミング合宿を開催",
                    "content2": "3日間でオリジナルアプリを完成",
                    "content3": "日程：8月10日〜12日、オンライン開催"
                }],
                "best_posting_times": ["09:00", "12:30", "20:00"],
                "engagement_tips": ["緊急性を出す", "限定感を演出"]
            },
            "development": {
                "trending_topics": [
                    "生徒のAIアプリ作品",
                    "ゲーム開発実績",
                    "Webサービス公開"
                ],
                "popular_hooks": [
                    "高校生が作ったAIアプリが凄い",
                    "3時間でこれ作った",
                    "中学生エンジニア誕生"
                ],
                "content_ideas": [{
                    "cover": "高校生が作ったAIチャットボット",
                    "content1": "勉強の質問に答えてくれるAIが欲しかった",
                    "content2": "ChatGPT APIを使って自分専用の先生を作成",
                    "content3": "今ではクラス全員が使ってます"
                }],
                "best_posting_times": ["12:30", "18:00", "21:00"],
                "engagement_tips": ["実際の画面を見せる", "ビフォーアフター"]
            },
            "activity": {
                "trending_topics": [
                    "授業風景レポート",
                    "ハッカソン結果",
                    "生徒インタビュー"
                ],
                "popular_hooks": [
                    "今日の授業、盛り上がりすぎた",
                    "ハッカソン優勝！",
                    "新しい仲間が増えました"
                ],
                "content_ideas": [{
                    "cover": "本日のハッカソン結果発表！",
                    "content1": "24時間でアプリを作るハッカソンを開催",
                    "content2": "参加者8名、熱い議論が交わされました",
                    "content3": "子どもたちの発想力に驚かされた1日でした"
                }],
                "best_posting_times": ["18:00", "20:00", "21:00"],
                "engagement_tips": ["リアルな写真を使う", "生徒の声を入れる"]
            },
            "education": {
                "trending_topics": [
                    "AI時代の教育",
                    "プログラミング教育の意義",
                    "子どもの将来スキル"
                ],
                "popular_hooks": [
                    "『プログラミングは不要』は本当か？",
                    "AI時代に消える仕事、残る仕事",
                    "学校の成績より大切なこと"
                ],
                "content_ideas": [{
                    "cover": "プログラミングは本当に必要？",
                    "content1": "コードを書くだけの仕事はAIに代替される",
                    "content2": "大切なのは『何を作るか』を考える力",
                    "content3": "若いうちからAIを使う側に回る経験を"
                }],
                "best_posting_times": ["09:00", "12:30", "20:00"],
                "engagement_tips": ["問いかけで始める", "保存したくなる情報"]
            },
            "ai_column": {
                "trending_topics": [
                    "Gemini 2.5の新機能",
                    "ChatGPT活用術",
                    "画像生成AI比較"
                ],
                "popular_hooks": [
                    "ChatGPT、まだ普通に使ってるの？",
                    "Gemini 2.5がヤバすぎる",
                    "これ知らないと損するAIツール"
                ],
                "content_ideas": [{
                    "cover": "Gemini 2.5、ここがヤバい",
                    "content1": "Googleの最新AI「Gemini 2.5」が登場",
                    "content2": "宿題の写真を送ると解説してくれる",
                    "content3": "ただし計算ミスもあるので検算必須"
                }],
                "best_posting_times": ["12:30", "18:00", "21:00"],
                "engagement_tips": ["具体的なツール名を出す", "保存・シェア促進"]
            },
            "business": {
                "trending_topics": [
                    "中学生の副業術",
                    "LINEスタンプ販売",
                    "スキルを売る方法"
                ],
                "popular_hooks": [
                    "中学生でも月3万稼ぐ方法",
                    "LINEスタンプで小遣い稼ぎ",
                    "高校生が副業で○万円"
                ],
                "content_ideas": [{
                    "cover": "中学生でも月3万稼げる方法",
                    "content1": "生成AIでイラストを作ってLINEスタンプ販売",
                    "content2": "Midjourney→Photoshop→申請の3ステップ",
                    "content3": "売れるまで改善し続けるPDCAが身につく"
                }],
                "best_posting_times": ["18:00", "20:00", "21:00"],
                "engagement_tips": ["具体的な金額を出す", "手順を明確に"]
            }
        }

        return mock_data.get(category_id, mock_data["activity"])


class ContentGenerationAgent:
    """
    コンテンツ生成エージェント
    5シーン構成のコンテンツを生成
    """

    def __init__(self, client: GeminiClient):
        self.client = client
        self.model = MODELS["content"]

    def generate_5scene_content(self, category_id: str, topic: str) -> dict:
        """5シーン構成のコンテンツを生成"""
        if not self.client.is_available():
            return self._mock_content(category_id, topic)

        category = CATEGORIES[category_id]

        prompt = f"""
以下の条件で、Instagram投稿用の5シーンコンテンツを生成してください。

カテゴリ: {category['name']}
トピック: {topic}

5シーン構成:
1. 表紙: {category['cover_format']}
2. 内容1: {category['content1_format']}
3. 内容2: {category['content2_format']}
4. 内容3: {category['content3_format']}
5. サンクス: アクション誘導（固定画像使用）

ブランド: {BRAND_CONFIG['name']}
トーン: {BRAND_CONFIG['style']['tone']}

JSON形式で出力:
{{
    "cover": {{
        "headline": "表紙のタイトル（短く、インパクト重視）",
        "subtext": "補足テキスト"
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
    "caption": "Instagramキャプション（改行入り）",
    "hashtags": ["ハッシュタグ1", "ハッシュタグ2"]
}}
"""

        try:
            response = self.client.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )

            return json.loads(response.text)

        except Exception as e:
            print(f"Content generation error: {e}")
            return self._mock_content(category_id, topic)

    def _mock_content(self, category_id: str, topic: str) -> dict:
        """モックコンテンツ"""
        return {
            "cover": {
                "headline": topic[:20],
                "subtext": "if塾からお届け"
            },
            "content1": {
                "headline": "こんな悩みありませんか？",
                "subtext": ""
            },
            "content2": {
                "headline": "解決策をご紹介",
                "subtext": ""
            },
            "content3": {
                "headline": "今すぐ始めよう",
                "subtext": ""
            },
            "caption": f"{topic}\n\nif塾からお届けします。\n\n詳細はプロフィール欄から！",
            "hashtags": CATEGORIES[category_id]["hashtags"][:10]
        }


class ImageGenerationAgent:
    """
    画像生成エージェント v3.0
    Gemini 3 Pro Image Preview で純粋なアニメイラストを生成

    【Material vs Context 分離アプローチ】
    - 画像: 純粋なアニメイラスト素材（テキスト・UI要素なし）
    - テキスト: フロントエンドでオーバーレイ表示
    - ロゴ: フロントエンドで重ねて表示
    """

    def __init__(self, client: GeminiClient):
        self.client = client
        self.model = MODELS["image"]  # gemini-3-pro-image-preview
        self.output_dir = Path(__file__).parent.parent.parent / "assets" / "img" / "posts"
        self.max_retries = 3
        self.image_config = IMAGE_GENERATION_CONFIG
        self.style_presets = STYLE_PRESETS
        self.negative_prompts = NEGATIVE_PROMPTS
        self.concept_to_visual = CONCEPT_TO_VISUAL
        self.category_anime_styles = CATEGORY_ANIME_STYLES
        self.scene_templates = SCENE_MATERIAL_TEMPLATES

    def generate_scene_image(
        self,
        post_id: str,
        scene: dict,
        category: dict,
        size: dict = None
    ) -> str:
        """
        シーン用画像を生成（Gemini 3 Pro Image Preview）
        純粋なアニメイラスト素材を生成（テキスト・UI要素なし）

        Args:
            post_id: 投稿ID
            scene: シーン情報（headline, subtext含む）
            category: カテゴリ情報
            size: 画像サイズ（未使用、ImageConfigで制御）

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

        # 純粋なアニメイラスト用プロンプトを構築（英語）
        prompt = self._build_material_prompt(
            visual_scene=visual_scene,
            style=style,
            anime_style=anime_style,
            scene_template=scene_template,
            category=category
        )

        # ネガティブプロンプトを構築
        negative_prompt = self._build_negative_prompt()

        print(f"      [Prompt] {prompt[:100]}...")

        # リトライロジック付きで画像生成
        last_error = None
        for attempt in range(self.max_retries):
            try:
                # Gemini 3 Pro Image Preview API を使用
                response = self.client.client.models.generate_content(
                    model=self.model,
                    contents=f"{prompt}\n\nNegative: {negative_prompt}",
                    config=types.GenerateContentConfig(
                        image_config=types.ImageConfig(
                            aspect_ratio=self.image_config["aspect_ratio"],  # "4:5"
                            image_size=self.image_config["resolution"]       # "1K"
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

                        image.save(str(output_path))
                        print(f"      [OK] Scene {scene_id}: Pure anime illustration saved")
                        return f"assets/img/posts/{filename}"

                raise Exception("No image data in response")

            except Exception as e:
                last_error = e
                print(f"      [Retry {attempt + 1}/{self.max_retries}] {e}")
                if attempt < self.max_retries - 1:
                    import time
                    time.sleep(2)

        raise Exception(f"Image generation failed after {self.max_retries} attempts: {last_error}")

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
        UI要素、テキスト、低品質要素を除外
        """
        all_negatives = []
        all_negatives.extend(self.negative_prompts.get('global', []))
        all_negatives.extend(self.negative_prompts.get('ui_elements', []))
        all_negatives.extend(self.negative_prompts.get('text_elements', []))
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
                    response_mime_type="application/json"
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
