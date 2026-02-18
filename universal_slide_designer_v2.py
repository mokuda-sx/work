#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汎用スライドデザイナー v2
SX テンプレートの配置制約に準拠したスライドレイアウト設計

Canvas で見える座標 = PPTX に配置される座標（完全一致）
"""

import json
from pathlib import Path
from typing import List, Dict, Any

class UniversalSlideDesignerV2:
    """SX テンプレート対応の汎用スライドデザイナー"""
    
    def __init__(self, template_id: str = "sx_proposal"):
        """
        初期化
        
        Args:
            template_id: テンプレート ID（"sx_proposal" のみ対応）
        """
        self.template_id = template_id
        
        # SX テンプレート専用の配置制約
        if template_id == "sx_proposal":
            # スライド全体
            self.slide_width = 13.333
            self.slide_height = 7.5
            
            # Body content エリア（content layout [14] placeholder の範囲）
            self.body_left = 0.997
            self.body_top = 1.545
            self.body_width = 11.340
            self.body_height = 5.512
            self.body_right = self.body_left + self.body_width
            self.body_bottom = self.body_top + self.body_height
            
            # Title area
            self.title_top = 0.459
            self.title_height = 0.300
            
            # Subtitle area
            self.subtitle_top = 0.782
            self.subtitle_height = 0.538
        
        self.objects: List[Dict[str, Any]] = []
        self.title = ""
        self.subtitle = ""
    
    def _validate_bounds(self, left: float, top: float, width: float, height: float) -> bool:
        """オブジェクトが body エリア内に収まっているか確認"""
        if left < self.body_left or top < self.body_top:
            return False
        if left + width > self.body_right or top + height > self.body_bottom:
            return False
        return True
    
    def add_box(
        self,
        left: float,
        top: float,
        width: float,
        height: float,
        text: str = "",
        fill_color: str = "4472C4",
        font_color: str = "FFFFFF",
        font_size: int = 12
    ) -> None:
        """
        背景付きボックスを追加
        
        Args:
            left, top, width, height: 座標とサイズ（インチ）
            text: テキスト内容
            fill_color: 背景色（16進数, SX color semantics に従う）
            font_color: テキスト色（16進数）
            font_size: フォントサイズ
        """
        if not self._validate_bounds(left, top, width, height):
            print(f"⚠️  警告: オブジェクトがエリア外です")
            print(f"   Required: left={self.body_left:.2f}\"-{self.body_right:.2f}\"")
            print(f"             top={self.body_top:.2f}\"-{self.body_bottom:.2f}\"")
            print(f"   Got: left={left:.2f}\", top={top:.2f}\", width={width:.2f}\", height={height:.2f}\"")
        
        self.objects.append({
            "type": "box",
            "left": round(left, 3),
            "top": round(top, 3),
            "width": round(width, 3),
            "height": round(height, 3),
            "text": text,
            "fill_color": fill_color,
            "font_color": font_color,
            "font_size": font_size
        })
    
    def add_text(
        self,
        left: float,
        top: float,
        width: float,
        height: float,
        text: str = "",
        font_color: str = "404040",
        font_size: int = 11
    ) -> None:
        """背景なしテキストボックスを追加"""
        if not self._validate_bounds(left, top, width, height):
            print(f"⚠️  警告: オブジェクトがエリア外です")
        
        self.objects.append({
            "type": "text",
            "left": round(left, 3),
            "top": round(top, 3),
            "width": round(width, 3),
            "height": round(height, 3),
            "text": text,
            "font_color": font_color,
            "font_size": font_size
        })
    
    def add_arrow(
        self,
        left: float,
        top: float,
        width: float,
        height: float,
        color: str = "ED7D31"
    ) -> None:
        """矢印を追加（SX: 遷移・矢印のみに ED7D31 を使用）"""
        if not self._validate_bounds(left, top, width, height):
            print(f"⚠️  警告: 矢印がエリア外です")
        
        self.objects.append({
            "type": "arrow",
            "left": round(left, 3),
            "top": round(top, 3),
            "width": round(width, 3),
            "height": round(height, 3),
            "fill_color": color
        })
    
    def set_title(self, title: str) -> None:
        """スライドタイトルを設定"""
        self.title = title
    
    def set_subtitle(self, subtitle: str) -> None:
        """スライドサブタイトルを設定"""
        self.subtitle = subtitle
    
    def export_json(self, output_path: str) -> bool:
        """JSON として export"""
        try:
            data = {
                "template": self.template_id,
                "title": self.title,
                "subtitle": self.subtitle,
                "slide_size": {
                    "width": self.slide_width,
                    "height": self.slide_height
                },
                "body_area": {
                    "left": self.body_left,
                    "top": self.body_top,
                    "width": self.body_width,
                    "height": self.body_height
                },
                "objects": self.objects
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"エラー: {e}")
            return False
    
    def print_summary(self) -> None:
        """設計情報を表示"""
        print("\n" + "="*70)
        print(f"Universal Slide Designer v2 - {self.template_id}")
        print("="*70)
        print(f"\nSlide Title: {self.title}")
        if self.subtitle:
            print(f"Subtitle: {self.subtitle}")
        print(f"\nCanvas Configuration:")
        print(f"  Slide Size: {self.slide_width}\" × {self.slide_height}\"")
        print(f"  Body Content Area:")
        print(f"    - Left: {self.body_left:.3f}\" → Right: {self.body_right:.3f}\" (width {self.body_width:.3f}\")")
        print(f"    - Top: {self.body_top:.3f}\" → Bottom: {self.body_bottom:.3f}\" (height {self.body_height:.3f}\")")
        
        print(f"\nObjects ({len(self.objects)}):")
        for i, obj in enumerate(self.objects, 1):
            obj_type = obj['type']
            left = obj['left']
            top = obj['top']
            width = obj['width']
            height = obj['height']
            
            print(f"  {i}. [{obj_type}] @ ({left:.3f}\", {top:.3f}\") : {width:.3f}\" × {height:.3f}\"")
            
            if 'text' in obj and obj['text']:
                preview = obj['text'][:40]
                if len(obj['text']) > 40:
                    preview += "..."
                print(f"      Text: {preview}")
        
        print("\n✅ これらの座標は PPTX に直接使用されます")
        print("="*70 + "\n")


# ─────────────────────────────────────────────────────────────────────
# デモ生成
# ─────────────────────────────────────────────────────────────────────

def demo_1_comparison():
    """Demo 1: 左右比較レイアウト"""
    designer = UniversalSlideDesignerV2("sx_proposal")
    designer.set_title("AI生成の課題と解決策")
    
    # 上部タイトルバー
    designer.add_box(
        left=0.997,
        top=1.545,
        width=11.340,
        height=0.500,
        text="AI生成の課題と解決策",
        fill_color="4472C4",
        font_color="FFFFFF",
        font_size=14
    )
    
    # 左側: 従来の課題
    designer.add_box(
        left=0.997,
        top=2.150,
        width=5.000,
        height=1.800,
        text="❌ 従来の課題\n\n・コンテキスト制限（4K tokens）\n・複数計画を一度に実装不可\n・品質ばらつき",
        fill_color="ED7D31",
        font_color="FFFFFF",
        font_size=10
    )
    
    # 右側: 解決策（Tier化）
    designer.add_box(
        left=6.337,
        top=2.150,
        width=5.000,
        height=1.800,
        text="✅ 解決策（Tier化）\n\n・段階的なレシピ使用\n・各 Tier で品質保証\n・スケーラブルなパイプライン",
        fill_color="4472C4",
        font_color="FFFFFF",
        font_size=10
    )
    
    # 下部: 補足テキスト
    designer.add_text(
        left=0.997,
        top=4.100,
        width=11.340,
        height=2.457,
        text="プロセス内に段階を組み込むことで、複雑なタスクでも安定した AI 生成が可能に\n\n"
             "・Tier 1: 基本と要件出し\n"
             "・Tier 2: テンプレートと配置\n"
             "・Tier 3: 最終調整と出力",
        font_color="404040",
        font_size=9
    )
    
    designer.print_summary()
    designer.export_json("test_output/demo1_sx_template.json")
    return designer


def demo_2_three_tier():
    """Demo 2: 3層フロー"""
    designer = UniversalSlideDesignerV2("sx_proposal")
    designer.set_title("AI + 人間協働：段階的生成パイプライン")
    
    # 上部ヘッダー
    designer.add_box(
        left=0.997,
        top=1.545,
        width=11.340,
        height=0.450,
        text="AI + 人間協働：段階的生成パイプライン",
        fill_color="4472C4",
        font_color="FFFFFF",
        font_size=13
    )
    
    # Tier 1
    designer.add_box(
        left=1.200,
        top=2.200,
        width=3.200,
        height=1.500,
        text="既存品\n（Outline）\n\nPrompt + Context",
        fill_color="ED7D31",
        font_color="FFFFFF",
        font_size=9
    )
    
    # 矢印 1→2
    designer.add_arrow(
        left=4.500,
        top=2.950,
        width=0.600,
        height=0.100,
        color="ED7D31"
    )
    
    # Tier 2
    designer.add_box(
        left=5.200,
        top=2.200,
        width=3.200,
        height=1.500,
        text="新方式\n（ビジュアル\nフィードバック）",
        fill_color="4472C4",
        font_color="FFFFFF",
        font_size=9
    )
    
    # 矢印 2→3
    designer.add_arrow(
        left=8.500,
        top=2.950,
        width=0.600,
        height=0.100,
        color="ED7D31"
    )
    
    # Tier 3
    designer.add_box(
        left=9.200,
        top=2.200,
        width=2.137,
        height=1.500,
        text="完成向かい方\n（Output）\n\nPPTX",
        fill_color="4472C4",
        font_color="FFFFFF",
        font_size=9
    )
    
    # 説明テキスト
    designer.add_text(
        left=1.200,
        top=3.900,
        width=10.337,
        height=1.657,
        text="Canvas で見える座標 = PPTX に配置される座標（完全一致）\n"
             "これにより、配置計算エラーを完全に排除し、見たままの PPTX を生成可能に",
        font_color="404040",
        font_size=9
    )
    
    designer.print_summary()
    designer.export_json("test_output/demo2_sx_template.json")
    return designer


def demo_3_ui_flow():
    """Demo 3: UI フロー"""
    designer = UniversalSlideDesignerV2("sx_proposal")
    designer.set_title("AI デジタルツイン：パイプライン")
    designer.set_subtitle("CoTier Architecture Flow")
    
    # ヘッダー
    designer.add_box(
        left=0.997,
        top=1.545,
        width=11.340,
        height=0.400,
        text="AI + 人間協働：段階的生成パイプライン",
        fill_color="4472C4",
        font_color="FFFFFF",
        font_size=12
    )
    
    # Tier 1 - Input
    designer.add_box(
        left=1.200,
        top=2.100,
        width=2.500,
        height=1.600,
        text="入力\n（情報出し）\n\nPrompt",
        fill_color="404040",
        font_color="FFFFFF",
        font_size=9
    )
    
    # 矢印 1→2
    designer.add_arrow(left=3.800, top=2.850, width=0.500, height=0.100)
    
    # Tier 2 - Process
    designer.add_box(
        left=4.400,
        top=2.100,
        width=2.500,
        height=1.600,
        text="処理\n（カスタマイズ）\n\nCanvas",
        fill_color="4472C4",
        font_color="FFFFFF",
        font_size=9
    )
    
    # 矢印 2→3
    designer.add_arrow(left=7.000, top=2.850, width=0.500, height=0.100)
    
    # Tier 3 - Output
    designer.add_box(
        left=7.600,
        top=2.100,
        width=2.500,
        height=1.600,
        text="出力\n（完成向かい方）\n\nPPTX",
        fill_color="4472C4",
        font_color="FFFFFF",
        font_size=9
    )
    
    # 補足説明
    designer.add_text(
        left=1.200,
        top=3.900,
        width=10.337,
        height=1.657,
        text="各ステップで人間が確認・調整できる設計\n"
             "Canvas デザイナー中心のワークフロー：見たままが最終出力",
        font_color="404040",
        font_size=9
    )
    
    designer.print_summary()
    designer.export_json("test_output/demo3_sx_template.json")
    return designer


def main():
    print("\n" + "="*70)
    print("Universal Slide Designer v2 - SX Template Compliance")
    print("="*70)
    
    print("\n[1] Demo 1: 左右比較レイアウト")
    demo_1_comparison()
    
    print("\n[2] Demo 2: 3層フロー")
    demo_2_three_tier()
    
    print("\n[3] Demo 3: UI フロー")
    demo_3_ui_flow()
    
    print("\n" + "="*70)
    print("✅ 完了：3つのデモが SX テンプレート対応 JSON で出力されました")
    print("="*70)
    print("\n📋 出力ファイル:")
    print("   • test_output/demo1_sx_template.json")
    print("   • test_output/demo2_sx_template.json")
    print("   • test_output/demo3_sx_template.json")
    print("\n🔑 重要: 各 JSON の座標は SX template の body area に準拠")
    print("   → Canvas で見える = PPTX に配置される（完全一致）\n")


if __name__ == "__main__":
    main()
