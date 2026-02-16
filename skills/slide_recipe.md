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
| `row_label_content` | 左ラベル列 + 右コンテンツ列（行グループ） | あり | なし | スコープ定義、フェーズ別説明 |
| `swimlane_process` | 行ラベル（スイムレーン） + 各行にプロセスフロー | あり | なし | 並行プロセス、複数フェーズ計画 |
| `matrix_table` | ヘッダー付き多列テーブル（複雑） | あり | なし | 作業定義、RACI、詳細スコープ |
| `circular_flow` | 循環プロセス（円形に配置されたステップ） | あり | なし | PDCA、継続改善、スプリント |
| `value_chain` | 横長の連結ブロック（左→右の価値連鎖） | あり | なし | バリューチェーン、サプライチェーン |
| `cause_effect` | 原因群→結果の構造（左に原因、右に結果） | あり | なし | 課題分析、根本原因、因果関係 |
| `roadmap` | 時系列ロードマップ（フェーズ + マイルストーン） | あり | なし | 中長期計画、段階的導入 |
| `traffic_light` | 信号式ステータス表示（赤黄緑 + 項目） | あり | なし | 進捗報告、リスク評価、ヘルスチェック |
| `team_profile` | メンバー紹介カード（名前 + 役割 + 写真エリア） | あり | 任意 | 体制紹介、チーム紹介 |

### ビジネスフレームワーク（構造パターンの特化版）

| pattern | ベース構造 | 説明 |
|---|---|---|
| `swot` | `matrix_2x2` | Strengths/Weaknesses/Opportunities/Threats |
| `asis_tobe` | `before_after` | As-Is / To-Be 比較 |
| `pdca` | `four_column` | Plan/Do/Check/Act |
| `sora_ame_kasa` | `three_column` | 空（事実）→ 雨（解釈）→ 傘（行動） |
| `timeline` | `process_flow` | 時系列のマイルストーン |
| `funnel` | `pyramid`（逆） | ステージごとの絞り込み |
| `fishbone` | `cause_effect` | 特性要因図（魚の骨） |
| `customer_journey` | `process_flow` | 顧客体験の段階フロー |

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

### row_label_content（左ラベル + 右コンテンツ）

**参照作品**: `sx_ctc_jre_suica` スライド3, 5 / `sx_ai_callcenter` スライド7

```json
{
  "index": 4, "type": "content",
  "title": "ご支援スコープの定義",
  "message": "目的・ゴール・体制・期間の4軸でスコープを明確に合意する",
  "pattern": "row_label_content",
  "tone": "neutral",
  "body_points": [
    "目的: サービス企画の全体構想を具体化する",
    "ゴール: 2026年Q1までに投資意思決定が可能な状態",
    "体制: クライアント3名 + 支援側3名のOne Team",
    "期間: 2025年12月〜2026年3月（4ヶ月）"
  ],
  "visual": {
    "labels": ["目的", "ゴール", "体制", "期間"],
    "emphasis": "equal"
  }
}
```

> **変換ルール**: labels の数 = 行数。各行は「左の label ボックス（dark）+ 右のテキストエリア」で構成。
> body_points の N 番目が labels の N 番目に対応する。

---

### swimlane_process（スイムレーン + プロセス）

**参照作品**: `sx_ai_callcenter` スライド4

```json
{
  "index": 6, "type": "content",
  "title": "フェーズ別の実施ステップ",
  "message": "現状分析とPoC検証を並行して進め、4ヶ月で導入判断を行う",
  "pattern": "swimlane_process",
  "tone": "progression",
  "body_points": [
    "現状分析と戦略策定: 業務把握 → 自動化診断 → コンセプト策定 → スケジュール",
    "PoC実施: 現状理解 → 検証計画 → 検証実施 → 結果取りまとめ"
  ],
  "visual": {
    "labels": ["現状分析・\n戦略策定", "PoC"],
    "emphasis": "equal"
  }
}
```

> **変換ルール**: labels = スイムレーンの行ラベル（N行）。body_points の各行を ` → ` で分割してプロセスボックスに変換。

---

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

### circular_flow（循環プロセス）

```json
{
  "index": 9, "type": "content",
  "title": "継続的改善サイクルの定着",
  "message": "Plan→Do→Check→Actの4ステップを毎スプリント回す",
  "pattern": "circular_flow",
  "tone": "solution",
  "body_points": [
    "Plan: 仮説設定とKPI目標の合意",
    "Do: 2週間スプリントでの施策実行",
    "Check: データ分析と効果測定",
    "Act: 改善アクションの反映と次サイクルへ"
  ],
  "visual": {
    "labels": ["Plan", "Do", "Check", "Act"],
    "emphasis": "equal"
  }
}
```

### value_chain（バリューチェーン）

