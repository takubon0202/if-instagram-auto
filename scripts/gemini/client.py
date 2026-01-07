"""
Gemini API Client
Google Gemini APIとの連携を行うメインクライアント
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

from .config import GEMINI_API_KEY, MODELS, IMAGE_SIZES, BRAND_CONFIG


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
    """

    def __init__(self, client: GeminiClient):
        self.client = client
        self.model = MODELS["research"]

    def research_instagram_trends(self, track: str = "juku") -> dict:
        """
        Instagramのトレンドをリサーチ

        Args:
            track: "juku" or "business"

        Returns:
            トレンド情報の辞書
        """
        if not self.client.is_available():
            return self._mock_trends(track)

        hashtags = BRAND_CONFIG.get("instagram_hashtags", {}).get(track, [])
        hashtag_str = " ".join(hashtags[:5])

        prompt = f"""
あなたはInstagramのトレンドリサーチャーです。
以下のハッシュタグに関連する最新のInstagramトレンドを調査してください。

ハッシュタグ: {hashtag_str}
対象: {"塾・教育・不登校支援" if track == "juku" else "企業向けAI研修・DX"}

以下の情報をJSON形式で出力してください:
{{
    "trending_topics": ["トピック1", "トピック2", "トピック3"],
    "popular_content_types": ["カルーセル", "リール", etc],
    "engagement_insights": "エンゲージメントの傾向",
    "recommended_hooks": ["フック案1", "フック案2", "フック案3"],
    "best_posting_times": ["時間1", "時間2"],
    "competitor_analysis": "競合の動向",
    "content_recommendations": ["提案1", "提案2", "提案3"]
}}
"""

        try:
            # Google検索によるグラウンディングを使用
            grounding_tool = types.Tool(
                google_search=types.GoogleSearch()
            )

            config = types.GenerateContentConfig(
                tools=[grounding_tool],
                response_mime_type="application/json"
            )

            response = self.client.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config
            )

            return json.loads(response.text)

        except Exception as e:
            print(f"Research error: {e}")
            return self._mock_trends(track)

    def analyze_competitor_posts(self, urls: list = None) -> dict:
        """競合投稿の分析"""
        if not self.client.is_available():
            return {"analysis": "API not available", "insights": []}

        prompt = f"""
Instagram上の教育系・オンライン塾の人気投稿を分析してください。
特に以下の点に注目:
1. エンゲージメント率が高い投稿の特徴
2. 使用されているビジュアルスタイル
3. キャプションの書き方
4. CTAの配置方法
5. ハッシュタグ戦略

JSON形式で出力してください。
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
            print(f"Competitor analysis error: {e}")
            return {"analysis": "Error", "insights": []}

    def get_realtime_trends(self) -> dict:
        """リアルタイムトレンド取得"""
        if not self.client.is_available():
            return self._mock_realtime_trends()

        prompt = """
現在の日本における以下のトレンドを調査してください:
1. 教育・学習に関するトレンド
2. 不登校・子育てに関する話題
3. AI・DXに関するビジネストレンド
4. SNSで話題になっているトピック

