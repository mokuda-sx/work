# think-cell Pattern Taxonomy

> 分析日: 2026-02-16 | 分析: Claude Code (Opus 4.6)
> 元データ: refs/thinkcell/_analysis_summary.json (26 files, 249 slides)

## 概要

think-cellのスライドテンプレートライブラリを分析し、スライドパターンの分類体系を整理した。
現在の `slide_recipe.md` のパターンカタログ（17種）との対応を示し、追加すべきパターンを特定する。

---

## 1. think-cell カテゴリ → 既存パターンマッピング

### A. プロセス・フロー系（43 slides）

| think-cell パターン | 既存 recipe pattern | 備考 |
|---|---|---|
| Process flow | `process_flow` | 既存でカバー |
| Process flow with swim lanes | `swimlane_process` | 既存でカバー |
| Process stages | `process_flow` | ステージ表現 |
| Infographic process I-VII | `process_flow` | インフォグラフィック調 |
| Infographic process with highlight | - | **新規候補**: 強調付きプロセス |
| Infographic process with results | - | **新規候補**: 結果付きプロセス |
| Four steps | `four_column` | 既存でカバー |
| Path | `process_flow` | 既存でカバー |
| Numbered process | `process_flow` | 番号付き |
| Circular sprint / Circular text | - | **新規候補**: `circular_flow` |
| Process circle | - | **新規候補**: 円形プロセス |
| Value chain I-III | - | **新規候補**: `value_chain` |
| Customer journey / dashboard | - | **新規候補**: `customer_journey` |
| Swim lane, complex | `swimlane_process` | 既存の拡張 |
| Building blocks | `matrix_table` | 既存で近似可能 |
| Cause and effect I-VI | - | **新規候補**: `cause_effect` |
| Phases/processes | `process_flow` | 既存でカバー |
| Circular arrows, cycles | - | **新規候補**: `circular_flow` |
| Circle segments I-II | - | 円グラフ的分割 |

### B. ダイアグラム系（34 slides）

| think-cell パターン | 既存 recipe pattern | 備考 |
|---|---|---|
| Funnel I-III | `funnel` | 既存でカバー |
| Funnel, horizontal | `funnel` | 横向きバリエーション |
| Funnel dashboard | `funnel` + `kpi_cards` | 複合パターン |
| Organigram / Hierarchy tree | - | **新規候補**: `org_chart` |
| Decision tree | - | **新規候補**: `decision_tree` |
| Problem tree | - | `cause_effect` で近似可能 |
| Pyramid (3D/flat/cropped) | `pyramid` | 既存でカバー |
| Ziggurat diagram | `pyramid` | バリエーション |
| Triangles with text | `pyramid` | バリエーション |
| Core elements | - | **新規候補**: `core_elements`（中心+周辺） |
| Sunburst diagram | - | 階層円グラフ（実装困難） |
| Spiderweb/Radar | - | レーダーチャート（実装困難） |
| Venn diagram | - | **新規候補**: `venn` |

### C. マトリクス・SWOT（12 slides）

| think-cell パターン | 既存 recipe pattern | 備考 |
|---|---|---|
| Matrix: Good/neutral/bad | `matrix_2x2` | 既存でカバー |
| Matrix: Four blocks I-II | `matrix_2x2` | 既存でカバー |
| Matrix: Nine blocks | - | **新規候補**: `matrix_3x3` |
| Aspect matrix | `matrix_table` | 既存でカバー |
| Icon matrix | `matrix_table` | アイコン付き |
| Process matrix | `matrix_table` + `process_flow` | 複合 |
| SWOT analysis I-III | `swot` | 既存でカバー |
| SWOT analysis dashboard | `swot` + `kpi_cards` | 複合 |

### D. ダッシュボード・統計（5 slides）

| think-cell パターン | 既存 recipe pattern | 備考 |
|---|---|---|
| Dashboard | `kpi_cards` | 既存で近似 |
| Traffic light dashboard | - | **新規候補**: `traffic_light` |
| Management summary | `kpi_cards` | 既存でカバー |
| Stats dashboard | `kpi_cards` | 既存でカバー |

