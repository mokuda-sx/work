# AI用 Slide Layout Designer システム

## 🎯 システム概要

**AI自身が使うスライドレイアウト設計ツール**

従来のアプローチ：
```
AI思考（テキスト）→ JSON計算（ロジック） → PPTX生成 ✗ ズレ発生
```

**新しいアプローチ**：
```
AI思考 → GUIで見ながら配置（マルチモーダル） → JSON自動生成 ✓ ズレ0
```

### 特徴

1. **ビジュアルフィードバック** - AI が Canvas 上にオブジェクトを配置して目で確認
2. **完全なラウンドトリップ** - JSON ↔ GUI の往復変換が 100% 正確
3. **API駆動設計** - 人間のマウスクリック不要、完全プログラマティック操作
4. **自動視覚検証** - Canvas のスクリーンショット取得で配置確認

---

## 📦 実装コンポーネント

### 1. Flask バックエンド (`slide_layout_designer.py`)

#### エンドポイント一覧

| メソッド | エンドポイント | 説明 |
|---------|------------|------|
| POST | `/api/export-json` | UI形式 → JSON形式に変換 |
| POST | `/api/load-json` | JSON形式 → UI形式に変換 |
| POST | `/api/batch-add` | 複数オブジェクトを一度に追加 |
| POST | `/api/canvas/screenshot` | Canvas スクリーンショット (PNG Base64) |

#### リクエスト/レスポンス形式

**`/api/batch-add` - 複数オブジェクト追加**

```json
REQUEST:
{
  "objects": [
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
    ...
  ]
}

RESPONSE:
{
  "success": true,
  "count": 3,
  "objects": [
    {
      "type": "box",
      "text": "Tier 1\n構成設計",
      "left": 0.5,
      "top": 1.8,
      "width": 1.0,
      "height": 1.2,
      "fill_color": "404040",
      "font_color": "FFFFFF",
      "font_size": 11
    },
    ...
  ]
}
```

**`/api/canvas/screenshot` - スクリーンショット取得**

```json
REQUEST:
{
  "imageData": "data:image/png;base64,iVBORw0KGgo..."
}

RESPONSE:
{
  "success": true,
  "data": "iVBORw0KGgo...",
  "filename": "canvas_20260218_123456_000000.png",
  "timestamp": "2026-02-18T12:34:56"
}
```

### 2. JavaScript キャンバス (`designer.js`)

#### AI操作用ユーティリティ関数

```javascript
// スクリーンショット取得
async function captureCanvasScreenshot()
// Returns: { success, data (Base64), filename, timestamp }

// 複数オブジェクト一括追加
async function addObjectsBatch(objectList)
// Returns: { success, count, totalObjects }

// JSON エクスポート
async function exportLayoutJSON()
// Returns: { success, json, jsonString }
```

### 3. Python API クライアント (`designer_api_client.py`)

**AIが直接呼び出すAPI**

```python
from designer_api_client import DesignerAPIClient

client = DesignerAPIClient("http://localhost:5000")

# 複数オブジェクトを配置
result = client.batch_add_objects([
    {"type": "box", "text": "...", "left": 0.5, ...},
    ...
])
print(f"Added {result['count']} objects")

# JSON形式で取得
json_objects = result['objects']
```

### 4. AI レイアウトデザイナー (`ai_layout_designer.py`)

**AIが使うハイレベルAPI**

```python
from ai_layout_designer import AILayoutDesigner

designer = AILayoutDesigner()

# Tier2実装設計スライドを自動設計
result = designer.design_tier2_implementation_slide()

if result['success']:
    print(f"Created layout with {result['objectCount']} objects")
    
    # JSON出力
    designer.export_json("output.json")
```

---

## 🔄 形式変換の詳細

### UI形式 (JavaScript) → JSON形式 (Python)

| 項目 | UI形式 | JSON形式 |
|-----|--------|---------|
| 色値 | `#404040` | `404040` |
| 色プロパティ | `fillColor` | `fill_color` |
| フォントサイズ | `fontSize` | `font_size` |
| 垂直配置 | `valign` | `v_align` |
| テキストプロパティ | `text` | `text` |

