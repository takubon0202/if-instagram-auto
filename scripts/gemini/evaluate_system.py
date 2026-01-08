"""
Instagram自動投稿システム評価エージェント v1.0
システムの品質と動作を検証し、95%以上の合格率を目指す

評価項目:
1. モジュールインポート検証
2. 設定ファイル検証
3. 画像処理機能検証
4. テキストオーバーレイ機能検証
5. フォールバック機能検証
6. ワークフロー統合検証
"""
import os
import sys
from pathlib import Path
from datetime import datetime
import json
import traceback

# パスを追加
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class SystemEvaluator:
    """システム評価エージェント"""

    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        self.total = 0

    def add_result(self, test_name: str, passed: bool, message: str = ""):
        """テスト結果を追加"""
        self.total += 1
        if passed:
            self.passed += 1
            status = "[PASS]"
        else:
            self.failed += 1
            status = "[FAIL]"

        self.results.append({
            "test": test_name,
            "passed": passed,
            "status": status,
            "message": message
        })
        print(f"  {status}: {test_name}")
        if message and not passed:
            print(f"         {message}")

    def get_pass_rate(self) -> float:
        """合格率を取得"""
        if self.total == 0:
            return 0.0
        return (self.passed / self.total) * 100

    def print_summary(self):
        """結果サマリーを出力"""
        rate = self.get_pass_rate()
        print(f"\n{'='*60}")
        print(f"  Evaluation Summary")
        print(f"{'='*60}")
        print(f"  Passed: {self.passed}/{self.total} ({rate:.1f}%)")
        print(f"  Failed: {self.failed}")
        print(f"  Target: 95%+")
        print(f"  Result: {'PASS' if rate >= 95 else 'NEEDS IMPROVEMENT'}")
        print(f"{'='*60}\n")

        if self.failed > 0:
            print("Failed tests:")
            for r in self.results:
                if not r["passed"]:
                    print(f"  - {r['test']}: {r['message']}")


def test_module_imports(evaluator: SystemEvaluator):
    """モジュールインポート検証"""
    print("\n[Test 1] モジュールインポート検証")

    # PIL
    try:
        from PIL import Image, ImageDraw, ImageFont
        evaluator.add_result("PIL (Pillow) インポート", True)
    except ImportError as e:
        evaluator.add_result("PIL (Pillow) インポート", False, str(e))

    # Config
    try:
        from scripts.gemini.config import (
            CATEGORIES, BRAND_CONFIG, TEXT_OVERLAY_CONFIG,
            IMAGE_GENERATION_CONFIG
        )
        evaluator.add_result("config.py インポート", True)
    except ImportError as e:
        evaluator.add_result("config.py インポート", False, str(e))

    # Client
    try:
        from scripts.gemini.client import (
            GeminiClient, ImageGenerationAgent,
            ContentGenerationAgent, TrendResearchAgent
        )
        evaluator.add_result("client.py インポート", True)
    except ImportError as e:
        evaluator.add_result("client.py インポート", False, str(e))

    # Text Overlay
    try:
        from scripts.gemini.text_overlay import TextOverlayEngine
        evaluator.add_result("text_overlay.py インポート", True)
    except ImportError as e:
        evaluator.add_result("text_overlay.py インポート", False, str(e))

    # Workflow
    try:
        from scripts.gemini.workflow import InstagramWorkflowV3
        evaluator.add_result("workflow.py インポート", True)
    except ImportError as e:
        evaluator.add_result("workflow.py インポート", False, str(e))


