"""
slide_layout_designer.py
PPTX スライドレイアウト設計用 GUI ツール

起動: python slide_layout_designer.py
ブラウザで http://localhost:5000 を開く

機能:
- HTML5 Canvas 上でオブジェクト（テキスト・矢印）を配置
- リアルタイムプレビュー
- 自動 JSON 生成（01_content.json 形式）
"""

from flask import Flask, render_template, jsonify, request
import json
from pathlib import Path
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# スライド設定（SX提案書 3.0テンプレート基準）
SLIDE_CONFIG = {
    "width": 12.8,      # インチ（content area）
    "height": 7.2,      # インチ（推定）
    "dpi": 96,          # スクリーン DPI
}

# 色パレット定義（design_guide.md より）
COLOR_PALETTE = {
    "404040": {"name": "Neutral Dark", "ja": "ニュートラル濃灰"},
    "8FAADC": {"name": "Tier1 Light", "ja": "Tier1 薄青"},
    "4472C4": {"name": "Tier2 Mid", "ja": "Tier2 中間青"},
    "1F3864": {"name": "Tier3 Dark", "ja": "Tier3 濃紺"},
    "ED7D31": {"name": "Accent Orange", "ja": "アクセント橙"},
    "FFFFFF": {"name": "White", "ja": "白"},
}

@app.route('/')
def designer():
    """メイン UI ページ"""
    return render_template('designer.html', 
                         slideConfig=SLIDE_CONFIG,
                         colorPalette=COLOR_PALETTE)

