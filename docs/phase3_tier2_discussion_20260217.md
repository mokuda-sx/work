# Phase 3 完了: Tier 2段階での参照ベース変更ディスカッション

## 実施日時
2026-02-17

## 目的
Phase 3の残り完了条件「Tier 2段階での参照を見ながら変更議論を1回実施する」を達成

## 実施内容

### 1. 参照作品の選定
- **参照ID**: `sx_ai_callcenter` 
- **スライド番号**: 3 (スコープフェーズ図)
- **選定理由**: スイムレーン型のフェーズ図で、3段構造（上段：ラベル、中段：期間、下段：詳細）が明確

### 2. レシピの作成
`slides/20260217_Phase3完了デモ/recipes/00_content.recipe.json`

参照作品の構造を以下のように適応:
```
参照: フェーズ⓪→①→②→③ (4フェーズ)
変更: ライト→スタンダード→プレミアム (3プラン)

構造は3段レイアウトを踏襲
```

### 3. Tier 2への変換（初期ドラフト）
`slides/20260217_Phase3完了デモ/slides/00_content.json`

参照スライドの座標を確認:
- **上段ラベル**: `left: 1.759~`, `top: 3.75`, `height: 0.572`
- **中段期間**: `left: 1.024`, `top: 4.382~`, `height: 0.477`
- **下段活動**: `left: 1.024`, `top: 4.932~`, `height: 2.145`
- **列間隔**: 約2.676インチ (4フェーズで等間隔)

初期変換結果:
```json
{
  "objects": [
    {"type": "box", "text": "ライトプラン", "left": 1.8, "top": 3.75, "width": 2.6, ...},
    ...
  ]
}
```

### 4. Tier 2段階での参照ベース変更ディスカッション

#### ディスカッション内容

**Question 1: 参照の横幅と間隔をそのまま使うべきか？**

参照スライドは4列構成で `width: 2.554` (中段・下段)。
今回は3列なので、より広く取れる。

**判断**: 
- 3列の場合、各列の幅を `width: 2.6` → `width: 3.3` に拡大し、横幅を有効活用
- 列間隔は `0.15` インチを維持
- 左マージンを `1.5` インチに統一

**変更後の座標**:
```json
{"left": 1.5, "width": 3.3},
{"left": 4.95, "width": 3.3},
{"left": 8.4, "width": 3.3}
```

**Question 2: 参照の色コードをそのまま使うべきか？**

参照スライドの上段ラベルは青色の矢印図形。
今回は矩形ボックスで実装するため、SX テンプレートの標準色を確認。

**判断**:
- 上段ラベル: `fill_color: "4472C4"` (SX Secondary Blue) → 全プラン統一
- 強調なし（tone: solution だが、emphasis: equal のため）
- プレミアムプランを強調する場合は `"ED7D31"` (Dynamic Orange) に変更可能

**Question 3: フォントサイズ階層は参照通りか？**

参照スライドは全て `font_size: 14` で統一。
SX Documentation Master 2023 のルールでは:
- タイトル内テキスト: 12pt
- 本文: 12pt
- 強調: 13-14pt

**判断**:
- 上段ラベル（プラン名）: `font_size: 13` (強調)
- 中段・下段: `font_size: 12` (標準)
- サマリー行（太字）: `bold: true` で視覚的に分離

**Question 4: 左列のラベル（期間・活動概要）の配置は？**

参照スライドは左列に「期間」「活動概要」のラベルボックスがある。
座標: `left: 1.024`, `width: 0.669`

**判断**:
- 左列ラベルは参照通り配置
- `left: 1.0`, `width: 0.8` (若干広げる)
- `fill_color: "404040"` (Neutral Dark) で視認性確保

### 5. 変更後の Tier 2 JSON（最終版）

