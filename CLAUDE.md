# AI PowerPoint Generator

## このプロジェクトでできること

Claude Code との対話で、PowerPoint テンプレートから提案書を生成する。
複数テンプレート対応（自社・他社テンプレートの切り替え可能）。

---

## テンプレート管理

### テンプレート構成
```
templates/
├── sx_proposal/              # デフォルト（SX提案書 3.0 16:9）
│   ├── template.pptx         # テンプレートファイル
│   ├── profile.json          # 機械可読: layouts, placeholders, image_areas, colors
│   └── design_guide.md       # AI可読: テンプレート固有のデザインルール
└── <other_template>/         # 追加テンプレート
    ├── template.pptx
    ├── profile.json
    └── design_guide.md
```

### テンプレート指定方法
- **CLI**: `python generate_pptx.py --assemble-only --project "xxx" --template "client_acme"`
- **チャット**: ユーザーが「ACMEテンプレートで」→ `--template client_acme` を使う
- **デフォルト**: outline.json の `"template"` フィールド → 未指定時 `sx_proposal`

### テンプレート登録（ユーザーが「このpptxをテンプレート登録して」と言ったら）
1. `python template_analyzer.py analyze "path.pptx" --id "<id>" --name "<name>"`
2. 生成された `templates/<id>/profile.json` を確認・調整
3. `templates/<id>/design_guide.md` にテンプレート固有のデザインルールを記述

---

## Claude Code への指示（ここが最重要）

**ユーザーが提案書・スライドの作成を依頼したら、以下の2階層フローで進めること。**

```
Tier 1（軽量インデックス）→ Tier 2（スライド単位の詳細）→ PPTX 結合
```

### ステップ1: Tier 1 アウトライン生成（全体の骨格）

ユーザーの要望をもとに **Tier 1 形式** の JSON を Claude Code 自身が生成する。
アウトラインが複雑な場合は先に `skills/outline_guide.md` を Read してから設計する。

**Tier 1 フォーマット**:
```json
{
  "title": "提案書タイトル（20〜35文字）",
  "description": "全体の流れ・ナラティブ（1〜3文。各章の接続・目的を説明）",
  "slides": [
    {"index": 0, "type": "title",   "title": "提案書タイトル", "note": "表紙"},
    {"index": 1, "type": "agenda",  "title": "目次",           "note": "3〜5章"},
    {"index": 2, "type": "chapter", "title": "1. 背景と課題",   "note": ""},
    {"index": 3, "type": "content", "title": "現状の課題",      "note": "時間・品質・再利用の3点"},
    {"index": 4, "type": "end",     "title": "ご確認ありがとうございました", "note": ""}
  ]
}
```

生成したら `outline_<タイトル>.json` として保存し、VSCode で開く:
```
code outline_<タイトル>.json
```
「[outline_<タイトル>.json](outline_<タイトル>.json) を開きました。章立てと流れを確認してください」と伝える。
チャットに JSON を貼り付けない。

### ステップ2: Tier 1 確認・修正

- ユーザーが VSCode で直接編集してもよい
- チャットで修正依頼が来たら Edit ツールで `outline_<タイトル>.json` を直接編集
- 「OK」「展開して」などの承認が出たらステップ3へ

### ステップ3: Tier 2 スライド展開（1枚ずつ詳細化）

**Tier 1 から1枚ずつ詳細な Tier 2 ファイルを生成する。**
各スライドにトークンを集中させることで、高密度なスライドも品質を保てる。

まず `generate_pptx.py --outline` でプロジェクト構造を作成:
```bash
python generate_pptx.py --outline "outline_<タイトル>.json" --project "<タイトル>"
```
→ `slides/YYYYMMDD_<タイトル>/slides/` に Tier 2 スタブファイル（`00_title.json`, `01_agenda.json` ...）が生成される。

次に **スライド1枚ずつ**、Tier 2 ファイルを展開（Write/Edit ツールで保存）:

**Tier 2 フォーマット**（1スライド分）:
```json
{
  "index": 3,
  "type": "content",
  "title": "スライドタイトル（20〜35文字）",
  "subtitle": "キーメッセージ（40〜70文字）",
  "body": "・箇条書き1\n・箇条書き2\n・箇条書き3",
  "objects": [
    {"type": "box", "text": "現状", "left": 3.8, "top": 4.5, "width": 2.5, "height": 0.9,
     "fill_color": "404040", "font_color": "FFFFFF", "font_size": 13},
    {"type": "arrow", "left": 6.4, "top": 4.7, "width": 0.6, "height": 0.5, "fill_color": "ED7D31"},
    {"type": "box", "text": "目標", "left": 7.1, "top": 4.5, "width": 2.5, "height": 0.9,
     "fill_color": "4472C4", "font_color": "FFFFFF", "font_size": 13}
  ]
}
```

> **注意**: objects と images は同一スライドに混在させない（パターン A/B/C から選択）。

