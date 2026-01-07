"""
Gemini統合ワークフロー v2.0
if塾 Instagram自動投稿システム

6カテゴリ × 5シーン構成
- 表紙 → 内容1 → 内容2 → 内容3 → サンクス

使用方法:
    python -m scripts.gemini.workflow daily --date 2026-01-08
    python -m scripts.gemini.workflow research --category ai_column
    python -m scripts.gemini.workflow generate --category development --topic "AIチャットボット"
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
    ContentImprovementAgent,
    ContentGenerationAgent
)
from scripts.gemini.config import (
    BRAND_CONFIG,
    IMAGE_SIZES,
    CATEGORIES,
    WEEKLY_SCHEDULE,
    POSTING_TIMES,
    THANKS_IMAGE,
    SCENE_STRUCTURE,
    RESEARCH_CONFIG
)


class InstagramWorkflowV2:
    """
    Instagram投稿ワークフロー v2.0
    6カテゴリ × 5シーン構成
    """

    def __init__(self, api_key: str = None):
        self.client = GeminiClient(api_key)
        self.research_agent = TrendResearchAgent(self.client)
        self.image_agent = ImageGenerationAgent(self.client)
        self.content_agent = ContentGenerationAgent(self.client)
        self.improvement_agent = ContentImprovementAgent(self.client)

        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.output_dir = Path(__file__).parent.parent.parent / "scripts"
        self.assets_dir = Path(__file__).parent.parent.parent / "assets" / "img" / "posts"

    def get_category_for_date(self, date_str: str) -> str:
        """指定日付のカテゴリを取得"""
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        weekday = date_obj.weekday()
        return WEEKLY_SCHEDULE.get(weekday, "activity")

    def run_daily_workflow(self, date: str = None) -> dict:
        """
        毎日のワークフローを実行
        5シーン構成のカルーセル投稿を生成
        """
        date = date or datetime.now().strftime("%Y-%m-%d")
        category_id = self.get_category_for_date(date)
        category = CATEGORIES[category_id]
        day_names = ["月", "火", "水", "木", "金", "土", "日"]
        day_of_week = day_names[datetime.strptime(date, "%Y-%m-%d").weekday()]

        print(f"\n{'='*60}")
        print(f"  if塾 Daily Workflow v2.0 - {date} ({day_of_week})")
        print(f"  カテゴリ: {category['name']}")
        print(f"{'='*60}\n")

        results = {
            "date": date,
            "day_of_week": day_of_week,
            "category": category_id,
            "category_name": category["name"],
            "posts": [],
            "status": "success"
        }

        # Step 1: トレンドリサーチ
        print("[Step 1/5] トレンドリサーチ...")
        try:
            trends = self.research_agent.research_category_trends(category_id)
            results["research"] = trends
            print(f"  [OK] {category['name']}のトレンド取得完了")
        except Exception as e:
            print(f"  [NG] リサーチエラー: {e}")
            results["research"] = {"error": str(e)}

        # Step 2: コンテンツ企画（5シーン構成）
        print("\n[Step 2/5] コンテンツ企画（5シーン構成）...")
        post = self._plan_5scene_post(date, category_id, results.get("research", {}))
        results["posts"].append(post)
        print(f"  [OK] 投稿企画完了: {post['title']}")

        # Step 3: 画像生成（4枚 + サンクス画像）
        print("\n[Step 3/5] 画像生成...")
        try:
            image_paths = self._generate_5scene_images(post, category)
            post["generated_images"] = image_paths
            print(f"  [OK] {len(image_paths)}枚生成（サンクス画像含む）")
        except Exception as e:
            print(f"  [NG] 画像生成エラー: {e}")
            post["generated_images"] = self._create_fallback_images(post, category)

        # Step 4: データ更新
        print("\n[Step 4/5] データ更新...")
        try:
            self._update_posts_json([post])
            print("  [OK] posts.json 更新完了")
        except Exception as e:
            print(f"  [NG] データ更新エラー: {e}")
            results["status"] = "partial"

        # Step 5: レポート生成
        print("\n[Step 5/5] レポート生成...")
        report_path = self._generate_daily_report(date, results)
        print(f"  [OK] レポート保存: {report_path}")

        print(f"\n{'='*60}")
        print(f"  ワークフロー完了: {results['status']}")
        print(f"{'='*60}\n")

        return results

    def _plan_5scene_post(self, date: str, category_id: str, research: dict) -> dict:
        """5シーン構成の投稿を企画"""
        category = CATEGORIES[category_id]
        post_id = f"{date}-0900-{category_id}-carousel-01"

        # トレンドからトピックを選択
        topics = research.get("trending_topics", [])
        topic = topics[0] if topics else f"{category['name']}について"

        # 5シーン構成
        scenes = [
            {
                "scene_id": 1,
                "scene_name": "cover",
                "label": "表紙",
                "headline": topic,
                "subtext": "",
                "purpose": category["cover_format"]
            },
            {
                "scene_id": 2,
                "scene_name": "content1",
                "label": "内容1",
                "headline": "",
                "subtext": "",
                "purpose": category["content1_format"]
            },
            {
                "scene_id": 3,
                "scene_name": "content2",
                "label": "内容2",
                "headline": "",
                "subtext": "",
                "purpose": category["content2_format"]
            },
            {
                "scene_id": 4,
                "scene_name": "content3",
                "label": "内容3",
                "headline": "",
                "subtext": "",
                "purpose": category["content3_format"]
            },
            {
                "scene_id": 5,
                "scene_name": "thanks",
                "label": "サンクス",
                "headline": "いつもありがとうございます！",
                "subtext": "詳細はプロフィール欄から",
                "purpose": "アクション誘導",
                "fixed_image": THANKS_IMAGE
            }
        ]

        # キャプション生成
        caption = self._generate_caption(category, topic)

        return {
            "id": post_id,
            "datetime": f"{date}T09:00:00+09:00",
            "type": "carousel",
            "category": category_id,
            "category_name": category["name"],
            "title": topic,
            "scenes": scenes,
            "caption": caption,
            "hashtags": category["hashtags"][:10],
            "cta_url": BRAND_CONFIG["url"],
            "colors": category["colors"],
            "visual_style": category["visual_style"]
        }

    def _generate_5scene_images(self, post: dict, category: dict) -> list:
        """5シーン分の画像を生成"""
        image_paths = []
        size = IMAGE_SIZES["feed_portrait"]

        for scene in post["scenes"]:
            if scene.get("fixed_image"):
                # サンクス画像は固定
                image_paths.append(scene["fixed_image"])
            else:
                # 各シーンの画像を生成
                try:
                    path = self.image_agent.generate_scene_image(
                        post_id=post["id"],
                        scene=scene,
                        category=category,
                        size=size
                    )
                    image_paths.append(path)
                except Exception as e:
                    print(f"    Scene {scene['scene_id']} error: {e}")
                    # フォールバック
                    fallback = self._create_scene_placeholder(post, scene, category)
                    image_paths.append(fallback)

        return image_paths

    def _create_fallback_images(self, post: dict, category: dict) -> list:
        """フォールバック画像を作成"""
        image_paths = []
        for scene in post["scenes"]:
            if scene.get("fixed_image"):
                image_paths.append(scene["fixed_image"])
            else:
                path = self._create_scene_placeholder(post, scene, category)
                image_paths.append(path)
        return image_paths

    def _create_scene_placeholder(self, post: dict, scene: dict, category: dict) -> str:
        """シーン用プレースホルダーSVGを作成"""
        filename = f"{post['id']}-{scene['scene_id']:02d}.svg"
        colors = category["colors"]
        headline = scene.get("headline", scene["label"])[:20]
        purpose = scene.get("purpose", "")[:30]

        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{colors['primary']};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{colors['secondary']};stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect fill="url(#bg)" width="1080" height="1350"/>
  <rect fill="{colors['accent']}" x="80" y="100" width="920" height="200" rx="20" opacity="0.9"/>
  <text x="540" y="220" text-anchor="middle" fill="{colors['text']}" font-family="sans-serif" font-size="60" font-weight="bold">{headline}</text>
  <text x="540" y="280" text-anchor="middle" fill="{colors['text']}" font-family="sans-serif" font-size="30" opacity="0.8">{purpose}</text>
  <circle cx="540" cy="700" r="150" fill="white" opacity="0.2"/>
  <text x="540" y="720" text-anchor="middle" fill="white" font-family="sans-serif" font-size="80" font-weight="bold">if塾</text>
  <text x="540" y="1280" text-anchor="middle" fill="white" font-family="sans-serif" font-size="24" opacity="0.7">Scene {scene['scene_id']}: {scene['label']}</text>
</svg>'''

        output_path = self.assets_dir / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)

        return f"assets/img/posts/{filename}"

    def _generate_caption(self, category: dict, topic: str) -> str:
        """キャプションを生成"""
        caption = f"""{topic}