JSON形式で出力:
{
    "education_trends": [],
    "parenting_trends": [],
    "ai_business_trends": [],
    "social_media_trends": [],
    "recommended_content_angles": []
}
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
            print(f"Realtime trends error: {e}")
            return self._mock_realtime_trends()

    def _mock_trends(self, track: str) -> dict:
        """モックデータ（API未接続時）"""
        if track == "juku":
            return {
                "trending_topics": [
                    "新学期の準備",
                    "子どもの居場所づくり",
                    "オンライン学習のコツ"
                ],
                "popular_content_types": ["カルーセル", "リール"],
                "engagement_insights": "保護者向けの共感型コンテンツが高エンゲージメント",
                "recommended_hooks": [
                    "「学校に行きたくない」と言われたら",
                    "不登校の子どもが笑顔になった理由",
                    "うちの子、発達特性かも？と思ったとき"
                ],
                "best_posting_times": ["09:00", "20:00"],
                "competitor_analysis": "教育系アカウントは共感→解決策→CTAの流れが効果的",
                "content_recommendations": [
                    "保護者の悩みに寄り添うカルーセル",
                    "子どもの気持ちを代弁するリール",
                    "FAQ形式の情報発信"
                ]
            }
        else:
            return {
                "trending_topics": [
                    "生成AI活用事例",
                    "ChatGPTプロンプト術",
                    "中小企業DX成功例"
                ],
                "popular_content_types": ["カルーセル", "チェックリスト"],
                "engagement_insights": "実践的なテンプレート・チェックリストが保存されやすい",
                "recommended_hooks": [
                    "AI導入で失敗する会社の特徴",
                    "このプロンプト1つで業務効率化",
                    "うちの会社でもAI使える？"
                ],
                "best_posting_times": ["12:30", "18:00"],
                "competitor_analysis": "B2B系は具体的な数値・事例が信頼性を高める",
                "content_recommendations": [
                    "チェックリスト形式のカルーセル",
                    "Before/After事例",
                    "無料テンプレート配布"
                ]
            }

    def _mock_realtime_trends(self) -> dict:
        """リアルタイムトレンドのモックデータ"""
        return {
            "education_trends": [
                "オンライン学習の多様化",
                "個別最適化学習",
                "プログラミング教育必修化"
            ],
            "parenting_trends": [
                "子どもの居場所づくり",
                "不登校支援の多様化",
                "発達特性への理解促進"
            ],
            "ai_business_trends": [
                "生成AI業務活用",
                "プロンプトエンジニアリング",
                "AI研修需要増加"
            ],
            "social_media_trends": [
                "縦長動画コンテンツ",
                "カルーセル投稿の保存率",
                "ストーリーでのエンゲージメント"
            ],
            "recommended_content_angles": [
                "共感→解決策→CTA",
                "Before/After形式",
                "チェックリスト・テンプレート"
            ]
        }


