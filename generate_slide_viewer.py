#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
スライド自動ロード & スクリーンショット取得ツール
HTMLファイルを作成して、ブラウザで確認可能にする
"""

import json
from pathlib import Path

# Tier1, Tier2 JSON をロード
tier1_path = Path("test_output") / "slide_tier1.json"
tier2_path = Path("test_output") / "slide_tier2.json"

with open(tier1_path, "r", encoding="utf-8") as f:
    tier1_data = json.load(f)

with open(tier2_path, "r", encoding="utf-8") as f:
    tier2_data = json.load(f)

# HTML テンプレート生成
html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI生成スライド - ビジュアル確認</title>
    <style>
        {{
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    min-height: 100vh; padding: 40px 20px; }}
            
            .container {{ max-width: 1300px; margin: 0 auto; }}
            
            h1 {{ color: white; text-align: center; margin-bottom: 30px; font-size: 32px; }}
            
            .slide-viewer {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                perspective: 1000px;
            }}
            
            .slide-card {{
                background: white;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }}
            
            .slide-card:hover {{
                transform: translateY(-10px);
                box-shadow: 0 30px 90px rgba(0,0,0,0.4);
            }}
            
            .slide-header {{
                background: linear-gradient(135deg, #4472C4 0%, #2f5aa0 100%);
                color: white;
                padding: 20px;
            }}
            
            .slide-header h2 {{
                margin: 0 0 10px 0;
                font-size: 18px;
            }}
            
            .slide-header p {{
                margin: 5px 0;
                font-size: 13px;
                opacity: 0.9;
            }}
            
            .slide-canvas {{
                aspect-ratio: 16/9;
                background: #f9f9f9;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
                position: relative;
                height: 500px;
            }}
            
            canvas {{
                max-width: 100%;
                max-height: 100%;
                box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
                background: white;
            }}
            
            .slide-controls {{
                padding: 20px;
                background: #f5f5f5;
                border-top: 1px solid #eee;
                display: flex;
                gap: 10px;
            }}
            
            button {{
                flex: 1;
                padding: 10px 15px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-weight: 600;
                font-size: 14px;
                transition: all 0.2s;
            }}
            
            .btn-load {{
                background: #4472C4;
                color: white;
            }}
            
            .btn-load:hover {{
                background: #2f5aa0;
                transform: scale(1.02);
            }}
            
            .btn-load:active {{
                transform: scale(0.98);
            }}
            
            .slide-info {{
                padding: 20px;
                background: #e3f2fd;
                border-left: 4px solid #4472C4;
                font-size: 12px;
                color: #1565c0;
            }}
            
            .info-row {{
                display: flex;
                justify-content: space-between;
                margin: 8px 0;
            }}
            
            .status-bar {{
                background: white;
                padding: 20px;
                border-radius: 8px;
                margin-top: 30px;
                text-align: center;
            }}
            
            .status-msg {{
                color: #4472C4;
                font-weight: 600;
            }}
            
            .grid-lines {{
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-image: 
                    linear-gradient(0deg, transparent 24%, rgba(255,0,0,.05) 25%, rgba(255,0,0,.05) 26%, transparent 27%, transparent 74%, rgba(255,0,0,.05) 75%, rgba(255,0,0,.05) 76%, transparent 77%, transparent),
                    linear-gradient(90deg, transparent 24%, rgba(255,0,0,.05) 25%, rgba(255,0,0,.05) 26%, transparent 27%, transparent 74%, rgba(255,0,0,.05) 75%, rgba(255,0,0,.05) 76%, transparent 77%, transparent);
                background-size: 50px 50px;
                pointer-events: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 AI生成スライド - ビジュアル確認</h1>
        
        <div class="slide-viewer">
            <!-- Slide 1: Tier1 -->
            <div class="slide-card">
                <div class="slide-header">
                    <h2>📄 Slide 1: Tier1</h2>
                    <p>AIコンテキスト制約への対応：スキル化戦略</p>
                </div>
                
                <div class="slide-canvas" id="canvas-tier1-container">
                    <div class="grid-lines"></div>
                    <canvas id="canvasTier1" width="1280" height="720" style="border: 1px solid #ddd;"></canvas>
                </div>
                
                <div class="slide-info">
                    <strong>📊 構成情報</strong>
                    <div class="info-row">
                        <span>オブジェクト数:</span>
                        <strong>{len(tier1_data['objects'])}個</strong>
                    </div>
                    <div class="info-row">
                        <span>タイプ:</span>
                        <strong>コンテンツスライド</strong>
                    </div>
                    <div class="info-row">
                        <span>ファイルサイズ:</span>
                        <strong>1.3 KB</strong>
                    </div>
                </div>
                
                <div class="slide-controls">
                    <button class="btn-load" onclick="renderTier1()">📥 レンダリング</button>
                </div>
            </div>
            
            <!-- Slide 2: Tier2 -->
            <div class="slide-card">
                <div class="slide-header">
                    <h2>📄 Slide 2: Tier2</h2>
                    <p>AI + 人間協働：3層フロー</p>
                </div>
                
                <div class="slide-canvas" id="canvas-tier2-container">
                    <div class="grid-lines"></div>
                    <canvas id="canvasTier2" width="1280" height="720" style="border: 1px solid #ddd;"></canvas>
                </div>
                
                <div class="slide-info">
                    <strong>📊 構成情報</strong>
                    <div class="info-row">
                        <span>オブジェクト数:</span>
                        <strong>{len(tier2_data['objects'])}個</strong>
                    </div>
                    <div class="info-row">
                        <span>タイプ:</span>
                        <strong>3層フロー図解</strong>
                    </div>
                    <div class="info-row">
                        <span>ファイルサイズ:</span>
                        <strong>4.3 KB</strong>
                    </div>
                </div>
                
                <div class="slide-controls">
                    <button class="btn-load" onclick="renderTier2()">📥 レンダリング</button>
                </div>
            </div>
        </div>
        
        <div class="status-bar">
            <p class="status-msg">✅ AI により2枚のスライドが自動設計されました</p>
            <p style="margin-top: 10px; color: #666;">各スライドの「📥 レンダリング」ボタンをクリックすると、Canvas に配置が表示されます</p>
        </div>
    </div>
    
    <script>
        // Tier1 データ
        const TIER1_JSON = {json.dumps(tier1_data)};
        
        // Tier2 データ
        const TIER2_JSON = {json.dumps(tier2_data)};
        
        // Canvas レンダリング共通関数
        function drawSlide(canvas, slideData) {{
            const ctx = canvas.getContext('2d');
            
            // 背景クリア
            ctx.fillStyle = '#FFFFFF';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // DPI 調整 (Canvas: 96 DPI, PowerPoint: 96 DPI)
            const dpiScale = 96 / 72;
            const inchToPixel = dpiScale * 96; // 96 DPI で 1 inch = 96 pixels
            
            // オブジェクト描画
            slideData.objects.forEach(obj => {{
                const x = obj.left * inchToPixel;
                const y = obj.top * inchToPixel;
                const w = obj.width * inchToPixel;
                const h = obj.height * inchToPixel;
                
                if (obj.type === 'box' || (obj.type === 'arrow' && !obj.type.includes('-'))) {{
                    // 背景
                    if (obj.fill_color) {{
                        ctx.fillStyle = '#' + (obj.fill_color || 'FFFFFF');
                        ctx.fillRect(x, y, w, h);
                    }}
                    
                    // テキスト
                    if (obj.text) {{
                        const fontSize = obj.font_size || 12;
                        ctx.fillStyle = '#' + (obj.font_color || '000000');
                        ctx.font = fontSize + 'px Arial';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        
                        const lines = obj.text.split('\\n');
                        const lineHeight = fontSize * 1.2;
                        const startY = y + (h - (lines.length - 1) * lineHeight) / 2;
                        
                        lines.forEach((line, i) => {{
                            ctx.fillText(line, x + w / 2, startY + i * lineHeight);
                        }});
                    }}
                }}
            }});
        }}
        
        function renderTier1() {{
            const canvas = document.getElementById('canvasTier1');
            console.log('Rendering Tier1...');
            drawSlide(canvas, TIER1_JSON);
            alert('✅ Tier1 スライドがレンダリングされました');
        }}
        
        function renderTier2() {{
            const canvas = document.getElementById('canvasTier2');
            console.log('Rendering Tier2...');
            drawSlide(canvas, TIER2_JSON);
            alert('✅ Tier2 スライドがレンダリングされました');
        }}
        
        // ページロード時に自動レンダリング
        window.addEventListener('load', () => {{
            renderTier1();
            renderTier2();
        }});
    </script>
</body>
</html>
"""

# ファイルに保存
output_path = Path("test_output") / "slide_viewer_visual.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"\n{'='*70}")
print("✅ スライドビューアーHTMLを生成しました")
print(f"{'='*70}")
print(f"\n📍 file:\n   {output_path}")
print(f"\n📊 内容:")
print(f"   - Tier1: {len(tier1_data['objects'])} オブジェクト")
print(f"   - Tier2: {len(tier2_data['objects'])} オブジェクト")
print(f"   - サイズ: Canvas 12.8\" × 7.2\" (1280×720 pixels)")
print(f"\n🌐 使用方法:")
print(f"   1. VS Code で {output_path} をプレビュー")
print(f"   または")
print(f"   2. ブラウザで直接開く")
print(f"\n{'='*70}")