{category['name']}をお届けします。

---

いつもご覧いただきありがとうございます！
if塾では、子どもの可能性を最大限に発揮する
プログラミング教育を提供しています。

詳細・お申し込みはプロフィール欄から！

{' '.join(category['hashtags'][:10])}"""

        return caption

    def _update_posts_json(self, new_posts: list):
        """posts.jsonを更新"""
        posts_path = self.data_dir / "posts.json"

        if posts_path.exists():
            with open(posts_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {"posts": []}

        for post in new_posts:
            # 既存の投稿を削除
            data["posts"] = [p for p in data["posts"] if p["id"] != post["id"]]

            # 新しい投稿データを整形
            post_data = {
                "id": post["id"],
                "datetime": post["datetime"],
                "type": post["type"],
                "category": post["category"],
                "title": post["title"],
                "caption": post["caption"],
                "hashtags": post["hashtags"],
                "cta_url": post["cta_url"],
                "media": [
                    {"kind": "image", "src": img, "alt": f"シーン{i+1}"}
                    for i, img in enumerate(post.get("generated_images", []))
                ],
                "highlight": post["category_name"],
                "notes_for_instagram": {
                    "cover_text": post["title"][:20],
                    "first_comment": "詳細は if-juku.net から",
                    "scenes": post.get("scenes", [])
                }
            }
            data["posts"].append(post_data)

        # 日時でソート
        data["posts"].sort(key=lambda x: x["datetime"], reverse=True)

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
- カテゴリ: {results['category_name']}
- 生成投稿数: {len(results['posts'])}

## 5シーン構成
| シーン | ラベル | 内容 |
|--------|--------|------|
| 1 | 表紙 | インパクト重視のタイトル |
| 2 | 内容1 | 概要・課題提示 |
| 3 | 内容2 | メリット・解決策 |
| 4 | 内容3 | 詳細・提案 |
| 5 | サンクス | アクション誘導（固定画像） |

## リサーチ結果
```json
{json.dumps(results.get('research', {}), ensure_ascii=False, indent=2)}
```

## 生成された投稿
"""
        for post in results['posts']:
            report_content += f"""
### {post['title']}
- ID: {post['id']}
- カテゴリ: {post['category_name']}
- 画像数: {len(post.get('generated_images', []))}枚（サンクス画像含む）
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

    def run_research_only(self, category_id: str = None) -> dict:
        """リサーチのみ実行"""
        print("\n[Research Mode]")
        results = {}

        if category_id:
            categories = [category_id]
        else:
            categories = list(CATEGORIES.keys())

        for cat_id in categories:
            category = CATEGORIES[cat_id]
            print(f"{category['name']}のトレンドリサーチ中...")
            results[cat_id] = self.research_agent.research_category_trends(cat_id)

        # 結果を保存
        output_path = self.output_dir / "research_results.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"\nリサーチ結果を保存: {output_path}")
        return results


def main():
    parser = argparse.ArgumentParser(description="if塾 Instagram Workflow v2.0 with Gemini")
    parser.add_argument("command", choices=["daily", "research", "generate"],
                       help="実行するコマンド")
    parser.add_argument("--date", help="対象日付 (YYYY-MM-DD)")
    parser.add_argument("--category", help="カテゴリID")
    parser.add_argument("--topic", help="トピック（generateコマンド用）")
    parser.add_argument("--api-key", help="Gemini API Key")

    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
    workflow = InstagramWorkflowV2(api_key)

    if args.command == "daily":
        workflow.run_daily_workflow(args.date)
    elif args.command == "research":
        workflow.run_research_only(args.category)
    elif args.command == "generate":
        if not args.category:
            print("Error: --category is required for generate command")
            sys.exit(1)
        # カスタム生成（将来実装）
        print("Custom generation not yet implemented")


if __name__ == "__main__":
    main()
