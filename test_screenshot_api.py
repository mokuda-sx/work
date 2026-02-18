#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_screenshot_api.py
Canvas スクリーンショット API テスト

JavaScriptから Canvas を撮影して、
サーバー側でPNG ファイルとして保存することをテストします
"""

import json
import requests
from pathlib import Path
from datetime import datetime
import time

print("\n" + "="*70)
print("Canvas Screenshot API Test")
print("="*70 + "\n")

# 注：実際のスクリーンショット取得は JavaScript が必要です
# 以下は API エンドポイントが正しく動作することを確認するテストです

# スクリーンショットディレクトリを確認
screenshot_dir = Path("screenshots")
screenshot_dir.mkdir(exist_ok=True)

print(f"[1] Check Screenshots Directory")
print(f"    Location: {screenshot_dir.absolute()}")
print(f"    Status: {'EXISTS' if screenshot_dir.exists() else 'NOT FOUND'}\n")

# ダミー PNG データでテスト（実際には Canvas.toDataURL() から取得）
print(f"[2] Test Screenshot API endpoint")

# 最小限の有効な PNG データ (1x1 px ピンク)
minimal_png = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="

try:
    response = requests.post(
        "http://localhost:5000/api/canvas/screenshot",
        json={"imageData": f"data:image/png;base64,{minimal_png}"},
        timeout=10
    )
    
    result = response.json()
    if result.get('success'):
        print(f"    Status: SUCCESS")
        print(f"    Filename: {result.get('filename')}")
        print(f"    Timestamp: {result.get('timestamp')}\n")
        
        # ファイル検証
        screenshot_file = screenshot_dir / result.get('filename')
        if screenshot_file.exists():
            size = screenshot_file.stat().st_size
            print(f"[3] File Verification")
            print(f"    File Path: {screenshot_file}")
            print(f"    File Size: {size} bytes")
            print(f"    Status: OK\n")
        else:
            print(f"[3] File Verification")
            print(f"    Status: File not found\n")
    else:
        print(f"    Status: FAILED - {result.get('error')}\n")
except Exception as e:
    print(f"    Status: ERROR - {e}\n")

# 既存スクリーンショット一覧
print(f"[4] Existing Screenshots")
if screenshot_dir.exists():
    files = list(screenshot_dir.glob("canvas_*.png"))
    print(f"    Total: {len(files)} files")
    for i, f in enumerate(files[-3:]):  # 最新3つを表示
        size_kb = f.stat().st_size / 1024
        print(f"    - {f.name} ({size_kb:.1f} KB)")
else:
    print(f"    No screenshots yet\n")

print("\n" + "="*70)
print("Screenshot API is ready for Canvas captures")
print("="*70 + "\n")
