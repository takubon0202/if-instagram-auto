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
    CATEGORIES, THANKS_IMAGE, SCENE_STRUCTURE
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
    画像生成エージェント
    Gemini 2.5 Flash Image (Nano Banana) で Instagram用画像を生成
    5シーン構成対応
    """

    def __init__(self, client: GeminiClient):
        self.client = client
        self.model = MODELS["image"]
        self.output_dir = Path(__file__).parent.parent.parent / "assets" / "img" / "posts"

    def generate_scene_image(
        self,
        post_id: str,
        scene: dict,
        category: dict,
        size: dict
    ) -> str:
        """
        シーン用画像を生成（Gemini 2.5 Flash Image）

        Args:
            post_id: 投稿ID
            scene: シーン情報
            category: カテゴリ情報
            size: 画像サイズ
        """
        if not self.client.is_available():
            raise Exception("Gemini client not available")

        # Gemini 2.5 Flash Image用プロンプト
        prompt = f"""
Create an Instagram post background image for a programming school.

Style: {category['visual_style']}
Category: {category['name']}
Color scheme: Primary {category['colors']['primary']}, Secondary {category['colors']['secondary']}
Scene: {scene.get('label', '')} - {scene.get('purpose', 'content slide')}

Requirements:
- Modern, clean design suitable for text overlay
- Tech-inspired aesthetic with gradient backgrounds
- Leave clear space in center for Japanese text overlay
- No text, letters, or words in the image
- Professional look for education/programming school
- Aspect ratio: {size.get('ratio', '4:5')} ({size.get('width', 1080)}x{size.get('height', 1350)}px)
"""

        try:
            # Gemini 2.5 Flash Image API を使用
            response = self.client.client.models.generate_content(
                model=self.model,
                contents=[prompt],
            )

            # レスポンスから画像を抽出
            for part in response.parts:
                if part.text is not None:
                    # テキストレスポンスはスキップ
                    continue
                elif part.inline_data is not None:
                    # 画像データを保存
                    image = part.as_image()

                    filename = f"{post_id}-{scene['scene_id']:02d}.png"
                    output_path = self.output_dir / filename
                    output_path.parent.mkdir(parents=True, exist_ok=True)

                    image.save(str(output_path))

                    return f"assets/img/posts/{filename}"

            raise Exception("No image data in response")

        except Exception as e:
            raise Exception(f"Image generation failed: {e}")


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