```json
{
  "index": 10, "type": "content",
  "title": "サービス提供の価値連鎖",
  "message": "企画から運用まで一気通貫で支援し、各段階で価値を付加",
  "pattern": "value_chain",
  "tone": "solution",
  "body_points": [
    "企画: ニーズ調査・要件定義",
    "設計: アーキテクチャ設計・UXデザイン",
    "開発: アジャイル開発・テスト",
    "展開: 導入支援・トレーニング",
    "運用: 継続改善・モニタリング"
  ],
  "visual": {
    "labels": ["企画", "設計", "開発", "展開", "運用"],
    "emphasis": "left_to_right"
  }
}
```

### cause_effect（原因→結果）

```json
{
  "index": 11, "type": "content",
  "title": "業務効率低下の根本原因",
  "message": "3つの構造的課題が連鎖して全体の生産性を下げている",
  "pattern": "cause_effect",
  "tone": "problem",
  "body_points": [
    "原因1: 手作業による情報転記（年間500時間のロス）",
    "原因2: 部門間の情報サイロ化（意思決定の遅延）",
    "原因3: 属人化した業務プロセス（引継ぎ不能）",
    "結果: 全体の生産性が30%低下、顧客対応も遅延"
  ],
  "visual": {
    "labels": ["手作業", "サイロ化", "属人化", "生産性低下"],
    "emphasis": "right"
  }
}
```

### roadmap（ロードマップ）

```json
{
  "index": 12, "type": "content",
  "title": "3フェーズでの段階的導入計画",
  "message": "Phase 0で検証、Phase 1で基盤構築、Phase 2で全社展開",
  "pattern": "roadmap",
  "tone": "neutral",
  "body_points": [
    "Phase 0（3ヶ月）: PoC実施・効果検証・要件確定",
    "Phase 1（6ヶ月）: 基盤システム構築・パイロット部門導入",
    "Phase 2（6ヶ月）: 全社展開・運用定着・効果測定"
  ],
  "visual": {
    "labels": ["Phase 0\nPoC", "Phase 1\n基盤構築", "Phase 2\n全社展開"],
    "emphasis": "left_to_right"
  }
}
```

### traffic_light（信号式ステータス）

```json
{
  "index": 13, "type": "content",
  "title": "各領域の進捗ステータス",
  "message": "開発は順調、テストに遅延リスク、インフラは完了",
  "pattern": "traffic_light",
  "tone": "neutral",
  "body_points": [
    "開発: 予定通り進行中（完了率85%）",
    "テスト: 一部遅延あり（テストデータ準備に課題）",
    "インフラ: 完了（本番環境構築済み）",
    "トレーニング: 未着手（Phase 2で実施予定）"
  ],
  "visual": {
    "labels": ["開発", "テスト", "インフラ", "トレーニング"],
    "status": ["green", "yellow", "green", "gray"],
    "emphasis": "equal"
  }
}
```

### team_profile（チーム紹介）

```json
{
  "index": 14, "type": "content",
  "title": "プロジェクト推進メンバー",
  "message": "各領域の専門家がワンチームで支援",
  "pattern": "team_profile",
  "tone": "neutral",
  "body_points": [
    "PM: プロジェクト全体統括、クライアント窓口",
    "テックリード: アーキテクチャ設計、技術選定",
    "UXデザイナー: ユーザー調査、UI設計",
    "データサイエンティスト: 分析基盤構築、AI/ML実装"
  ],
  "visual": {
    "labels": ["PM", "テックリード", "UXデザイナー", "データサイエンティスト"],
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
  ├→ スコープ・定義の整理 → いくつの属性？
  │   ├→ 3〜5属性（目的/ゴール/体制等） → row_label_content (tone: neutral)
  │   └→ 多列定義（項目×作業×成果物等） → matrix_table (tone: neutral)
  │
  ├→ 並行プロセス・複数フェーズ → swimlane_process (tone: progression)
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
| `row_label_content` | N行の「label box + text area」 |
| `swimlane_process` | N行の「lane_label + process_flow」 |
| `matrix_table` | ヘッダー行 + N データ行（各行に複数セル） |

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

## 8. 参照ライブラリの活用

### 参照ライブラリとは

`refs/` ディレクトリに登録された過去の優良スライドのこと。
`refs/index.json` に全参照作品が一覧されている。

```
refs/
├── index.json               ← 全参照作品の目次（purpose, tags, summary 付き）
├── sx/
│   ├── sx_ctc_jre_suica/    ← JRE様 Suica 提案書（19枚）
│   │   ├── analysis.json    ← 構造分析（機械可読）
│   │   └── thumbnails/      ← PNG サムネイル（目視確認用）
│   └── sx_ai_callcenter/    ← コールセンター AI 提案書（22枚）
├── jr/
│   └── jr_20251209_teireikai/ ← JR 全体定例会（27枚）
└── thinkcell/               ← think-cell パターンカタログ（249枚）
    ├── _analysis_summary.json ← 全パターンの構造分析
    └── pattern_taxonomy.md    ← パターン分類体系と既存マッピング