class ImageGenerationAgent:
    """
    画像生成エージェント
    Gemini 2.5 Flash で Instagram用画像を生成
    """

    def __init__(self, client: GeminiClient):
        self.client = client
        self.model = MODELS["image"]
        self.output_dir = Path(__file__).parent.parent.parent / "assets" / "img" / "posts"

    def generate_carousel_images(
        self,
        post_id: str,
        slides: list,
        size_key: str = "feed_portrait"
    ) -> list:
        """
        カルーセル投稿用の画像を生成

        Args:
            post_id: 投稿ID
            slides: スライド情報のリスト
            size_key: 画像サイズキー（feed_portrait推奨: 4:5）

        Returns:
            生成された画像パスのリスト
        """
        size = IMAGE_SIZES.get(size_key, IMAGE_SIZES["feed_portrait"])
        generated_paths = []

        for i, slide in enumerate(slides, 1):
            prompt = self._build_image_prompt(slide, size)

            try:
                image_path = self._generate_single_image(
                    prompt=prompt,
                    filename=f"{post_id}-{i:02d}.png",
                    size=size
                )
                generated_paths.append(image_path)
            except Exception as e:
                print(f"Image generation error for slide {i}: {e}")
                # フォールバック: プレースホルダーSVGを作成
                fallback_path = self._create_placeholder_svg(
                    slide, f"{post_id}-{i:02d}.svg", size
                )
                generated_paths.append(fallback_path)

        return generated_paths

    def generate_reel_thumbnail(
        self,
        post_id: str,
        content: dict,
        size_key: str = "reel_story"
    ) -> str:
        """
        リール用サムネイル画像を生成

        Args:
            post_id: 投稿ID
            content: リールコンテンツ情報
            size_key: 画像サイズキー（reel_story: 9:16）

        Returns:
            生成された画像パス
        """
        size = IMAGE_SIZES.get(size_key, IMAGE_SIZES["reel_story"])

        prompt = f"""
Instagram リールのサムネイル画像を生成してください。

タイトル: {content.get('title', '')}
フック: {content.get('hook', '')}
スタイル: {BRAND_CONFIG['style']['visual']}
カラー: {', '.join(BRAND_CONFIG['style']['colors'])}

要件:
- 9:16の縦長フォーマット
- 目を引くビジュアル
- テキストオーバーレイ用のスペースを確保
- 日本アニメ風、やわらかい雰囲気
- 安心感・信頼感を与えるデザイン
"""

        try:
            return self._generate_single_image(
                prompt=prompt,
                filename=f"{post_id}-thumb.png",
                size=size
            )
        except Exception as e:
            print(f"Reel thumbnail generation error: {e}")
            return self._create_placeholder_svg(
                content, f"{post_id}-thumb.svg", size
            )

    def _build_image_prompt(self, slide: dict, size: dict) -> str:
        """画像生成プロンプトを構築"""
        slide_type = slide.get("type", "content")
        headline = slide.get("headline", "")
        subtext = slide.get("subtext", "")

        base_prompt = f"""
Instagram投稿用の画像を生成してください。

## コンテンツ
見出し: {headline}
補足: {subtext}
スライドタイプ: {slide_type}

## スタイル要件
- アスペクト比: {size['ratio']} ({size['width']}x{size['height']}px)
- スタイル: 日本アニメ風、やわらかい線、安心感
- 背景: 白または淡いブルー/グリーン基調
- 余白: 十分に確保（テキストオーバーレイ用）
- カラーパレット: {', '.join(BRAND_CONFIG['style']['colors'])}

## 禁止事項
- 派手すぎるデザイン
- 過度なキラキラ効果
- リアルな人物写真
- 文字のレンダリング（後から追加するため）

## 追加指示
- 清潔感と信頼感を重視
- 教育・学習をイメージさせる要素
- 親子や家庭の温かさを感じさせる雰囲気
"""
        return base_prompt

    def _generate_single_image(self, prompt: str, filename: str, size: dict) -> str:
        """単一画像を生成"""
        if not self.client.is_available():
            raise Exception("Gemini client not available")

        try:
            response = self.client.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["image"],
                )
            )

            # 画像データを保存
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        image_data = part.inline_data.data
                        output_path = self.output_dir / filename
                        output_path.parent.mkdir(parents=True, exist_ok=True)

                        with open(output_path, 'wb') as f:
                            f.write(base64.b64decode(image_data) if isinstance(image_data, str) else image_data)

                        return str(output_path.relative_to(self.output_dir.parent.parent))

            raise Exception("No image data in response")

        except Exception as e:
            raise Exception(f"Image generation failed: {e}")

    def _create_placeholder_svg(self, content: dict, filename: str, size: dict) -> str:
        """プレースホルダーSVGを作成"""
        headline = content.get("headline", content.get("title", ""))[:20]
        width = size["width"]
        height = size["height"]

        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
  <rect fill="#f0f7f9" width="{width}" height="{height}"/>
  <rect fill="#4A90A4" x="{width*0.1}" y="{height*0.1}" width="{width*0.8}" height="{height*0.15}" rx="8"/>
  <text x="{width/2}" y="{height*0.19}" text-anchor="middle" fill="white" font-family="sans-serif" font-size="{width*0.04}" font-weight="bold">{headline}</text>
  <circle cx="{width/2}" cy="{height*0.5}" r="{width*0.15}" fill="#7CB8A8" opacity="0.3"/>
  <text x="{width/2}" y="{height*0.53}" text-anchor="middle" fill="#4A90A4" font-family="sans-serif" font-size="{width*0.08}">if</text>
  <text x="{width/2}" y="{height*0.9}" text-anchor="middle" fill="#999" font-family="sans-serif" font-size="{width*0.025}">Generated by Gemini</text>
