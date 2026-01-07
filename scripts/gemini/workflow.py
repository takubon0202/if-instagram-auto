"""
Gemini統合ワークフロー v3.0
if塾 Instagram自動投稿システム

6カテゴリ × 5シーン構成
- 表紙 → 内容1 → 内容2 → 内容3 → サンクス

【v3.0 新機能】
- 時間認識機能（Time-Aware）: 常に現在の年月を認識
- 動的リサーチ: 2026年の最新情報を検索
- 日付ベースのファイル命名: YYYYMMDD形式

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
    RESEARCH_CONFIG,
    get_current_time_context,
    TIME_CONTEXT
)
from scripts.gemini.staff import StaffImageAgent, StaffImageManager


class InstagramWorkflowV3:
    """
    Instagram投稿ワークフロー v3.0
    6カテゴリ × 5シーン構成
    時間認識機能（Time-Aware）対応
    """

    def __init__(self, api_key: str = None):
        self.client = GeminiClient(api_key)
        self.research_agent = TrendResearchAgent(self.client)
        self.image_agent = ImageGenerationAgent(self.client)
        self.content_agent = ContentGenerationAgent(self.client)
        self.improvement_agent = ContentImprovementAgent(self.client)
        self.staff_agent = StaffImageAgent()

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

        # Step 2: コンテンツ企画（5シーン構成）+ スタッフ選択
        print("\n[Step 2/5] コンテンツ企画（5シーン構成）...")
        post = self._plan_5scene_post(date, category_id, results.get("research", {}))
        results["posts"].append(post)
        print(f"  [OK] 投稿企画完了: {post['title']}")
        if post.get("staff"):
            print(f"  [OK] スタッフ選択: {post['staff'].get('name', 'なし')}")

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
        """5シーン構成の投稿を企画（AIコンテンツ生成含む）時間認識対応"""
        category = CATEGORIES[category_id]

        # 時間コンテキストを取得
        time_ctx = get_current_time_context()
        date_id = datetime.strptime(date, "%Y-%m-%d").strftime("%Y%m%d")

        # 日付ベースのpost_id生成（YYYYMMDD_category形式）
        post_id = f"{date_id}_{category_id}"

        # トレンドからトピックを選択
        topics = research.get("trending_topics", [])
        topic = topics[0] if topics else f"{category['name']}について"

        # コンテンツ生成（ContentGenerationAgentを使用）
        print("    [AI] コンテンツ生成中...")
        content = self.content_agent.generate_5scene_content(category_id, topic)
        print(f"    [OK] コンテンツ生成完了")

        # スタッフ画像を選択
        staff_suggestion = self.staff_agent.suggest_staff_for_post(category_id, topic)
        selected_staff = staff_suggestion.get("suggested_staff")
        staff_info = None
        if selected_staff:
            staff_info = self.staff_agent.manager.get_staff_info_for_post(selected_staff["id"])

        # 各シーンのスタッフ画像を取得
        scene_staff_images = {}
        for scene_name in ["cover", "content1", "content2", "content3"]:
            staff_id = selected_staff["id"] if selected_staff else None
            image_path = self.staff_agent.get_image_for_scene(category_id, scene_name, staff_id)
            if image_path:
                scene_staff_images[scene_name] = image_path

        # 5シーン構成（AIで生成したテキストを含む）
        scenes = [
            {
                "scene_id": 1,
                "scene_name": "cover",
                "label": "表紙",
                "headline": content.get("cover", {}).get("headline", topic),
                "subtext": content.get("cover", {}).get("subtext", "if塾からお届け"),
                "purpose": category["cover_format"],
                "staff_image": scene_staff_images.get("cover")
            },
            {
                "scene_id": 2,
                "scene_name": "content1",
                "label": "内容1",
                "headline": content.get("content1", {}).get("headline", "こんな悩みありませんか？"),
                "subtext": content.get("content1", {}).get("subtext", ""),
                "purpose": category["content1_format"],
                "staff_image": scene_staff_images.get("content1")
            },
            {
                "scene_id": 3,
                "scene_name": "content2",
                "label": "内容2",
                "headline": content.get("content2", {}).get("headline", "解決策をご紹介"),
                "subtext": content.get("content2", {}).get("subtext", ""),
                "purpose": category["content2_format"],
                "staff_image": scene_staff_images.get("content2")
            },
            {
                "scene_id": 4,
                "scene_name": "content3",
                "label": "内容3",
                "headline": content.get("content3", {}).get("headline", "今すぐ始めよう"),
                "subtext": content.get("content3", {}).get("subtext", ""),
                "purpose": category["content3_format"],
                "staff_image": scene_staff_images.get("content3")
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

        # キャプション生成（AIで生成したものがあれば使用）
        caption = content.get("caption") or self._generate_caption(category, topic, staff_info)
        hashtags = content.get("hashtags", category["hashtags"][:10])

        return {
            "id": post_id,
            "datetime": f"{date}T09:00:00+09:00",
            "type": "carousel",
            "category": category_id,
            "category_name": category["name"],
            "title": content.get("cover", {}).get("headline", topic),
            "scenes": scenes,
            "caption": caption,
            "hashtags": hashtags if isinstance(hashtags, list) else category["hashtags"][:10],
            "cta_url": BRAND_CONFIG["url"],
            "colors": category["colors"],
            "visual_style": category["visual_style"],
            "staff": staff_info,
            "staff_selection": {
                "staff_id": selected_staff["id"] if selected_staff else None,
                "image_type": staff_suggestion.get("image_type"),
                "reason": staff_suggestion.get("reason")
            },
            "generated_content": content  # 生成されたコンテンツを保存
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
        """シーン用プレースホルダーSVGを作成（テキスト込み完成版）"""
        filename = f"{post['id']}-{scene['scene_id']:02d}.svg"
        colors = category["colors"]
        headline = scene.get("headline", scene["label"])
        subtext = scene.get("subtext", "")
        scene_id = scene.get("scene_id", 1)

        # ヘッドラインが長い場合は複数行に分割
        headline_lines = self._split_text_to_lines(headline, 12)
        subtext_lines = self._split_text_to_lines(subtext, 20) if subtext else []

        # シーン別のデザイン設定
        scene_designs = {
            1: {"title_size": 72, "bg_style": "cover", "brand_size": 60},
            2: {"title_size": 56, "bg_style": "content", "brand_size": 40},
            3: {"title_size": 56, "bg_style": "content", "brand_size": 40},
            4: {"title_size": 56, "bg_style": "content", "brand_size": 40},
            5: {"title_size": 48, "bg_style": "thanks", "brand_size": 80},
        }
        design = scene_designs.get(scene_id, scene_designs[2])

        # ヘッドラインテキストを生成
        headline_y_start = 400 if scene_id == 1 else 350
        headline_texts = ""
        for i, line in enumerate(headline_lines[:4]):  # 最大4行
            y = headline_y_start + (i * (design["title_size"] + 20))
            headline_texts += f'  <text x="540" y="{y}" text-anchor="middle" fill="{colors["text"]}" font-family="sans-serif" font-size="{design["title_size"]}" font-weight="bold">{self._escape_svg_text(line)}</text>\n'

        # サブテキストを生成
        subtext_y_start = headline_y_start + (len(headline_lines[:4]) * (design["title_size"] + 20)) + 60
        subtext_texts = ""
        for i, line in enumerate(subtext_lines[:3]):  # 最大3行
            y = subtext_y_start + (i * 45)
            subtext_texts += f'  <text x="540" y="{y}" text-anchor="middle" fill="{colors["text"]}" font-family="sans-serif" font-size="36" opacity="0.9">{self._escape_svg_text(line)}</text>\n'

        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350">
  <defs>
    <linearGradient id="bg{scene_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{colors['primary']};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{colors['secondary']};stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect fill="url(#bg{scene_id})" width="1080" height="1350"/>

  <!-- メインコンテンツエリア -->
  <rect fill="rgba(255,255,255,0.1)" x="60" y="200" width="960" height="900" rx="30"/>

  <!-- ヘッドライン -->
{headline_texts}
  <!-- サブテキスト -->
{subtext_texts}
  <!-- ブランドマーク -->
  <circle cx="540" cy="1150" r="80" fill="rgba(255,255,255,0.2)"/>
  <text x="540" y="1170" text-anchor="middle" fill="white" font-family="sans-serif" font-size="{design["brand_size"]}" font-weight="bold">if</text>

  <!-- シーン番号 -->
  <text x="540" y="1320" text-anchor="middle" fill="rgba(255,255,255,0.5)" font-family="sans-serif" font-size="20">{scene['label']} ({scene_id}/5)</text>
</svg>'''

        output_path = self.assets_dir / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)

        return f"assets/img/posts/{filename}"

    def _split_text_to_lines(self, text: str, max_chars: int) -> list:
        """テキストを指定文字数で分割"""
        if not text:
            return []
        lines = []
        current_line = ""
        for char in text:
            current_line += char
            if len(current_line) >= max_chars:
                lines.append(current_line)
                current_line = ""
        if current_line:
            lines.append(current_line)
        return lines

    def _escape_svg_text(self, text: str) -> str:
        """SVG用にテキストをエスケープ"""
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def _generate_caption(self, category: dict, topic: str, staff_info: dict = None) -> str:
        """キャプションを生成"""
        staff_line = ""
        if staff_info:
            staff_line = f"\n担当: {staff_info.get('caption_text', '')}\n"

        caption = f"""{topic}

