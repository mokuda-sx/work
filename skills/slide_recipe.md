# スキル: スライドレシピ（設計意図の中間言語）

> **使い方**: Tier 2 スライド JSON を生成する**前に**必ずこのスキルを参照する。
> レシピはテンプレート非依存。同じレシピから SX でも JR でも変換可能。

---

## 0. レシピとは何か

**レシピ = スライドの設計意図を、テンプレート固有の座標・色コードなしで記述したもの。**

```
Tier 1（アウトライン）→ レシピ（設計意図）→ Tier 2（テンプレート固有JSON）
       構成・流れ         何をどう見せるか      座標・色・フォントサイズ
```

### なぜ必要か

| 問題 | レシピがあると |
|---|---|
| AIが直接 Tier 2 を書くと設計意図が暗黙化 | 設計判断が明示される |
| テンプレート変更時に Tier 2 を全書き直し | レシピから再変換するだけ |
| レビュー時に「なぜこのレイアウト？」が不明 | レシピを見れば意図がわかる |
| パターンの知識が毎回ゼロスタート | パターンカタログから選べる |

---

## 1. レシピ JSON フォーマット

```json
{
  "index": 3,
  "type": "content",
  "title": "現状の課題を3軸で整理",
  "message": "提案書作成には時間・品質・再利用の3つの根本課題がある",
  "pattern": "three_column",
  "tone": "problem",
  "body_points": [
    "作成に平均8時間、急ぎの案件では徹夜も発生",
    "デザインの属人化で品質にばらつき",
    "過去資産が埋もれ、毎回ゼロから作成"
  ],
  "visual": {
    "labels": ["時間の課題", "品質の課題", "再利用の課題"],
    "emphasis": "equal"
  }
}
```

### フィールド定義

| フィールド | 必須 | 説明 |
|---|---|---|
| `index` | Yes | スライド番号 |
| `type` | Yes | `title` / `agenda` / `chapter` / `content` / `end` |
| `title` | Yes | スライドタイトル（20〜35文字） |
| `message` | content のみ | キーメッセージ（40〜70文字）→ Tier 2 の subtitle になる |
| `pattern` | content のみ | パターンカタログから選択（後述） |
| `tone` | content のみ | `problem` / `solution` / `neutral` / `comparison` / `progression` |
| `body_points` | content のみ | 箇条書き内容（3〜5項目、各30〜50文字） |
| `visual` | 任意 | パターンの詳細設定 |
| `visual.labels` | 任意 | ボックス等のラベル一覧 |
| `visual.emphasis` | 任意 | `equal` / `first` / `last` / `center` |
| `image_hint` | 任意 | 画像が必要な場合の意図（日本語でOK） |

### tone → 色マッピング（変換時にテンプレートの色に解決される）

| tone | 意味 | objects の色の選び方 |
|---|---|---|
| `problem` | 課題・現状のネガティブ面 | 全ボックス neutral |
| `solution` | 提案・解決策 | 全ボックス secondary |
| `neutral` | 情報の整理・説明 | 全ボックス secondary |
| `comparison` | Before/After の対比 | neutral → accent矢印 → secondary |
| `progression` | 段階・フェーズの進行 | 全ボックス secondary、矢印 accent |

---

## 2. パターンカタログ

### 構造パターン（基本レイアウト）

| pattern | 説明 | objects? | images? | 使いどころ |
|---|---|---|---|---|
| `bullet_list` | 標準の箇条書き（body のみ） | なし | 任意 | 数値ファクト、要件一覧 |
| `text_and_image` | 左テキスト + 右画像 | なし | あり | 概念説明、ビジョン系 |
| `two_column` | 2カード横並び | あり | なし | 対比、Before/After |
| `three_column` | 3カード横並び | あり | なし | 並列3項目、3軸整理 |
| `four_column` | 4カード横並び | あり | なし | 4フェーズ、4ステップ |
| `process_flow` | ステップ + 矢印の連鎖 | あり | なし | 業務フロー、導入手順 |
| `before_after` | 現状→矢印→提案 | あり | なし | 変革の提案 |
| `matrix_2x2` | 2x2 グリッド | あり | なし | 優先順位、分類 |
| `pyramid` | 上が小さく下が大きい階層 | あり | なし | 戦略→戦術→実行 |
| `kpi_cards` | 数値を大きく見せるカード | あり | なし | KPI、成果指標 |
| `single_message` | 大きな1メッセージ | なし | 任意 | インパクト重視 |