def test_config_values(evaluator: SystemEvaluator):
    """設定ファイル検証"""
    print("\n[Test 2] 設定ファイル検証")

    try:
        from scripts.gemini.config import TEXT_OVERLAY_CONFIG, CATEGORIES

        # フォントサイズ検証
        title_size = TEXT_OVERLAY_CONFIG.get("title_font_size", 0)
        if 80 <= title_size <= 120:
            evaluator.add_result("タイトルフォントサイズ (80-120)", True, f"value={title_size}")
        else:
            evaluator.add_result("タイトルフォントサイズ (80-120)", False, f"value={title_size}")

        content_size = TEXT_OVERLAY_CONFIG.get("content_font_size", 0)
        if 40 <= content_size <= 80:
            evaluator.add_result("コンテンツフォントサイズ (40-80)", True, f"value={content_size}")
        else:
            evaluator.add_result("コンテンツフォントサイズ (40-80)", False, f"value={content_size}")

        # パディング検証
        padding = TEXT_OVERLAY_CONFIG.get("padding_ratio", 0)
        if 0.05 <= padding <= 0.15:
            evaluator.add_result("パディング比率 (0.05-0.15)", True, f"value={padding}")
        else:
            evaluator.add_result("パディング比率 (0.05-0.15)", False, f"value={padding}")

        # 行間検証
        line_height = TEXT_OVERLAY_CONFIG.get("line_height_ratio", 0)
        if 1.2 <= line_height <= 2.0:
            evaluator.add_result("行間比率 (1.2-2.0)", True, f"value={line_height}")
        else:
            evaluator.add_result("行間比率 (1.2-2.0)", False, f"value={line_height}")

        # カテゴリ数検証
        if len(CATEGORIES) >= 6:
            evaluator.add_result("カテゴリ数 (>=6)", True, f"count={len(CATEGORIES)}")
        else:
            evaluator.add_result("カテゴリ数 (>=6)", False, f"count={len(CATEGORIES)}")

    except Exception as e:
        evaluator.add_result("設定ファイル読み込み", False, str(e))


def test_image_processing(evaluator: SystemEvaluator):
    """画像処理機能検証"""
    print("\n[Test 3] 画像処理機能検証")

    try:
        from PIL import Image

        # 画像生成テスト
        test_img = Image.new("RGB", (800, 1000), (255, 100, 100))
        evaluator.add_result("PIL Image生成", True)

        # リサイズテスト（workflow.pyの_resize_to_instagramを使用）
        from scripts.gemini.workflow import InstagramWorkflowV3
        workflow = InstagramWorkflowV3()

        resized = workflow._resize_to_instagram(test_img, 1080, 1350)
        if resized.size == (1080, 1350):
            evaluator.add_result("画像リサイズ (1080x1350)", True)
        else:
            evaluator.add_result("画像リサイズ (1080x1350)", False, f"size={resized.size}")

        # グラデーション生成テスト
        from scripts.gemini.config import CATEGORIES
        category = CATEGORIES.get("ai_column", {})
        gradient = workflow._create_gradient_background(category)
        if gradient.size == (1080, 1350):
            evaluator.add_result("グラデーション背景生成", True)
        else:
            evaluator.add_result("グラデーション背景生成", False, f"size={gradient.size}")

    except Exception as e:
        evaluator.add_result("画像処理", False, f"{e}\n{traceback.format_exc()}")


def test_text_overlay(evaluator: SystemEvaluator):
    """テキストオーバーレイ機能検証"""
    print("\n[Test 4] テキストオーバーレイ機能検証")

    try:
        from scripts.gemini.text_overlay import TextOverlayEngine
        from PIL import Image
        import tempfile
        import os

        # エンジン初期化
        engine = TextOverlayEngine()
        evaluator.add_result("TextOverlayEngine初期化", True)

        # フォント検出
        font = engine._find_japanese_font()
        if font:
            evaluator.add_result("日本語フォント検出", True, f"font={font}")
        else:
            evaluator.add_result("日本語フォント検出", False, "フォントが見つかりません")

        # テスト画像を作成
        test_img = Image.new("RGB", (1080, 1350), (100, 100, 200))
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            test_img.save(tmp.name)
            temp_path = tmp.name

        try:
            # オーバーレイテスト
            output_path = temp_path.replace(".png", "_overlay.png")
            engine.create_instagram_post(
                background_image_path=temp_path,
                headline="テストタイトル日本語",
                subtext="サブテキストのテスト",
                output_path=output_path,
                style="ai_column"
            )

            if os.path.exists(output_path):
                result_img = Image.open(output_path)
                if result_img.size == (1080, 1350):
                    evaluator.add_result("テキストオーバーレイ出力", True)
                else:
                    evaluator.add_result("テキストオーバーレイ出力", False, f"size={result_img.size}")
                result_img.close()  # Windowsでファイルロックを解除
                try:
                    os.unlink(output_path)
                except PermissionError:
                    pass  # Windows環境での一時ファイル削除エラーは無視
            else:
                evaluator.add_result("テキストオーバーレイ出力", False, "ファイルが生成されませんでした")

        finally:
            try:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
            except PermissionError:
                pass  # Windows環境での一時ファイル削除エラーは無視

    except Exception as e:
        evaluator.add_result("テキストオーバーレイ", False, f"{e}\n{traceback.format_exc()}")


