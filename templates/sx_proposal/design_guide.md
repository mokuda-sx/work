# SX提案書 3.0 (16:9) デザインガイド

> **使い方**: このテンプレートでスライドを設計する時に読む。
> 共通デザイン原則は `skills/design_principles.md` を参照。

---

## 1. スライドサイズと座標空間

```
幅: 13.333インチ  高さ: 7.5インチ（16:9）
コンテンツエリア: top 1.5〜7.0（テンプレートタイトルバー除く）
左マージン: left ≥ 0.5
右端制限: left + width ≤ 12.8
下端制限: top + height ≤ 6.8（フッター前）
左半分: left 0.0〜6.6
右半分: left 6.6〜13.3
```

---

## 2. レイアウト一覧

| type | layout index | 用途 | 画像エリア |
|---|---|---|---|
| `title` | 0 | 表紙（写真あり）| 1.012, 2.253, 11.348x4.646 |
| `agenda` | 2 | 目次/アジェンダ（写真あり）| 6.981, 0.443, 5.356x6.615（右半分）|
| `chapter_photo` | 4 | 章扉（写真あり）| 1.012, 2.411, 11.348x4.646 |
| `chapter` | 5 | 章扉（写真なし）| なし |
| `content` | 6 | コンテンツ | なし（images で任意配置）|
| `end` | 14 | エンド（写真あり）| 0.997, 0.831, 11.348x4.646 |

### プレースホルダー対応表

| type | title (ph_idx) | subtitle (ph_idx) | body (ph_idx) |
|---|---|---|---|
| `title` | 0 | 1 | - |
| `agenda` | 0 | - | 10 |
| `chapter` | 0 | 1 | - |
| `chapter_photo` | 0 | 1 | - |
| `content` | 0 | 13 | 14 |
| `end` | 0 | - | - |

---

## 3. カラーパレット

| 用途 | カラーコード | セマンティック名 | 使用場面 |
|---|---|---|---|
| 主張・強調 | `C00000`（深紅）| primary | 課題・リスク・現状NG |
| 提案・解決 | `4472C4`（青）| secondary | 提案・目標・将来 |
| アクセント | `ED7D31`（橙）| accent | 矢印・遷移・変化のみ |
| 補足・中立 | `404040`（濃グレー）| neutral | 補足テキスト・ニュートラル |
| 背景白抜き | `FFFFFF`（白）| background | 囲み・ラベル（テキスト色を黒に）|

### 色の意味（意味的一貫性）

| 色 | 意味 | OK | NG |
|---|---|---|---|
| `C00000` 赤 | 問題・警告 | 課題ボックス・Before | 解決策・未来像 |
| `4472C4` 青 | 解決・提案 | 提案ボックス・After・カード並列 | 課題・リスク |
| `ED7D31` 橙 | 遷移・変化 | 矢印のみ | メインのボックス |
| `404040` 濃グレー | 中立・補足 | サブ情報 | 強調したい要素 |

### 状況別カラー選択

```
並列（3つとも同等価値）→ 全部 4472C4（青）
Before/After（対比）   → C00000 → ED7D31(矢印) → 4472C4
段階・フェーズ         → 4472C4（強調）+ 404040（落ち着き）
3段階の重要度差        → 1F3864（濃紺）→ 4472C4（青）→ 8FAADC（薄青）
```

---

## 4. 図解パターン集（具体的座標）

### パターンC: body上部 + objects下部
body: `top: 1.5〜3.5`、objects: `top: 4.2〜5.4`
```json
"body": "...",
"objects": [
  {"type":"box","text":"現状","left":0.5,"top":4.2,"width":2.8,"height":1.0,"fill_color":"C00000","font_color":"FFFFFF","font_size":12},
  {"type":"arrow","left":3.4,"top":4.55,"width":0.6,"height":0.5,"fill_color":"ED7D31"},
  {"type":"box","text":"提案後","left":4.1,"top":4.2,"width":2.8,"height":1.0,"fill_color":"4472C4","font_color":"FFFFFF","font_size":12}
]
```

### パターンD: 全幅3カード
`width = (12.8 - 0.5 - 0.2*2) / 3 = 3.9`, `gap = 0.2`
```json
"objects": [
  {"type":"box","left":0.5,"top":3.5,"width":3.9,"height":1.5,"fill_color":"4472C4","font_color":"FFFFFF","font_size":12},
  {"type":"box","left":4.6,"top":3.5,"width":3.9,"height":1.5,"fill_color":"4472C4","font_color":"FFFFFF","font_size":12},
  {"type":"box","left":8.7,"top":3.5,"width":3.9,"height":1.5,"fill_color":"4472C4","font_color":"FFFFFF","font_size":12}
]
```