### ビジネスフレームワーク（構造パターンの特化版）

| pattern | ベース構造 | 説明 |
|---|---|---|
| `swot` | `matrix_2x2` | Strengths/Weaknesses/Opportunities/Threats |
| `asis_tobe` | `before_after` | As-Is / To-Be 比較 |
| `pdca` | `four_column` | Plan/Do/Check/Act |
| `sora_ame_kasa` | `three_column` | 空（事実）→ 雨（解釈）→ 傘（行動） |
| `timeline` | `process_flow` | 時系列のマイルストーン |
| `funnel` | `pyramid`（逆） | ステージごとの絞り込み |

---

## 3. パターン別レシピ例

### three_column（3カード並列）

```json
{
  "index": 3, "type": "content",
  "title": "現状の課題を3軸で整理",
  "message": "提案書作成には時間・品質・再利用の3つの根本課題がある",
  "pattern": "three_column",
  "tone": "problem",
  "body_points": [
    "作成に平均8時間、急ぎの案件では徹夜も発生",
    "デザインの属人化で品質にばらつき",
    "過去資産が埋もれ、毎回ゼロから作成"
  ],
  "visual": {
    "labels": ["時間の課題", "品質の課題", "再利用の課題"],
    "emphasis": "equal"
  }
}
```

### before_after（現状→提案の対比）

```json
{
  "index": 5, "type": "content",
  "title": "AIエンジンで品質とスピードを両立",
  "message": "テンプレート×AIで統一品質の提案書を10分の1の時間で生成できる",
  "pattern": "before_after",
  "tone": "comparison",
  "body_points": [
    "Before: 手作業で平均8時間、デザインは属人化",
    "After: AI対話で30分、テンプレート準拠の統一品質",
    "中間言語（JSON）による設計と描画の分離で再現性を確保"
  ],
  "visual": {
    "labels": ["現状\n手作業8時間", "提案\nAI生成30分"],
    "emphasis": "last"
  }
}
```

### process_flow（ステップフロー）

```json
{
  "index": 6, "type": "content",
  "title": "対話だけで完結する操作フロー",
  "message": "要望を伝えるだけで、構成設計から品質確認まで一気通貫で完結する",
  "pattern": "process_flow",
  "tone": "progression",
  "body_points": [
    "Step1: 要望を伝える → AIが構成案を自動生成",
    "Step2: 構成案を確認・修正（編集 or チャット指示）",
    "Step3: 承認後、詳細展開 → PowerPoint自動生成",
    "Step4: サムネイルで品質チェック → AIが改善を提案"
  ],
  "visual": {
    "labels": ["要望", "構成確認", "PPTX生成", "品質確認"],
    "emphasis": "equal"
  }
}
```

### swot（SWOT分析）

```json
{
  "index": 4, "type": "content",
  "title": "AI提案書生成のSWOT分析",
  "message": "技術的強みと市場機会を活かし、導入障壁を戦略的に克服する",
  "pattern": "swot",
  "tone": "neutral",
  "body_points": [
    "強み: テンプレート準拠の一貫品質、対話UIで学習コストゼロ",
    "弱み: 複雑なカスタムレイアウトへの対応限界",
    "機会: 提案書作成の標準化ニーズの高まり",
    "脅威: 汎用AIツール（Copilot等）の急速な進化"
  ],
  "visual": {
    "labels": ["Strengths", "Weaknesses", "Opportunities", "Threats"],
    "emphasis": "equal"
  }
}
```

### text_and_image（テキスト + 右画像）

