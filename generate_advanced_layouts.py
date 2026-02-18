#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高度なレイアウトパターン生成

slide_recipe.md の複雑なパターン（row_label_content, swimlane_process）
を使用して、情報密度の高い、洗練されたスライドを生成

Canvas デザイナー GUI との連携を想定
"""

import json
from pathlib import Path

class AdvancedSXLayoutGenerator:
    """高度な SX テンプレート対応レイアウト生成"""
    
    def __init__(self):
        # SX テンプレートの body placeholder [14] の範囲に合わせる
        # body: left 0.997", top 1.545", width 11.340", height 5.512"
        self.left_margin = 0.997
        self.top_margin = 1.545
        self.available_width = 11.340
        self.available_height = 5.512
        self.right_margin = self.left_margin + self.available_width
        self.bottom_margin = self.top_margin + self.available_height
    
    def swimlane_process_layout(self, title: str, subtitle: str, 
                                rows: list, cols: int = 3) -> dict:
        """
        Swimlane Process Layout
        
        複数の行（Tier）×複数の列（段階）の構造
        
        rows: [
          {"label": "Tier 1", "items": ["要件", "検討", "決定"]},
          {"label": "Recipe", "items": ["パターン選択", "詳細設計", "..."]},
          {"label": "Tier 2", "items": ["色・フォント", "配置", "PPTX生成"]}
        ]
        """
        
        objects = []
        
        # レイアウト計算
        label_width = 1.6  # 左のラベル列の幅
        content_width = self.available_width - label_width - 0.2  # gap 0.2
        col_width = (content_width - 0.15 * (cols - 1)) / cols  # gaps between cols
        
        row_height = 0.9
        row_gap = 0.15
        
        # 色スキーム（濃灰→薄青→中間青→濃紺のグラデーション）
        color_scheme = ["404040", "8FAADC", "4472C4", "1F3864"]
        
        current_top = self.top_margin
        
        for row_idx, row in enumerate(rows):
            label = row.get("label", "")
            items = row.get("items", [])
            
            # ─── 左側ラベル ───
            objects.append({
                "type": "box",
                "left": self.left_margin,
                "top": current_top,
                "width": label_width,
                "height": row_height,
                "text": label,
                "fill_color": color_scheme[min(row_idx, len(color_scheme)-1)],
                "font_color": "FFFFFF",
                "font_size": 14
            })
            
            # ─── 各列の内容 ───
            for col_idx, item in enumerate(items[:cols]):
                col_left = self.left_margin + label_width + 0.2 + col_idx * (col_width + 0.15)
                
                # 矢印の色
                arrow_color = "ED7D31"  # accent
                
                # コンテンツボックス
                objects.append({
                    "type": "box",
                    "left": col_left,
                    "top": current_top,
                    "width": col_width,
                    "height": row_height,
                    "text": item,
                    "fill_color": color_scheme[min(row_idx, len(color_scheme)-1)],
                    "font_color": "FFFFFF",
                    "font_size": 14
                })
                
                # 列間の矢印（最後の列以外）
                if col_idx < len(items) - 1:
                    objects.append({
                        "type": "arrow",
                        "left": col_left + col_width + 0.05,
                        "top": current_top + row_height / 2 - 0.15,
                        "width": 0.3,
                        "height": 0.3,
                        "fill_color": arrow_color
                    })
            
            current_top += row_height + row_gap
        
        return {
            "template": "sx_proposal",
            "type": "content",
            "title": title,
            "subtitle": subtitle,
            "objects": objects,
            "body_area": {
                "left": self.left_margin,
                "top": self.top_margin,
                "width": self.available_width,
                "height": self.available_height
            }
        }
    
    def matrix_3x3_layout(self, title: str, subtitle: str,
                          header_labels: list, row_labels: list,
                          items: list) -> dict:
        """
        3×3 マトリックスレイアウト
        
        items: 9要素の一次元リスト（行優先）
        """
        
        objects = []
        
        # 計算
        label_width = 1.5
        cell_width = (self.available_width - label_width - 0.3) / 3
        cell_height = 0.7
        
        start_top = self.top_margin + 0.5
        
        # ─── ヘッダー行 ───
        for col_idx, header in enumerate(header_labels):
            objects.append({
                "type": "box",
                "left": self.left_margin + label_width + 0.3 + col_idx * cell_width,
                "top": self.top_margin,
                "width": cell_width,
                "height": 0.4,
                "text": header,
                "fill_color": "404040",
                "font_color": "FFFFFF",
                "font_size": 14
            })
        
        # ─── データセル（3×3） ───
        for row_idx, row_label in enumerate(row_labels):
            # 行ラベル
            objects.append({
                "type": "box",
                "left": self.left_margin,
                "top": start_top + row_idx * cell_height,
                "width": label_width,
                "height": cell_height,
                "text": row_label,
                "fill_color": "8FAADC",
                "font_color": "FFFFFF",
                "font_size": 14
            })
            
            # 各列のセル
            for col_idx in range(3):
                item_idx = row_idx * 3 + col_idx
                item = items[item_idx] if item_idx < len(items) else ""
                
                objects.append({
                    "type": "box",
                    "left": self.left_margin + label_width + 0.3 + col_idx * cell_width,
                    "top": start_top + row_idx * cell_height,
                    "width": cell_width,
                    "height": cell_height,
                    "text": item,
                    "fill_color": "4472C4",
                    "font_color": "FFFFFF",
                    "font_size": 14
                })
        
        return {
            "template": "sx_proposal",
            "type": "content",
            "title": title,
            "subtitle": subtitle,
            "objects": objects,
            "body_area": {
                "left": self.left_margin,
                "top": self.top_margin,
                "width": self.available_width,
                "height": self.available_height
            }
        }


def main():
    print("\n" + "="*70)
    print("高度なレイアウトパターン生成")
    print("="*70)
    
    gen = AdvancedSXLayoutGenerator()
    
    # ─── パターン1: Swimlane Process（3層×3段階）───
    demo_swimlane = gen.swimlane_process_layout(
        title="AI + 人間協働：3層フロー",
        subtitle="段階ごとに必要なコンテキストだけを読み込むことで、AIの生成品質を最適化する",
        rows=[
            {
                "label": "Tier 1\n構成設計",
                "items": ["構成方針\nを決定", "outline.json\n生成", "スライド\n構成確定"]
            },
            {
                "label": "Recipe\n意図設計",
                "items": ["スライド\nパターン選択", "レイアウト\nの設計", "recipe.json\n生成"]
            },
            {
                "label": "Tier 2\n実装設計",
                "items": ["色・フォント\n指定", "座標\n配置", "PPTX JSON\n生成"]
            }
        ],
        cols=3
    )
    
    # ─── パターン2: 3×3 マトリックス ───
    demo_matrix = gen.matrix_3x3_layout(
        title="提案価値のマトリックス分析",
        subtitle="市場機会 × 実装難度で優先順位を判定",
        header_labels=["高", "中", "低"],
        row_labels=["高機会", "中機会", "低機会"],
        items=[
            "優先度1\n実装Go",
            "優先度2\n要検討",
            "保留\n将来オプション",
            "優先度2\n要検討",
            "中実装\n段階的",
            "スコープ外",
            "保留\n将来オプション",
            "スコープ外",
            "実施不要"
        ]
    )
    
    # 保存
    output_dir = Path("test_output")
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / "advanced_swimlane.json", 'w', encoding='utf-8') as f:
        json.dump(demo_swimlane, f, indent=2, ensure_ascii=False)
    
    with open(output_dir / "advanced_matrix.json", 'w', encoding='utf-8') as f:
        json.dump(demo_matrix, f, indent=2, ensure_ascii=False)
    
    print("\n✅ 生成完了")
    print(f"   • test_output/advanced_swimlane.json")
    print(f"   • test_output/advanced_matrix.json")
    
    print("\n📊 パターン:")
    print(f"   Swimlane: 3層×3段階={len(demo_swimlane['objects'])}個オブジェクト")
    print(f"   Matrix:   3×3={len(demo_matrix['objects'])}個オブジェクト")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
