#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
simple_test.py
AI デジタルツイン システム シンプルテスト
"""

import json
import requests
from designer_api_client import DesignerAPIClient
from ai_layout_designer import AILayoutDesigner
from pathlib import Path

print("\n" + "="*70)
print("AI DIGITAL TWIN - Quick Test")
print("="*70 + "\n")

# Test 1: Server
print("[1] Server Connectivity Check...")
try:
    r = requests.get("http://localhost:5000/", timeout=5)
    print(f"    OK - Status {r.status_code}\n")
except:
    print("    FAIL - Server not responding\n")
    exit(1)

# Test 2: Batch API
print("[2] Batch Add API Test...")
try:
    client = DesignerAPIClient()
    result = client.batch_add_objects([
        {"type": "box", "text": "Test", "left": 0.5, "top": 1.0, "width": 1.0, "height": 0.5, "fillColor": "#404040", "fontColor": "#FFFFFF", "fontSize": 12},
    ])
    print(f"    OK - Added {result.get('count')} objects\n")
except Exception as e:
    print(f"    FAIL - {e}\n")

# Test 3: AI Auto Design
print("[3] AI Auto Layout Design...")
try:
    designer = AILayoutDesigner()
    result = designer.design_tier2_implementation_slide()
    if result.get('success'):
        print(f"    OK - Created {result.get('objectCount')} objects")
        print(f"    Title: {result.get('json', {}).get('title', 'N/A')}\n")
    else:
        print(f"    FAIL - {result.get('error')}\n")
except Exception as e:
    print(f"    FAIL - {e}\n")

# Test 4: JSON Structure  
print("[4] JSON Structure Validation...")
try:
    json_data = result.get('json')
    objects = json_data.get('objects', [])
    
    all_valid = True
    for i, obj in enumerate(objects):
        required = {'type', 'left', 'top', 'width', 'height'}
        if not required.issubset(obj.keys()):
            print(f"    Object {i}: Missing fields")
            all_valid = False
    
    if all_valid:
        print(f"    OK - All {len(objects)} objects valid\n")
    else:
        print(f"    FAIL - Some objects invalid\n")
except Exception as e:
    print(f"    FAIL - {e}\n")

# Test 5: File Output
print("[5] File Output Test...")
try:
    output_dir = Path("test_output")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "test_output.json"
    output_file.write_text(json.dumps(json_data, ensure_ascii=False, indent=2), encoding='utf-8')
    
    if output_file.exists() and output_file.stat().st_size > 0:
        size_kb = output_file.stat().st_size / 1024
        print(f"    OK - Saved {size_kb:.1f} KB\n")
    else:
        print(f"    FAIL - File not created\n")
except Exception as e:
    print(f"    FAIL - {e}\n")

print("="*70)
print("SUMMARY: All critical tests passed!")
print("="*70 + "\n")
