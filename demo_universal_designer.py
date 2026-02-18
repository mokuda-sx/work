#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汎用 Slide Designer デモンストレーション
任意のスライドを設計できることを実証
"""

import json
from pathlib import Path
from universal_slide_designer import UniversalSlideDesigner

def demo():
    print("\n" + "="*70)
    print("UNIVERSAL SLIDE DESIGNER - デモンストレーション")
    print("="*70)
    
    designer = UniversalSlideDesigner()
    output_dir = Path("test_output")
    output_dir.mkdir(exist_ok=True)
    
    # ========================================
    # デモ1: 左右比較レイアウト（汎用テンプレート）
    # ========================================
    print("\n[DEMO 1] 左右比較レイアウト")
    print("─" * 70)
    
    result1 = designer.design_horizontal_comparison(
        left_title="❌ 従来の課題",
        left_items=[
            "コンテキスト制約（4K tokens）",
            "複雑な計画を一度に実装不可",
            "品質のばらつき"
        ],
        right_title="✅ 解決策（Tier化）",
        right_items=[
            "段階的設計で最適化",
            "各層で機能を分割",
            "一貫した品質保証"
        ],
        title="AI生成の課題と解決策",
        title_color="#4472C4",
        left_color="#ED7D31",
        right_color="#4472C4"
    )
    
    print(f"✅ 完成")
    print(f"   タイトル: {result1.get('title')}")
    print(f"   オブジェクト数: {result1.get('object_count')}")
    
    # 保存
    if result1.get("success"):
        designer.export_json(result1, str(output_dir / "demo1_comparison.json"))
        print(f"   JSON保存: demo1_comparison.json")
    
    # ========================================
    # デモ2: 3層フロー（汎用テンプレート）
    # ========================================
    print("\n[DEMO 2] 3層フロー（Tier構造）")
    print("─" * 70)
    
    result2 = designer.design_three_tier_flow(
        tier1_title="Tier 1",
        tier1_subtitle="構成設計\n(Outline)",
        tier1_color="#404040",
        
        tier2_title="Tier 2",
        tier2_subtitle="コンテンツ詳細\n(Content)",
        tier2_color="#4472C4",
        
        tier3_title="出力",
        tier3_subtitle="最終PPTX\n(Output)",
        tier3_color="#1F3864",
        
        title="AI + 人間協働：段階的生成パイプライン"
    )
    
    print(f"✅ 完成")
    print(f"   タイトル: {result2.get('title')}")
    print(f"   オブジェクト数: {result2.get('object_count')}")
    
    # 保存
    if result2.get("success"):
        designer.export_json(result2, str(output_dir / "demo2_three_tier.json"))
        print(f"   JSON保存: demo2_three_tier.json")
    
    # ========================================
    # デモ3: 完全カスタムレイアウト
    # ========================================
    print("\n[DEMO 3] 完全カスタムレイアウト")
    print("─" * 70)
    
    custom_objects = [
        {
            "type": "box",
            "text": "AI + 人間協働：デジタルツイン",
            "left": 0.5,
            "top": 0.3,
            "width": 4.3,
            "height": 0.6,
            "fillColor": "#4472C4",
            "fontColor": "#FFFFFF",
            "fontSize": 14
        },
        {
            "type": "text",
            "text": "Canvas で見ながら配置 → JSON 自動生成 → PPTX 完成",
            "left": 0.5,
            "top": 1.1,
            "width": 4.3,
            "height": 0.4,
            "fontColor": "#404040",
            "fontSize": 11
        },
        {
            "type": "box",
            "text": "従来\n（テキストベース\n計算）",
            "left": 0.5,
            "top": 1.8,
            "width": 1.3,
            "height": 1.2,
            "fillColor": "#ED7D31",
            "fontColor": "#FFFFFF",
            "fontSize": 10
        },
        {
            "type": "arrow",
            "left": 2.0,
            "top": 2.2,
            "width": 0.5,
            "height": 0.3,
            "fillColor": "#ED7D31"
        },
        {
            "type": "box",
            "text": "新方式\n（ビジュアル\nフィードバック）",
            "left": 2.7,
            "top": 1.8,
            "width": 1.3,
            "height": 1.2,
            "fillColor": "#4472C4",
            "fontColor": "#FFFFFF",
            "fontSize": 10
        },
        {
            "type": "arrow",
            "left": 4.2,
            "top": 2.2,
            "width": 0.5,
            "height": 0.3,
            "fillColor": "#4472C4"
        },
        {
            "type": "box",
            "text": "完璧な\nレイアウト",
            "left": 4.9,
            "top": 1.8,
            "width": 1.3,
            "height": 1.2,
            "fillColor": "#1F3864",
            "fontColor": "#FFFFFF",
            "fontSize": 10
        }
    ]
    
    result3 = designer.design(
        objects=custom_objects,
        title="AI デジタルツイン：パイプライン",
        subtitle="ビジュアルフィードバックで精度向上"
    )
    
    print(f"✅ 完成")
    print(f"   タイトル: {result3.get('title')}")
    print(f"   オブジェクト数: {result3.get('object_count')}")
    
    # 保存
    if result3.get("success"):
        designer.export_json(result3, str(output_dir / "demo3_custom.json"))
        print(f"   JSON保存: demo3_custom.json")
    
    # ========================================
    # 統計
    # ========================================
    print("\n" + "="*70)
    print("✅ デモンストレーション完了")
    print("="*70)
    
    print(f"\n📊 生成されたスライド数: 3")
    print(f"   Demo1: {result1.get('object_count')} オブジェクト")
    print(f"   Demo2: {result2.get('object_count')} オブジェクト")
    print(f"   Demo3: {result3.get('object_count')} オブジェクト")
    total = (result1.get('object_count', 0) + 
             result2.get('object_count', 0) + 
             result3.get('object_count', 0))
    print(f"   合計: {total} オブジェクト")
    
    print(f"\n📁 出力ファイル:")
    print(f"   • demo1_comparison.json")
    print(f"   • demo2_three_tier.json")
    print(f"   • demo3_custom.json")
    
    print(f"\n🎯 これで、『任意のスライド』を設計できます")
    print(f"   - テンプレートを使用")
    print(f"   - 完全カスタム配置")
    print(f"   - 組み合わせ")
    
    print(f"\n🔗 使用方法:")
    print(f"   from universal_slide_designer import UniversalSlideDesigner")
    print(f"   designer = UniversalSlideDesigner()")
    print(f"   result = designer.design_horizontal_comparison(...)")
    print(f"   # または")
    print(f"   result = designer.design(custom_objects, title='Custom')")
    print(f"   # JSON 化")
    print(f"   designer.export_json(result, 'my_slide.json')")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    demo()
