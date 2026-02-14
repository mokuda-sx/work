# ADR 004: 全生成ファイルの Git 管理ポリシー

## Status
Accepted (2026-02-14)

## Context

当初は生成物（PPTX、サムネイル PNG、Tier 2 JSON）を `.gitignore` で除外していた。

- PPTX を git 追跡しないと、成果物のバージョン管理が別途必要
- サムネイルがないと、過去の状態を視覚的に確認できない
- Tier 2 JSON を除外すると、Recipe → Tier 2 の変換結果を検証できない
- 複数 AI が協業する場合、全ファイルが git にないと状態共有ができない

## Decision

PPTX、サムネイル PNG、Tier 2 JSON、AI 生成画像を含め、全てのファイルを git で追跡する。

- `.gitignore` は最小限（`.env`、`__pycache__`、`.DS_Store` 等のみ）
- バイナリファイル（PPTX、PNG）もコミット対象
- git 履歴がバージョン管理の唯一の手段

## Consequences

- **利点**: 成果物の完全な履歴。状態の完全な共有。別セッション・別 AI からの引き継ぎが容易
- **代償**: リポジトリサイズの増大（バイナリファイル蓄積）。将来的に Git LFS 等の対策が必要になる可能性
- **監視項目**: リポジトリサイズの推移を定期評価で確認する

## References
- [docs/vision.md](../vision.md) 原則5「早い段階でレビューする」
- [docs/assessment_20260214.md](../assessment_20260214.md) 次回確認事項