def test_fallback_functionality(evaluator: SystemEvaluator):
    """フォールバック機能検証"""
    print("\n[Test 5] フォールバック機能検証")

    try:
        from scripts.gemini.workflow import InstagramWorkflowV3
        from scripts.gemini.config import CATEGORIES
        import tempfile
        import os

        workflow = InstagramWorkflowV3()
        category = CATEGORIES.get("ai_column", {})

        # フォールバック画像生成テスト
        test_scene = {
            "scene_id": 1,
            "headline": "テストヘッドライン",
            "subtext": "テストサブテキスト"
        }

        # 一時的にassets_dirを設定
        original_assets_dir = workflow.assets_dir
        with tempfile.TemporaryDirectory() as tmp_dir:
            workflow.assets_dir = Path(tmp_dir)

            fallback_path = workflow._get_fallback_image(
                "test_20260108",
                test_scene,
                category
            )

            # パスが返されることを確認
            if fallback_path:
                evaluator.add_result("フォールバックパス生成", True, f"path={fallback_path}")
            else:
                evaluator.add_result("フォールバックパス生成", False, "パスが空です")

            # ファイルが生成されたか確認
            full_path = Path(tmp_dir) / fallback_path.replace("assets/img/posts/", "")
            if full_path.exists():
                evaluator.add_result("フォールバック画像ファイル生成", True)
            else:
                # サンクス画像にフォールバックした場合
                if "ifjukuthanks" in fallback_path:
                    evaluator.add_result("フォールバック画像ファイル生成", True, "サンクス画像を使用")
                else:
                    evaluator.add_result("フォールバック画像ファイル生成", False, f"ファイルなし: {full_path}")

        workflow.assets_dir = original_assets_dir

    except Exception as e:
        evaluator.add_result("フォールバック機能", False, f"{e}\n{traceback.format_exc()}")


def test_client_methods(evaluator: SystemEvaluator):
    """クライアントメソッド検証"""
    print("\n[Test 6] クライアントメソッド検証")

    try:
        from scripts.gemini.client import GeminiClient, ImageGenerationAgent
        from scripts.gemini.config import CATEGORIES
        from PIL import Image

        # クライアント初期化（APIキーなしでも動作確認）
        client = GeminiClient()
        evaluator.add_result("GeminiClient初期化", True)

        # ImageGenerationAgent初期化
        agent = ImageGenerationAgent(client)
        evaluator.add_result("ImageGenerationAgent初期化", True)

        # _resize_to_instagram メソッド存在確認
        if hasattr(agent, '_resize_to_instagram'):
            # メソッドが3つの引数を取ることを確認
            import inspect
            sig = inspect.signature(agent._resize_to_instagram)
            params = list(sig.parameters.keys())
            if len(params) >= 3:  # self, img, target_w, target_h
                evaluator.add_result("_resize_to_instagram引数 (3+)", True, f"params={params}")
            else:
                evaluator.add_result("_resize_to_instagram引数 (3+)", False, f"params={params}")
        else:
            evaluator.add_result("_resize_to_instagramメソッド存在", False)

        # _create_gradient_background メソッド存在確認
        if hasattr(agent, '_create_gradient_background'):
            category = CATEGORIES.get("ai_column", {})
            gradient = agent._create_gradient_background(category)
            if gradient.size == (1080, 1350):
                evaluator.add_result("_create_gradient_background動作", True)
            else:
                evaluator.add_result("_create_gradient_background動作", False, f"size={gradient.size}")
        else:
            evaluator.add_result("_create_gradient_backgroundメソッド存在", False)

        # _generate_mock_image メソッド存在確認
        if hasattr(agent, '_generate_mock_image'):
            evaluator.add_result("_generate_mock_imageメソッド存在", True)
        else:
            evaluator.add_result("_generate_mock_imageメソッド存在", False)

    except Exception as e:
        evaluator.add_result("クライアントメソッド", False, f"{e}\n{traceback.format_exc()}")