### E. インフォグラフィック・数値（11 slides）

| think-cell パターン | 既存 recipe pattern | 備考 |
|---|---|---|
| Target market | `kpi_cards` | 近似 |
| Supply chain management | `process_flow` | 近似 |
| Density / 100 people | - | ピクトグラム（実装困難） |
| Quantity comparison | `kpi_cards` | 数値比較 |
| Comparison of percentages | `kpi_cards` | 近似 |
| Ring diagrams | - | 円グラフ（think-cell固有） |
| Barometers | - | ゲージ（実装困難） |
| Goal | `kpi_cards` | 近似 |
| Iceberg | - | **新規候補**: `iceberg`（見える/見えない） |

### F. テーブル（5 slides）

| think-cell パターン | 既存 recipe pattern | 備考 |
|---|---|---|
| Table with header | `matrix_table` | 既存でカバー |
| Sectioned summary | `row_label_content` | 既存でカバー |
| Table 4-5 columns | `matrix_table` | 既存でカバー |

### G. タイムライン（16 slides）

| think-cell パターン | 既存 recipe pattern | 備考 |
|---|---|---|
| Timeline / Historical | `timeline` | 既存でカバー |
| Timeline with slide transitions | `timeline` | アニメーション系 |
| Status timeline | `timeline` | 状態表示付き |
| Milestones I-II | `timeline` | マイルストーン強調 |
| Road map | - | **新規候補**: `roadmap`（timeline拡張） |
| Sprint planning | `swimlane_process` | アジャイル系 |
| Calendar dashboards | - | カレンダー（実装困難） |

### H. メンタルモデル・フレームワーク（19 slides）

| think-cell パターン | 既存 recipe pattern | 備考 |
|---|---|---|
| Honeycomb | - | **新規候補**: `honeycomb`（六角形グリッド） |
| Puzzle | - | パズルピース（実装困難） |
| Pillar text box | `three_column` | 柱状レイアウト |
| Business model | `matrix_table` | 近似 |
| Pros and cons I-III | `two_column` | 既存でカバー |
| Five steps / Buildup / Stairs | `process_flow` | ステップ系 |
| Ladder to goal | `process_flow` + `pyramid` | 複合 |
| Radiate | - | **新規候補**: `radiate`（中心→放射） |
| Mind map | - | **新規候補**: `mind_map` |
| Circle with numbered text | - | `circular_flow` で近似可能 |

### I. アジェンダ・スケジュール（11 slides）

| think-cell パターン | 既存 recipe pattern | 備考 |
|---|---|---|
| Agenda I-III | agenda type | 既存 type でカバー |
| Agenda with icons | - | アイコン付きアジェンダ |
| Table of contents | agenda type | 既存でカバー |
| Schedule I-IV | `matrix_table` | 表形式スケジュール |
| Dashboard schedule | `kpi_cards` + `timeline` | 複合 |

### J. チーム紹介（10 slides）

| think-cell パターン | 既存 recipe pattern | 備考 |
|---|---|---|
| Team slide (various) | - | **新規候補**: `team_profile` |
| Business cards | - | `team_profile` バリエーション |
| Personal profile | - | `team_profile` バリエーション |

### K. テキストボックス（14 slides）

| think-cell パターン | 既存 recipe pattern | 備考 |
|---|---|---|
| Text boxes with pictures | `text_and_image` | 既存で近似 |
| Assessment | `matrix_2x2` | 評価マトリクス |
| Building blocks | `three_column` / `four_column` | 既存でカバー |
| Goals / Objectives | `kpi_cards` | 近似 |
| Matrix/prioritization 2x2/2x3 | `matrix_2x2` | 既存でカバー |
| Text boxes with enumeration | `row_label_content` | 既存でカバー |

### L. think-cell チャート（37 slides）

チャート系は think-cell 拡張機能依存のため、我々のobjectsベースでは直接再現不可。
ただし「どんなデータ表現が求められるか」のカタログとしては参考になる。

