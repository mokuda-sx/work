#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Layout Verification Tool
AI側でレイアウト JSON が適切に生成されたかチェックする

使用方法:
    python ai_verify_layout.py <json_file>

動作:
    1. JSON ファイルを読み込む
    2. Flask Canvas API に JSON を送信（自動配置）
    3. Canvas のスクリーンショットを手動で取得（またはブラウザ自動操作）
    4. レイアウト検証結果をレポート出力
"""

import json
import requests
import sys
import webbrowser
from pathlib import Path
from datetime import datetime
import time

def verify_layout(json_path: str, canvas_url: str = "http://localhost:5000", auto_screenshot: bool = False) -> dict:
    """
    レイアウト JSON を Canvas に配置してスクリーンショット取得
    
    Args:
        json_path: 検証する JSON ファイルパス
        canvas_url: Flask Canvas URL
        auto_screenshot: 自動でスクリーンショット取得（Selenium 別途インストール必要）
    
    Returns:
        検証結果 dict
    """
    print("\n" + "="*70)
    print("🔍 AI Layout Verification Tool")
    print("="*70)
    
    # 1. JSON 読み込み
    json_file = Path(json_path)
    if not json_file.exists():
        print(f"\n❌ エラー: ファイルが見つかりません: {json_file}")
        return {"success": False, "error": "File not found"}
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            slide_data = json.load(f)
    except Exception as e:
        print(f"\n❌ JSON 読み込みエラー: {e}")
        return {"success": False, "error": str(e)}
    
    print(f"\n📄 JSON ファイル読み込み完了")
    print(f"   ファイル: {json_file.name}")
    print(f"   タイトル: {slide_data.get('title', '(なし)')}")
    print(f"   オブジェクト数: {len(slide_data.get('objects', []))}")
    
    # 2. Canvas に配置（API から取得した objects を UI 形式に変換）
    print(f"\n📐 Canvas に配置中...")
    
    ui_objects = []
    for obj in slide_data.get('objects', []):
        ui_obj = {
            "type": obj.get('type'),
            "left": float(obj.get('left', 0)),
            "top": float(obj.get('top', 0)),
            "width": float(obj.get('width', 1)),
            "height": float(obj.get('height', 0.5)),
            "text": obj.get('text', ''),
            "fillColor": '#' + obj.get('fill_color', 'FFFFFF').upper(),
            "fontColor": '#' + obj.get('font_color', '000000').upper(),
            "fontSize": int(obj.get('font_size', 12))
        }
        
        # v_align が存在する場合のみ含める
        if 'v_align' in obj:
            ui_obj['valign'] = obj.get('v_align')
        
        ui_objects.append(ui_obj)
    
    try:
        response = requests.post(
            f"{canvas_url}/api/batch-add",
            json={"objects": ui_objects},
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"❌ API エラー: {response.status_code}")
            return {"success": False, "error": f"HTTP {response.status_code}"}
        
        api_result = response.json()
        if not api_result.get('success'):
            print(f"❌ Canvas エラー: {api_result.get('error')}")
            return {"success": False, "error": api_result.get('error')}
        
        print(f"   ✅ {len(ui_objects)} 個のオブジェクトを配置")
    
    except requests.exceptions.ConnectionError:
        print(f"❌ Canvas 接続エラー")
        print(f"   💡 Flask サーバーが起動していることを確認してください:")
        print(f"      python -m flask --app slide_layout_designer run --port 5000")
        return {"success": False, "error": "Connection failed"}
    
    except Exception as e:
        print(f"❌ Canvas エラー: {e}")
        return {"success": False, "error": str(e)}
    
    # 3. スクリーンショット取得
    print(f"\n📸 スクリーンショット取得...")
    
    screenshot_file = None
    
    if auto_screenshot:
        # Selenium を使った自動スクリーンショット取得（オプション）
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            
            driver = webdriver.Chrome()
            try:
                driver.get(canvas_url)
                time.sleep(2)  # Canvas レンダリング完了まで待機
                
                screenshot_dir = Path(__file__).parent / "layout_verification"
                screenshot_dir.mkdir(exist_ok=True)
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                screenshot_file = screenshot_dir / f"layout_verify_{timestamp}.png"
                
                driver.get_screenshot_as_file(str(screenshot_file))
                print(f"   ✅ スクリーンショット保存: {screenshot_file}")
            
            finally:
                driver.quit()
        
        except ImportError:
            print(f"   ⚠️  Selenium がインストールされていません")
            print(f"      pip install selenium")
            auto_screenshot = False
    
    if not auto_screenshot:
        # ブラウザを開いて手動スクリーンショット
        print(f"\n   📝 ブラウザでスクリーンショットを取得してください:")
        print(f"      1. Canvas ページが自動で開きます")
        print(f"      2. 左下の「📸 スクリーンショット」ボタンをクリック")
        print(f"      3. screenshots/ フォルダでキャプチャが保存されます")
        
        # ブラウザを開く
        webbrowser.open(canvas_url)
        print(f"\n   🌐 Canvas を開いています... {canvas_url}")
        
        screenshot_dir = Path(__file__).parent / "screenshots"
        screenshot_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_file = screenshot_dir / f"layout_verify_{timestamp}.png"
    
    result = {
        "success": True,
        "title": slide_data.get('title'),
        "objects_count": len(ui_objects),
        "screenshot": str(screenshot_file) if screenshot_file else "manual",
        "timestamp": datetime.now().isoformat(),
        "canvas_url": canvas_url
    }
    
    return result

def main():
    if len(sys.argv) < 2:
        print("\n使用方法:")
        print("  python ai_verify_layout.py <json_file> [--auto]")
        print("\n例:")
        print("  # ブラウザで手動スクリーンショット（推奨）")
        print("  python ai_verify_layout.py test_output/demo1_comparison.json")
        print("\n  # Selenium で自動スクリーンショット")
        print("  python ai_verify_layout.py test_output/demo1_comparison.json --auto")
        sys.exit(1)
    
    json_path = sys.argv[1]
    auto_screenshot = '--auto' in sys.argv
    
    result = verify_layout(json_path, auto_screenshot=auto_screenshot)
    
    print("\n" + "="*70)
    if result.get('success'):
        print("✅ レイアウト検証完了")
        print(f"   タイトル: {result.get('title')}")
        print(f"   オブジェクト数: {result.get('objects_count')}")
        if result.get('screenshot') != 'manual':
            print(f"   スクリーンショット: {result.get('screenshot')}")
        print(f"   タイムスタンプ: {result.get('timestamp')}")
        print(f"\n   次のステップ:")
        print(f"   1. Canvas で「📸 スクリーンショット」ボタンをクリック")
        print(f"   2. screenshots/ フォルダに画像が保存されます")
        print(f"   3. 画像を確認してレイアウトチェック")
    else:
        print("❌ レイアウト検証失敗")
        print(f"   エラー: {result.get('error')}")
    
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
