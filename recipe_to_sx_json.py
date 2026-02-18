#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
スライドレシピ → SX テンプレート JSON 生成

design_principles.md と slide_recipe.md のルールに従う
"""

import json
from pathlib import Path

class SXTemplateJsonGenerator:
    """SX テンプレート向け JSON 生成"""
    
    def __init__(self):
        # SX テンプレートの座標制約
        self.available_left = 0.5
        self.available_right = 12.8
        self.available_width = 12.3
        self.available_top = 1.5
        self.available_bottom = 6.8
        self.available_height = 5.3
    
    def recipe_to_json(self, recipe: dict) -> dict:
        """
        レシピ → SX テンプレート JSON
        
        重要: tone と pattern から式に基づいて自動計算
        """
        
        result = {
            "template": "sx_proposal",
            "type": recipe.get("type", "content"),
            "title": recipe.get("title", ""),
            "subtitle": recipe.get("message", ""),
            "objects": []
        }
        
        # tone に基づいて色を決定
        tone = recipe.get("tone", "neutral")
        pattern = recipe.get("pattern", "default")
        labels = recipe.get("visual", {}).get("labels", [])
        
        # パターン別にオブジェクト生成
        if pattern == "two_column":
            result["objects"] = self._generate_two_column(tone, labels)
        elif pattern == "three_column":
            result["objects"] = self._generate_three_column(tone, labels)
        elif pattern == "process_flow":
            result["objects"] = self._generate_process_flow(tone, labels)
        
        return result
    
    def _generate_two_column(self, tone: str, labels: list) -> list:
        """
        2カード横並び
        
        tone:
          comparison → neutral(Before) + accent矢印 + secondary(After)
        """
        
        if tone == "comparison":
            # Before → arrow → After
            color_before = "C00000"  # primary（課題・現状）
            color_after = "4472C4"   # secondary（提案）
            color_arrow = "ED7D31"   # accent（矢印）
            
            label_before = labels[0] if len(labels) > 0 else "現状"
            label_after = labels[1] if len(labels) > 1 else "提案"
            
            width_box = 5.0
            gap = 0.2
            
            return [
                {
                    "type": "box",
                    "left": self.available_left,
                    "top": 3.5,
                    "width": width_box,
                    "height": 1.5,
                    "text": label_before,
                    "fill_color": color_before,
                    "font_color": "FFFFFF",
                    "font_size": 12
                },
                {
                    "type": "arrow",
                    "left": self.available_left + width_box + 0.1,
                    "top": 4.2,
                    "width": 0.6,
                    "height": 0.1,
                    "fill_color": color_arrow
                },
                {
                    "type": "box",
                    "left": self.available_left + width_box + 0.8,
                    "top": 3.5,
                    "width": width_box,
                    "height": 1.5,
                    "text": label_after,
                    "fill_color": color_after,
                    "font_color": "FFFFFF",
                    "font_size": 12
                }
            ]
        
        return []
    
    def _generate_three_column(self, tone: str, labels: list) -> list:
        """
        3カード横並び
        
        tone:
          problem → 全 neutral（課題）
          solution → 全 secondary（提案）
          neutral → 全 secondary（情報整理）
        """
        
        if tone == "problem":
            color = "C00000"  # primary（課題）
        else:
            color = "4472C4"  # secondary（提案・その他）
        
        # 3カード均等配置（SX テンプレートドキュメント推奨値を使用）
        width_box = 3.9
        gap = 0.2
        
        left_positions = [0.5, 4.6, 8.7]
        
        objects = []
        for i, left in enumerate(left_positions):
            label = labels[i] if i < len(labels) else f"項目{i+1}"
            
            objects.append({
                "type": "box",
                "left": left,
                "top": 3.5,
                "width": width_box,
                "height": 1.5,
                "text": label,
                "fill_color": color,
                "font_color": "FFFFFF",
                "font_size": 12
            })
        
        return objects
    
    def _generate_process_flow(self, tone: str, labels: list) -> list:
        """
        プロセスフロー（3〜4ステップ）
        
        tone: progression
          色: 全ボックス secondary + accent 矢印
        """
        
        color = "4472C4"       # secondary（各ステップ）
        color_arrow = "ED7D31" # accent（矢印）
        
        width_box = 2.5
        gap = 0.5
        
        objects = []
        left_pos = 0.5
        
        for i, label in enumerate(labels):
            # ボックス
            objects.append({
                "type": "box",
                "left": left_pos,
                "top": 4.0,
                "width": width_box,
                "height": 1.0,
                "text": label,
                "fill_color": color,
                "font_color": "FFFFFF",
                "font_size": 11
            })
            
            # 矢印（最後のステップ以外）
            if i < len(labels) - 1:
                objects.append({
                    "type": "arrow",
                    "left": left_pos + width_box + 0.05,
                    "top": 4.4,
                    "width": 0.4,
                    "height": 0.1,
                    "fill_color": color_arrow
                })
                left_pos += width_box + gap + 0.4
            else:
                left_pos += width_box + gap
        
        return objects


def main():
    print("\n" + "="*70)
    print("レシピ → SX テンプレート JSON 生成")
    print("="*70)
    
    # Demo 1: 課題と解決策の対比（comparison）
    demo1_recipe = {
        "index": 1,
        "type": "content",
        "title": "AI生成の課題と解決策",
        "message": "従来の手作業による課題を、Tier化による段階的生成で解決する",
        "pattern": "two_column",
        "tone": "comparison",
        "visual": {
            "labels": ["❌ 従来の課題", "✅ 解決策（Tier化）"],
            "emphasis": "last"
        }
    }
    
    # Demo 2: 3層フロー（progression）
    demo2_recipe = {
        "index": 2,
        "type": "content",
        "title": "AI + 人間協働：段階的生成パイプライン",
        "message": "3つのステップで、複雑な PPTX 生成を確実に実現",
        "pattern": "process_flow",
        "tone": "progression",
        "visual": {
            "labels": ["Tier 1\n既存品\n（Outline）", "Tier 2\n新方式\n（ビジュアル）", "Tier 3\n完成向かい方\n（Output）"],
            "emphasis": "equal"
        }
    }
    
    # Demo 3: 3項目比較（solution）
    demo3_recipe = {
        "index": 3,
        "type": "content",
        "title": "AI デジタルツイン：パイプライン",
        "message": "Canvas で見える座標 = PPTX に配置される座標（完全一致）",
        "pattern": "three_column",
        "tone": "solution",
        "visual": {
            "labels": ["入力\n（情報出し）", "処理\n（カスタマイズ）", "出力\n（完成向かい方）"],
            "emphasis": "equal"
        }
    }
    
    generator = SXTemplateJsonGenerator()
    
    demos = [
        (demo1_recipe, "test_output/recipe_demo1_sx.json"),
        (demo2_recipe, "test_output/recipe_demo2_sx.json"),
        (demo3_recipe, "test_output/recipe_demo3_sx.json"),
    ]
    
    for recipe, output_path in demos:
        json_data = generator.recipe_to_json(recipe)
        
        # body_area メタデータを追加
        json_data["body_area"] = {
            "left": generator.available_left,
            "top": generator.available_top,
            "width": generator.available_width,
            "height": generator.available_height
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ {output_path}")
        print(f"   Title: {recipe['title']}")
        print(f"   Pattern: {recipe['pattern']}")
        print(f"   Tone: {recipe['tone']}")
        print(f"   Objects: {len(json_data['objects'])}")
    
    print("\n" + "="*70)
    print("✅ 完了")
    print("="*70)

if __name__ == "__main__":
    main()