{category['name']}をお届けします。
{staff_line}
---

いつもご覧いただきありがとうございます！
if塾では、子どもの可能性を最大限に発揮する
プログラミング教育を提供しています。

詳細・お申し込みはプロフィール欄から！

{' '.join(category['hashtags'][:10])}"""

        return caption

    def _update_posts_json(self, new_posts: list):
        """
        posts.jsonを更新（蓄積方式）
        - 既存の投稿を削除せず、新しい投稿を追加
        - 同じIDの投稿がある場合のみ更新
        - 投稿はdatetime降順（新しい順）でソート
        """
        posts_path = self.data_dir / "posts.json"

        if posts_path.exists():
            with open(posts_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {"posts": [], "metadata": {}}

        # 既存の投稿IDをセットで管理
        existing_ids = {p["id"] for p in data["posts"]}

        for post in new_posts:
            # シーンとメディアを結合してpages構造を作成
            scenes = post.get("scenes", [])
            generated_images = post.get("generated_images", [])

            # Material vs Context分離: 各ページに画像素材とオーバーレイテキストを分離
            pages = []
            for i, (scene, img_path) in enumerate(zip(scenes, generated_images)):
                page = {
                    "page_number": i + 1,
                    "scene_id": scene.get("scene_id", i + 1),
                    "scene_name": scene.get("scene_name", f"scene{i+1}"),
                    "layout_type": scene.get("scene_name", "content"),
                    "label": scene.get("label", f"シーン{i+1}"),
                    "main_title": scene.get("headline", ""),
                    "sub_title": scene.get("subtext", ""),
                    "text_content": scene.get("headline", ""),
                    "image_prompt": f"Japanese anime style, {scene.get('purpose', 'illustration')}, clean background, no text, no ui",
                    "image_url": img_path,
                    "image_file": img_path,
                    "overlay_text": scene.get("headline", ""),
                    "subtext": scene.get("subtext", ""),
                    "alt": f"{scene.get('label', f'シーン{i+1}')} - {scene.get('headline', '')[:20]}"
                }
                pages.append(page)

            # 時間コンテキストを取得
            time_ctx = get_current_time_context()

            # 新しい投稿データを整形（Material vs Context対応 + 時間認識）
            post_data = {
                "id": post["id"],
                "post_id": post["id"],  # YYYYMMDD_category形式
                "created_at": time_ctx["timestamp"],
                "datetime": post["datetime"],
                "type": post["type"],
                "category": post["category"],
                "theme": post["title"],
                "target_audience": "Students & Parents",
                "title": post["title"],
                "caption": post["caption"],
                "caption_text": post["caption"],  # 別名
                "hashtags": post["hashtags"],
                "cta_url": post["cta_url"],
                "slides": pages,  # 新スキーマ名
                "pages": pages,   # 互換性維持
                "media": [
                    {"kind": "image", "src": img, "alt": f"シーン{i+1}"}
                    for i, img in enumerate(generated_images)
                ],
                "highlight": post["category_name"],
                "staff": post.get("staff"),
                "staff_selection": post.get("staff_selection"),
                "status": "published",
                "research_date": post.get("generated_content", {}).get("generated_at", time_ctx["today_str"]),
                "engagement": {
                    "likes": 0,
                    "comments": 0,
                    "saves": 0,
                    "shares": 0
                },
                "notes_for_instagram": {
                    "cover_text": post["title"][:20],
                    "first_comment": "詳細は if-juku.net から",
                    "scenes": scenes
                }
            }

            if post["id"] in existing_ids:
                # 同じIDの投稿がある場合は更新
                data["posts"] = [
                    post_data if p["id"] == post["id"] else p
                    for p in data["posts"]
                ]
            else:
                # 新しい投稿を追加
                data["posts"].append(post_data)

        # datetime降順（新しい順）でソート
        data["posts"].sort(key=lambda x: x["datetime"], reverse=True)

        # メタデータを更新
        data["metadata"] = {
            "version": "3.0",
            "total_posts": len(data["posts"]),
            "last_updated": datetime.now().isoformat(),
            "categories": list(CATEGORIES.keys())
        }

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
            staff_name = post.get('staff', {}).get('name', 'なし') if post.get('staff') else 'なし'
            staff_reason = post.get('staff_selection', {}).get('reason', '') if post.get('staff_selection') else ''
            report_content += f"""
### {post['title']}
- ID: {post['id']}
- カテゴリ: {post['category_name']}
- 担当スタッフ: {staff_name}
- 選択理由: {staff_reason}
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
    parser = argparse.ArgumentParser(description="if塾 Instagram Workflow v3.0 with Gemini (Time-Aware)")
    parser.add_argument("command", choices=["daily", "research", "generate"],
                       help="実行するコマンド")
    parser.add_argument("--date", help="対象日付 (YYYY-MM-DD)")
    parser.add_argument("--category", help="カテゴリID")
    parser.add_argument("--topic", help="トピック（generateコマンド用）")
    parser.add_argument("--api-key", help="Gemini API Key")

    args = parser.parse_args()

    # 時間コンテキストを表示
    time_ctx = get_current_time_context()
    print(f"\n[Time-Aware Mode] 現在: {time_ctx['current_year']}年{time_ctx['current_month_name']}")

    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
    workflow = InstagramWorkflowV3(api_key)

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
