# AI PowerPoint Generator - Claude Code ガイド

## プロジェクト概要

Claude API + Gemini API を使って、会社テンプレート（SX_提案書_3.0_16x9.pptx）から
PowerPoint ファイルを自動生成するツール。

## 主要ファイル

| ファイル | 役割 |
|---|---|
| `generate_pptx.py` | CLI エントリポイント。Claude API でアウトライン生成 → PPTX 生成 |
| `pptx_engine.py` | PPTX 生成コアエンジン。中間言語 JSON → python-pptx |
| `app.py` | Streamlit UI 版（`start.bat` で起動、ポート 8501）|
| `SX_提案書_3.0_16x9.pptx` | 社内テンプレート（コミット済み）|
| `recipes/` | 再利用可能なアウトライン JSON（レシピ）|
| `output/` | 生成された PPTX の保存先（.gitignore 対象）|
| `.env` | API キー（.gitignore 対象、コミット禁止）|

## 基本的な使い方

```bash
# テキストで説明して生成（Claude がアウトライン作成）
python generate_pptx.py "DX推進の提案書、製造業向け、5スライド"

# レシピ（JSON）から生成
python generate_pptx.py --recipe recipes/dx_manufacturing.json

# 画像生成なし（Gemini API スキップ、高速）
python generate_pptx.py "提案書タイトル" --no-image

# レシピとして保存しながら生成
python generate_pptx.py "提案書タイトル" --save-recipe my_recipe.json

# 生成後に git commit & push
python generate_pptx.py "提案書タイトル" --git
```

## 中間言語 JSON スキーマ

アウトラインは以下の JSON 配列で表現される。Claude API が生成し、pptx_engine.py が処理する。

```json
[
  {
    "type": "title",
    "title": "提案書タイトル（20〜35文字）",
    "subtitle": "2026年X月　クライアント名御中"
  },
  {
    "type": "agenda",
    "title": "目次",
    "body": "1. 背景と課題\n2. 提案内容\n3. 期待効果\n4. スケジュール"
  },
  {
    "type": "chapter",
    "title": "1. 背景と課題"
  },
  {
    "type": "content",
    "title": "スライドタイトル（20〜35文字）",
    "subtitle": "キーメッセージ（40〜70文字）",
    "body": "・箇条書き1\n・箇条書き2\n・箇条書き3",
    "objects": [
      {"type": "box",   "text": "現状", "left": 0.5, "top": 4.5, "width": 2.5, "height": 0.9,
       "fill_color": "C00000", "font_color": "FFFFFF", "font_size": 13},
      {"type": "arrow", "left": 3.1, "top": 4.7, "width": 0.6, "height": 0.5, "fill_color": "ED7D31"},
      {"type": "box",   "text": "目標", "left": 3.8, "top": 4.5, "width": 2.5, "height": 0.9,
       "fill_color": "4472C4", "font_color": "FFFFFF", "font_size": 13}
    ],
    "images": [
      {
        "prompt": "Professional business illustration related to the slide topic, clean minimal style",
        "model": "gemini-3-pro-image-preview",
        "left": 7.5,
        "top": 1.5,
        "width": 5.3
      }
    ]
  },
  {"type": "end"}
]
```

### objects の type

| type | 説明 |
|---|---|
| `box` / `rect` | 塗りつぶし矩形（テキスト付き可）|
| `arrow` | 右矢印（RIGHT_ARROW）|
| `text` | テキストボックス |

### 座標系

- 幅: 13.3 インチ、高さ: 7.5 インチ（16:9）
- コンテンツエリア: top 1.5〜7.0
- 画像配置推奨: left 7.0以上（スライド右半分）

## テンプレートレイアウト（重要）

| layout index | type | ph_idx |
|---|---|---|
| 0 | title スライド | 0=タイトル, 1=サブタイトル |
| 2 | agenda（目次） | 0=タイトル, 10=本文 |
| 4 | chapter（章扉） | 0=タイトル |
| 6 | content（本文） | 0=タイトル, 13=キーメッセージ, 14=本文 |
| 14 | end（最終）| なし |

## 環境設定

`.env` ファイル（コミット禁止）:
```
ANTHROPIC_API_KEY=sk-ant-api03-...
GEMINI_API_KEY=AIzaSy...
```

## 依存パッケージ

```bash
pip install python-pptx anthropic google-genai streamlit python-dotenv
```

## よくある問題と対処

### Gemini 画像生成エラー
- モデル名は `gemini-3-pro-image-preview`（NANOBANAPRO）
- `GEMINI_API_KEY` が .env に設定されているか確認
- `--no-image` フラグで画像生成をスキップ可能

### PPTX 本文テキストが入らない
- `set_body_text` は ph_idx [10, 14, 1, 2] の順で試みる
- レイアウト 6 の本文は ph_idx=14

### git コマンド
- bash シェルでは git が PATH にない場合がある
- PowerShell から実行: `powershell -Command "git push origin main"`

## ワークフロー（Claude Code での使い方）

1. このリポジトリで Claude Code を起動
2. 「〇〇の提案書を作って」と依頼
3. Claude Code が `generate_pptx.py` を呼び出してアウトライン生成・PPTX 作成
4. `output/` に PPTX が保存される
5. 必要に応じて `--git` フラグで GitHub にコミット

## レシピの活用

繰り返し使うスライド構成は `recipes/` にJSON保存して再利用:
```bash
# 初回: レシピ保存
python generate_pptx.py "製造業DX提案書" --save-recipe dx_manufacturing.json

# 次回以降: レシピから即生成
python generate_pptx.py --recipe recipes/dx_manufacturing.json
python generate_pptx.py --recipe recipes/dx_manufacturing.json --no-image
```