```json
{
  "index": 7, "type": "content",
  "title": "学習データの蓄積で精度が向上",
  "message": "作るたびにスキルが蓄積され、次回以降の提案書がより高品質になる",
  "pattern": "text_and_image",
  "tone": "solution",
  "body_points": [
    "デザイン原則・構成パターンをスキルファイルとして蓄積",
    "過去の成功レシピを再利用し、品質の底上げを実現",
    "テンプレート固有のルールと共通原則を分離管理",
    "プロジェクトごとの知見が組織のナレッジとして定着"
  ],
  "image_hint": "知識が積み重なっていくイメージ、本やデータが層になっている"
}
```

### kpi_cards（数値強調カード）

```json
{
  "index": 8, "type": "content",
  "title": "導入効果の定量的インパクト",
  "message": "時間・コスト・品質の3軸で大幅な改善効果が見込める",
  "pattern": "kpi_cards",
  "tone": "solution",
  "body_points": [
    "作成時間を8時間から30分に短縮（93%削減）",
    "デザイン品質のばらつきをゼロに（テンプレート準拠）",
    "過去資産の再利用率を0%から80%に向上"
  ],
  "visual": {
    "labels": ["93%\n時間削減", "100%\n品質統一", "80%\n再利用率"],
    "emphasis": "equal"
  }
}
```

---

## 4. スキル1: レシピ生成（Tier 1 → レシピ）

### いつ使うか
- Tier 1 アウトラインが確定し、Tier 2 展開に入る前
- ユーザーが「展開して」「詳細化して」と言った時

### 手順

1. **Tier 1 のスライド情報を読む**: `index`, `type`, `title`, `note`
2. **type に応じて分岐**:
   - `title` / `agenda` / `chapter` / `end` → レシピ不要（定型のため直接 Tier 2 へ）
   - `content` → レシピを生成する
3. **content スライドのレシピ生成**:
   a. note からスライドの目的を把握
   b. パターンカタログから最適なパターンを選択
   c. tone を決定（problem / solution / neutral / comparison / progression）
   d. body_points を 3〜5 項目で記述
   e. visual.labels を設定（ボックスのラベル）
   f. message（キーメッセージ）を 40〜70 文字で書く
4. **ユーザーにレシピを提示し、設計意図をディスカッションする**:
   - パターン選択は適切か？（別パターンの提案も歓迎）
   - トーン・ラベル・メッセージの方向性は合っているか？
   - body_points の内容に過不足はないか？
   - **ユーザーの承認が出てから** Tier 2 変換に進む
   - 「一気にやって」と言われた場合のみバッチ処理OK

### パターン選択の判断フロー

```
スライドの目的は？
  ├→ 課題・問題点の提示 → いくつの軸？
  │   ├→ 1つ → bullet_list (tone: problem)
  │   ├→ 2つ → two_column (tone: problem)
  │   ├→ 3つ → three_column (tone: problem)
  │   └→ 4つ → four_column (tone: problem) or matrix_2x2
  │
  ├→ 解決策・提案の説明 → 比較が必要？
  │   ├→ Before/After → before_after (tone: comparison)
  │   ├→ ステップ説明 → process_flow (tone: progression)
  │   ├→ 概念的 → text_and_image (tone: solution)
  │   └→ 数値効果 → kpi_cards (tone: solution)
  │
  ├→ 分析・整理 → フレームワーク？
  │   ├→ SWOT → swot
  │   ├→ 空雨傘 → sora_ame_kasa
  │   ├→ As-Is/To-Be → asis_tobe
  │   └→ 時系列 → timeline
  │
  └→ 情報の羅列 → bullet_list (tone: neutral)
```

### Tier 1 の拡張（将来形）

AI の学習が進めば、Tier 1 の段階でパターンヒントを出力できる:

```json
{
  "index": 3, "type": "content",
  "title": "現状の課題",
  "note": "時間・品質・再利用の3点",
  "pattern": "three_column"
}
```

この `pattern` が Tier 1 にあれば、レシピ生成のパターン選択ステップをスキップできる。

---

## 5. スキル2: レシピ → Tier 2 変換（レシピ + テンプレート → JSON）

### いつ使うか
- レシピが確定した後、Tier 2 スライド JSON を書く時
- テンプレートを変えて同じ内容を再生成する時

### 手順

