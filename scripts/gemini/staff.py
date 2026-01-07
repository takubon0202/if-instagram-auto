"""
スタッフ画像管理モジュール
if塾スタッフ画像の選択・管理を行う
"""
import json
import os
import random
from pathlib import Path
from typing import Optional, List, Dict


class StaffImageManager:
    """
    スタッフ画像管理クラス
    カテゴリに応じた適切なスタッフ画像を選択
    """

    def __init__(self, staff_json_path: str = None):
        if staff_json_path is None:
            staff_json_path = Path(__file__).parent.parent.parent / "data" / "staff.json"

        self.staff_json_path = Path(staff_json_path)
        self.staff_data = self._load_staff_data()
        self.base_dir = Path(__file__).parent.parent.parent

    def _load_staff_data(self) -> dict:
        """staff.jsonを読み込み"""
        if self.staff_json_path.exists():
            with open(self.staff_json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"staff": [], "selection_rules": {}}

    def get_all_staff(self) -> List[dict]:
        """全スタッフ情報を取得"""
        return self.staff_data.get("staff", [])

    def get_staff_by_id(self, staff_id: str) -> Optional[dict]:
        """IDでスタッフを取得"""
        for staff in self.staff_data.get("staff", []):
            if staff["id"] == staff_id:
                return staff
        return None

    def get_staff_for_category(self, category_id: str) -> List[dict]:
        """カテゴリに適したスタッフを取得"""
        available_staff = []
        for staff in self.staff_data.get("staff", []):
            if category_id in staff.get("available_for", []):
                available_staff.append(staff)
        return available_staff

    def select_staff_image(
        self,
        category_id: str,
        staff_id: str = None,
        image_type: str = None
    ) -> Optional[str]:
        """
        カテゴリに応じたスタッフ画像を選択

        Args:
            category_id: カテゴリID
            staff_id: 特定のスタッフを指定（省略時は自動選択）
            image_type: 画像タイプ（省略時はカテゴリルールに従う）

        Returns:
            画像パス（存在する場合）またはNone
        """
        rules = self.staff_data.get("selection_rules", {}).get(category_id, {})

        # 画像タイプを決定
        if image_type is None:
            image_type = rules.get("image_type", "profile")

        # スタッフを選択
        if staff_id is None:
            priority = rules.get("priority", ["all"])
            if "all" in priority:
                available = self.get_staff_for_category(category_id)
                if available:
                    staff = random.choice(available)
                    staff_id = staff["id"]
            else:
                # 優先リストから選択
                for sid in priority:
                    staff = self.get_staff_by_id(sid)
                    if staff and category_id in staff.get("available_for", []):
                        staff_id = sid
                        break

        if staff_id is None:
            return None

        # 画像パスを取得
        staff = self.get_staff_by_id(staff_id)
        if staff is None:
            return None

        images = staff.get("images", {})
        image_path = images.get(image_type)

        if image_path:
            full_path = self.base_dir / image_path
            if full_path.exists():
                return image_path

        # フォールバック: 存在する画像を探す
        for img_type, img_path in images.items():
            full_path = self.base_dir / img_path
            if full_path.exists():
                return img_path

        return None

    def get_available_images(self, staff_id: str) -> Dict[str, str]:
        """指定スタッフの利用可能な画像を取得"""
        staff = self.get_staff_by_id(staff_id)
        if staff is None:
            return {}

        available = {}
        for img_type, img_path in staff.get("images", {}).items():
            full_path = self.base_dir / img_path
            if full_path.exists():
                available[img_type] = img_path

        return available

    def check_missing_images(self) -> Dict[str, List[str]]:
        """不足している画像をチェック"""
        missing = {}
        for staff in self.staff_data.get("staff", []):
            staff_missing = []
            for img_type, img_path in staff.get("images", {}).items():
                full_path = self.base_dir / img_path
                if not full_path.exists():
                    staff_missing.append(f"{img_type}: {img_path}")
            if staff_missing:
                missing[staff["name"]] = staff_missing
        return missing

    def get_staff_info_for_post(self, staff_id: str) -> dict:
        """投稿用のスタッフ情報を取得"""
        staff = self.get_staff_by_id(staff_id)
        if staff is None:
            return {}

        return {
            "name": staff.get("name", ""),
            "role": staff.get("role", "講師"),
            "specialties": staff.get("specialties", []),
            "caption_text": f"{staff.get('name', '')}（{staff.get('role', '講師')}）"
        }


