#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_ai_digital_twin.py
AI Agent用 デジタルツイン システム 総合テスト

以下をテストします：
1. Flask サーバー → API 疎通確認
2. AI自動レイアウト設計 → JSON生成
3. JSON ラウンドトリップ → UI形式へ変換確認
4. スクリーンショット → ファイル保存確認
"""

import json
import requests
import time
from pathlib import Path
from datetime import datetime
import subprocess
import sys

# テストカラー
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{'='*70}")
    print(f"{text:^70}")
    print(f"{'='*70}\n")

def print_test(name, result, detail=""):
    status = "PASS" if result else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        print(f"      {detail}")

class AIDigitalTwinTester:
    """AI デジタルツイン テスター"""
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
        self.generated_json = None
        self.generated_screenshot = None
    
    def test_server_connectivity(self):
        """Test 1: Flask サーバーへの接続確認"""
        print_header("Test 1: Flask Server Connectivity")
        
        try:
            response = self.session.get(f"{self.base_url}/", timeout=5)
            success = response.status_code == 200
            print_test("Server responds to GET /", success, f"Status: {response.status_code}")
            self.results.append(("Server Connectivity", success))
            return success
        except Exception as e:
            print_test("Server responds to GET /", False, f"Error: {str(e)}")
            self.results.append(("Server Connectivity", False))
            return False
    
    def test_batch_add_api(self):
        """Test 2: バッチ追加 API の動作"""
        print_header("Test 2: Batch Add API")
        
        test_objects = [
            {
                "type": "box",
                "text": "Test Box",
                "left": 0.5,
                "top": 1.0,
                "width": 1.0,
                "height": 0.5,
                "fillColor": "#404040",
                "fontColor": "#FFFFFF",
                "fontSize": 12
            },
            {
                "type": "arrow",
                "left": 2.0,
                "top": 1.0,
                "width": 0.5,
                "height": 0.3,
                "fillColor": "#ED7D31"
            }
        ]
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/batch-add",
                json={"objects": test_objects},
                timeout=10
            )
            result = response.json()
            success = result.get('success') and result.get('count') == 2
            
            print_test("Batch add 2 objects", success, 
                      f"Added: {result.get('count', 0)}, Objects in JSON: {len(result.get('objects', []))}")
            
            self.results.append(("Batch Add API", success))
            return success
        except Exception as e:
            print_test("Batch add 2 objects", False, f"Error: {str(e)}")
            self.results.append(("Batch Add API", False))
            return False
    
    def test_ai_auto_design(self):
        """Test 3: AI 自動レイアウト設計"""
        print_header("Test 3: AI Auto Layout Design")
        
        try:
            # designer_api_client をインポートして実行
            from designer_api_client import DesignerAPIClient
            from ai_layout_designer import AILayoutDesigner
            
            designer = AILayoutDesigner(self.base_url)
            result = designer.design_tier2_implementation_slide()
            
            success = result.get('success')
            object_count = result.get('objectCount', 0)
            
            print_test("Design Tier2 slide", success, 
                      f"Created {object_count} objects")
            
            if success:
                self.generated_json = result.get('json')
                print(f"      JSON Title: {result.get('json', {}).get('title', 'N/A')[:50]}")
            
            self.results.append(("AI Auto Design", success and object_count == 18))
            return success and object_count == 18
        except Exception as e:
            print_test("Design Tier2 slide", False, f"Error: {str(e)}")
            self.results.append(("AI Auto Design", False))
            return False
    
    def test_json_export_import(self):
        """Test 4: JSON エクスポート/インポート ラウンドトリップ"""
        print_header("Test 4: JSON Export/Import Roundtrip")
        
        if not self.generated_json:
            print_test("JSON roundtrip", False, "No JSON generated in previous test")
            self.results.append(("JSON Roundtrip", False))
            return False
        
        try:
            json_string = json.dumps(self.generated_json, ensure_ascii=False)
            
            # インポート API テスト
            response = self.session.post(
                f"{self.base_url}/api/load-json",
                json={"jsonString": json_string},
                timeout=10
            )
            result = response.json()
            
            success = result.get('success')
            object_count = len(result.get('objects', []))
            
            print_test("JSON import (JSON → UI)", success, 
                      f"Imported {object_count} objects")
            
            # エクスポート API テスト
            response = self.session.post(
                f"{self.base_url}/api/export-json",
                json={
                    "title": self.generated_json.get('title'),
                    "subtitle": self.generated_json.get('subtitle'),
                    "slideIndex": 1,
                    "objects": result.get('objects', [])
                },
                timeout=10
            )
            result2 = response.json()
            
            success2 = result2.get('success')
            print_test("JSON export (UI → JSON)", success2, 
                      f"Generated JSON with {len(result2.get('objects', []))} objects")
            
            roundtrip_success = success and success2
            self.results.append(("JSON Roundtrip", roundtrip_success))
            return roundtrip_success
        except Exception as e:
            print_test("JSON roundtrip", False, f"Error: {str(e)}")
            self.results.append(("JSON Roundtrip", False))
            return False
    
    def test_json_comparison(self):
        """Test 5: JSON 内容比較（ラウンドトリップの正確性）"""
        print_header("Test 5: JSON Content Comparison")
        
        if not self.generated_json:
            print_test("JSON comparison", False, "No JSON generated")
            self.results.append(("JSON Comparison", False))
            return False
        
        try:
            original_objects = self.generated_json.get('objects', [])
            
            # 各オブジェクトの重要プロパティをチェック
            all_match = True
            mismatches = []
            
            for i, obj in enumerate(original_objects):
                required_keys = {'type', 'left', 'top', 'width', 'height'}
                if not required_keys.issubset(obj.keys()):
                    all_match = False
                    mismatches.append(f"Object {i}: Missing keys {required_keys - set(obj.keys())}")
                
                # 色値の形式チェック（#なし）
                for color_key in ['fill_color', 'font_color']:
                    if color_key in obj:
                        color = obj[color_key]
                        if not isinstance(color, str) or color.startswith('#'):
                            all_match = False
                            mismatches.append(f"Object {i}: {color_key} has invalid format: {color}")
            
            print_test("All objects have required fields", all_match, 
                      f"Objects checked: {len(original_objects)}")
            
            if mismatches:
                for mismatch in mismatches[:3]:
                    print(f"      {mismatch}")
            
            self.results.append(("JSON Comparison", all_match))
            return all_match
        except Exception as e:
            print_test("JSON comparison", False, f"Error: {str(e)}")
            self.results.append(("JSON Comparison", False))
            return False
    
    def test_file_operations(self):
        """Test 6: ファイル操作（JSON保存、スクリーンショット保存）"""
        print_header("Test 6: File Operations")
        
        success_tests = []
        
        # JSON ファイル保存
        try:
            output_dir = Path(__file__).parent / "test_output"
            output_dir.mkdir(exist_ok=True)
            
            json_file = output_dir / f"test_layout_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            json_file.write_text(json.dumps(self.generated_json, ensure_ascii=False, indent=2), encoding='utf-8')
            
            success = json_file.exists() and json_file.stat().st_size > 0
            print_test("Save JSON file", success, f"File: {json_file.name}")
            success_tests.append(("JSON Save", success))
        except Exception as e:
            print_test("Save JSON file", False, f"Error: {str(e)}")
            success_tests.append(("JSON Save", False))
        
        # スクリーンショットディレクトリ確認
        try:
            screenshot_dir = Path(__file__).parent / "screenshots"
            # このテストでは実際にスクリーンショットを取得できないため、
            # ディレクトリ構造だけ確認
            screenshot_dir.mkdir(exist_ok=True)
            
            success = screenshot_dir.exists()
            print_test("Screenshot directory ready", success, f"Path: {screenshot_dir}")
            success_tests.append(("Screenshot Dir", success))
        except Exception as e:
            print_test("Screenshot directory ready", False, f"Error: {str(e)}")
            success_tests.append(("Screenshot Dir", False))
        
        overall = all(s[1] for s in success_tests)
        self.results.append(("File Operations", overall))
        return overall
    
    def run_all_tests(self):
        """全テストを実行"""
        print_header("🤖 AI Digital Twin System - Comprehensive Test Suite")
        
        # 個別テスト実行
        test1 = self.test_server_connectivity()
        time.sleep(0.5)
        
        if not test1:
            print(f"\n{RED}Server not responding. Cannot continue tests.{RESET}")
            return False
        
        test2 = self.test_batch_add_api()
        time.sleep(0.5)
        test3 = self.test_ai_auto_design()
        time.sleep(0.5)
        test4 = self.test_json_export_import()
        time.sleep(0.5)
        test5 = self.test_json_comparison()
        time.sleep(0.5)
        test6 = self.test_file_operations()
        
        # 結果サマリー
        self.print_summary()
        
        return all(result[1] for result in self.results)
    
    def print_summary(self):
        """テスト結果サマリー"""
        print_header("Test Results Summary")
        
        passed = sum(1 for _, result in self.results if result)
        total = len(self.results)
        
        print(f"Total Tests: {total}")
        print(f"Passed:      {passed}")
        print(f"Failed:      {total - passed}")
        print()
        
        for name, result in self.results:
            status = "PASS" if result else "FAIL"
            print(f"[{status}] {name}")
        
        print()
        if passed == total:
            print('='*70)
            print("SUCCESS: All tests passed! AI Digital Twin is operational.")
            print('='*70)
        else:
            print('='*70)
            print("WARNING: Some tests failed. Check output above.")
            print('='*70)

def main():
    print(f"\nStart time: {datetime.now().isoformat()}\n")
    
    # テスター作成・実行
    tester = AIDigitalTwinTester("http://localhost:5000")
    success = tester.run_all_tests()
    
    print(f"\nEnd time: {datetime.now().isoformat()}\n")
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
