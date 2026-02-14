# ADR 005: テンプレート定義の二重化（JSON + Markdown）

## Status
Accepted (2026-02-13)

## Context

テンプレートの情報（レイアウト、色、座標、プレースホルダー）をどう管理するか。

- **エンジン（Python コード）** が必要とするのは機械可読な構造化データ
- **AI** が必要とするのは「このテンプレートでは3カラムをこう配置する」という文脈付きの説明
- 1つの形式では両方を満たせない

## Decision

テンプレート定義を2つの形式で保持する:

- **`profile.json`**（機械可読）: スライドサイズ、レイアウト名、プレースホルダー座標、画像エリア、色定義。`TemplateConfig` クラスが読み込む
- **`design_guide.md`**（AI 可読）: 図解パターン集（座標付き）、色パレットの使い分け、レイアウトルール。AI が Recipe → Tier 2 変換時に参照

両者は同じテンプレートの「同じ情報」を異なる粒度・形式で表現する。

## Consequences

- **利点**: エンジンと AI がそれぞれ最適な形式でテンプレート情報を消費できる。テンプレート追加時の作業手順が明確
- **代償**: 情報の二重管理。profile.json と design_guide.md の不整合リスク。テンプレート登録時に両方を更新する必要がある
- **緩和策**: `template_analyzer.py` で profile.json を自動生成。design_guide.md は手動だが、profile.json を参照して書く

## References
- [docs/vision.md](../vision.md) 原則4「分業には共通言語が必要」
- [docs/discussion_20260214.md](../discussion_20260214.md) Q5
