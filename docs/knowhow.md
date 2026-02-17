# AI スライド生成ノウハウ・技術メモ

> **AIセッション向け注意**: このファイルは過去の発見を記録したものです。
> 新しいセッションを始める前に必ず読んでください。

---

## テンプレートのレイアウト構造（最重要）

テンプレート: `SX_提案書_3.0_16x9.pptx`（13.3×7.5インチ）

| type キー | layout[n] | 名称 | 主なプレースホルダ |
|---|---|---|---|
| `title` | [0] | タイトル（写真あり） | ph_idx=0（タイトル）, 1（サブタイトル）|
| `agenda` | [2] | 目次（写真あり） | ph_idx=0（タイトル）, 10（本文）|
| `chapter` | **[5]** | 章扉（**写真なし**）★デフォルト | ph_idx=0（タイトル）at top=2.095 |
| `chapter_photo` | [4] | 章扉（写真あり） | ph_idx=0（タイトル）at top=0.457 |
| `content` | [6] | コンテンツ | ph_idx=0（見出し）, 13（キーメッセージ）, 14（本文）|
| `end` | [14] | エンドスライド（写真あり）| ph_idx=0（タイトル）at top=5.641 |

### 重要: プレースホルダーの ph_idx と ph_type の不一致

python-pptx が報告する `ph_type` はテンプレート独自の名称割り当てのため
実際の用途と異なる場合がある。**ph_idx で識別すること。**

例:
- layout[5] chapter の `ph_idx=0` → `ph_type=DATE` と報告されるが実際はタイトル
- layout[2] agenda の `ph_idx=0` → `ph_type=DATE` と報告されるが実際はタイトル
- layout[6] content の `ph_idx=14` → `ph_type=CENTER_TITLE` だが実際は本文

---

## 「画像挿入位置」シェイプ

写真あり系レイアウトには `text="画像挿入位置"` の `AUTO_SHAPE` が埋め込まれている。
これは PICTURE プレースホルダーではなく**固定シェイプ**。
AI生成画像は `add_picture()` でこの上に重ねて配置する。

| layout | 座標 (left, top, width, height インチ) |
|---|---|
| title [0] | 1.012, 2.253, 11.348, 4.646 |
| chapter_photo [4] | 1.012, 2.411, 11.348, 4.646 |
| agenda [2] | 6.981, 0.443, 5.356, 6.615 |
| end [14] | 0.997, 0.831, 11.348, 4.646 |

→ `images` フィールドに `"position": "auto"` を指定すると自動使用。

---

## `fill_text_frame` のスタイル保持問題

### 問題
`tf.clear()` を使うとテンプレートの段落書式（`<a:pPr>` / lstStyle 経由の
フォント・色・サイズ）が失われる。

### 解決策（現在の実装）
XML レベルで既存の `<a:p>` から `<a:r>` だけを削除して `<a:pPr>` を保持する。
→ `pptx_engine.py` の `fill_text_frame()` 参照

### 残課題
`chapter` (layout[5]) のタイトルは `<a:pPr>` を保持しても視覚的に
「シンプルな黒テキスト、top=2.095」のまま。
これは **テンプレートの意図したデザイン**（写真なし = ミニマル）。
目立つ章扉が必要なら `type: "chapter_photo"` を使う。

---

## OPC（Open Packaging Convention）の落とし穴

### 問題
`prs.slides._sldIdLst` から sldId を削除するだけではスライドが消えない。
OPC パッケージ内の relationship も削除しないと "Duplicate name" ZIP 警告が出て
新しいスライドのコンテンツが上書きされる。

### 解決策
```python
def remove_all_slides(prs):
    r_ns = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    slide_id_list = prs.slides._sldIdLst
    for sld_id in list(slide_id_list):
        rId = sld_id.get(f'{{{r_ns}}}id')
        if rId:
            prs.part.rels.pop(rId)   # ← これが必須
        slide_id_list.remove(sld_id)
```

---

## `set_body_text` の本文プレースホルダー探索順

layout[6] content の本文は `ph_idx=14`。
layout[2] agenda の本文は `ph_idx=10`。
他のレイアウトとの互換性のため `[10, 14, 1, 2]` の順で試みる。

---

## `MSO_AUTO_SHAPE_TYPE` の注意点

| 用途 | 正しい値 | 間違いやすい値 |
|---|---|---|
| 右矢印 | `RIGHT_ARROW` (=33) | 13 は `CAN`（円柱）|
| 矩形 | `RECTANGLE` (=1) | |

---

## Gemini API 画像生成

- モデル名: `gemini-3-pro-image-preview`（社内呼称: NANOBANAPRO）
- SDK: `from google import genai`（旧 `google.generativeai` は廃止）
- `response_modalities=["IMAGE", "TEXT"]` が必要
- 生成失敗時は `part.inline_data` が None → スキップして続行

