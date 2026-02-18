#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universal Slide Designer API
任意のスライド設計に対応する汎用AIツール
"""

import requests
import json
from pathlib import Path
from typing import List, Dict, Optional

class UniversalSlideDesigner:
    """
    汎用スライド設計ツール
    
    使用方法:
        designer = UniversalSlideDesigner()
        
        # パターン1: 手動でオブジェクトを指定
        objects = [
            {"type": "box", "text": "タイトル", "left": 0.5, "top": 0.5, ...},
            {"type": "arrow", "left": 1.0, "top": 1.0, ...},
        ]
        result = designer.design(objects, title="My Slide", subtitle="Subtitle")
        
        # パターン2: JSON ファイルから読み込み
        result = designer.design_from_json("slide.json")
        
        # パターン3: Tier配置テンプレート（汎用）
        result = designer.design_horizontal_comparison(
            left_title="左側タイトル", left_items=["item1", "item2"],
            right_title="右側タイトル", right_items=["item3", "item4"],
            title="メインタイトル"
        )
    """
    
    def __init__(self, api_url: str = "http://localhost:5000"):
        self.api_url = api_url
    
    def design(self, objects: List[Dict], title: str = "", subtitle: str = "") -> Dict:
        """
        任意のオブジェクトリストからスライドを設計
        
        Args:
            objects: オブジェクトリスト
            title: スライドタイトル
            subtitle: スライドサブタイトル
        
        Returns:
            設計結果（JSON形式）
        """
        try:
            response = requests.post(
                f"{self.api_url}/api/batch-add",
                json={"objects": objects},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    return {
                        "success": True,
                        "title": title,
                        "subtitle": subtitle,
                        "object_count": len(objects),
                        "objects": objects,
                        "json_objects": result.get("objects", [])
                    }
            
            return {
                "success": False,
                "error": f"API Error: {response.status_code}"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def design_from_json(self, json_path: str) -> Dict:
        """
        JSON ファイルから既存スライドを読み込み
        
        Args:
            json_path: JSON ファイルパス
        
        Returns:
            読み込み結果
        """
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                slide_data = json.load(f)
            
            result = self.design(
                objects=slide_data.get("objects", []),
                title=slide_data.get("title", ""),
                subtitle=slide_data.get("subtitle", "")
            )
            
            result["json_data"] = slide_data
            return result
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to load JSON: {str(e)}"
            }
    
    def design_horizontal_comparison(self,
        left_title: str = "",
        left_items: List[str] = None,
        right_title: str = "",
        right_items: List[str] = None,
        title: str = "Comparison",
        title_color: str = "#4472C4",
        left_color: str = "#ED7D31",
        right_color: str = "#4472C4"
    ) -> Dict:
        """
        左右比較レイアウト（汎用パターン）
        
        Args:
            left_title: 左側タイトル
            left_items: 左側項目リスト
            right_title: 右側タイトル
            right_items: 右側項目リスト
            title: メインタイトル
            title_color: タイトル色
            left_color: 左側色
            right_color: 右側色
        
        Returns:
            スライド設計結果
        """
        left_items = left_items or []
        right_items = right_items or []
        
        objects = []
        
        # メインタイトル
        objects.append({
            "type": "box",
            "text": title,
            "left": 0.5,
            "top": 0.3,
            "width": 4.3,
            "height": 0.6,
            "fillColor": title_color,
            "fontColor": "#FFFFFF",
            "fontSize": 14
        })
        
        # 左側タイトル
        objects.append({
            "type": "box",
            "text": left_title,
            "left": 0.5,
            "top": 1.1,
            "width": 1.9,
            "height": 0.5,
            "fillColor": left_color,
            "fontColor": "#FFFFFF",
            "fontSize": 12
        })
        
        # 左側項目
        item_height = 0.3
        for i, item in enumerate(left_items):
            objects.append({
                "type": "text",
                "text": f"• {item}",
                "left": 0.5,
                "top": 1.7 + i * item_height,
                "width": 1.9,
                "height": item_height,
                "fontColor": "#404040",
                "fontSize": 10
            })
        
        # 右側タイトル
        objects.append({
            "type": "box",
            "text": right_title,
            "left": 3.0,
            "top": 1.1,
            "width": 1.9,
            "height": 0.5,
            "fillColor": right_color,
            "fontColor": "#FFFFFF",
            "fontSize": 12
        })
        
        # 右側項目
        for i, item in enumerate(right_items):
            objects.append({
                "type": "text",
                "text": f"• {item}",
                "left": 3.0,
                "top": 1.7 + i * item_height,
                "width": 1.9,
                "height": item_height,
                "fontColor": "#FFFFFF" if right_color != "#FFFFFF" else "#404040",
                "fontSize": 10,
                "fillColor": right_color if right_color != "#FFFFFF" else None
            })
        
        return self.design(
            objects=objects,
            title=title,
            subtitle=f"{left_title} vs {right_title}"
        )
    
    def design_three_tier_flow(self,
        tier1_title: str = "Tier 1",
        tier1_subtitle: str = "",
        tier1_color: str = "#404040",
        
        tier2_title: str = "Tier 2",
        tier2_subtitle: str = "",
        tier2_color: str = "#4472C4",
        
        tier3_title: str = "Tier 3",
        tier3_subtitle: str = "",
        tier3_color: str = "#1F3864",
        
        title: str = "3-Tier Flow",
        show_arrows: bool = True
    ) -> Dict:
        """
        3層フロー レイアウト（汎用パターン）
        
        Args:
            tier1_title, tier2_title, tier3_title: 各層タイトル
            tier1_subtitle, tier2_subtitle, tier3_subtitle: 各層説明
            tier1_color, tier2_color, tier3_color: 各層の色
            title: メインタイトル
            show_arrows: 層間の矢印を表示するか
        
        Returns:
            スライド設計結果
        """
        objects = []
        
        # メインタイトル
        objects.append({
            "type": "box",
            "text": title,
            "left": 0.5,
            "top": 0.2,
            "width": 4.3,
            "height": 0.5,
            "fillColor": "#4472C4",
            "fontColor": "#FFFFFF",
            "fontSize": 14
        })
        
        # Tier 1
        objects.append({
            "type": "box",
            "text": f"{tier1_title}\n{tier1_subtitle}",
            "left": 0.5,
            "top": 1.0,
            "width": 1.5,
            "height": 1.0,
            "fillColor": tier1_color,
            "fontColor": "#FFFFFF",
            "fontSize": 11
        })
        
        # 矢印 1→2
        if show_arrows:
            objects.append({
                "type": "arrow",
                "left": 2.2,
                "top": 1.4,
                "width": 0.4,
                "height": 0.2,
                "fillColor": "#ED7D31"
            })
        
        # Tier 2
        objects.append({
            "type": "box",
            "text": f"{tier2_title}\n{tier2_subtitle}",
            "left": 2.8,
            "top": 1.0,
            "width": 1.5,
            "height": 1.0,
            "fillColor": tier2_color,
            "fontColor": "#FFFFFF",
            "fontSize": 11
        })
        
        # 矢印 2→3
        if show_arrows:
            objects.append({
                "type": "arrow",
                "left": 4.5,
                "top": 1.4,
                "width": 0.4,
                "height": 0.2,
                "fillColor": "#ED7D31"
            })
        
        # Tier 3
        objects.append({
            "type": "box",
            "text": f"{tier3_title}\n{tier3_subtitle}",
            "left": 5.1,
            "top": 1.0,
            "width": 1.5,
            "height": 1.0,
            "fillColor": tier3_color,
            "fontColor": "#FFFFFF",
            "fontSize": 11
        })
        
        return self.design(
            objects=objects,
            title=title,
            subtitle="3-Tier Architecture Flow"
        )
    
    def export_json(self, design_result: Dict, output_path: str) -> bool:
        """
        設計結果を JSON ファイルに保存
        
        Args:
            design_result: design() の戻り値
            output_path: 出力ファイルパス
        
        Returns:
            成功したか
        """
        try:
            slide_data = {
                "type": "content",
                "title": design_result.get("title", ""),
                "subtitle": design_result.get("subtitle", ""),
                "objects": design_result.get("json_objects", [])
            }
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(slide_data, f, ensure_ascii=False, indent=2)
            
            return True
        
        except Exception as e:
            print(f"Error saving JSON: {e}")
            return False
    
    def load_to_canvas(self, design_result: Dict) -> bool:
        """
        設計結果を Canvas にロード
        
        Args:
            design_result: design() の戻り値
        
        Returns:
            成功したか
        """
        try:
            # JSON 形式を UI 形式に逆変換
            ui_objects = []
            for obj in design_result.get("objects", []):
                ui_obj = {
                    "type": obj.get("type"),
                    "left": obj.get("left", 0),
                    "top": obj.get("top", 0),
                    "width": obj.get("width", 1),
                    "height": obj.get("height", 0.5),
                    "text": obj.get("text", ""),
                    "fillColor": obj.get("fillColor", "#FFFFFF"),
                    "fontColor": obj.get("fontColor", "#000000"),
                    "fontSize": obj.get("fontSize", 12)
                }
                ui_objects.append(ui_obj)
            
            response = requests.post(
                f"{self.api_url}/api/batch-add",
                json={"objects": ui_objects},
                timeout=10
            )
            
            return response.status_code == 200 and response.json().get("success", False)
        
        except Exception as e:
            print(f"Error loading to canvas: {e}")
            return False


if __name__ == "__main__":
    # テスト例
    designer = UniversalSlideDesigner()
    
    # 例1: 汎用左右比較レイアウト
    result = designer.design_horizontal_comparison(
        left_title="従来方式",
        left_items=["単一処理", "コンテキスト制約", "品質のばらつき"],
        right_title="新方式（Tier化）",
        right_items=["段階的処理", "コンテキスト最適化", "一貫した品質"],
        title="処理方式の比較"
    )
    
    print("\n✅ スライド設計完了")
    print(f"  オブジェクト数: {result.get('object_count')}")
    print(f"  タイトル: {result.get('title')}")
    
    # 例2: 3層フロー
    result2 = designer.design_three_tier_flow(
        tier1_title="構成設計",
        tier1_subtitle="Outline",
        tier2_title="コンテンツ詳細",
        tier2_subtitle="Content",
        tier3_title="最終出力",
        tier3_subtitle="Output"
    )
    
    print("\n✅ 3層フロー設計完了")
    print(f"  オブジェクト数: {result2.get('object_count')}")