class StaffImageAgent:
    """
    スタッフ画像選択エージェント
    投稿に最適なスタッフ画像を提案
    """

    def __init__(self):
        self.manager = StaffImageManager()

    def suggest_staff_for_post(self, category_id: str, topic: str = None) -> dict:
        """
        投稿に適したスタッフを提案

        Args:
            category_id: カテゴリID
            topic: 投稿トピック（オプション）

        Returns:
            提案情報
        """
        available_staff = self.manager.get_staff_for_category(category_id)

        if not available_staff:
            return {
                "suggested_staff": None,
                "reason": "このカテゴリに適したスタッフが登録されていません",
                "alternatives": []
            }

        # カテゴリルールに基づいて選択
        rules = self.manager.staff_data.get("selection_rules", {}).get(category_id, {})
        priority = rules.get("priority", ["all"])
        image_type = rules.get("image_type", "profile")

        selected_staff = None
        if "all" not in priority:
            for staff_id in priority:
                staff = self.manager.get_staff_by_id(staff_id)
                if staff and staff in available_staff:
                    selected_staff = staff
                    break

        if selected_staff is None and available_staff:
            selected_staff = random.choice(available_staff)

        # 画像の存在確認
        image_path = None
        if selected_staff:
            image_path = self.manager.select_staff_image(
                category_id,
                selected_staff["id"],
                image_type
            )

        return {
            "suggested_staff": selected_staff,
            "image_type": image_type,
            "image_path": image_path,
            "reason": f"{category_id}カテゴリの優先ルールに基づいて選択",
            "alternatives": [s["id"] for s in available_staff if s != selected_staff]
        }

    def get_image_for_scene(
        self,
        category_id: str,
        scene_name: str,
        staff_id: str = None
    ) -> Optional[str]:
        """
        シーンに適した画像を取得

        Args:
            category_id: カテゴリID
            scene_name: シーン名（cover, content1, content2, content3）
            staff_id: スタッフID（オプション）
        """
        # シーンに応じた画像タイプを決定
        scene_image_map = {
            "cover": "profile",
            "content1": "teaching",
            "content2": "teaching",
            "content3": "casual"
        }

        image_type = scene_image_map.get(scene_name, "profile")

        return self.manager.select_staff_image(
            category_id,
            staff_id,
            image_type
        )


def setup_staff_directories():
    """スタッフ画像ディレクトリを作成"""
    base_dir = Path(__file__).parent.parent.parent
    staff_json_path = base_dir / "data" / "staff.json"

    if not staff_json_path.exists():
        print("staff.jsonが見つかりません")
        return

    with open(staff_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    staff_dir = base_dir / "assets" / "img" / "staff"
    staff_dir.mkdir(parents=True, exist_ok=True)

    for staff in data.get("staff", []):
        staff_folder = staff_dir / staff["id"]
        staff_folder.mkdir(exist_ok=True)
        print(f"Created: {staff_folder}")

        # プレースホルダーファイルを作成
        readme_path = staff_folder / "README.txt"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(f"""# {staff['name']}のスタッフ画像フォルダ

Google Driveから画像をダウンロードしてこのフォルダに配置してください。

## 必要な画像
- profile.png: プロフィール写真（正面、上半身）
- teaching.png: 授業風景写真
- casual.png: カジュアル写真

## ダウンロード元
Google Drive: {data.get('source_folder', '')}
フォルダ名: {staff.get('gdrive_folder', '')}
""")

    print(f"\nスタッフディレクトリのセットアップ完了")
    print(f"Google Driveから画像をダウンロードして各フォルダに配置してください")
    print(f"ソースフォルダ: {data.get('source_folder', '')}")


def check_staff_images():
    """スタッフ画像の状態をチェック"""
    manager = StaffImageManager()
    missing = manager.check_missing_images()

    if missing:
        print("\n=== 不足している画像 ===")
        for staff_name, images in missing.items():
            print(f"\n{staff_name}:")
            for img in images:
                print(f"  - {img}")
    else:
        print("\n全てのスタッフ画像が揃っています")

    print("\n=== 利用可能な画像 ===")
    for staff in manager.get_all_staff():
        available = manager.get_available_images(staff["id"])
        print(f"\n{staff['name']}:")
        if available:
            for img_type, path in available.items():
                print(f"  [OK] {img_type}: {path}")
        else:
            print("  (画像なし)")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "setup":
            setup_staff_directories()
        elif sys.argv[1] == "check":
            check_staff_images()
    else:
        print("使用方法:")
        print("  python -m scripts.gemini.staff setup  # ディレクトリ作成")
        print("  python -m scripts.gemini.staff check  # 画像チェック")
