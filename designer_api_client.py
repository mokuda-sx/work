#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
designer_api_client.py
AI用 Designer API クライアント

Slide Layout Designer に自動配置指示を出すための Python ライブラリ

使用例:
    client = DesignerAPIClient("http://localhost:5000")
    
    # 複数オブジェクトを一度に配置
    layout = [
        {"type": "box", "text": "Tier 1\n構成設計", "left": 0.5, "top": 1.8, "width": 1.0, "height": 1.2, "fillColor": "#404040", "fontColor": "#FFFFFF", "fontSize": 11},
        {"type": "arrow", "left": 3.3, "top": 2.05, "width": 0.5, "height": 0.3, "fillColor": "#ED7D31"},
    ]
    
    result = client.batch_add_objects(layout)
    print(f"Added {result['count']} objects")
    
    # スクリーンショット取得
    screenshot = client.capture_screenshot()
    
    # JSON出力
    json_result = client.export_layout()
    print(json_result['jsonString'])
"""

import requests
import json
from typing import List, Dict, Optional
import base64
from pathlib import Path

class DesignerAPIClient:
    """Slide Layout Designer API クライアント"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        """初期化
        
        Args:
            base_url: Designer サーバーの URL
        """
        self.base_url = base_url
        self.session = requests.Session()
    
    def batch_add_objects(self, objects: List[Dict]) -> Dict:
        """複数オブジェクトを一度に追加
        
        Args:
            objects: UV形式のオブジェクト配列
                [
                    {"type": "box", "text": "...", "left": 0.5, "top": 1.8, "width": 1.0, "height": 1.2, "fillColor": "#404040", "fontColor": "#FFFFFF", "fontSize": 11},
                    ...
                ]
        
        Returns:
            {
                "success": true,
                "count": 2,
                "objects": [...] (JSON形式)
            }
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/batch-add",
                json={"objects": objects},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def capture_screenshot(self, save_path: Optional[str] = None) -> Dict:
        """Canvas のスクリーンショットを取得
        
        注意：JavaScriptで canvas.toDataURL() を呼び出してからこの API を使う構成になっているため、
        実際にはクライアント側（JavaScript）で canvas.toDataURL('image/png') を実行し、
        その結果をこのメソッドに渡す必要があります。
        
        代わりに、Selenium や Puppeteer を使ってヘッドレスブラウザからスクリーンショットを取得することもできます。
        
        Args:
            save_path: ローカルに保存する場合のファイルパス
        
        Returns:
            {
                "success": true,
                "data": "iVBORw0KGgo...",
                "filename": "canvas_20260218_123456_000000.png",
                "timestamp": "2026-02-18T12:34:56"
            }
        """
        # このメソッドは JavaScript 側で canvas.toDataURL() を呼び出す必要があります
        # 以下は JavaScriptで実装するなし、ここでは呼び出し方法を示します
        return {
            "success": False,
            "error": "Use JavaScript to capture: canvas.toDataURL('image/png')"
        }
    
    def export_layout(self, title: str = "AI + 人間協働：3層フロー", subtitle: str = "") -> Dict:
        """現在のレイアウトを JSON 形式で出力
        
        注意：このメソッドは GUI 側の状態を JSON に変換します。
        実際の呼び出しは JavaScript 側で /api/export-json エンドポイントをコールします。
        
        Args:
            title: スライドタイトル
            subtitle: スライトサブタイトル
        
        Returns:
            {
                "success": true,
                "json": {...},
                "jsonString": "JSON文字列"
            }
        """
        # このメソッドは GUI の objects 配列が必要なため、
        # 実際には JavaScript 側で export-json エンドポイントをコールします
        return {
            "success": False,
            "error": "Use /api/export-json endpoint with current GUI state"
        }
    
    def import_layout(self, json_string: str) -> Dict:
        """JSON 形式のレイアウトをインポート
        
        Args:
            json_string: スライド JSON 文字列
        
        Returns:
            {
                "success": true,
                "title": "...",
                "subtitle": "...",
                "objects": [...]
            }
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/load-json",
                json={"jsonString": json_string},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def create_slide_layout(self, objects: List[Dict], title: str = "", subtitle: str = "") -> Dict:
        """スライドレイアウトを作成（オブジェクト追加 → JSON エクスポート）
        
        Args:
            objects: UI形式のオブジェクト配列
            title: スライドタイトル
            subtitle: スライトサブタイトル
        
        Returns:
            JSON 形式のスライドデータ
        """
        # 1. オブジェクトを追加
        add_result = self.batch_add_objects(objects)
        if not add_result.get('success'):
            return {"success": False, "error": f"Failed to add objects: {add_result.get('error')}"}
        
        # 2. JSON に変換
        json_objects = add_result.get('objects', [])
        
        slide_data = {
            "index": 1,
            "type": "content",
            "title": title,
            "subtitle": subtitle,
            "objects": json_objects
        }
        
        return {
            "success": True,
            "json": slide_data,
            "jsonString": json.dumps(slide_data, ensure_ascii=False, indent=2)
        }

def demo():
    """デモンストレーション"""
    print("=" * 70)
    print("🎨 Designer API Client Demo")
    print("=" * 70)
    
    client = DesignerAPIClient("http://localhost:5000")
    
    # サンプルレイアウト（Tier2実装設計スライド）
    sample_layout = [
        {
            "type": "box",
            "text": "Tier 1\n構成設計",
            "left": 0.5,
            "top": 1.8,
            "width": 1.0,
            "height": 1.2,
            "fillColor": "#404040",
            "fontColor": "#FFFFFF",
            "fontSize": 11
        },
        {
            "type": "box",
            "text": "outline_guide\n指定",
            "left": 1.7,
            "top": 1.8,
            "width": 1.4,
            "height": 0.8,
            "fillColor": "#4472C4",
            "fontColor": "#FFFFFF",
            "fontSize": 11
        },
        {
            "type": "arrow",
            "left": 3.3,
            "top": 2.05,
            "width": 0.5,
            "height": 0.3,
            "fillColor": "#ED7D31"
        }
    ]
    
    print("\n📍 Adding 3 objects...")
    result = client.batch_add_objects(sample_layout)
    
    if result.get('success'):
        print(f"✓ Added {result.get('count')} objects")
        print(f"  JSON objects:")
        for i, obj in enumerate(result.get('objects', [])):
            print(f"    [{i}] {obj.get('type')}: {obj.get('text', '...')[:20]}")
    else:
        print(f"✗ Error: {result.get('error')}")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    demo()
