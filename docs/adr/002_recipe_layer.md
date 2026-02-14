# ADR 002: Recipe 層の導入

## Status
Accepted (2026-02-13)

## Context

3階層のうち、Tier 1（構成）と Tier 2（実装）だけでは「意図」が消失する問題が残った。

- Tier 1 は「このスライドは課題整理」と書いてあるだけ。どう見せるかの情報がない
- Tier 2 に直接変換すると、AI が座標を決める過程で設計意図が暗黙化する
- ユーザーとの設計ディスカッションの成果物がない（チャット履歴に埋もれる）

## Decision

Tier 1 と Tier 2 の間に **Recipe 層** を設ける。

Recipe は「設計意図の中間言語」:
- `pattern`: レイアウトパターン（three_column, comparison, flow 等）
- `tone`: 色調の方向性（problem, solution, neutral 等）
- `message`: このスライドで伝えたいこと（1文）
- `body_points`: 箇条書きの内容
- `visual.labels`: 図解のラベル

Recipe はテンプレート非依存。同じ Recipe から `sx_proposal` 用にも `jr_east` 用にも Tier 2 を生成できる。

## Consequences

- **利点**: 設計意図が保存される。テンプレート切り替えが容易。ユーザーとの設計ディスカッションの基盤になる
- **代償**: recipe → Tier 2 の変換ルールをテンプレートごとに定義する必要がある（design_guide.md の役割）
- **教訓**: 映像制作の絵コンテ、建築の設計図と同じ。分業には「共通言語」が必要

## References
- [docs/vision.md](../vision.md) 原則1「意図と実装の分離」、原則4「分業には共通言語が必要」
- [skills/slide_recipe.md](../../skills/slide_recipe.md)
