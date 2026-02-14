# 開発ロードマップ

> 最終更新: 2026-02-14 | ビジョン: [docs/vision.md](vision.md)

## 現在地

PPTX生成の3層アーキテクチャ（Tier 1 → Recipe → Tier 2 → Assembly）が動作する状態。
2テンプレート対応（sx_proposal, jr_east）。対話ベースの制作ワークフローが確立。

**次に取り組むべきこと**: Phase 3（参照ライブラリ）

| フェーズ | 回顧録 |
|---|---|
| Phase 0 + Phase 1 | [retrospective_phase1_20260214.md](retrospective_phase1_20260214.md) |
| Phase 2 | [retrospective_phase2_20260214.md](retrospective_phase2_20260214.md) |

---

## Phase 0: 知識の外部化 — 「なぜ」を残す

**目的**: 別のAI・人間が「このプロジェクトが何を目指しているか」を理解できる状態にする。

**背景**: 現在の設計思想・判断理由はチャットセッション内にしか存在しない。セッションが終わると消える。

### 成果物

| ファイル | 内容 | 状態 |
|---|---|---|
| `docs/vision.md` | プロジェクトビジョン（Q1-Q6の結論を圧縮） | 完了 |
| `docs/discussion_20260214.md` | ビジョン策定ディスカッション記録 | 完了 |
| `docs/ROADMAP.md` | 本ファイル | 完了 |
| `README.md` | プロジェクト概要・セットアップ・使い方 | 完了 |
| `docs/adr/001_three_tier_process.md` | ADR: なぜ3層にしたか | 完了 |
| `docs/adr/002_recipe_layer.md` | ADR: なぜRecipe層を追加したか | 完了 |
| `docs/adr/003_skills_on_demand.md` | ADR: なぜSkillsをオンデマンドにしたか | 完了 |
| `docs/adr/004_git_all_files.md` | ADR: なぜ全ファイルgit管理にしたか | 完了 |
| `docs/adr/005_template_dual_definition.md` | ADR: なぜ二重定義（JSON+MD）か | 完了 |

### 完了条件
- [x] README.md にセットアップ手順と基本的な使い方が記載されている
- [x] ADR が最低3本作成されている（5本作成）
- [x] 新規参加者が docs/ を読んで「何を目指しているか」「なぜこう作ったか」を理解できる

---

## Phase 1: 契約の定義 — 「何を出力すべきか」を定義する

**目的**: 任意のAI・人間が正しい形式で成果物を生成できる状態にする。

**背景**: JSON形式はCLAUDE.mdに自然言語で記述されている。機械的に検証できない。

### 成果物

| ファイル | 内容 |
|---|---|
| `schemas/outline.schema.json` | Tier 1 アウトラインの JSON Schema |
| `schemas/recipe.schema.json` | Recipe の JSON Schema |
| `schemas/tier2.schema.json` | Tier 2 スライドJSONの JSON Schema |
| `schemas/evaluation.schema.json` | 評価結果の JSON Schema（Phase 4 準備） |
| `docs/WORKFLOW.md` | エージェント非依存のプロセス定義 |
| `CONTRIBUTING.md` | 参加方法（人間向け・AI向けオンボーディング） |

### 完了条件
- [x] 各 Schema で既存の JSON ファイルがバリデーションを通る（40/40 通過確認済み）
- [x] WORKFLOW.md が Claude Code 以外のAIでも理解・実行可能な記述になっている
- [x] CONTRIBUTING.md に AI 向けオンボーディング順序が記載されている

---

## Phase 2: 自動化基盤 — PRを出せば検証される

**目的**: GitHub Actionsで自動的にバリデーション・結合・品質チェックが走る状態にする。

**背景**: 現在は全て手動CLI実行。複数人・複数AIが参加するには自動化が必須。

### 成果物

| ファイル | 内容 |
|---|---|
| `.github/workflows/validate.yml` | JSON Schema バリデーション |
| `.github/workflows/assemble.yml` | PPTX 自動結合 + サムネイル生成 |
| `.github/workflows/quality.yml` | 形式的品質チェック（情報密度等） |
| `requirements.txt` | Python 依存パッケージ定義 |

### 完了条件
- [x] Tier 2 ファイルの PR に対して自動バリデーションが走る
- [x] バリデーション通過後に自動で PPTX が結合される
- [x] 品質チェック結果が PR コメントに表示される

### 前提条件
- Phase 1 の JSON Schema が完成していること

---

## Phase 3: 参照ライブラリ — 手本を見て作る

**目的**: 良い作品から学び、模倣→昇華のフローを実現する。

**背景**: 現在のシステムは毎回ゼロから「発明」している。人間のデザイナーが持つ「見てきた良い作品の記憶」に相当するものがない。

### 成果物

| ファイル | 内容 |
|---|---|
| 参照分析ツール | 既存PPTXからRecipeを逆算するスクリプト |
| `refs/` ディレクトリ | 参照作品ライブラリ（分析結果 + サムネイル） |
| Recipe `reference` フィールド | 何を参照して何を変えたかの記録 |
| パターンカタログ拡充 | 参照から抽出した新パターンを slide_recipe.md に追加 |

### 完了条件
- [ ] 最低3つの参照作品が分析・登録されている
- [ ] Recipe 生成時に参照作品を提示するフローが機能する
- [ ] 「この参照をベースに、ここを変える」というディスカッションが成立する

### 前提条件
- Phase 0 が完了していること（最低限）
- 参照として使える優良な PPTX 作品があること

---

## Phase 4: 自己改善ループ — 形式的品質のAI自律改善

**目的**: 生成→評価→修正のループをAIが自律的に回せる状態にする（形式的品質のみ）。

**背景**: 現在の評価は全て人間がトリガーを引いている。形式的品質（情報密度、配置バランス等）はルール化できるため、AI自律で回せるはず。

### 成果物

| ファイル | 内容 |
|---|---|
| `skills/evaluation_format.md` | 構造化された評価出力フォーマット |
| `skills/correction_strategies.md` | 問題→修正方法の戦略マップ |
| 自動評価スクリプト | Tier 2 JSON を読んで形式的品質を評価 |
| 停止条件の定義 | 改善ループの終了判定基準 |

### 完了条件
- [ ] Tier 2 JSON に対して形式的品質評価が自動実行される
- [ ] 評価結果に基づいた修正提案が生成される
- [ ] 3回以内のループで品質スコアが改善する（改悪しない）
- [ ] 人間は意味的品質の判断のみに集中できる

### 前提条件
- Phase 1 の evaluation.schema.json が定義されていること
- Phase 2 の自動化基盤が動いていること

---

## フェーズ間の依存関係

```
Phase 0 ──→ Phase 1 ──→ Phase 2 ──→ Phase 4
   │                                    ↑
   └──────→ Phase 3 ───────────────────┘
```

- Phase 0 は全ての前提条件
- Phase 1 → 2 → 4 は順序依存（スキーマ→自動化→自己改善）
- Phase 3（参照ライブラリ）は Phase 0 完了後ならいつでも開始可能
- Phase 3 の成果は Phase 4 の「学習」ステップに接続する

---

## 備考

- 各 Phase の詳細タスク分解は、そのフェーズに着手するときに行う（今全部書かない）
- Phase の進捗は `docs/assessment_YYYYMMDD.md` で定期的に評価する
- このロードマップ自体も定期的に見直す
