# ワークフロー定義

> このドキュメントは **エージェント非依存** です。Claude Code、Gemini、GPT-4、人間のエディター、いずれが作業しても同じプロセスを踏めるよう定義しています。

## 前提

- 全ての JSON ファイルは `schemas/` の Schema に準拠していること
- 作業単位は「1コミットで完結」すること
- 作業開始前に [STATUS.md](../STATUS.md) のオンボーディングテストを通過していること

---

## プロセス全体像

```
[ユーザーの依頼]
      |
      v
[Step 1] Tier 1 生成 ─── 確認 ──→ (修正) ──→ 承認
      |
      v
[Step 2] プロジェクト初期化
      |
      v
[Step 3] Recipe 生成 ─── 1枚ずつ確認 ──→ (修正) ──→ 承認
      |
      v
[Step 4] Tier 2 変換
      |
      v
[Step 5] PPTX 結合 → サムネイル確認 ──→ (修正) ──→ 完成
```

各ステップで **ユーザーの承認** を得てから次に進む。一括処理はユーザーが明示的に許可した場合のみ。

---

## Step 1: Tier 1 アウトライン生成

### 目的
提案書の構成・ストーリーライン・スライド一覧を確定する。

### 入力
- ユーザーの依頼（テーマ、対象、目的、スライド枚数）

### 処理
1. 依頼の背景・目的を整理する
2. ナラティブ構造を設計する（例: 課題→解決策→効果→次のステップ）
3. Tier 1 JSON を生成する（[schemas/outline.schema.json](../schemas/outline.schema.json) 準拠）
4. ファイルをプロジェクトフォルダ（後述）に保存する

### Tier 1 JSON 構造
```json
{
  "title": "提案書タイトル（20〜35文字）",
  "description": "全体の流れ・ナラティブ（1〜3文）",
  "template": "sx_proposal",
  "slides": [
    {"index": 0, "type": "title",   "title": "...", "note": "表紙"},
    {"index": 1, "type": "agenda",  "title": "目次", "note": "章の一覧"},
    {"index": 2, "type": "chapter", "title": "1. ...", "note": ""},
    {"index": 3, "type": "content", "title": "...", "note": "伝えたいこと"},
    {"index": 4, "type": "end",     "title": "ご確認ありがとうございました", "note": ""}
  ]
}
```

### 出力
- `slides/YYYYMMDD_<タイトル>/outline.json`
- ユーザーへ「構成と流れを確認してください」と提示（JSON をチャットに貼らない）

### 完了条件
- ユーザーが「OK」「進めて」等の承認を出した

---

## Step 2: プロジェクト初期化

### 目的
フォルダ構造とスタブファイルを作成する。

### 処理
```bash
python generate_pptx.py --outline "slides/YYYYMMDD_タイトル/outline.json" --project "タイトル"
```

### 出力
```
slides/YYYYMMDD_<タイトル>/
├── outline.json        ← コピー済み
├── recipes/            ← 空（Step 3 で埋める）
└── slides/             ← スタブ JSON（Step 4 で埋める）
    ├── 00_title.json
    ├── 01_agenda.json
    └── ...
```

---

## Step 3: Recipe 生成（content スライドのみ）

### 目的
各 content スライドの「設計意図」を明文化し、テンプレート非依存の形で保存する。

### 処理（1枚ずつ）
1. `skills/slide_recipe.md` を参照してパターン・トーンを選択する
2. Recipe JSON を生成する（[schemas/recipe.schema.json](../schemas/recipe.schema.json) 準拠）
3. ユーザーに提示し、承認を得る
4. `slides/YYYYMMDD_<タイトル>/recipes/NN_content.recipe.json` に保存する

### Recipe JSON 構造
```json
{
  "index": 3,
  "type": "content",
  "title": "スライドタイトル",
  "message": "このスライドで伝えたいこと（1文）",
  "pattern": "three_column",
  "tone": "problem",
  "body_points": ["箇条書き1", "箇条書き2", "箇条書き3"],
  "visual": {
    "labels": ["ラベル1", "ラベル2", "ラベル3"],
    "emphasis": "equal"
  }
}
```

### 判断基準
- `pattern`: レイアウトパターン（`skills/slide_recipe.md` のパターンカタログを参照）
- `tone`: 色調の方向性（`problem` = 課題色、`solution` = 解決策色、`neutral` = 中立）
- `visual.emphasis`: どの要素を強調するか

### 完了条件
- 全 content スライドの Recipe が保存されている
- ユーザーが各 Recipe を確認・承認している

---

## Step 4: Tier 2 変換（Recipe → テンプレート固有 JSON）

### 目的
Recipe をテンプレートの具体的な座標・色・フォントサイズに変換する。

### 処理
1. テンプレートの `templates/<id>/design_guide.md` を参照する
2. Recipe の `pattern` → 対応する図解パターンの座標を取得する
3. Recipe の `tone` → テンプレートの色コードに変換する
4. Tier 2 JSON を生成する（[schemas/tier2.schema.json](../schemas/tier2.schema.json) 準拠）

### title / agenda / chapter / end スライド
これらはテンプレートの定型レイアウトを使うため Recipe 不要。
スタブをそのまま必要な内容で埋める。

### 完了条件
- 全スライドの Tier 2 JSON が `slides/YYYYMMDD_<タイトル>/slides/` に揃っている
- Schema バリデーション通過（`python validate_schemas.py` で確認）

---

## Step 5: PPTX 結合とレビュー

### 処理

```bash
# 結合
python generate_pptx.py --assemble-only --project "タイトル"

# サムネイル付き結合
python generate_pptx.py --assemble-only --project "タイトル" --thumbnail

# 画像生成なし（高速）
python generate_pptx.py --assemble-only --project "タイトル" --no-image
```

### レビュー手順（PNG 一括読み込み禁止）
1. `/compact` でコンテキストを整理してから開始
2. `outline.json` を読んでストーリーラインを確認（PNG は読まない）
3. サムネイルを **1枚ずつ** 確認 → 問題があれば Tier 2 を Edit → 再結合
4. 評価基準: `skills/critique_rubric.md` を参照

### 完了条件
- 全スライドを目視確認済み
- 重大な問題がない
- コミット済み

---

## プロジェクトフォルダ命名規則

```
slides/YYYYMMDD_<タイトル>/
```

- `YYYYMMDD`: 作成日（例: `20260214`）
- `<タイトル>`: Tier 1 の `title` から特殊文字を除いたもの

---

## エラー対応

| 症状 | 原因 | 対処 |
|---|---|---|
| PPTX 生成で `Duplicate name` エラー | スライド削除時の ZIP エントリ残留 | `docs/knowhow.md` 参照 |
| 画像生成失敗 | Gemini API Key 未設定 or モデル名変更 | `.env` 確認、`docs/knowhow.md` 参照 |
| Schema バリデーション失敗 | Tier 2 JSON の構造不正 | エラーメッセージのパスを確認して修正 |
