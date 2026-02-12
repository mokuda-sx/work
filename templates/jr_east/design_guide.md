# JR東日本提案書 デザインガイド

> **使い方**: このテンプレートでスライドを設計する時に読む。
> 共通デザイン原則は `skills/design_principles.md` を参照。

---

## 1. スライドサイズと座標空間

```
幅: 13.333インチ  高さ: 7.5インチ（16:9）
コンテンツエリア: top 1.4〜6.7
左マージン: left >= 0.4
右端制限: left + width <= 13.0
```

---

## 2. レイアウト一覧

| type | layout index | 用途 | 画像 | テンプレート装飾 |
|---|---|---|---|---|
| `title` | 0 | 表紙（テキストのみ）| 不可 | SIGMAXYZフッター |
| `title_photo` | 1 | 表紙（KVあり）| 右半分(ph15) | 右側に画像エリア |
| `chapter` | 2 | 中表紙（章扉）| 不可 | 装飾ボックス+緑矢印が組み込み済み |
| `content` | 3 | 本紙（1行タイトル）| 自由配置可 | 緑ヘッダーバー+緑フッターバー |
| `agenda` | 3 | 目次（contentと同一）| 自由配置可 | 同上 |
| `end` | 8 | 背表紙 | 不可 | JR東日本ロゴのみ |

### プレースホルダー対応表

| type | title (ph_idx) | subtitle (ph_idx) | body (ph_idx) |
|---|---|---|---|
| `title` | 11 | 13 | - |
| `title_photo` | 11 | 13 | - |
| `chapter` | 11 | 12 | - |
| `content` | 12 | - | 13 |
| `agenda` | 12 | - | 13 |
| `end` | - | - | - |

### レイアウト別の重要な制約

**title (layout 0)**:
- テキストのみ。画像を配置するとプレースホルダーと重なる
- 写真付き表紙が必要な場合は `title_photo` (layout 1) を使う
- ph11(タイトル): top 3.153, 幅12.582（スライド中央）
- ph13(サブタイトル): top 4.964, 会社名・日付等

**title_photo (layout 1)**:
- タイトルテキストは**左半分のみ**（幅7.528インチ）
- 画像エリア: left 8.267, top 0.0, 5.066x7.5（右側全面）
- `position: "auto"` で画像エリアに自動配置される

**chapter (layout 2)**:
- テンプレートに装飾ボックス+緑矢印が**組み込み済み**
- タイトル（ph11）のみ設定すればよい。body/objects/images は不要
- subtitleは小さいので省略推奨

**content (layout 3)**:
- 緑ヘッダーバー内にタイトル（ph12, top 0.708）
- 本文エリア（ph13）は **top 1.417〜6.724** の大面積（5.3インチ高）
- objects と images は本文エリア内に自由配置可

**end (layout 8)**:
- JR東日本ロゴのみ表示する背表紙
- title/body/images 一切不可（プレースホルダーなし）

---

## 3. カラーパレット

| 用途 | カラーコード | セマンティック名 | 使用場面 |
|---|---|---|---|
| ブランド | `1B813E`（JRグリーン）| primary | テンプレートヘッダー/フッター/章扉（自動） |
| 提案・解決 | `4472C4`（青）| secondary | 提案ボックス・目標・カード並列 |
| 遷移 | `ED7D31`（橙）| accent | 矢印のみ |
| 補足・中立 | `404040`（濃グレー）| neutral | 補足テキスト・サブ情報 |
| 背景 | `FFFFFF`（白）| background | 囲み・ラベル |

### 色の使い方ルール
- JRグリーン(`1B813E`)はテンプレート装飾として自動表示される。**objects での使用は避ける**（テンプレート装飾と混同するため）
- objects のメインカラーは `4472C4`（青）を使う
- Before/After対比: 赤系(`C00000`) → 橙矢印(`ED7D31`) → 青(`4472C4`)

---

