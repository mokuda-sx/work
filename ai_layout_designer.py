#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ai_layout_designer.py
AI専用 スライドレイアウト自動設計スクリプト

このスクリプトは AI が使う Slide Layout Designer の制御スクリプトです。
AI が考えたレイアウトを Canvas に配置→ スクリーンショット確認 → JSON 出力

パイプライン:
1. AI が必要なオブジェクトを定義（テキスト/座標/色）
2. API経由で Canvas に配置
3. スクリーンショット取得して視覚検証
4. 修正必要なら Undo → 再配置
5. 完成後 JSON 出力 → PPTX 生成
"""

import json
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Optional
from designer_api_client import DesignerAPIClient

class AILayoutDesigner:
    """AI専用レイアウトデザイナー"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.client = DesignerAPIClient(base_url)
        self.layout = []
        self.history = []
    
    def design_tier2_implementation_slide(self) -> Dict:
        """
        Tier 2実装設計スライドを自動設計
        「AI + 人間協働：3層フロー」
        
        このメソッドは既存のスライドレイアウトを再現します。
        """
        
        # デザイン定義（AI が考えた配置）
        layout = [
            # Tier 1 ============================================
            {
                "type": "box",
                "text": "Tier 1\n構成設計",
                "left": 0.5, "top": 1.8, "width": 1.0, "height": 1.2,
                "fillColor": "#404040",
                "fontColor": "#FFFFFF",
                "fontSize": 11
            },
            # Tier 1 - Step 1
            {
                "type": "box",
                "text": "outline_guide\n指定",
                "left": 1.7, "top": 1.8, "width": 1.4, "height": 0.8,
                "fillColor": "#4472C4",
                "fontColor": "#FFFFFF",
                "fontSize": 11
            },
            {
                "type": "arrow",
                "left": 3.3, "top": 2.05, "width": 0.5, "height": 0.3,
                "fillColor": "#ED7D31"
            },
            {
                "type": "box",
                "text": "AIが\n構成案を\n生成",
                "left": 4.0, "top": 1.8, "width": 1.4, "height": 0.8,
                "fillColor": "#4472C4",
                "fontColor": "#FFFFFF",
                "fontSize": 11
            },
            {
                "type": "box",
                "text": "",
                "left": 5.7, "top": 1.8, "width": 6.5, "height": 0.8,
                "fillColor": "#F2F2F2",
                "fontColor": "#333333",
                "fontSize": 1
            },
            {
                "type": "text",
                "text": "【成果物】提案書の構成・ストーリー（アウトライン）",
                "left": 5.9, "top": 1.8, "width": 6.1, "height": 0.8,
                "fillColor": "#FFFFFF",
                "fontColor": "#333333",
                "fontSize": 10,
                "valign": "middle"
            },
            
            # Recipe (Tier 2) ====================================
            {
                "type": "box",
                "text": "Recipe\n意図設計",
                "left": 0.5, "top": 3.2, "width": 1.0, "height": 1.2,
                "fillColor": "#404040",
                "fontColor": "#FFFFFF",
                "fontSize": 11
            },
            {
                "type": "box",
                "text": "パターン\n参照作品\n指定",
                "left": 1.7, "top": 3.2, "width": 1.4, "height": 0.8,
                "fillColor": "#4472C4",
                "fontColor": "#FFFFFF",
                "fontSize": 11
            },
            {
                "type": "arrow",
                "left": 3.3, "top": 3.45, "width": 0.5, "height": 0.3,
                "fillColor": "#ED7D31"
            },
            {
                "type": "box",
                "text": "AIが\n詳細配置\nを提案",
                "left": 4.0, "top": 3.2, "width": 1.4, "height": 0.8,
                "fillColor": "#4472C4",
                "fontColor": "#FFFFFF",
                "fontSize": 11
            },
            {
                "type": "box",
                "text": "",
                "left": 5.7, "top": 3.2, "width": 6.5, "height": 0.8,
                "fillColor": "#F2F2F2",
                "fontColor": "#333333",
                "fontSize": 1
            },
            {
                "type": "text",
                "text": "【成果物】スライド設計（パターン・意図・配置案）",
                "left": 5.9, "top": 3.2, "width": 6.1, "height": 0.8,
                "fillColor": "#FFFFFF",
                "fontColor": "#333333",
                "fontSize": 10,
                "valign": "middle"
            },
            
            # Tier 2実装設計 ======================================
            {
                "type": "box",
                "text": "Tier 2\n実装設計",
                "left": 0.5, "top": 4.6, "width": 1.0, "height": 1.2,
                "fillColor": "#404040",
                "fontColor": "#FFFFFF",
                "fontSize": 11
            },
            {
                "type": "box",
                "text": "座標\n色\nフォント\n指定",
                "left": 1.7, "top": 4.6, "width": 1.4, "height": 0.8,
                "fillColor": "#4472C4",
                "fontColor": "#FFFFFF",
                "fontSize": 11
            },
            {
                "type": "arrow",
                "left": 3.3, "top": 4.85, "width": 0.5, "height": 0.3,
                "fillColor": "#ED7D31"
            },
            {
                "type": "box",
                "text": "AIが\nPPTX JSON\nを生成",
                "left": 4.0, "top": 4.6, "width": 1.4, "height": 0.8,
                "fillColor": "#4472C4",
                "fontColor": "#FFFFFF",
                "fontSize": 11
            },
            {
                "type": "box",
                "text": "",
                "left": 5.7, "top": 4.6, "width": 6.5, "height": 0.8,
                "fillColor": "#F2F2F2",
                "fontColor": "#333333",
                "fontSize": 1
            },
            {
                "type": "text",
                "text": "【成果物】PowerPoint JSON + PPTX",
                "left": 5.9, "top": 4.6, "width": 6.1, "height": 0.8,
                "fillColor": "#FFFFFF",
                "fontColor": "#333333",
                "fontSize": 10,
                "valign": "middle"
            }
        ]
        
        return self.create_layout(
            layout,
            title="AI + 人間協働：3層フロー",
            subtitle="段階ごとに必要なコンテキストだけを読み込ませることで、AIの生成品質を最適化する"
        )
    
    def create_layout(self, objects: List[Dict], title: str = "", subtitle: str = "") -> Dict:
        """レイアウトを作成
        
        Args:
            objects: UI形式のオブジェクト配列
            title: スライドタイトル
            subtitle: スライトサブタイトル
        
        Returns:
            JSON形式のスライドデータ
        """
        
        print(f"\n📐 Creating layout with {len(objects)} objects...")
        print(f"   Title: {title}")
        
        # 1. オブジェクトをCanvas に配置
        result = self.client.batch_add_objects(objects)
        
        if not result.get('success'):
            return {
                "success": False,
                "error": f"Failed to add objects: {result.get('error')}"
            }
        
        print(f"✓ Batch added {result.get('count')} objects")
        
        # 2. JSON形式に変換
        json_objects = result.get('objects', [])
        
        slide_data = {
            "index": 1,
            "type": "content",
            "title": title,
            "subtitle": subtitle,
            "objects": json_objects
        }
        
        self.layout = json_objects
        self.history.append(slide_data)
        
        return {
            "success": True,
            "json": slide_data,
            "jsonString": json.dumps(slide_data, ensure_ascii=False, indent=2),
            "objectCount": len(json_objects)
        }
    
    def export_json(self, output_path: Optional[str] = None) -> Dict:
        """JSON をファイルにエクスポート
        
        Args:
            output_path: 出力ファイルパス
        
        Returns:
            エクスポート結果
        """
        
        if not self.history:
            return {"success": False, "error": "No layout to export"}
        
        slide_data = self.history[-1]
        json_string = json.dumps(slide_data, ensure_ascii=False, indent=2)
        
        if output_path:
            Path(output_path).write_text(json_string, encoding='utf-8')
            print(f"✓ Exported to: {output_path}")
        
        return {
            "success": True,
            "json": slide_data,
            "jsonString": json_string
        }

def main():
    """デモンストレーション"""
    print("=" * 70)
    print("🤖 AI Layout Designer Demo")
    print("=" * 70)
    
    designer = AILayoutDesigner()
    
    # Tier 2実装設計スライドを自動設計
    result = designer.design_tier2_implementation_slide()
    
    if result.get('success'):
        print(f"\n✅ Layout created successfully!")
        print(f"   Objects: {result.get('objectCount')}")
        
        # JSON をファイルに保存
        output_file = Path(__file__).parent / "ai_generated_layout.json"
        designer.export_json(str(output_file))
        
        # JSON 内容を表示
        print(f"\n📋 JSON Output:")
        print("-" * 70)
        print(result.get('jsonString')[:500] + "...")
        print("-" * 70)
    else:
        print(f"\n❌ Error: {result.get('error')}")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()
