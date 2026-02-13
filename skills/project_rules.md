# スキル: プロジェクト管理ルール

> **使い方**: プロジェクト作成・整理時に参照。通常のスライド編集では不要。

---

## 1. フォルダ構造

```
slides/
└── YYYYMMDD_テンプレート_プロジェクト名/
    ├── outline.json              ← Tier 1 アウトライン（template フィールドあり）
    ├── recipes/                  ← レシピ（テンプレート非依存の設計意図）
    │   ├── 03_content.recipe.json
    │   ├── 05_content.recipe.json
    │   └── ...
    ├── slides/                   ← Tier 2 個別スライド JSON
    │   ├── images/               ← AI生成画像キャッシュ
    │   ├── 00_title.json         ← Tier 2（定型スライドはレシピ不要）
    │   ├── 03_content.json       ← Tier 2（テンプレート固有の座標・色）
    │   └── ...
    ├── YYYYMMDD_HHMM_*.pptx     ← 生成 PPTX
    ├── thumbnails/               ← サムネイル PNG
    └── refs/                     ← 参考資料・リサーチメモ（任意）
```

### 命名規則

| 対象 | 命名パターン | 例 |
|---|---|---|
| プロジェクトフォルダ | `YYYYMMDD_<template_id>_プロジェクト名` | `20260212_sx_proposal_AI提案書自動生成システム紹介` |
| PPTX ファイル | `YYYYMMDD_HHMM_<template_id>_<プロジェクト名>.pptx` | `20260213_0708_sx_proposal_AI提案書.pptx` |
| サムネイルフォルダ | `thumbnails/` | `thumbnails/` |

### 管理ルール

1. **1フォルダ = 1テンプレート**: 同じ内容でも別テンプレートなら別フォルダ（Tier 2 JSONの色・座標・master_title等がテンプレート依存のため）
2. **全ファイル git 管理**: PPTX・サムネイル・Tier 2 JSON・画像を含め全て git で追跡する。バージョン管理は git 履歴で行う
3. **サムネイル**: `thumbnails/` に集約
4. **参考資料**: `refs/` に保存（リサーチメモ、出典リスト等）
5. **テンプレート別の Tier 2 差分**: `master_title`（JR East 等）、色コード、座標はテンプレート固有。同じ内容を別テンプレートで作る場合はレシピから再変換
6. **レシピの再利用**: 別テンプレートで同じ内容を作る場合、プロジェクトの `recipes/` からレシピを読み込み `skills/slide_recipe.md` のスキル2 で再変換する