## 4. 図解パターン集（具体的座標）

### content_area の有効範囲
```
objects/images の配置可能範囲:
  top: 1.4〜6.7（テンプレートヘッダー/フッター外）
  left: 0.4〜13.0
```

### パターンC: body上部 + objects下部
body: `top: 1.4〜3.5`、objects: `top: 4.2〜5.4`
```json
"body": "...",
"objects": [
  {"type":"box","text":"現状","left":0.4,"top":4.2,"width":2.8,"height":1.0,"fill_color":"C00000","font_color":"FFFFFF","font_size":12},
  {"type":"arrow","left":3.3,"top":4.55,"width":0.6,"height":0.5,"fill_color":"ED7D31"},
  {"type":"box","text":"提案後","left":4.0,"top":4.2,"width":2.8,"height":1.0,"fill_color":"4472C4","font_color":"FFFFFF","font_size":12}
]
```

### パターンD: 全幅3カード
```
使用可能幅: 12.6インチ（左 0.4〜右 13.0）
width = (12.6 - 0.2*2) / 3 = 3.93
gap = 0.2

left[0]=0.4  left[1]=4.53  left[2]=8.66
```

### パターンB: 3カード + 右画像
```json
"objects": [
  {"type":"box","left":0.4,"top":3.5,"width":2.1,"height":1.5,"fill_color":"4472C4","font_color":"FFFFFF","font_size":11},
  {"type":"box","left":2.7,"top":3.5,"width":2.1,"height":1.5,"fill_color":"4472C4","font_color":"FFFFFF","font_size":11},
  {"type":"box","left":5.0,"top":3.5,"width":2.1,"height":1.5,"fill_color":"4472C4","font_color":"FFFFFF","font_size":11}
],
"images": [{"left":7.5,"top":1.5,"width":5.3}]
```

### フェーズ図（3ステップ）
```json
"objects": [
  {"type":"box","text":"Phase 1","left":0.4,"top":4.3,"width":2.5,"height":1.0,"fill_color":"4472C4","font_color":"FFFFFF"},
  {"type":"arrow","left":3.0,"top":4.55,"width":0.5,"height":0.5,"fill_color":"ED7D31"},
  {"type":"box","text":"Phase 2","left":3.6,"top":4.3,"width":2.5,"height":1.0,"fill_color":"4472C4","font_color":"FFFFFF"},
  {"type":"arrow","left":6.2,"top":4.55,"width":0.5,"height":0.5,"fill_color":"ED7D31"},
  {"type":"box","text":"Phase 3","left":6.8,"top":4.3,"width":2.5,"height":1.0,"fill_color":"4472C4","font_color":"FFFFFF"}
]
```

---

## 5. 画像スタイル

| スライド種別 | 画像 | 備考 |
|---|---|---|
| `title` | 不可 | テキストのみ |
| `title_photo` | position: "auto" | テンプレート画像エリアに自動配置。実写風推奨 |
| `chapter` | 不可 | テンプレート装飾のみ |
| `content` | 右半分に自由配置 | フラットイラスト推奨。left: 7.5, top: 1.5, width: 5.3 |
| `end` | 不可 | ロゴのみ |

---

## 6. SXテンプレートとの主な違い

| 項目 | SX提案書 | JR東日本 |
|---|---|---|
| 表紙画像 | layout 0 に画像エリアあり | layout 0 は画像不可、layout 1 で対応 |
| 章扉装飾 | なし（シンプル）| ボックス+緑矢印が組み込み済み |
| ヘッダーバー | なし | 緑ヘッダーバー（テンプレート自動） |
| フッター | 各レイアウトに固定 | 緑フッターバー（Copyright JR East） |
| title ph_idx | 0 | 11 or 12（レイアウトにより異なる） |
| body ph_idx | 14 (content) | 13 (content) |
| ブランドカラー | 赤(C00000) | 緑(1B813E) |