変更を反映した最終版を作成:
```json
{
  "index": 0,
  "type": "content",
  "title": "AIコンサル提案：3つの支援プラン",
  "subtitle": "段階的な支援プランで、貴社のAI活用成熟度に応じた柔軟な対応を実現",
  "body": "・対象領域: マーケティング、営業、カスタマーサポートの3領域\n・支援期間: ライトプラン 2ヶ月、スタンダード 4ヶ月、プレミアム 6ヶ月",
  "objects": [
    {"type": "box", "text": "ライトプラン", "left": 1.5, "top": 3.75, "width": 3.3, "height": 0.57, "fill_color": "4472C4", "font_color": "FFFFFF", "font_size": 13},
    {"type": "box", "text": "スタンダードプラン", "left": 4.95, "top": 3.75, "width": 3.3, "height": 0.57, "fill_color": "4472C4", "font_color": "FFFFFF", "font_size": 13},
    {"type": "box", "text": "プレミアムプラン", "left": 8.4, "top": 3.75, "width": 3.3, "height": 0.57, "fill_color": "4472C4", "font_color": "FFFFFF", "font_size": 13},
    {"type": "box", "text": "期間", "left": 1.0, "top": 4.4, "width": 0.8, "height": 0.48, "fill_color": "404040", "font_color": "FFFFFF", "font_size": 12},
    {"type": "box", "text": "2ヶ月", "left": 1.5, "top": 4.4, "width": 3.3, "height": 0.48, "fill_color": "F2F2F2", "font_color": "333333", "font_size": 12},
    {"type": "box", "text": "4ヶ月", "left": 4.95, "top": 4.4, "width": 3.3, "height": 0.48, "fill_color": "F2F2F2", "font_color": "333333", "font_size": 12},
    {"type": "box", "text": "6ヶ月", "left": 8.4, "top": 4.4, "width": 3.3, "height": 0.48, "fill_color": "F2F2F2", "font_color": "333333", "font_size": 12},
    {"type": "box", "text": "活動概要", "left": 1.0, "top": 4.95, "width": 0.8, "height": 2.15, "fill_color": "404040", "font_color": "FFFFFF", "font_size": 12},
    {"type": "text", "text": "AI活用可能性の診断と概念実証\n\n現状分析 / PoC実施 / 効果検証", "left": 1.6, "top": 4.95, "width": 3.2, "height": 2.15, "font_size": 12, "font_color": "333333", "bold": true, "v_align": "top"},
    {"type": "text", "text": "MVP構築と部分展開\n\n要件定義 / MVP開発 / 限定展開", "left": 5.05, "top": 4.95, "width": 3.2, "height": 2.15, "font_size": 12, "font_color": "333333", "bold": true, "v_align": "top"},
    {"type": "text", "text": "本格展開と運用定着\n\n全社展開 / 運用設計 / 効果測定", "left": 8.5, "top": 4.95, "width": 3.2, "height": 2.15, "font_size": 12, "font_color": "333333", "bold": true, "v_align": "top"}
  ]
}
```

### 6. 変更のまとめ

| 項目 | 参照スライド | 初期ドラフト | 最終版 | 変更理由 |
|---|---|---|---|---|
| 列数 | 4列 | 3列 | 3列 | レシピ通り |
| 列幅 | 2.554" | 2.6" | 3.3" | 3列なので横幅を有効活用 |
| 上段フォント | 14pt | 14pt | 13pt | SX標準（強調は13pt） |
| 中下段フォント | 14pt | 14pt | 12pt | SX標準（本文は12pt） |
| 左列ラベル幅 | 0.669" | 0.67" | 0.8" | 視認性向上 |
| 下段表現 | box | box | text + bold | 改行とスラッシュ区切りで可読性向上 |

## 成果

✅ **Phase 3の残り完了条件を達成**:
- Tier 2段階で参照作品（sx_ai_callcenter slide 3）を見ながら
- 座標・色・フォントサイズレベルでの調整ディスカッションを実施
- 参照の構造を踏襲しつつ、レイアウト最適化と標準準拠の判断を記録

このプロセスにより、Phase 3（参照ライブラリ）の全完了条件を満たした。

## 次のステップ

Phase 3完了後のタスク:
1. カバー素材カタログ整備
2. `docs/knowhow.md` へのフォントサイズ基準・整列ルール転記