1. **テンプレートの design_guide.md を読む**（座標・色コード・パターン別座標例）
2. **レシピの pattern を元に、テンプレートの図解パターン集から対応する座標を取得**
3. **tone → テンプレートの色に変換**:
   - テンプレートの `profile.json` の `colors` と `color_semantics` を参照
   - tone: problem → neutral 色
   - tone: solution → secondary 色
   - tone: comparison → neutral + accent矢印 + secondary
   - tone: progression → secondary + accent矢印
   - tone: neutral → secondary 色
4. **visual.labels → objects の text に変換**
5. **body_points → body 文字列に変換**（`"・" + point` を `\n` で結合）
6. **message → subtitle に変換**
7. **image_hint → images の prompt に変換**（英語に翻訳、スタイル指示を追加）

### 変換ルール詳細

#### pattern → objects 構造

| pattern | objects の構造 |
|---|---|
| `bullet_list` | objects なし |
| `text_and_image` | objects なし、images あり |
| `two_column` | 2 box 横並び |
| `three_column` | 3 box 横並び |
| `four_column` | 4 box 横並び（矢印なし） or 4 box + 3 arrow |
| `process_flow` | N box + (N-1) arrow の横並び |
| `before_after` | box + arrow + box |
| `matrix_2x2` | 4 box を 2x2 配置 |
| `kpi_cards` | N box 横並び（数値を大きく） |
| `swot` | 4 box を 2x2 配置、ラベル固定 |

#### emphasis → 色の差別化

| emphasis | 効果 |
|---|---|
| `equal` | 全ボックス同色（tone に応じた色） |
| `first` | 最初のボックスだけ強調色、残りは neutral |
| `last` | 最後のボックスだけ強調色（secondary）、残りは neutral |
| `center` | 中央のボックスだけ強調色 |

#### matrix_2x2 の座標計算（テンプレート非依存の考え方）

```
content_area から左半分・右半分、上半分・下半分に分割:

  [TL] gap [TR]
  gap       gap
  [BL] gap [BR]

box_width = (available_width - gap) / 2
box_height = (available_height - gap) / 2
```

---

## 6. レシピファイルの保存

### 保存先
```
slides/YYYYMMDD_<template>_プロジェクト名/recipes/NN_type.recipe.json
```

プロジェクトフォルダ内の `recipes/` サブフォルダに保存。
Tier 2 JSON（`slides/` サブフォルダ、gitignore対象）とは分離して git 管理する。

### 保存タイミング
- Tier 2 展開前にレシピを生成 → `.recipe.json` として保存
- Tier 2 JSON 生成後も `.recipe.json` は保持（テンプレート変更時に再利用）

### テンプレート変更時の再利用
```
1. プロジェクトの recipes/ フォルダの .recipe.json を読み込む
2. 新テンプレートの design_guide.md を読む
3. スキル2 で再変換 → 新テンプレート用の Tier 2 JSON を生成
```

---

## 7. 非 content スライドの扱い

`title`, `agenda`, `chapter`, `chapter_photo`, `end` はレシピ不要。
テンプレートの定型レイアウトに従って直接 Tier 2 を書く。

| type | レシピ | 理由 |
|---|---|---|
| `title` | 不要 | タイトル + サブタイトル + 写真の定型 |
| `agenda` | 不要 | 目次 + 写真の定型 |
| `chapter` | 不要 | 章タイトルのみ |
| `chapter_photo` | 不要 | 章タイトル + 写真 |
| `content` | **必要** | パターン・色・レイアウトの設計判断が必要 |
| `end` | 不要 | 締めの定型 |

---

## 8. レシピ品質チェック

レシピ生成後、以下を確認:

- [ ] `pattern` がパターンカタログに存在するか
- [ ] `tone` がスライドの内容と合っているか（課題に solution を使っていないか）
- [ ] `body_points` が 3〜5 項目、各 30〜50 文字か
- [ ] `visual.labels` の数が pattern に合っているか（three_column なら 3 つ）
- [ ] `message` が 40〜70 文字で、結論を含んでいるか
- [ ] 同じデッキ内で同じ pattern が連続していないか（単調さを回避）
