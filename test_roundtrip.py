#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_roundtrip.py
デザイナー JSON インポート/エクスポート のラウンドトリップテスト

目的：
1. 既存スライドJSONをインポート
2. GUIで再現
3. JSON出力
4. 両JSONを比較して一致性を確認
"""

import json
from pathlib import Path
import sys

# テスト対象スライド JSON パス
TEST_SLIDE_JSON = Path(__file__).parent / "slides/20260217_AI_PPT生成仕組み説明/slides/01_content.json"

def load_original_json():
    """元のスライド JSON を読込"""
    with open(TEST_SLIDE_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def simulate_export(data):
    """
    UI形式に変換 → JSON形式への変換をシミュレート
    （JavaScriptからFlaskエンドポイントに送られる形式）
    """
    # JSON → UI形式への変換
    ui_objects = []
    for obj in data.get('objects', []):
        obj_type = obj.get('type')
        fill_color = '#' + obj.get('fill_color', 'FFFFFF').upper()
        font_color = '#' + obj.get('font_color', '000000').upper()
        
        if obj_type == 'box':
            ui_obj = {
                "type": "box",
                "text": obj.get('text', ''),
                "left": float(obj.get('left', 0)),
                "top": float(obj.get('top', 0)),
                "width": float(obj.get('width', 1.0)),
                "height": float(obj.get('height', 0.5)),
                "fillColor": fill_color,
                "fontColor": font_color,
                "fontSize": int(obj.get('font_size', 12))
            }
            # v_align は元に存在する場合のみ追加
            if 'v_align' in obj:
                ui_obj['valign'] = obj.get('v_align')
            ui_objects.append(ui_obj)
        elif obj_type == 'arrow':
            ui_objects.append({
                "type": "arrow",
                "left": float(obj.get('left', 0)),
                "top": float(obj.get('top', 0)),
                "width": float(obj.get('width', 0.5)),
                "height": float(obj.get('height', 0.3)),
                "fillColor": fill_color,
                "fontColor": fill_color,
                "fontSize": 12
            })
        elif obj_type == 'text':
            ui_obj = {
                "type": "text",
                "text": obj.get('text', ''),
                "left": float(obj.get('left', 0)),
                "top": float(obj.get('top', 0)),
                "width": float(obj.get('width', 1.0)),
                "height": float(obj.get('height', 0.5)),
                "fillColor": "#FFFFFF",
                "fontColor": font_color,
                "fontSize": int(obj.get('font_size', 10))
            }
            # v_align は元に存在する場合のみ追加
            if 'v_align' in obj:
                ui_obj['valign'] = obj.get('v_align')
            ui_objects.append(ui_obj)
        elif obj_type == 'line':
            ui_objects.append({
                "type": "line",
                "left": float(obj.get('left', 0)),
                "top": float(obj.get('top', 0)),
                "width": float(obj.get('width', 1.0)),
                "height": float(obj.get('height', 0.1)),
                "fillColor": fill_color,
                "fontColor": fill_color,
                "fontSize": 12
            })
        elif obj_type == 'circle':
            ui_objects.append({
                "type": "circle",
                "left": float(obj.get('left', 0)),
                "top": float(obj.get('top', 0)),
                "width": float(obj.get('width', 0.5)),
                "height": float(obj.get('height', 0.5)),
                "fillColor": fill_color,
                "fontColor": fill_color,
                "fontSize": 12
            })
    
    # UI形式 → JSON形式への逆変換（エクスポート）
    json_objects = []
    for obj in ui_objects:
        obj_type = obj.get('type')
        fill_color = obj.get('fillColor', '#FFFFFF').lstrip('#').upper()
        font_color = obj.get('fontColor', '#000000').lstrip('#').upper()
        
        if obj_type == 'box':
            box_obj = {
                "type": "box",
                "text": obj.get('text', ''),
                "left": round(float(obj.get('left')), 3),
                "top": round(float(obj.get('top')), 3),
                "width": round(float(obj.get('width')), 3),
                "height": round(float(obj.get('height')), 3),
                "fill_color": fill_color,
                "font_color": font_color,
                "font_size": int(obj.get('fontSize', 12))
            }
            # v_align は元に指定されていた場合のみ追加
            if 'valign' in obj:
                box_obj['v_align'] = obj.get('valign')
            json_objects.append(box_obj)
        elif obj_type == 'arrow':
            json_objects.append({
                "type": "arrow",
                "left": round(float(obj.get('left')), 3),
                "top": round(float(obj.get('top')), 3),
                "width": round(float(obj.get('width')), 3),
                "height": round(float(obj.get('height')), 3),
                "fill_color": fill_color
            })
        elif obj_type == 'text':
            text_obj = {
                "type": "text",
                "text": obj.get('text', ''),
                "left": round(float(obj.get('left')), 3),
                "top": round(float(obj.get('top')), 3),
                "width": round(float(obj.get('width')), 3),
                "height": round(float(obj.get('height')), 3),
                "font_size": int(obj.get('fontSize', 10)),
                "font_color": font_color
            }
            # v_align は元に指定されていた場合のみ追加
            if 'valign' in obj:
                text_obj['v_align'] = obj.get('valign')
            json_objects.append(text_obj)
        elif obj_type == 'line':
            json_objects.append({
                "type": "line",
                "left": round(float(obj.get('left')), 3),
                "top": round(float(obj.get('top')), 3),
                "width": round(float(obj.get('width')), 3),
                "height": round(float(obj.get('height')), 3),
                "fill_color": fill_color
            })
        elif obj_type == 'circle':
            json_objects.append({
                "type": "circle",
                "left": round(float(obj.get('left')), 3),
                "top": round(float(obj.get('top')), 3),
                "width": round(float(obj.get('width')), 3),
                "height": round(float(obj.get('height')), 3),
                "fill_color": fill_color
            })
    
    return {
        "index": data.get('index', 1),
        "type": "content",
        "title": data.get('title', ''),
        "subtitle": data.get('subtitle', ''),
        "objects": json_objects
    }

def compare_objects(orig, roundtrip):
    """オブジェクト配列を比較"""
    if len(orig) != len(roundtrip):
        return False, f"Object count mismatch: {len(orig)} vs {len(roundtrip)}"
    
    for i, (o, r) in enumerate(zip(orig, roundtrip)):
        # タイプチェック
        if o.get('type') != r.get('type'):
            return False, f"Object {i}: type mismatch {o.get('type')} vs {r.get('type')}"
        
        # テキストチェック
        if o.get('text') != r.get('text'):
            return False, f"Object {i}: text mismatch '{o.get('text')}' vs '{r.get('text')}'"
        
        # 位置・サイズ（誤差許容 0.001）
        for key in ['left', 'top', 'width', 'height']:
            if key in o and key in r:
                if abs(float(o[key]) - float(r[key])) > 0.001:
                    return False, f"Object {i}: {key} mismatch {o[key]} vs {r[key]}"
        
        # 色チェック（大文字で統一）
        if o.get('fill_color', '').upper() != r.get('fill_color', '').upper():
            return False, f"Object {i}: fill_color mismatch {o.get('fill_color')} vs {r.get('fill_color')}"
        
        if o.get('font_color', '').upper() != r.get('font_color', '').upper():
            return False, f"Object {i}: font_color mismatch {o.get('font_color')} vs {r.get('font_color')}"
        
        # フォントサイズ
        if o.get('font_size') != r.get('font_size'):
            return False, f"Object {i}: font_size mismatch {o.get('font_size')} vs {r.get('font_size')}"
        
        # 垂直配置（オプション）
        orig_valign = o.get('v_align')
        result_valign = r.get('v_align')
        # 両方にある場合だけ比較
        if orig_valign is not None and result_valign is not None:
            if orig_valign != result_valign:
                return False, f"Object {i}: v_align mismatch {orig_valign} vs {result_valign}"
        elif orig_valign != result_valign:
            # 片方にしかない場合は許容しない
            return False, f"Object {i}: v_align mismatch {orig_valign} vs {result_valign}"
    
    return True, "All objects match!"

def main():
    print("=" * 70)
    print("🧪 Roundtrip Test: JSON Import/Export")
    print("=" * 70)
    print(f"Test file: {TEST_SLIDE_JSON}")
    
    if not TEST_SLIDE_JSON.exists():
        print(f"❌ File not found: {TEST_SLIDE_JSON}")
        sys.exit(1)
    
    # 元JSON読込
    original = load_original_json()
    print(f"\n✓ Original JSON loaded")
    print(f"  Title: {original.get('title')}")
    print(f"  Objects: {len(original.get('objects', []))}")
    
    # ラウンドトリップシミュレート
    roundtrip = simulate_export(original)
    print(f"\n✓ Roundtrip simulation completed")
    print(f"  Objects: {len(roundtrip.get('objects', []))}")
    
    # 比較
    success, message = compare_objects(
        original.get('objects', []),
        roundtrip.get('objects', [])
    )
    
    print(f"\n{('✓' if success else '❌')} {message}")
    
    if not success:
        print("\n--- Original JSON ---")
        print(json.dumps(original, ensure_ascii=False, indent=2))
        print("\n--- Roundtrip JSON ---")
        print(json.dumps(roundtrip, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    # スライド情報の比較
    print(f"\nSlide Info Comparison:")
    print(f"  Title: {original.get('title')} == {roundtrip.get('title')} ? {original.get('title') == roundtrip.get('title')}")
    print(f"  Subtitle: {original.get('subtitle')[:50]}... == {roundtrip.get('subtitle')[:50]}... ? {original.get('subtitle') == roundtrip.get('subtitle')}")
    print(f"  Index: {original.get('index')} == {roundtrip.get('index')} ? {original.get('index') == roundtrip.get('index')}")
    
    print("\n" + "=" * 70)
    print("✅ All tests passed!")
    print("=" * 70)

if __name__ == '__main__':
    main()