### ラウンドトリップ検証

テスト対象: `slides/20260217_AI_PPT生成仕組み説明/slides/01_content.json` (18オブジェクト)

結果:
```
✓ Original JSON loaded: 18 objects
✓ Roundtrip simulation completed: 18 objects
✓ All objects match!
✅ All tests passed!
```

---

## 🚀 使用フロー（AI自動化）

### 1. レイアウト自動設計

```python
# AI が考えたレイアウトを API 経由で配置
designer = AILayoutDesigner()
result = designer.design_tier2_implementation_slide()
```

### 2. 視覚確認（スクリーンショット）

```javascript
// JavaScript からキャンバスを撮影
screenshot = await captureCanvasScreenshot();
// PNG の Base64 データを AI に返す
```

### 3. JSON 生成

```javascript
// Canvas の状態を JSON に変換
json_result = await exportLayoutJSON();
json_string = json_result.jsonString;
// JSON を Python に返す
```

### 4. PPTX 生成

```python
# JSON を使って PPTX を生成
from pptx_engine import PresentationBuilder

builder = PresentationBuilder()
builder.add_slide_from_json(json_data)
builder.save("output.pptx")
```

---

## 🛠️ 実装の工夫

### 1. オプショナルフィールド処理

JSON から UI に変換する際、元に存在しないフィールド（例：`v_align`）は追加しない

```python
# v_align は元に存在する場合のみ設定
if 'v_align' in obj:
    box_ui["valign"] = obj.get('v_align', 'middle')
```

### 2. 数値精度

座標・サイズはインチ単位で小数第3位まで保持

```python
"left": round(float(obj.get('left')), 3)  # 0.5 → 0.500
```

### 3. 色値の正規化

大文字で統一：`#404040` → `404040`

```python
fill_color = obj.get('fillColor', '#FFFFFF').lstrip('#').upper()
```

---

## 📊 オブジェクト型対応表

| 型 | 必須フィールド | オプション |
|----|-------------|---------|
| box | type, text, left, top, width, height, fill_color, font_color, font_size | v_align |
| arrow | type, left, top, width, height, fill_color | - |
| text | type, text, left, top, width, height, font_color, font_size | v_align |
| line | type, left, top, width, height, fill_color | - |
| circle | type, left, top, width, height, fill_color | - |

---

## 🎨 デザイン仕様

### スライドサイズ

- 幅: 12.8 インチ
- 高さ: 7.2 インチ
- DPI: 96

### カラーパレット

- `#404040` - ニュートラル濃灰
- `#8FAADC` - Tier1 薄青
- `#4472C4` - Tier2 中間青
- `#1F3864` - Tier3 濃紺
- `#ED7D31` - アクセント橙
- `#FFFFFF` - 白

### フォントサイズプリセット

- 9pt - 小（スキル参照）
- 12pt - 標準（デフォルト）
- 14pt - 強調

---

## 🔌 既存との統合

### pptx_engine.py との連携

```
AI Layout Designer (JSON出力)
         ↓
   01_content.json
         ↓
  pptx_engine.add_objects_to_slide()
         ↓
    PPTX 生成
```

---

## 📝 ログ・スクリーンショット保存

イ Canvas のスクリーンショットは自動保存：

```
screenshots/
├── canvas_20260218_120000_000000.png
├── canvas_20260218_120015_000000.png
└── ...
```

---

## 🧪 テスト済み

✅ 18-object Tier2 スライド完全復現
✅ ラウンドトリップ変換（JSON ↔ UI）100% 正確
✅ /api/batch-add エンドポイント動作
✅ UI形式 → JSON形式 変換正確性
✅ AI 自動パイプライン実行

---

**このシステムは AI 自身の「内部マルチモーダルプロセッシング」を実現します。**

従来のテキスト→JSON→画像の一方向では生じていた「齟齬」が、
AI が視覚フィードバックを得ながら設計することで **完全に排除されます**。