### パターンB: 3カード + 右画像
```json
"objects": [
  {"type":"box","left":0.5,"top":3.5,"width":2.1,"height":1.5,"fill_color":"4472C4","font_color":"FFFFFF","font_size":11},
  {"type":"box","left":2.8,"top":3.5,"width":2.1,"height":1.5,"fill_color":"4472C4","font_color":"FFFFFF","font_size":11},
  {"type":"box","left":5.1,"top":3.5,"width":2.1,"height":1.5,"fill_color":"4472C4","font_color":"FFFFFF","font_size":11}
],
"images": [{"left":7.6,"top":1.8,"width":5.3}]
```

### フェーズ図（3ステップ）
```json
"objects": [
  {"type":"box","text":"Phase 1","left":0.5,"top":4.3,"width":2.5,"height":1.0,"fill_color":"4472C4","font_color":"FFFFFF"},
  {"type":"arrow","left":3.1,"top":4.55,"width":0.5,"height":0.5,"fill_color":"ED7D31"},
  {"type":"box","text":"Phase 2","left":3.7,"top":4.3,"width":2.5,"height":1.0,"fill_color":"4472C4","font_color":"FFFFFF"},
  {"type":"arrow","left":6.3,"top":4.55,"width":0.5,"height":0.5,"fill_color":"ED7D31"},
  {"type":"box","text":"Phase 3","left":6.9,"top":4.3,"width":2.5,"height":1.0,"fill_color":"4472C4","font_color":"FFFFFF"}
]
```

---

## 5. 座標計算テンプレート

### N個の等幅ボックスを均等配置
```
使用可能幅: 12.3インチ（左 0.5〜右端 12.8）
ボックス幅 = (12.3 - gap*(N-1)) / N

gap=0.2 の場合:
N=2:  width=6.05  left[0]=0.5  left[1]=6.75
N=3:  width=3.97  left[0]=0.5  left[1]=4.67  left[2]=8.84
N=4:  width=2.93  left[0]=0.5  left[1]=3.63  left[2]=6.76  left[3]=9.89

推奨（N=3, width=3.9, gap=0.2）:
left[0]=0.5  left[1]=4.6  left[2]=8.7
```

### 画像エリアとの衝突回避
```
objects の right端 < images の left - 0.4
例: objects 右端 = 5.1+2.1 = 7.2 → images left = 7.6（バッファ 0.4）
```

### contentスライドの画像推奨位置
```
右半分: left: 7.5〜8.0, top: 1.5〜2.0, width: 5.0〜5.5
```

---

## 6. 画像スタイルの使い分け

| スライド種別 | 推奨スタイル | プロンプト例 |
|---|---|---|
| title / agenda / chapter_photo / end | **実写風プロ写真** | `professional photograph, city skyline at night with digital network connections, high quality, corporate` |
| content | **フラットイラスト** | `clean minimal business illustration, flat design, blue tones` |

テンプレートの画像エリア（大面積）を使うスライドは実写風写真が映える。
contentスライドの小さめ画像エリアにはイラスト系が適切。

### 画像の再利用（統一感の鉄則）
- 表紙(title)と目次(agenda)は**同じ画像を使う**のがコンサル提案書の基本
- `"file": "images/xxx.png"` で生成済み画像を再利用する
- 章扉(chapter_photo)も同じテーマの写真を使うと全体に統一感が出る
- 毎スライドで違う画像にしない（バラバラ感が出る）

---

## 7. スライド種別ごとの設計指針

| type | 目的 | 推奨パターン |
|---|---|---|
| `title` | 第一印象・権威付け | タイトル＋サブタイトル（`会社名\n日付`の2行）のみ。実写風写真 |
| `agenda` | 全体像の提示 | タイトルは**「アジェンダ」**。階層構造可。表紙と同じ画像を再利用 |
| `chapter` | 章の区切り | 短く力強いタイトルのみ。写真なし（ミニマル）|
| `chapter_photo` | 章の区切り（写真あり）| 視覚インパクト重視の章扉 |
| `content` | 主張・証拠 | A/B/C/Dパターンから1つ選ぶ。3要素共存は禁止 |
| `end` | 締め・次のアクション | 「ご清聴ありがとうございました」系。シンプルに |
