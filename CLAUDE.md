# AI PowerPoint Generator

## このプロジェクトでできること

Claude Code との対話で、会社テンプレート（SX_提案書_3.0_16x9.pptx）から
PowerPoint ファイルを生成する。

---

## Claude Code への指示（ここが最重要）

**ユーザーが提案書・スライドの作成を依頼したら、以下の対話フローで進めること。**

### ステップ1: アウトライン生成 → ファイル保存

ユーザーの要望をもとに、以下のスキーマに従った JSON アウトラインを Claude Code 自身が生成する。
`generate_pptx.py` の Claude API 呼び出しは使わない（Claude Code 自身が考える）。

生成したら **必ず `outline_temp.json` にファイルとして保存**し、VSCode で自動的に開く:
```
code outline_temp.json
```
その後「[outline_temp.json](outline_temp.json) を開きました。確認・編集してください」と伝える。
チャットに JSON を貼り付けない。

### ステップ2: 対話・修正

- ユーザーが VSCode で `outline_temp.json` を直接編集してもよい
- チャットで「〇枚目を変えて」などの修正依頼が来たら、Edit ツールで `outline_temp.json` を直接編集する
- 「確認して」と言われたら Read ツールで内容を読んで要約する
- 「OK」「これで生成して」などの承認が出たら次のステップへ

### ステップ3: PPTX 生成

承認されたら:
1. 以下を実行:
   ```
   python generate_pptx.py --outline outline_temp.json
   ```
2. 生成完了後、PowerPoint が自動的に開く
3. サムネイルも必要な場合は `--thumbnail` を追加（pywin32 が必要）

### ステップ4: 視覚的セルフコレクション（任意）

サムネイルが生成されていれば Read ツールで PNG を読み込み、レイアウトを目視確認する:
- テキストが枠をはみ出していないか
- 画像の配置がスライドに合っているか
- objects（図解）の位置関係が意図通りか

問題があれば `outline_temp.json` を Edit ツールで修正し、再生成する。

### ステップ5: 画像生成の確認

デフォルトは画像あり（Gemini API 使用、時間がかかる）。
ユーザーが「画像なし」「速く」などと言った場合は `--no-image` を付ける。

---

## 中間言語 JSON スキーマ

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
    "body": "・箇条書き1（30〜50文字）\n・箇条書き2\n・箇条書き3\n・箇条書き4",
    "objects": [
      {"type": "box",   "text": "現状", "left": 0.5, "top": 4.5, "width": 2.5, "height": 0.9,
       "fill_color": "C00000", "font_color": "FFFFFF", "font_size": 13},
      {"type": "arrow", "left": 3.1, "top": 4.7, "width": 0.6, "height": 0.5, "fill_color": "ED7D31"},
      {"type": "box",   "text": "目標", "left": 3.8, "top": 4.5, "width": 2.5, "height": 0.9,
       "fill_color": "4472C4", "font_color": "FFFFFF", "font_size": 13}
    ],
    "images": [
      {
        "prompt": "Professional business illustration, clean minimal style, related to the slide topic",
        "model": "gemini-3-pro-image-preview",
        "left": 7.5, "top": 1.5, "width": 5.3
        // または "position": "auto" でテンプレートの「画像挿入位置」に自動配置
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
| `arrow` | 右矢印 |
| `text` | テキストボックス |

### 座標系

- スライドサイズ: 幅 13.3 × 高さ 7.5 インチ（16:9）
- コンテンツエリア: top 1.5〜7.0
- 画像はスライド右半分（left 7.0 以上）に配置する

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

## テンプレートレイアウト（参考）

| layout index | type キー | 名称 | 画像エリア |
|---|---|---|---|
| 0 | `title` | タイトル（写真あり）| left=1.012, top=2.253, 11.3×4.6" |
| 2 | `agenda` | 目次（写真あり）| left=6.981, top=0.443, 5.4×6.6"（右半分）|
| 4 | `chapter_photo` | 章扉（写真あり）| left=1.012, top=2.411, 11.3×4.6" |
| 5 | `chapter` | 章扉（写真なし）★デフォルト | なし |
| 6 | `content` | コンテンツ | なし（images で任意配置）|
| 14 | `end` | エンドスライド（写真あり）| left=0.997, top=0.831, 11.3×4.6" |

- `position: "auto"` を images に指定するとテンプレートの画像エリアに自動配置
- chapter は写真なし（シンプル）がデフォルト。写真あり章扉は `type: "chapter_photo"` を使用

---

## generate_pptx.py の使い方（Claude Code が呼び出すコマンド）

```bash
# 対話で作成した outline_temp.json から生成（通常）
python generate_pptx.py --outline outline_temp.json

# 画像生成なし（高速）
python generate_pptx.py --outline outline_temp.json --no-image

# 生成後に git commit & push
python generate_pptx.py --outline outline_temp.json --git

# レシピとして保存
python generate_pptx.py --outline outline_temp.json --save-recipe my_recipe.json
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