@app.route('/api/export-json', methods=['POST'])
def export_json():
    """JSON エクスポート (UI形式 → JSON形式)"""
    data = request.json
    
    objects = []
    
    # UI からのオブジェクト情報を JSON に変換
    for obj in data.get('objects', []):
        obj_type = obj.get('type')
        
        # 色値から # を削除
        fill_color = obj.get('fillColor', 'FFFFFF').lstrip('#').upper()
        font_color = obj.get('fontColor', '000000').lstrip('#').upper()
        
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
                "font_size": int(obj.get('fontSize', 12)),
                "h_align": obj.get('halign', 'center'),
                "v_align": obj.get('valign', 'middle')
            }
            objects.append(box_obj)
        elif obj_type == 'arrow' or obj_type.startswith('arrow-'):
            # 矢印オブジェクト（方向を保持）
            direction = obj_type.split('-')[1] if '-' in obj_type else 'right'
            objects.append({
                "type": "arrow",
                "direction": direction,
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
                "font_color": font_color,
                "h_align": obj.get('halign', 'left'),
                "v_align": obj.get('valign', 'top')
            }
            objects.append(text_obj)
        elif obj_type == 'line':
            objects.append({
                "type": "line",
                "left": round(float(obj.get('left')), 3),
                "top": round(float(obj.get('top')), 3),
                "width": round(float(obj.get('width')), 3),
                "height": round(float(obj.get('height')), 3),
                "fill_color": fill_color
            })
        elif obj_type == 'circle':
            objects.append({
                "type": "circle",
                "left": round(float(obj.get('left')), 3),
                "top": round(float(obj.get('top')), 3),
                "width": round(float(obj.get('width')), 3),
                "height": round(float(obj.get('height')), 3),
                "fill_color": fill_color
            })
    
    slide_data = {
        "index": data.get('slideIndex', 1),
        "type": "content",
        "title": data.get('title', ''),
        "subtitle": data.get('subtitle', ''),
        "objects": objects
    }
    
    return jsonify({
        "success": True,
        "json": slide_data,
        "jsonString": json.dumps(slide_data, ensure_ascii=False, indent=2)
    })

@app.route('/api/load-json', methods=['POST'])
def load_json():
    """JSON 読込 (JSON形式 → UI形式に変換)"""
    json_str = request.json.get('jsonString', '')
    try:
        data = json.loads(json_str)
        
        # JSON形式のオブジェクトをUI形式に変換
        ui_objects = []
        for obj in data.get('objects', []):
            obj_type = obj.get('type')
            
            # 色値に # を追加
            fill_color = '#' + obj.get('fill_color', 'FFFFFF').upper()
            font_color = '#' + obj.get('font_color', '000000').upper()
            
            if obj_type == 'box':
                box_ui = {
                    "type": "box",
                    "text": obj.get('text', ''),
                    "left": float(obj.get('left', 0)),
                    "top": float(obj.get('top', 0)),
                    "width": float(obj.get('width', 1.0)),
                    "height": float(obj.get('height', 0.5)),
                    "fillColor": fill_color,
                    "fontColor": font_color,
                    "fontSize": int(obj.get('font_size', 12)),
                    "halign": obj.get('h_align', 'center'),
                    "valign": obj.get('v_align', 'middle')
                }
                ui_objects.append(box_ui)
            elif obj_type == 'arrow':
                ui_objects.append({
                    "type": "arrow",
                    "left": float(obj.get('left', 0)),
                    "top": float(obj.get('top', 0)),
                    "width": float(obj.get('width', 0.5)),
                    "height": float(obj.get('height', 0.3)),
                    "fillColor": fill_color,
                    "fontColor": fill_color,
                    "fontSize": 12,
                    "valign": "middle"
                })
            elif obj_type == 'text':
                text_ui = {
                    "type": "text",
                    "text": obj.get('text', ''),
                    "left": float(obj.get('left', 0)),
                    "top": float(obj.get('top', 0)),
                    "width": float(obj.get('width', 1.0)),
                    "height": float(obj.get('height', 0.5)),
                    "fillColor": fill_color,
                    "fontColor": font_color,
                    "fontSize": int(obj.get('font_size', 10)),
                    "halign": obj.get('h_align', 'left'),
                    "valign": obj.get('v_align', 'top')
                }
                ui_objects.append(text_ui)
            elif obj_type == 'line':
                ui_objects.append({
                    "type": "line",
                    "left": float(obj.get('left', 0)),
                    "top": float(obj.get('top', 0)),
                    "width": float(obj.get('width', 1.0)),
                    "height": float(obj.get('height', 0.1)),
                    "fillColor": fill_color,
                    "fontColor": fill_color,
                    "fontSize": 12,
                    "valign": "middle"
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
                    "fontSize": 12,
                    "valign": "middle"
                })
        
        return jsonify({
            "success": True,
            "title": data.get('title', ''),
            "subtitle": data.get('subtitle', ''),
            "slideIndex": data.get('index', 1),
            "objects": ui_objects
        })
    except json.JSONDecodeError as e:
        return jsonify({"success": False, "error": str(e)})

# ==================== AI操作用API ====================

@app.route('/api/canvas/screenshot', methods=['POST'])
def canvas_screenshot():
    """Canvas スクリーンショット取得 (Base64 PNG)
    
    リクエスト:
    {
        "imageData": Canvas.toDataURL('image/png') から送信される Base64 データ
    }
    
    レスポンス:
    {
        "success": true,
        "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+P+/HgAFhAJ/wlseKgAAAABJRU5ErkJggg==",
        "filename": "canvas_20260218_123456_000000.png",
        "timestamp": "2026-02-18T12:34:56"
    }
    """
    try:
        data = request.json
        image_data = data.get('imageData', '')
        
        if not image_data:
            return jsonify({"success": False, "error": "imageData is required"}), 400
        
        # Base64 データから PNG を抽出（data:image/png;base64, プリフィックス削除）
        if image_data.startswith('data:'):
            image_data = image_data.split(',', 1)[1]
        
        # ファイル保存（スクリーンショット履歴）
        screenshot_dir = Path(__file__).parent / 'screenshots'
        screenshot_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        screenshot_path = screenshot_dir / f'canvas_{timestamp}.png'
        
        # Base64 → PNG 保存
        image_bytes = base64.b64decode(image_data)
        with open(screenshot_path, 'wb') as f:
            f.write(image_bytes)
        
        return jsonify({
            "success": True,
            "data": image_data,  # Base64 データそのまま返す
            "filename": f'canvas_{timestamp}.png',
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/batch-add', methods=['POST'])
def batch_add_objects():
    """複数オブジェクトを一度に追加（UI形式で受け取って JSON形式に変換）
    
    リクエスト:
    {
        "objects": [
            {"type": "box", "text": "...", "left": 0.5, "top": 1.8, ...},
            {"type": "arrow", "left": 3.3, "top": 2.05, ...},
            ...
        ]
    }
    
    レスポンス:
    {
        "success": true,
        "count": 3,
        "objects": [...] (JSON形式に変換したもの)
    }
    """
    try:
        data = request.json
        ui_objects = data.get('objects', [])
        
        if not ui_objects:
            return jsonify({"success": False, "error": "objects is required"}), 400
        
        # UI形式 → JSON形式に変換
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
                if 'valign' in obj:
                    box_obj["v_align"] = obj.get('valign')
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
        
        return jsonify({
            "success": True,
            "count": len(json_objects),
            "objects": json_objects
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/view')
def view_slides():
    """スライドビューアーページ（生成済みスライド表示）"""
    from pathlib import Path
    viewer_path = Path(__file__).parent / "test_output" / "slide_viewer_visual.html"
    
    if viewer_path.exists():
        with open(viewer_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return """
        <html>
        <head><meta charset="UTF-8"><title>Error</title></head>
        <body style="font-family: sans-serif; padding: 40px; background: #f5f5f5;">
            <h1 style="color: #d32f2f;">❌ エラー</h1>
            <p>slide_viewer_visual.html が見つかりません。</p>
            <p>generate_slide_viewer.py を実行してください。</p>
        </body>
        </html>
        """, 404

if __name__ == "__main__":
    print("=" * 60)
    print("Slide Layout Designer")
    print("=" * 60)
    print(f"Starting server at http://localhost:5000")
    print(f"Designer: http://localhost:5000")
    print(f"Viewer: http://localhost:5000/view")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    app.run(debug=False, port=5000)