Tier 2 ファイルの保存先: `slides/YYYYMMDD_<タイトル>/slides/NN_<type>.json`

### ステップ4: PPTX 結合

全 Tier 2 ファイルが揃ったら結合:
```bash
python generate_pptx.py --assemble-only --project "<タイトル>"
```
- `slides/YYYYMMDD_<タイトル>/slides/` 内の全 JSON を番号順に読み込んで PPTX を生成
- PowerPoint が自動的に開く
- サムネイル生成: `--thumbnail` を追加

一部スライドだけ修正して再結合する場合も同じコマンド。

### ステップ5: 視覚的セルフコレクション（任意）

**重要: PNG の一括読み込みは禁止。コンテキストが枯渇する。**

正しい手順:
1. `/compact` でコンテキストを整理してから開始
2. まず `slides/YYYYMMDD_プロジェクト名/outline.json` を Read してストーリーライン・構成を確認（PNG は読まない）
3. スライドを **1枚ずつ** Read → 診断 → 問題があれば即 Tier 2 Edit → 次へ
4. 全スライド確認後に `--assemble-only --thumbnail` で再結合

詳細な評価基準: `skills/critique_rubric.md` を Read してから診断する。
デザイン改善が必要な場合は `skills/design_principles.md` を参照する。

問題があれば対象スライドの Tier 2 ファイルを Edit → `--assemble-only` で再結合。

### 画像生成の確認

デフォルトは画像あり（Gemini API 使用、時間がかかる）。
ユーザーが「画像なし」「速く」などと言った場合は `--no-image` を付ける。

---

## スキルライブラリ（オンデマンド読み込み）

必要な時だけ Read ツールで読み込む。通常の生成では読まない（トークン節約）。

### 共通スキル（全テンプレート共通）
| スキル | 読み込むタイミング |
|---|---|
| `skills/outline_guide.md` | アウトライン設計が難しい場合 |
| `skills/critique_rubric.md` | サムネイル診断時 |
| `skills/design_principles.md` | デザイン改善・図解設計時（共通原則）|
| `skills/project_rules.md` | プロジェクト作成・フォルダ整理時 |

### テンプレート固有スキル
| スキル | 読み込むタイミング |
|---|---|
| `templates/<id>/design_guide.md` | スライド設計時（座標・色コード・レイアウト）|
| `templates/<id>/profile.json` | エンジンが自動参照（Claude Codeが読む必要は通常なし）|

**AI判断ルール**: スライド設計時はまずテンプレートの `design_guide.md` を読む（具体的座標がある）。
デザインの原則・手法が必要な場合は追加で `skills/design_principles.md` を読む。

---

## リサーチ→スライド生成ワークフロー

ユーザーが「○○について調べてスライドにまとめて」と依頼した場合、以下のフローで進める。

### フロー

1. **リサーチ**: WebSearch ツールでトピックを調査（複数クエリで網羅的に）
2. **情報整理**: 調査結果をもとに要点・構成を整理（refs/ にメモを保存してもよい）
3. **Tier 1 生成**: 調査内容からアウトライン JSON を生成 → ユーザー確認
4. **Tier 2 展開**: 各スライドに調査データを反映。外部データには **出典を必ず記載**
5. **PPTX 結合**: 通常フローで結合 → サムネイル確認

### 出典の扱い

- 外部データ・統計・事例を記載するスライドには `出典` テキストオブジェクトを配置
- フォーマット: `skills/design_principles.md` Section 14 参照
- リサーチメモは `slides/YYYYMMDD_プロジェクト名/refs/` に保存可能

---

## Tier 2 スライド JSON スキーマ（1スライド分のフル詳細）

各スライドは `slides/YYYYMMDD_<タイトル>/slides/NN_<type>.json` に保存する。

```json
{
  "index": 0,
  "type": "title",
  "title": "提案書タイトル（20〜35文字）",
  "subtitle": "2026年X月　クライアント名御中"
}
```

```json
{
  "index": 2,
  "type": "agenda",
  "title": "目次",
  "body": "1. 背景と課題\n2. 提案内容\n3. 期待効果\n4. スケジュール"
}
```

```json
{
  "index": 3,
  "type": "chapter",
  "title": "1. 背景と課題"
}
```

```json
{
  "index": 4,
  "type": "content",
  "title": "スライドタイトル（20〜35文字）",
  "subtitle": "キーメッセージ（40〜70文字）",
  "body": "・箇条書き1（30〜50文字）\n・箇条書き2\n・箇条書き3\n・箇条書き4",
  "objects": [
    {"type": "box",   "text": "現状", "left": 3.8, "top": 4.5, "width": 2.5, "height": 0.9,
     "fill_color": "404040", "font_color": "FFFFFF", "font_size": 13},
    {"type": "arrow", "left": 6.4, "top": 4.7, "width": 0.6, "height": 0.5, "fill_color": "ED7D31"},
    {"type": "box",   "text": "目標", "left": 7.1, "top": 4.5, "width": 2.5, "height": 0.9,
     "fill_color": "4472C4", "font_color": "FFFFFF", "font_size": 13}
  ]
}
```