</svg>'''

        output_path = self.output_dir / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)

        return f"assets/img/posts/{filename}"


class ContentImprovementAgent:
    """
    コンテンツ改善エージェント
    投稿後のパフォーマンス分析と改善提案
    """

    def __init__(self, client: GeminiClient):
        self.client = client
        self.model = MODELS["content"]

    def analyze_post_performance(self, post_data: dict, metrics: dict) -> dict:
        """
        投稿パフォーマンスを分析

        Args:
            post_data: 投稿データ
            metrics: パフォーマンス指標

        Returns:
            分析結果と改善提案
        """
        if not self.client.is_available():
            return self._mock_analysis(post_data, metrics)

        prompt = f"""
以下のInstagram投稿のパフォーマンスを分析し、改善提案をしてください。

## 投稿データ
タイトル: {post_data.get('title', '')}
タイプ: {post_data.get('type', '')}
トラック: {post_data.get('track', '')}
キャプション: {post_data.get('caption', '')[:200]}...

## パフォーマンス指標
リーチ: {metrics.get('reach', 'N/A')}
インプレッション: {metrics.get('impressions', 'N/A')}
いいね: {metrics.get('likes', 'N/A')}
保存: {metrics.get('saves', 'N/A')}
コメント: {metrics.get('comments', 'N/A')}
シェア: {metrics.get('shares', 'N/A')}
プロフィール遷移: {metrics.get('profile_visits', 'N/A')}

## 分析項目
1. エンゲージメント率の評価
2. 強みと弱みの特定
3. 改善すべきポイント
4. 次回投稿への具体的な提案

JSON形式で出力:
{{
    "performance_score": 0-100,
    "strengths": [],
    "weaknesses": [],
    "improvement_suggestions": [],
    "next_post_recommendations": {{
        "hook_suggestions": [],
        "content_angle": "",
        "visual_recommendations": [],
        "caption_tips": []
    }}
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
            print(f"Performance analysis error: {e}")
            return self._mock_analysis(post_data, metrics)

    def suggest_improvements(self, post_data: dict) -> dict:
        """投稿内容の改善提案"""
        if not self.client.is_available():
            return self._mock_suggestions(post_data)

        prompt = f"""
以下のInstagram投稿内容を分析し、エンゲージメントを高めるための改善提案をしてください。

## 現在の投稿
タイトル: {post_data.get('title', '')}
キャプション: {post_data.get('caption', '')}
ハッシュタグ: {', '.join(post_data.get('hashtags', []))}

## ブランドガイドライン
- ブランド: {BRAND_CONFIG['name']}
- トーン: {BRAND_CONFIG['style']['tone']}
- 禁止ワード: {', '.join(BRAND_CONFIG['prohibited_words'])}

## 改善提案
1. フック（1枚目/冒頭）の改善案
2. キャプションの改善案
3. ハッシュタグの最適化
4. CTA（行動喚起）の改善
5. 視覚的な改善点

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
            print(f"Improvement suggestion error: {e}")
            return self._mock_suggestions(post_data)

    def _mock_analysis(self, post_data: dict, metrics: dict) -> dict:
        """モック分析データ"""
        return {
            "performance_score": 65,
            "strengths": [
                "配慮文が適切に含まれている",
                "CTAが明確",
                "ハッシュタグの数が適切"
            ],
            "weaknesses": [
                "フックがやや弱い",
                "視覚的なインパクトが不足",
                "投稿時間の最適化余地あり"
            ],
            "improvement_suggestions": [
                "1枚目のフックをより具体的な悩みに",
                "カルーセルの枚数を7-9枚に",
                "ストーリーでのシェアを追加"
            ],
            "next_post_recommendations": {
                "hook_suggestions": [
                    "「○○で悩んでいませんか？」形式",
                    "数字を使った具体的なフック",
                    "問いかけ形式で共感を誘う"
                ],
                "content_angle": "保護者の日常的な悩みに寄り添う",
                "visual_recommendations": [
                    "余白を増やす",
                    "文字サイズを大きく",
                    "ブランドカラーを統一"
                ],
                "caption_tips": [
                    "冒頭で共感を示す",
                    "箇条書きで読みやすく",
                    "最後にCTAを配置"
                ]
            }
        }

    def _mock_suggestions(self, post_data: dict) -> dict:
        """モック改善提案"""
        return {
            "hook_improvements": [
                "より具体的な数字を入れる",
                "ターゲットの悩みを直接言語化",
                "「知っていましたか？」形式で興味を引く"
            ],
            "caption_improvements": [
                "段落を短くして読みやすく",
                "絵文字は控えめに（1-2個）",
                "配慮文の位置を調整"
            ],
            "hashtag_improvements": [
                "ニッチなハッシュタグを追加",
                "トレンドハッシュタグを1-2個",
                "ブランド固有タグの作成を検討"
            ],
            "cta_improvements": [
                "具体的な行動を明示",
                "「無料」「簡単」などのハードルを下げる言葉",
                "次のステップを明確に"
            ],
            "visual_improvements": [
                "コントラストを高める",
                "重要な情報を上部に",
                "一貫したデザインシステム"
            ]
        }