| サブカテゴリ | slides | 用途 |
|---|---|---|
| Bar, Column | 9 | 時系列/比較/構成比 |
| Line, Area | 8 | 時系列トレンド |
| Pie, Doughnut | 3 | 構成比 |
| Mekko | 2 | 二次元構成比 |
| Scatter, Bubble | 2 | 相関/比較 |
| Waterfall | 3 | 要因分解 |
| Timeline, Gantt | 3 | プロジェクト管理 |
| Annotations | 7 | チャート注釈 |

### M. 地図・形状（30 slides）

| サブカテゴリ | slides | 備考 |
|---|---|---|
| Maps | 24 | 地理的分布。画像生成で対応可能 |
| Shapes, Icons | 6 | 素材パーツ |

---

## 2. 追加すべきパターン（優先順位付き）

### 優先度A: 提案書で頻出、objects で実装可能

| パターン名 | 説明 | think-cell の例 |
|---|---|---|
| `circular_flow` | 循環プロセス（PDCA等） | Circular sprint, Process circle, Circular arrows |
| `value_chain` | バリューチェーン（横長の連結ブロック） | Value chain I-III |
| `cause_effect` | 原因→結果の構造 | Cause and effect I-VI |
| `roadmap` | 時系列ロードマップ（timeline 拡張） | Road map |
| `traffic_light` | 信号式ステータス（赤黄緑） | Traffic light dashboard |
| `team_profile` | チームメンバー紹介 | Team slide variants |

### 優先度B: ニッチだが有用、objects で実装可能

| パターン名 | 説明 | think-cell の例 |
|---|---|---|
| `org_chart` | 組織図・ツリー構造 | Organigram, Hierarchy tree |
| `decision_tree` | 意思決定ツリー | Decision tree |
| `venn` | ベン図（2-3円の重なり） | Venn diagram |
| `iceberg` | 表層/深層の対比 | Iceberg |
| `radiate` | 中心から放射状に展開 | Radiate |
| `mind_map` | マインドマップ的展開 | Mind map |
| `matrix_3x3` | 3x3 グリッド | Matrix: Nine blocks |
| `honeycomb` | 六角形グリッド | Honeycomb |

### 優先度C: 実装困難（think-cell/チャート依存）

- Sunburst, Radar/Spiderweb: 複雑な図形
- Calendar: グリッド密度が高すぎる
- Pie/Doughnut/Mekko/Waterfall: チャートライブラリ必要
- Puzzle pieces: 不定形の図形
- Pictogram (100 people): 大量の小アイコン

---

## 3. 既存パターンのカバレッジ分析

| 既存パターン | think-cell でのカバー率 | 備考 |
|---|---|---|
| `bullet_list` | - | think-cell にはない（テキスト主体は対象外） |
| `text_and_image` | Low | Text boxes with pictures (3) |
| `two_column` | Medium | Pros and cons (3) |
| `three_column` | Medium | Pillar text box, Building blocks |
| `four_column` | Medium | Four steps |
| `process_flow` | **Very High** | 43 slides のプロセス系全般 |
| `before_after` | Low | 明示的な Before/After は少ない |
| `matrix_2x2` | High | Matrix, SWOT, Assessment |
| `pyramid` | High | 11 slides のピラミッド系 |
| `kpi_cards` | Medium | Dashboard, Stats, Goal |
| `single_message` | Low | Quote (3) |
| `row_label_content` | Medium | Sectioned summary, Enumeration |
| `swimlane_process` | Medium | Swim lane (2) |
| `matrix_table` | High | Table, Schedule |
| `swot` | High | SWOT analysis (4) |
| `funnel` | High | Funnel (6) |
| `timeline` | **Very High** | Timeline (16) |

---

## 4. 結論

1. **既存17パターンで think-cell の約60%をカバー**。特にプロセス・タイムライン・マトリクス系は充実
2. **追加すべきは優先度Aの6パターン**: circular_flow, value_chain, cause_effect, roadmap, traffic_light, team_profile
3. **think-cell チャート系（37 slides）はobjectsベースでは再現不可**だが、将来的に画像生成で対応する余地あり
4. **シンクセルの分類体系そのものが参照メタデータのタグ設計に使える**: カテゴリ名がそのまま意味的タグになる
