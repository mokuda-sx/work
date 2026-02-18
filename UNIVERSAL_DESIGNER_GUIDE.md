# Universal Slide Designer ツール

**目的**: AI が任意のスライドを設計する際に、Canvas で見ながら GUI レイアウトし、JSON を自動生成できる汎用ツール

**革新性**: テキストベース計算ではなく、ビジュアルフィードバック（Canvas）を得ながら設計

---

## 🎯 使用フロー

### Phase 1: AI がスライド内容を考える（テキスト思考）
```
AI: "このスライドは左右比較で表現したい"
     "左側: 従来方式（3項目）"
     "右側: 新方式（3項目）"
```

### Phase 2: Universal Slide Designer でレイアウト
```python
from universal_slide_designer import UniversalSlideDesigner

designer = UniversalSlideDesigner()

# パターン1: 既存テンプレートを使用
result = designer.design_horizontal_comparison(
    left_title="従来方式",
    left_items=["単一処理", "コンテキスト制約", "品質のばらつき"],
    right_title="新方式（Tier化）",
    right_items=["段階的処理", "コンテキスト最適化", "一貫した品質"],
    title="処理方式の比較"
)

# または

# パターン2: 完全カスタムレイアウト
objects = [
    {"type": "box", "text": "タイトル", "left": 0.5, "top": 0.5, ...},
    {"type": "arrow", "left": 2.0, "top": 1.5, ...},
    ...
]
result = designer.design(objects, title="My Custom Slide")
```

### Phase 3: Canvas でビジュアル確認
```
ブラウザで http://localhost:5000 を開く
↓
Canvas に設計されたレイアウトが表示される
↓
AI が見ながら必要に応じて調整（Canvas 上でドラッグ&ドロップ）
```

### Phase 4: JSON 生成
```python
# JSON を保存
designer.export_json(result, "my_slide.json")

# または Canvas にロード確認
designer.load_to_canvas(result)
```

### Phase 5: PPTX 生成
```python
from pptx_engine import PresentationBuilder

builder = PresentationBuilder()
builder.add_slide_from_json("my_slide.json")
builder.save("output.pptx")
```

---

## 📦 API リファレンス

### `UniversalSlideDesigner(api_url="http://localhost:5000")`

#### メソッド

##### `design(objects, title="", subtitle="")`
**任意のオブジェクトリストからスライドを設計**

```python
objects = [
    {
        "type": "box",           # "box", "arrow", "text", "line", "circle"
        "text": "タイトル",       
        "left": 0.5,             # インチ単位
        "top": 0.5,
        "width": 3.0,
        "height": 0.8,
        "fillColor": "#4472C4",
        "fontColor": "#FFFFFF",
        "fontSize": 14
    }
]

result = designer.design(objects, title="My Slide")
```

**戻り値**:
```json
{
    "success": true,
    "title": "My Slide",
    "subtitle": "",
    "object_count": 1,
    "objects": [...],
    "json_objects": [...]
}
```

---

##### `design_horizontal_comparison(left_title, left_items, right_title, right_items, title, ...)`
**左右比較レイアウト（テンプレート）**

```python
result = designer.design_horizontal_comparison(
    left_title="従来方式",
    left_items=["課題1", "課題2", "課題3"],
    right_title="解決策",
    right_items=["改善1", "改善2", "改善3"],
    title="課題と解決策"
)
```

**パラメータ**:
- `left_title`: 左側のセクションタイトル
- `left_items`: 左側の項目リスト（リスト形式）
- `right_title`: 右側のセクションタイトル
- `right_items`: 右側の項目リスト
- `title`: メインタイトル
- `title_color`: タイトルの背景色（デフォルト: "#4472C4"）
- `left_color`: 左側の色（デフォルト: "#ED7D31"）
- `right_color`: 右側の色（デフォルト: "#4472C4"）

---

##### `design_three_tier_flow(tier1_title, tier1_subtitle, tier1_color, tier2_title, tier2_subtitle, tier2_color, tier3_title, tier3_subtitle, tier3_color, title, show_arrows)`
**3層フロー レイアウト（テンプレート）**

```python
result = designer.design_three_tier_flow(
    tier1_title="構成設計",
    tier1_subtitle="Outline",
    tier1_color="#404040",
    
    tier2_title="コンテンツ詳細",
    tier2_subtitle="Content",
    tier2_color="#4472C4",
    
    tier3_title="最終出力",
    tier3_subtitle="Output",
    tier3_color="#1F3864",
    
    title="AI生成パイプライン"
)
```

