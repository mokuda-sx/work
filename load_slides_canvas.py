#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2つのスライドを Canvas にロードしてスクリーンショット取得
"""

import json
import time
from pathlib import Path
from designer_api_client import DesignerAPIClient

def main():
    print("\n" + "="*70)
    print("CANVAS スライド ロード試験")
    print("="*70)
    
    client = DesignerAPIClient()
    
    # Tier1 JSON をロード
    print("\n[1] Tier1 をロード...")
    tier1_path = Path("test_output") / "slide_tier1.json"
    with open(tier1_path, "r", encoding="utf-8") as f:
        tier1_data = json.load(f)
    
    result = client.import_layout(json.dumps(tier1_data, ensure_ascii=False))
    print(f"    ✅ Tier1: {len(tier1_data['objects'])} オブジェクト")
    print(f"       タイトル: {tier1_data['title']}")
    
    time.sleep(1)
    
    # スクリーンショット取得
    print("\n[2] Tier1 スクリーンショット取得...")
    screenshot_path = client.capture_screenshot()
    if screenshot_path:
        print(f"    ✅ Saved: {screenshot_path}")
    
    time.sleep(2)
    
    # Tier2 JSON をロード
    print("\n[3] Tier2 をロード...")
    tier2_path = Path("test_output") / "slide_tier2.json"
    with open(tier2_path, "r", encoding="utf-8") as f:
        tier2_data = json.load(f)
    
    result = client.import_layout(json.dumps(tier2_data, ensure_ascii=False))
    print(f"    ✅ Tier2: {len(tier2_data['objects'])} オブジェクト")
    print(f"       タイトル: {tier2_data['title']}")
    
    time.sleep(1)
    
    # スクリーンショット取得
    print("\n[4] Tier2 スクリーンショット取得...")
    screenshot_path = client.capture_screenshot()
    if screenshot_path:
        print(f"    ✅ Saved: {screenshot_path}")
    
    # 統計
    print("\n" + "="*70)
    print("✅ ロード完了")
    print("="*70)
    print(f"\n📊 統計:")
    print(f"  Tier1: {len(tier1_data['objects'])} オブジェクト")
    print(f"  Tier2: {len(tier2_data['objects'])} オブジェクト")
    print(f"  合計: {len(tier1_data['objects']) + len(tier2_data['objects'])} オブジェクト")
    print(f"\n📸 スクリーンショット:")
    print(f"   フォルダ: {Path.cwd()} / screenshots/")

if __name__ == "__main__":
    main()
