# 現在の状態

> 最終更新: 2026-02-14 | 更新者: Claude Code (Sonnet 4.5) | Phase: 2

## 今どこにいるか

**Phase 1: 契約の定義** — **完了**
**Phase 2: 自動化基盤** — **進行中**

ロードマップ全体: [docs/ROADMAP.md](docs/ROADMAP.md)

## 完了したこと

- [x] リポジトリ整理（v2削除、テストスクリプト統合、ルート清掃）
- [x] git管理方針変更（全ファイル追跡、gitignore簡素化）
- [x] システム評価 → [docs/assessment_20260214.md](docs/assessment_20260214.md)
- [x] ビジョン策定ディスカッション（Q1-Q8）→ [docs/discussion_20260214.md](docs/discussion_20260214.md)
- [x] ビジョン文書 → [docs/vision.md](docs/vision.md)
- [x] 開発ロードマップ → [docs/ROADMAP.md](docs/ROADMAP.md)
- [x] README.md 整備 — プロジェクト概要、セットアップ手順、CLI使い方
- [x] ADR 5本作成 → [docs/adr/](docs/adr/)
- [x] オンボーディングテスト → STATUS.md に組み込み済み
- [x] JSON Schema 3本 → [schemas/](schemas/)（既存40ファイルで全通過確認済み）
  - outline.schema.json, recipe.schema.json, tier2.schema.json
- [x] validate_schemas.py — バリデーション実行スクリプト
- [x] docs/WORKFLOW.md — エージェント非依存のプロセス定義
- [x] CONTRIBUTING.md — 人間向け・AI向け参加ガイド
- [x] requirements.txt — 依存パッケージ定義
- [x] .github/workflows/validate.yml — Schema バリデーション自動実行
- [x] .github/workflows/assemble.yml — PPTX 自動結合ワークフロー

## 次にやること

### Phase 2: 自動化基盤（続き）

自動化基盤の残タスクへ進む。

1. [x] Schema バリデーション（PR 時に自動実行）
2. [x] PPTX アセンブル（手動トリガーで実装済み）
3. [ ] 品質チェック（フォーマル評価の自動化）

## 未来の自分（次セッションのAI）への指示

### ステップ1: 読み込み（必須）

以下のファイルを順番に読む。スキップ禁止。

1. このファイル（STATUS.md）— 現在地の把握
2. [docs/vision.md](docs/vision.md) — プロジェクトの本質
3. [docs/ROADMAP.md](docs/ROADMAP.md) — 現在のフェーズと完了条件
4. [docs/adr/](docs/adr/) から最低2本 — 設計判断の理由

### ステップ2: オンボーディングテスト（必須）

**作業を開始する前に、以下の質問にユーザーへ回答を提示すること。**
ユーザーが承認するまで、コードの変更・ファイル作成に進んではならない。

#### Q1: プロジェクトの本質
> このプロジェクトは何か？ 「PowerPoint自動生成ツール」ではない理由を1-2文で説明せよ。

#### Q2: 3層アーキテクチャの「なぜ」
> Tier 1 → Recipe → Tier 2 に分離した理由を説明せよ。Recipe層が解決する具体的な問題は何か？

#### Q3: 現在の状態
> 現在のフェーズは何か？ そのフェーズの完了条件を列挙せよ。

#### Q4: ファイル検証
> 以下を実際にファイルシステムで確認し、結果を報告せよ:
> - `docs/adr/` にADRファイルが何本あるか（ファイル名を列挙）
> - `README.md` の内容が正しいか（削除済み機能の記述がないか）
> - Streamlit UI（app.py）は存在するか

### ステップ3: 作業開始

テスト通過後、「次にやること」セクションのタスクに着手する。

**作業ルール**:
- 作業完了ごとにこのファイルを更新する
- 「完了」と書く前に、成果物の内容が正しいか必ず検証する
- セッション終了前に必ずコミット・プッシュする

## リカバリ手順（セッションが中断した場合）

### 状態の確認

```bash
# 未コミットの変更があるか
git status

# 未プッシュのコミットがあるか
git log --oneline origin/main..HEAD

# 最後のコミットメッセージで何をしていたか
git log --oneline -5
```

### 中断パターン別の対応

**A. 未コミットの変更が残っている場合**
- `git diff` で変更内容を確認
- 完成しているファイルだけ `git add` → コミット
- 未完成の変更は内容を確認して判断（破棄 or 継続）

**B. コミット済み・未プッシュの場合**
- `git log --oneline origin/main..HEAD` で内容を確認
- 品質に問題なければそのまま `git push`
- 問題があれば `git reset` で戻してやり直す

**C. 前任のAIが壊れた成果物を残した場合**
- `git log --oneline origin/main..HEAD` で未プッシュのコミットを特定
- `git diff <commit>..HEAD --stat` で変更範囲を確認
- 問題のあるコミットまで `git reset --hard <good_commit>` で戻す
- STATUS.md の「完了したこと」と実際のファイル状態が一致するか検証する

### 検証チェックリスト

STATUS.md を信用する前に、以下を確認:
- [ ] 「完了」と書かれたファイルが実際に存在し、内容が正しいか
- [ ] 空ファイルや内容が重複したファイルがないか
- [ ] README.md に削除済み機能の記述がないか
- [ ] ADR が docs/adr/ に配置されているか（ルート直下ではないか）
