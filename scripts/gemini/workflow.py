"""
Gemini統合ワークフロー
if(塾) Instagram自動投稿のメインワークフロー

使用方法:
    python -m scripts.gemini.workflow daily
    python -m scripts.gemini.workflow research
    python -m scripts.gemini.workflow improve --post-id <POST_ID>
"""
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# パスを追加
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.gemini.client import (
    GeminiClient,
    TrendResearchAgent,
    ImageGenerationAgent,
    ContentImprovementAgent
)
from scripts.gemini.config import (
    BRAND_CONFIG,
    IMAGE_SIZES,
    RESEARCH_CONFIG
)


class InstagramWorkflow:
    """
    Instagram投稿ワークフロー
    Gemini APIを活用した自動コンテンツ生成
    """

    def __init__(self, api_key: str = None):
        self.client = GeminiClient(api_key)
        self.research_agent = TrendResearchAgent(self.client)
        self.image_agent = ImageGenerationAgent(self.client)
        self.improvement_agent = ContentImprovementAgent(self.client)

        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.output_dir = Path(__file__).parent.parent.parent / "scripts"

    def run_daily_workflow(self, date: str = None) -> dict:
        """
        毎日のワークフローを実行

        Args:
            date: 対象日付（YYYY-MM-DD形式）

        Returns:
            生成結果
        """
        date = date or datetime.now().strftime("%Y-%m-%d")
        day_of_week = self._get_day_of_week(date)

        print(f"\n{'='*50}")
        print(f"  if(塾) Daily Workflow - {date} ({day_of_week})")
        print(f"{'='*50}\n")

        results = {
            "date": date,
            "day_of_week": day_of_week,
            "research": {},
            "posts": [],
            "images": [],
            "status": "success"
        }

        # Step 1: トレンドリサーチ
        print("[Step 1/5] トレンドリサーチ...")
        try:
            juku_trends = self.research_agent.research_instagram_trends("juku")
            biz_trends = self.research_agent.research_instagram_trends("business")
            realtime_trends = self.research_agent.get_realtime_trends()

            results["research"] = {
                "juku": juku_trends,
                "business": biz_trends,
                "realtime": realtime_trends
            }
            print("  [OK] リサーチ完了")
        except Exception as e:
            print(f"  [NG] リサーチエラー: {e}")
            results["research"] = {"error": str(e)}

        # Step 2: コンテンツ企画
        print("\n[Step 2/5] コンテンツ企画...")
        posts = self._plan_daily_content(date, day_of_week, results["research"])
        results["posts"] = posts
        print(f"  [OK] {len(posts)}件の投稿を企画")

        # Step 3: 画像生成
        print("\n[Step 3/5] 画像生成...")
        for i, post in enumerate(posts):
            print(f"  投稿 {i+1}/{len(posts)}: {post['title']}")
            try:
                if post["type"] == "carousel":
                    image_paths = self.image_agent.generate_carousel_images(
                        post["id"],
                        post.get("slides", []),
                        "feed_portrait"  # 4:5 推奨
                    )
                    post["generated_images"] = image_paths
                elif post["type"] == "reel":
                    thumb_path = self.image_agent.generate_reel_thumbnail(
                        post["id"],
                        post,
                        "reel_story"  # 9:16
                    )
                    post["generated_images"] = [thumb_path]

                results["images"].extend(post.get("generated_images", []))
                print(f"    [OK] {len(post.get('generated_images', []))}枚生成")
            except Exception as e:
                print(f"    [NG] 画像生成エラー: {e}")
                post["generated_images"] = []

        # Step 4: データ更新
        print("\n[Step 4/5] データ更新...")
        try:
            self._update_posts_json(posts)
            print("  [OK] posts.json 更新完了")
        except Exception as e:
            print(f"  [NG] データ更新エラー: {e}")
            results["status"] = "partial"

        # Step 5: レポート生成
        print("\n[Step 5/5] レポート生成...")
        report_path = self._generate_daily_report(date, results)
        print(f"  [OK] レポート保存: {report_path}")

        print(f"\n{'='*50}")
        print(f"  ワークフロー完了: {results['status']}")
        print(f"{'='*50}\n")

        return results

    def run_research_only(self, track: str = "both") -> dict:
        """
        リサーチのみ実行

        Args:
            track: "juku", "business", or "both"
        """
        print("\n[Research Mode]")
        results = {}

        if track in ["juku", "both"]:
            print("塾向けトレンドリサーチ中...")
            results["juku"] = self.research_agent.research_instagram_trends("juku")

        if track in ["business", "both"]:
            print("企業向けトレンドリサーチ中...")
            results["business"] = self.research_agent.research_instagram_trends("business")

        print("リアルタイムトレンド取得中...")
        results["realtime"] = self.research_agent.get_realtime_trends()

        print("\n競合分析中...")
        results["competitor"] = self.research_agent.analyze_competitor_posts()

        # 結果を保存
        output_path = self.output_dir / "research_results.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"\nリサーチ結果を保存: {output_path}")
        return results

    def run_improvement_analysis(self, post_id: str, metrics: dict = None) -> dict:
        """
        投稿改善分析を実行

        Args:
            post_id: 分析対象の投稿ID
            metrics: パフォーマンス指標
        """
        print(f"\n[Improvement Analysis] Post: {post_id}")

        # 投稿データを取得
        posts_data = self._load_posts_json()
        post = next((p for p in posts_data.get("posts", []) if p["id"] == post_id), None)

        if not post:
            print(f"投稿が見つかりません: {post_id}")
            return {"error": "Post not found"}

        metrics = metrics or {}

        # パフォーマンス分析
        print("パフォーマンス分析中...")
        analysis = self.improvement_agent.analyze_post_performance(post, metrics)

        # 改善提案
        print("改善提案生成中...")
        suggestions = self.improvement_agent.suggest_improvements(post)

        results = {
            "post_id": post_id,
            "analysis": analysis,
            "suggestions": suggestions,
            "timestamp": datetime.now().isoformat()
        }

        # 結果を保存
        output_path = self.output_dir / f"improvement_{post_id}.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"\n分析結果を保存: {output_path}")
        return results

    def _plan_daily_content(self, date: str, day_of_week: str, research: dict) -> list:
        """日次コンテンツを企画"""
        posts = []

        # 週次テーママッピング
        juku_themes = {
            "月": "安心・居場所",
            "火": "学習のハードルを下げる",
            "水": "保護者向け（声かけ）",
            "木": "AI/ITスキル",
            "金": "無料体験の背中押し",
            "土": "FAQ",
            "日": "まとめ"
        }

        biz_themes = {
            "月": "研修の失敗パターン",
            "水": "ワークフロー設計",
            "金": "LP改善チェック",
        }

        # リサーチ結果から推奨フックを取得
        juku_hooks = research.get("juku", {}).get("recommended_hooks", [])
        biz_hooks = research.get("business", {}).get("recommended_hooks", [])

        # 09:00 - 塾向けカルーセル
        posts.append(self._create_post_plan(
            date=date,
            slot="0900",
            track="juku",
            post_type="carousel",
            theme=juku_themes.get(day_of_week, "安心・居場所"),
            hooks=juku_hooks,
            research=research.get("juku", {})
        ))

        # 12:30 - 企業向けカルーセル
        posts.append(self._create_post_plan(
            date=date,
            slot="1230",
            track="business",
            post_type="carousel",
            theme=biz_themes.get(day_of_week, "AI活用"),
            hooks=biz_hooks,
            research=research.get("business", {})
        ))

        # 20:00 - 塾向けリール
        posts.append(self._create_post_plan(
            date=date,
            slot="2000",
            track="juku",
            post_type="reel",
            theme=juku_themes.get(day_of_week, "共感・安心"),
            hooks=juku_hooks,
            research=research.get("juku", {})
        ))

        return posts

    def _create_post_plan(
        self,
        date: str,
        slot: str,
        track: str,
        post_type: str,
        theme: str,
        hooks: list,
        research: dict
    ) -> dict:
        """投稿企画を作成"""
        track_short = "biz" if track == "business" else track
        post_id = f"{date}-{slot}-{track_short}-{post_type}-01"

        # フックを選択（リサーチ結果から or デフォルト）
        hook = hooks[0] if hooks else f"{theme}について"

        # スライド構成（カルーセルの場合）
        slides = []
        if post_type == "carousel":
            num_slides = 7 if track == "juku" else 6
            slides = [
                {"number": 1, "type": "hook", "headline": hook, "subtext": ""},
                {"number": 2, "type": "problem", "headline": "こんな悩みありませんか？", "subtext": ""},
            ]
            for i in range(3, num_slides):
                slides.append({
                    "number": i,
                    "type": "solution",
                    "headline": f"ポイント{i-2}",
                    "subtext": ""
                })
            slides.append({
                "number": num_slides,
                "type": "cta",
                "headline": "詳しくはこちら",
                "subtext": "if-juku.net"
            })

        # リール台本（リールの場合）
        reel_script = None
        if post_type == "reel":
            reel_script = {
                "duration": 15,
                "sections": [
                    {"timestamp": "0:00-0:01", "text_overlay": hook},
                    {"timestamp": "0:01-0:04", "text_overlay": "（問題提起）"},
                    {"timestamp": "0:04-0:08", "text_overlay": "（視点転換）"},
                    {"timestamp": "0:08-0:12", "text_overlay": "（解決策）"},
                    {"timestamp": "0:12-0:15", "text_overlay": "if-juku.net"},
                ]
            }

        # ハッシュタグ
        base_hashtags = RESEARCH_CONFIG["instagram_hashtags"].get(track, [])
        trending_topics = research.get("trending_topics", [])

        return {
            "id": post_id,
            "datetime": f"{date}T{slot[:2]}:{slot[2:]}:00+09:00",
            "type": post_type,
            "track": track,
            "title": f"{theme}（{date}）",
            "theme": theme,
            "hook": hook,
            "slides": slides,
            "reel_script": reel_script,
            "caption": self._generate_caption(track, theme, hook),
            "hashtags": base_hashtags[:10],
            "cta_url": "https://if-juku.net/",
            "highlight": "保護者向け" if track == "juku" else "企業研修",
            "research_insights": {
                "trending_topics": trending_topics[:3],
                "recommended_content": research.get("content_recommendations", [])[:2]
            }
        }

    def _generate_caption(self, track: str, theme: str, hook: str) -> str:
        """キャプションを生成"""
        if track == "juku":
            caption = f"""{hook}

{theme}について、今日はお伝えします。

お子さまのペースを大切に、
一緒に考えていきましょう。

※お子さまの状況は一人ひとり異なります。
必要に応じて専門家へのご相談もご検討ください。

▼ 無料体験・ご相談は
if-juku.net"""
        else:
            caption = f"""{hook}

{theme}について解説します。

御社の課題に合わせた
具体的なご提案をいたします。

▼ 無料相談のご予約は
if-juku.net"""

        return caption

    def _load_posts_json(self) -> dict:
        """posts.jsonを読み込み"""
        posts_path = self.data_dir / "posts.json"
        if posts_path.exists():
            with open(posts_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"posts": []}

    def _update_posts_json(self, new_posts: list):
        """posts.jsonを更新"""
        data = self._load_posts_json()

        for post in new_posts:
            # 既存の投稿を削除（同じIDがあれば）
            data["posts"] = [p for p in data["posts"] if p["id"] != post["id"]]

            # 投稿データを整形
            post_data = {
                "id": post["id"],
                "datetime": post["datetime"],
                "type": post["type"],
                "track": post["track"],
                "title": post["title"],
                "caption": post["caption"],
                "hashtags": post["hashtags"],
                "cta_url": post["cta_url"],
                "media": [
                    {"kind": "image", "src": img, "alt": f"スライド{i+1}"}
                    for i, img in enumerate(post.get("generated_images", []))
                ] or [{"kind": "image", "src": f"assets/img/posts/{post['id']}.svg", "alt": post["title"]}],
                "highlight": post["highlight"],
                "notes_for_instagram": {
                    "cover_text": post.get("hook", "")[:20],
                    "first_comment": "詳細は if-juku.net から",
                    "reel_script": json.dumps(post.get("reel_script"), ensure_ascii=False) if post.get("reel_script") else None
                }
            }
            data["posts"].append(post_data)

        # 日時でソート
        data["posts"].sort(key=lambda x: x["datetime"])

        # 保存
        posts_path = self.data_dir / "posts.json"
        with open(posts_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _generate_daily_report(self, date: str, results: dict) -> str:
        """日次レポートを生成"""
        report_dir = self.output_dir / "daily_reports"
        report_dir.mkdir(exist_ok=True)

        report_path = report_dir / f"{date}.md"

        report_content = f"""# Daily Report - {date}

## サマリー
- ステータス: {results['status']}
- 生成投稿数: {len(results['posts'])}
- 生成画像数: {len(results['images'])}

## リサーチ結果

### 塾向けトレンド
{json.dumps(results['research'].get('juku', {}), ensure_ascii=False, indent=2)}

### 企業向けトレンド
{json.dumps(results['research'].get('business', {}), ensure_ascii=False, indent=2)}

## 生成された投稿

"""
        for i, post in enumerate(results['posts'], 1):
            report_content += f"""### {i}. {post['title']}
- ID: {post['id']}
- タイプ: {post['type']}
- トラック: {post['track']}
- フック: {post.get('hook', 'N/A')}
- 画像: {len(post.get('generated_images', []))}枚

"""

        report_content += f"""
## 次のステップ
1. 生成された画像を確認
2. キャプションを最終調整
3. Instagram投稿 or 予約投稿
4. パフォーマンス追跡

---
Generated at: {datetime.now().isoformat()}
"""

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        return str(report_path)

    def _get_day_of_week(self, date_str: str) -> str:
        """曜日を取得"""
        days = ["月", "火", "水", "木", "金", "土", "日"]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return days[date_obj.weekday()]


def main():
    parser = argparse.ArgumentParser(description="if(塾) Instagram Workflow with Gemini")
    parser.add_argument("command", choices=["daily", "research", "improve"],
                       help="実行するコマンド")
    parser.add_argument("--date", help="対象日付 (YYYY-MM-DD)")
    parser.add_argument("--post-id", help="投稿ID (improveコマンド用)")
    parser.add_argument("--track", choices=["juku", "business", "both"],
                       default="both", help="リサーチ対象")
    parser.add_argument("--api-key", help="Gemini API Key")

    args = parser.parse_args()

    # 環境変数からAPIキーを取得（引数で上書き可能）
    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")

    workflow = InstagramWorkflow(api_key)

    if args.command == "daily":
        workflow.run_daily_workflow(args.date)
    elif args.command == "research":
        workflow.run_research_only(args.track)
    elif args.command == "improve":
        if not args.post_id:
            print("Error: --post-id is required for improve command")
            sys.exit(1)
        workflow.run_improvement_analysis(args.post_id)


if __name__ == "__main__":
    main()