**パラメータ**:
- `tier${N}_title`: 各層のタイトル
- `tier${N}_subtitle`: 各層の説明
- `tier${N}_color`: 各層の色
- `title`: メインタイトル
- `show_arrows`: 層間の矢印を表示するか（デフォルト: True）

---

##### `design_from_json(json_path)`
**既存の JSON ファイルからスライドを読み込み**

```python
result = designer.design_from_json("existing_slide.json")
```

---

##### `export_json(design_result, output_path)`
**設計結果を JSON ファイルに保存**

```python
designer.export_json(result, "my_slide.json")
```

---

##### `load_to_canvas(design_result)`
**設計結果を Canvas にロード（ブラウザで確認用）**

```python
designer.load_to_canvas(result)
# ブラウザで http://localhost:5000 を開いて確認
```

---

## 🎨 色パレット

| 用途 | 色コード | 説明 |
|------|---------|------|
| Tier1（暗） | #404040 | ニュートラル濃灰 |
| Tier2（中） | #4472C4 | 中間青 |
| Tier3（濃紺） | #1F3864 | 濃紺 |
| 強調 | #ED7D31 | アクセント橙 |
| 背景浅青 | #8FAADC | Tier1 薄青 |
| 白 | #FFFFFF | 白 |

---

## 📐 寸法単位

**すべてインチ（inch）単位です**

標準スライドレイアウト:
- **幅**: 12.8 inch (1280 pixels @ 96 DPI)
- **高さ**: 7.2 inch (720 pixels @ 96 DPI)

一般的な要素サイズ:
```
タイトル: 4.3" × 0.6"
見出し: 1.9" × 0.5"
本文テキスト: 1.9" × 1.5"
矢印: 0.4" × 0.2"
```

---

## 💡 使用例

### 例1: AI が任意のスライドを自動設計（汎用）

```python
from universal_slide_designer import UniversalSlideDesigner

designer = UniversalSlideDesigner()

# ユースケース1: 左右比較
result = designer.design_horizontal_comparison(
    left_title="問題",
    left_items=["コンテキスト制約", "複雑性", "品質ばらつき"],
    right_title="解決策",
    right_items=["段階的処理", "シンプルな設計", "一貫した品質"],
    title="AI生成の課題と解決策"
)

# ユースケース2: 3層フロー
result = designer.design_three_tier_flow(
    tier1_title="Tier1",
    tier1_subtitle="構成",
    tier2_title="Tier2",
    tier2_subtitle="詳細",
    tier3_title="出力",
    tier3_subtitle="PPTX"
)

# ユースケース3: 完全カスタム
custom_objects = [
    {"type": "box", "text": "カスタムタイトル", "left": 0.5, "top": 0.5, "width": 4.3, "height": 0.8, "fillColor": "#4472C4", "fontColor": "#FFFFFF", "fontSize": 14},
    {"type": "circle", "left": 1.0, "top": 2.0, "width": 0.5, "height": 0.5, "fillColor": "#ED7D31"},
]
result = designer.design(custom_objects, title="完全カスタムスライド")

# JSON 保存
designer.export_json(result, "my_custom_slide.json")
```

---

## 🔄 統合フロー（AI × Designer × Canvas × PPTX）

```
AI エージェント
  ↓ (テキスト思考)
  "このスライドは比較構造にしよう"
  ↓
Universal Slide Designer
  ↓ (オブジェクト生成)
  design_horizontal_comparison(...) 呼び出し
  ↓
Canvas (Flask ブラウザ)
  ↓ (ビジュアル確認)
  http://localhost:5000 でプレビュー
  ↓ (必要に応じて調整)
  ドラッグ&ドロップで微調整
  ↓
JSON 出力
  ↓ (自動生成)
  {objects: [...], title: "...", subtitle: "..."}
  ↓
PPTX 生成
  ↓ (最終出力)
  PowerPoint ファイル完成
```

---

## ✨ 特徴

✅ **汎用性**
- 任意のレイアウトに対応
- テンプレート＋カスタマイズ可
- 拡張可能な設計

✅ **AI フレンドリー**
- プログラマティック API
- テキストベース入力
- 自動 JSON 出力

✅ **ビジュアル確認**
- Canvas で見ながら設計
- 座標計算エラー排除
- リアルタイムプレビュー

✅ **自動化可能**
- API で完全制御
- バッチ処理対応
- スクリプト化可能

---

## 🚀 開始方法

```bash
# 1. Flask サーバー起動
python slide_layout_designer.py

# 2. Designer ページを開く
http://localhost:5000

# 3. スライド設計（Python スクリプト）
python your_slide_design.py
```

---

**このツールは完全に汎用的です。任意のスライド設計に対応できます。**