def test_workflow_integration(evaluator: SystemEvaluator):
    """ワークフロー統合検証"""
    print("\n[Test 7] ワークフロー統合検証")

    try:
        from scripts.gemini.workflow import InstagramWorkflowV3
        from scripts.gemini.config import CATEGORIES, WEEKLY_SCHEDULE

        workflow = InstagramWorkflowV3()
        evaluator.add_result("InstagramWorkflowV3初期化", True)

        # カテゴリ取得テスト
        test_date = "2026-01-08"  # 木曜日
        category_id = workflow.get_category_for_date(test_date)
        if category_id in CATEGORIES:
            evaluator.add_result("カテゴリ取得 (日付ベース)", True, f"category={category_id}")
        else:
            evaluator.add_result("カテゴリ取得 (日付ベース)", False, f"unknown category: {category_id}")

        # 5シーン企画テスト
        mock_research = {
            "trending_topics": ["テストトピック"],
            "popular_hooks": ["テストフック"]
        }

        post = workflow._plan_5scene_post(test_date, category_id, mock_research)

        # 5シーン存在確認
        scenes = post.get("scenes", [])
        if len(scenes) == 5:
            evaluator.add_result("5シーン構成", True)
        else:
            evaluator.add_result("5シーン構成", False, f"scene_count={len(scenes)}")

        # シーン構造確認
        required_fields = ["scene_id", "headline", "subtext"]
        all_valid = True
        for scene in scenes:
            for field in required_fields:
                if field not in scene:
                    all_valid = False
                    break

        if all_valid:
            evaluator.add_result("シーン構造 (必須フィールド)", True)
        else:
            evaluator.add_result("シーン構造 (必須フィールド)", False, f"missing fields in scenes")

    except Exception as e:
        evaluator.add_result("ワークフロー統合", False, f"{e}\n{traceback.format_exc()}")


def test_no_unnecessary_elements(evaluator: SystemEvaluator):
    """不要要素削除検証"""
    print("\n[Test 8] 不要要素削除検証")

    try:
        from scripts.gemini.client import ImageGenerationAgent
        from scripts.gemini.workflow import InstagramWorkflowV3
        import inspect

        # client.py の _generate_mock_image をチェック
        client_source = inspect.getsource(ImageGenerationAgent._generate_mock_image)

        # 不要なテキスト描画がないことを確認
        unwanted_patterns = [
            "1/5",
            "2/5",
            "3/5",
            "4/5",
            "5/5",
            "if塾",
            "draw.text((42, 102)",  # カテゴリラベル位置
            "draw.text((982, 1262)",  # ページ番号位置
        ]

        found_unwanted = []
        for pattern in unwanted_patterns:
            if pattern in client_source:
                found_unwanted.append(pattern)

        if not found_unwanted:
            evaluator.add_result("client.py: 不要テキスト削除", True)
        else:
            evaluator.add_result("client.py: 不要テキスト削除", False, f"found: {found_unwanted}")

        # workflow.py の _get_fallback_image をチェック
        workflow_source = inspect.getsource(InstagramWorkflowV3._get_fallback_image)

        found_unwanted_wf = []
        for pattern in unwanted_patterns:
            if pattern in workflow_source:
                found_unwanted_wf.append(pattern)

        if not found_unwanted_wf:
            evaluator.add_result("workflow.py: 不要テキスト削除", True)
        else:
            evaluator.add_result("workflow.py: 不要テキスト削除", False, f"found: {found_unwanted_wf}")

    except Exception as e:
        evaluator.add_result("不要要素削除検証", False, f"{e}\n{traceback.format_exc()}")


def main():
    """評価実行"""
    print(f"\n{'='*60}")
    print(f"  Instagram自動投稿システム評価")
    print(f"  実行日時: {datetime.now().isoformat()}")
    print(f"{'='*60}")

    evaluator = SystemEvaluator()

    # 各テストを実行
    test_module_imports(evaluator)
    test_config_values(evaluator)
    test_image_processing(evaluator)
    test_text_overlay(evaluator)
    test_fallback_functionality(evaluator)
    test_client_methods(evaluator)
    test_workflow_integration(evaluator)
    test_no_unnecessary_elements(evaluator)

    # 結果サマリーを出力
    evaluator.print_summary()

    # 結果をJSONで保存
    output_dir = Path(__file__).parent.parent / "daily_reports"
    output_dir.mkdir(exist_ok=True)

    result_file = output_dir / f"evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "pass_rate": evaluator.get_pass_rate(),
            "passed": evaluator.passed,
            "failed": evaluator.failed,
            "total": evaluator.total,
            "target": 95,
            "results": evaluator.results
        }, f, ensure_ascii=False, indent=2)

    print(f"評価結果を保存: {result_file}")

    # 終了コード
    return 0 if evaluator.get_pass_rate() >= 95 else 1


if __name__ == "__main__":
    sys.exit(main())
