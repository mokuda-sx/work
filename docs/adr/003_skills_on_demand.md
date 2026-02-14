# ADR 003: スキルのオンデマンド読み込み

## Status
Accepted (2026-02-13)

## Context

AI の知識（デザイン原則、パターンカタログ、テンプレート座標等）を CLAUDE.md に全て記述していた。

- CLAUDE.md が肥大化（1000行超）し、メンテナンス困難
- AI のコンテキストウィンドウを常に消費（使わない知識も読み込む）
- テンプレート固有の情報と共通情報が混在

## Decision

AI 知識を外部 Markdown ファイル（Skills）に分離し、必要な時だけ Read ツールで読み込む。

**共通スキル**（`skills/`）:
- `slide_recipe.md` — レシピ生成・変換ルール
- `design_principles.md` — デザイン共通原則（CRAP等）
- `critique_rubric.md` — 診断・評価手法
- `outline_guide.md` — 構成パターン

**テンプレート固有スキル**（`templates/<id>/`）:
- `design_guide.md` — 具体的な座標・色コード・レイアウトパターン
- `profile.json` — エンジンが消費する機械可読設定

読み込みルール: CLAUDE.md に「いつ何を読むか」のトリガー条件を記述。

## Consequences

- **利点**: CLAUDE.md がコンパクトに。コンテキストの効率的利用。テンプレート追加時にスキルファイル追加だけで済む
- **代償**: AI が適切なタイミングでスキルを読み忘れるリスク。トリガー条件の設計が重要
- **教訓**: 人間のプロも「マニュアルを全暗記」せず「必要な時にリファレンスを引く」。AI のコンテキストは無限の知識ではなく有限のワーキングメモリ

## References
- [docs/vision.md](../vision.md) 原則2「AI のコンテキストは有限のワーキングメモリ」
- [CLAUDE.md](../../CLAUDE.md) スキルライブラリセクション