---

## PNG サムネイル生成（視覚的セルフコレクション）

```python
# 管理者権限不要・追加インストール不要（PowerPoint 必要）
python generate_pptx.py --outline outline_temp.json --thumbnail
```

PowerShell + PowerPoint COM で実装。pywin32 は不要。
生成された PNG を Claude Code が Read ツールで確認 → レイアウト問題を視覚的に検出。

---

## Windows 環境固有の注意

- bash シェルでは `git` / `python` が PATH にない場合がある → `powershell -Command` を使う
- print の絵文字（✅等）は cp932 でエラーになる → 絵文字を避けるか UTF-8 強制
- ファイル名に日本語を含む場合でもパス指定は問題なし
- 管理者権限なしで使えるツール: pip (--user), gh CLI (portable), PowerShell COM

---

## 対話フローのベストプラクティス

1. アウトラインは **必ずファイル保存** → `code outline_temp.json` で VSCode で開く
2. チャットに JSON を貼り付けない（長くなりすぎる）
3. 修正は **Edit ツールで直接ファイル編集** → ユーザーも VSCode で直接編集可
4. 生成後は **--thumbnail で視覚確認** → 問題発見時は JSON 修正→再生成
5. レシピとして保存 → `--save-recipe` で `recipes/` フォルダに残す

---

## フォントサイズ基準（SX Documentation Master 2023 準拠）

| サイズ | 用途 | 備考 |
|---|---|---|
| **14pt** | 本文の標準サイズ | 「読ませるテキスト」のデフォルト |
| **12pt** | 情報密度が高い場合の本文 | 許容される最小の「読ませる」サイズ |
| **9pt** | 補足・注釈 | 読む必要が低いが記載しておきたい情報 |
| **9pt未満** | **原則禁止** | 小さすぎて読めない評価になる |

### 同一グループ内の統一ルール（最重要）
- 同じリスト内の項目は全て同じ `font_size` であること
- 並列カラム内のテキストは全て同じ `font_size` であること
- 違反例: 箇条書き5項目のうち一部が9pt、他が18pt → 即修正（S優先度）

### フォント選択
- MSPゴシック（汎用）、游ゴシック（柔らかい）、游ゴシック Medium（見出し）
- プロジェクト・資料単位でフォントを統一（混在NG）
- 游ゴシックをタイトルに使う場合は Medium またはボールドにする（線が細く弱く見えるため）
- 英字のみの文書以外では Cambria を使わない（和英混在時は日本語フォントで統一）

---

## カラールール（SX Documentation Master 2023 準拠）

- **基本3色**: 白・黒・Dynamic Orange（`ED7D31`）
- **強調色は Dynamic Orange のみ**。追加色はテンプレートのカラーパレットから左→右の順
- 差別化はグレースケールの濃淡で。橙以外の有彩色を安易に増やさない
- キーメッセージを先に決め、そこに色と太さを集中させる（色の使い方に意図を持つ）
- 以前の design_guide.md にあった `4472C4`（青）は強調色として使わない

---

## 整列ルール

- **行方向の揃え統一**: ラベル=中央揃え → 隣のテキストも中央揃え（行内の不統一は違和感が出やすい）
- **列方向の揃え違い**: 上段=中央、下段=左 は許容される
- 縦のライン・横のラインが揃って見えると人間は美しく感じる

---

## pptx_engine.py テキスト処理の注意点

### `\n` を含む text オブジェクト
`p.text = "line1\nline2"` は python-pptx 内部で1つの paragraph になり、
`p.runs[0]` へのフォント設定は最初の行にしか適用されない。
→ `\n` で split して `tf.add_paragraph()` で個別段落を作成し、各 run にスタイル適用すること。

### 空 body プレースホルダの削除
`body` が空（or 未指定）で `objects` がある場合、body プレースホルダーが
画面上で点線枠として表示されてしまう。
→ `sp.getparent().remove(sp)` で XML 要素ごと削除する。

### v_align（縦方向揃え）
box / text 両方で `"v_align": "middle"` を指定可能。
内部実装: `tf._txBody.bodyPr.set("anchor", "ctr")`

### bold プロパティ
text オブジェクトで `"bold": true` を指定可能。run.font.bold に反映。

---

## 発見済みの既知問題・制約

| 問題 | 状態 | 回避策 |
|---|---|---|
| chapter(layout[5]) がシンプルすぎる | 仕様通り（テンプレートのデザイン） | `chapter_photo` を使う |
| タイトルスライドのサブタイトル | ph_idx=1（title/agenda）/ ph_idx=13（content）で別 | layout_key で分岐して設定 ✅修正済み |
| Gemini API レート制限 | 連続生成時に遅延の可能性 | `--no-image` で一時スキップ |
| 本文が長すぎるとはみ出す | 未対応 | JSONで文字数を調整（1行30-50文字推奨）|