```

### 参照作品のメタデータ構造

`refs/index.json` の各エントリには以下のフィールドがある:

| フィールド | 説明 | 用途 |
|---|---|---|
| `purpose` | 1文の自由記述（用途・文脈） | 口語指示とのマッチング |
| `tags` | 検索用キーワード配列 | タグベースのフィルタリング |
| `summary.tone` | 文書のトーン（formal_proposal, internal_report 等） | アウトラインのトーン設定 |
| `summary.structure_pattern` | 構成パターン名 | 章立ての前提ルール |
| `summary.chapter_flow` | 章の流れ配列 | アウトラインの骨格 |
| `summary.premise_rules` | 前提ルール配列 | アウトライン生成時の制約条件 |
| `summary.notable_patterns` | 使用されている recipe パターン | スライド設計のヒント |

### アウトライン生成前の参照マッチング手順

**ユーザーが資料作成を依頼したら、Tier 1 生成の前に以下を実行する。**

#### ステップ1: 口語指示からタグを抽出

ユーザーの指示を分析し、以下の軸でタグを推定する:

| 軸 | 例 |
|---|---|
| 文書タイプ | 提案, 報告, 企画, 研修, 定例, 調査 |
| トピック | AI, DX, コールセンター, 業務改善, 新規事業 |
| 対象 | 新規クライアント, 既存クライアント, 社内, 経営層 |
| トーン | フォーマル, カジュアル, 報告調, 訴求調 |

例: 「JR向けの月次定例報告を作りたい」→ `[報告, 定例, JR, 月次, 進捗]`

#### ステップ2: refs/index.json で参照をマッチング

1. `refs/index.json` を Read
2. 各参照の `tags` とステップ1で抽出したタグの重なりをチェック
3. `purpose` のセマンティックな類似度も考慮
4. マッチした参照をユーザーに提示:

```
参照候補:
- jr_20251209_teireikai（JR全体定例会, 27枚）— tags一致: 報告, 定例
  構成: 表紙→目次→[章扉→コンテンツ]繰り返し

この参照をベースにアウトラインを作成しますか？
```

#### ステップ3: 前提ルールの注入

マッチした参照の `summary.premise_rules` をアウトライン生成の制約として使う:

```
# アウトライン生成時の前提（jr_20251209_teireikai より）
- 目次スライドを章扉として再利用し、現在の章をハイライト
- 報告調のトーン（状況→課題→次アクション）
- 複数チーム/領域を同じフォーマットで並列に報告
- 詳細よりも概況把握を優先した情報密度
```

`summary.chapter_flow` は章立ての叩き台として使い、ユーザーの指示に応じて調整する。

#### ステップ4: マッチ結果なしの場合

タグがどの参照とも一致しない場合:
1. think-cell カタログ（`refs/thinkcell/pattern_taxonomy.md`）を参照して適切なパターンを提案
2. 新しい文書タイプとして汎用的なアウトラインを生成
3. 完成後に参照ライブラリへの登録を検討

### レシピ生成時の参照活用

レシピ生成時にも参照を活用できる:

1. マッチした参照の `summary.notable_patterns` を確認
2. 該当スライドの `analysis.json` で具体的な構造を確認
3. サムネイルを Read して視覚確認（1枚ずつ、一括読み込み禁止）
4. レシピに `reference` フィールドを追加:

```json
{
  "reference": {
    "ref_id": "sx_ai_callcenter",
    "ref_slide": 5,
    "adaptation": "スライド5の row_label_content 構造を参照。ラベルを4→3行に変更し、目的をより明確化"
  }
}
```

### パターン発見の記録

参照を見て「これはカタログにないパターンだ」と思ったら:
1. このファイル（slide_recipe.md）のパターンカタログに追記
2. 参照作品のスライド番号と参照IDをコメントとして残す
3. think-cell カタログとの対応があれば `pattern_taxonomy.md` にも追記

---

## 9. レシピ品質チェック

レシピ生成後、以下を確認:

- [ ] `pattern` がパターンカタログに存在するか
- [ ] `tone` がスライドの内容と合っているか（課題に solution を使っていないか）
- [ ] `body_points` が 3〜5 項目、各 30〜50 文字か
- [ ] `visual.labels` の数が pattern に合っているか（three_column なら 3 つ）
- [ ] `message` が 40〜70 文字で、結論を含んでいるか
- [ ] 同じデッキ内で同じ pattern が連続していないか（単調さを回避）