> objects と images は混在させない。画像を使う場合は objects を外して images のみにする。

### objects の type

| type | 説明 |
|---|---|
| `box` / `rect` | 塗りつぶし矩形（テキスト付き可）|
| `arrow` | 右矢印 |
| `text` | テキストボックス |

### 座標系

- スライドサイズ・コンテンツエリアはテンプレートの `profile.json` に定義
- 画像はスライド右半分に配置する
- 具体的座標はテンプレートの `design_guide.md` を参照

### 構成ルール

- `type: title` → 1枚目
- `type: agenda` → 目次（body に改行区切りで項目列挙）
- `type: chapter` → 章扉（大見出し）
- `type: content` → 本文スライド（subtitle/body/objects/images を含む）
- `type: end` → 最終スライド
- `content` スライドには適宜 `objects`（図解）と `images`（AI生成画像）を追加する
- `objects` は「現状→提案」「フェーズ図」「比較表」など図解が有効な場面で使う
- `images` の prompt は英語で具体的に記述する

---

## テンプレートレイアウト

テンプレート固有のレイアウト情報は `templates/<id>/design_guide.md` に記載。
`profile.json` にはエンジンが使う機械可読な座標・プレースホルダー情報がある。

- `position: "auto"` を images に指定するとテンプレートの画像エリアに自動配置
- chapter は写真なし（シンプル）がデフォルト。写真あり章扉は `type: "chapter_photo"` を使用

---

## generate_pptx.py の使い方（Claude Code が呼び出すコマンド）

```bash
# Tier 1 インデックスからプロジェクト構造を作成（スタブ生成 + 骨格PPTX）
python generate_pptx.py --outline "outline_DX推進提案書.json" --project "DX推進提案書"

# Tier 2 展開後に結合（最もよく使う）
python generate_pptx.py --assemble-only --project "DX推進提案書"

# サムネイル付きで結合
python generate_pptx.py --assemble-only --project "DX推進提案書" --thumbnail

# 画像生成なし（高速）
python generate_pptx.py --assemble-only --project "DX推進提案書" --no-image

# 別テンプレートで結合
python generate_pptx.py --assemble-only --project "xxx" --template "client_acme"

# 生成後に git commit & push
python generate_pptx.py --assemble-only --project "DX推進提案書" --git

# レシピとして保存
python generate_pptx.py --outline "outline_xxx.json" --save-recipe my_recipe.json

# テンプレート解析（新規登録用）
python template_analyzer.py analyze "path/to/template.pptx" --id "my_template" --name "Template Name"
```

---

## フォルダー構成

```
work/
├── templates/                  ← テンプレート管理（テンプレート別）
│   └── sx_proposal/
│       ├── template.pptx       ← テンプレートファイル
│       ├── profile.json        ← 機械可読設定（layouts, colors, coords）
│       └── design_guide.md     ← テンプレート固有デザインルール
├── slides/                     ← 生成された PPTX（プロジェクト別）
│   └── YYYYMMDD_プロジェクト名/
│       ├── outline.json        ← Tier 1 インデックス（template フィールドあり）
│       ├── slides/             ← Tier 2 個別スライド JSON（gitignore）
│       │   ├── 00_title.json
│       │   ├── 01_agenda.json
│       │   └── ...
│       ├── *.pptx              ← 結合後 PPTX
│       └── thumbnails/         ← PNG サムネイル（--thumbnail 時）
├── recipes/                    ← 再利用可能なアウトライン（レシピ）
├── skills/                     ← 共通スキル（全テンプレート共通）
│   ├── design_principles.md    ← デザイン共通原則
│   ├── critique_rubric.md      ← 診断手法
│   └── outline_guide.md        ← 構成パターン
├── docs/
│   ├── vision.md               ← プロジェクトビジョン
│   └── knowhow.md              ← 技術ノウハウ（セッション横断）
├── template_analyzer.py        ← テンプレート登録ツール
├── pptx_engine.py              ← PPTX生成エンジン
└── generate_pptx.py            ← CLI エントリーポイント
```

---

## 環境設定

`.env`（コミット禁止）:
```
ANTHROPIC_API_KEY=sk-ant-api03-...
GEMINI_API_KEY=AIzaSy...
```

依存パッケージ:
```bash
pip install python-pptx anthropic google-genai streamlit python-dotenv
```

---

## よくある問題

- **画像生成エラー**: `GEMINI_API_KEY` が未設定か、`gemini-3-pro-image-preview`（NANOBANAPRO）が使えない状態
- **git コマンドが動かない**: bash シェルでは PATH に git がない場合あり。PowerShell から実行
- **Streamlit UI が使いたい**: `start.bat` を実行（ポート 8501）
