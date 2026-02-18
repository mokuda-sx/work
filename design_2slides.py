#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2つのスライド（Tier1 + Tier2）を AIが自動設計して確認するスクリプト
"""

import sys
import json
from pathlib import Path
from ai_layout_designer import AILayoutDesigner

def main():
    print("\n" + "="*70)
    print("AI SLIDE DESIGN - 2スライド自動レイアウト設計")
    print("="*70)
    
    designer = AILayoutDesigner()
    
    # ========================================
    # SLIDE 1: Tier1 - AIコンテキスト制約への対応
    # ========================================
    print("\n[1] TIER1 スライド設計...")
    print("    タイトル: AIコンテキスト制約への対応：スキル化戦略")
    
    tier1_objects = [
        # 背景タイトル
        {"type": "box", "text": "AIコンテキスト制約への対応\nスキル化戦略", 
         "left": 0.5, "top": 0.3, "width": 4.3, "height": 0.9,
         "fillColor": "#4472C4", "fontColor": "#FFFFFF", "fontSize": 14},
        
        # サブタイトル
        {"type": "text", "text": "Tier 1 → Recipe → Tier 2 に分離した理由",
         "left": 0.5, "top": 1.3, "width": 4.3, "height": 0.4,
         "fontColor": "#404040", "fontSize": 11},
        
        # 左列: 従来の問題点
        {"type": "box", "text": "❌ 従来の課題",
         "left": 0.5, "top": 2.0, "width": 1.9, "height": 0.5,
         "fillColor": "#ED7D31", "fontColor": "#FFFFFF", "fontSize": 12},
        
        {"type": "text", "text": "• コンテキスト制約\n  (4K tokens)\n\n• 複雑な計画を一度に\n  実装不可\n\n• 品質のばらつき",
         "left": 0.5, "top": 2.6, "width": 1.9, "height": 1.5,
         "fontColor": "#404040", "fontSize": 10},
        
        # 中央: 矢印
        {"type": "arrow-right", "text": "→",
         "left": 2.6, "top": 3.0, "width": 0.5, "height": 0.4,
         "fillColor": "#ED7D31", "fontColor": "#FFFFFF", "fontSize": 10},
        
        # 右列: 解決策
        {"type": "box", "text": "✅ 3層フロー化",
         "left": 3.3, "top": 2.0, "width": 1.9, "height": 0.5,
         "fillColor": "#4472C4", "fontColor": "#FFFFFF", "fontSize": 12},
        
        {"type": "text", "text": "• 段階的設計\n  (Tier化)\n\n• 各層で機能を最適化\n  (Recipe)\n\n• 一貫した品質",
         "left": 3.3, "top": 2.6, "width": 1.9, "height": 1.5,
         "fontColor": "#FFFFFF", "fontSize": 10,
         "fillColor": "#4472C4"},
    ]
    
    tier1_result = designer.create_layout(
        tier1_objects,
        title="AIコンテキスト制約への対応：スキル化戦略",
        subtitle="Tier 1 → Recipe → Tier 2 に分離した理由"
    )
    
    if not tier1_result.get('success'):
        print(f"    ❌ エラー: {tier1_result.get('error')}")
        sys.exit(1)
    
    tier1_json = tier1_result.get('json')
    print(f"    ✅ {len(tier1_json['objects'])} オブジェクト生成")
    
    # ========================================
    # SLIDE 2: Tier2 - AI + 人間協働：3層フロー
    # ========================================
    print("\n[2] TIER2 スライド設計...")
    print("    タイトル: AI + 人間協働：3層フロー")
    
    tier2_result = designer.design_tier2_implementation_slide()
    
    if not tier2_result.get('success'):
        print(f"    ❌ エラー: {tier2_result.get('error')}")
        sys.exit(1)
    
    tier2_json = tier2_result.get('json')
    print(f"    ✅ {len(tier2_json['objects'])} オブジェクト生成")
    
    # ========================================
    # ファイル出力
    # ========================================
    output_dir = Path("test_output")
    output_dir.mkdir(exist_ok=True)
    
    # Tier1 保存
    tier1_path = output_dir / "slide_tier1.json"
    with open(tier1_path, "w", encoding="utf-8") as f:
        json.dump(tier1_json, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Tier1 JSON: {tier1_path}")
    
    # Tier2 保存
    tier2_path = output_dir / "slide_tier2.json"
    with open(tier2_path, "w", encoding="utf-8") as f:
        json.dump(tier2_json, f, ensure_ascii=False, indent=2)
    print(f"✅ Tier2 JSON: {tier2_path}")
    
    # スクリーンショット API でキャプチャ用に Canvas に送信
    print("\n✅ 設計データの生成完了")
    print(f"  - Tier1: {tier1_path}")
    print(f"  - Tier2: {tier2_path}")
    
    print("\n" + "="*70)
    print("✅ 設計完了")
    print("="*70)
    print(f"\n📊 統計:")
    print(f"  Tier1: {len(tier1_json['objects'])} オブジェクト")
    print(f"  Tier2: {len(tier2_json['objects'])} オブジェクト")
    print(f"  合計: {len(tier1_json['objects']) + len(tier2_json['objects'])} オブジェクト")
    
    print(f"\n🔗 確認方法:")
    print(f"  1. ブラウザで http://localhost:5000 を開く")
    print(f"  2. JSON をコピーして Canvas にロード")
    print(f"  3. Canvas に配置が表示されます")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
