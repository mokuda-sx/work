# スキル: スライドデザイン原則（美しいビジネス提案書）

> **使い方**: ビジュアル評価・設計時にこのファイルを読む。通常の生成作業では不要。

---

## 1. 情報密度の黄金律

### 1スライド1メッセージ
- 1スライドで伝えることは**1つだけ**
- タイトルに「何を言いたいか」が凝縮されているか確認
- 本文はタイトルの証拠・補足であるべき

### 文字量の目安（1行30-50文字）
| 要素 | 最大文字数 | 備考 |
|---|---|---|
| スライドタイトル | 25〜35文字 | 短すぎ/長すぎ両方NG |
| キーメッセージ | 40〜70文字 | 体言止めか動詞終止 |
| 箇条書き1項目 | 30〜50文字 | 体言止め推奨 |
| 箇条書き項目数 | 3〜5項目 | 6項目以上は分割検討 |

---

## 2. カラーパレット規律

### SXテンプレートの推奨色
| 用途 | カラーコード | 使用場面 |
|---|---|---|
| 主張・強調 | `C00000`（深紅） | 課題・リスク・現状NG |
| 提案・解決 | `4472C4`（青） | 提案・目標・将来 |
| アクセント | `ED7D31`（橙） | 矢印・遷移・変化 |
| テキスト | `404040`（濃グレー） | 補足テキスト |

### カラー使用ルール
- **3色以内**に抑える（背景色は除く）
- 赤＝問題、青＝解決 の対比は有効
- 同系色を並べない（コントラスト不足）

---

## 3. レイアウトゾーン設計（最重要）

### スライドの座標空間
```
幅: 13.3インチ  高さ: 7.5インチ
コンテンツエリア: top 1.5〜7.0（テンプレートタイトルバー除く）
左半分: left 0.0〜6.6
右半分: left 6.6〜13.3
```

### 要素の共存ルール（混在時の最重要原則）

**body + objects + images の3要素を同時に使うと必ず崩れる。以下のパターンから選ぶ。**

| パターン | body | objects | images | 使いどころ |
|---|---|---|---|---|
| A: テキスト＋画像 | あり（左） | なし | あり（右） | 説明・分析系スライド |
| B: 図解＋画像 | なし | あり（左） | あり（右） | 3要素並列・比較系 |
| C: テキスト＋図解 | あり（上） | あり（下） | なし | フロー・遷移型 |
| D: 全幅図解 | なし | あり（全幅） | なし | カード型・分類型 |

---

## 4. 図解パターン集（objects設計）

### パターンC: 現状→提案型（body上部 + objects下部）
body: `top: 1.5〜3.5`（テキスト）、objects: `top: 4.2〜5.4`
```json
"body": "・課題1\n・課題2\n・課題3",
"objects": [
  {"type":"box","text":"現状\n○○","left":0.5,"top":4.2,"width":2.8,"height":1.0,"fill_color":"C00000","font_color":"FFFFFF","font_size":12},
  {"type":"arrow","left":3.4,"top":4.55,"width":0.6,"height":0.5,"fill_color":"ED7D31"},
  {"type":"box","text":"提案後\n○○","left":4.1,"top":4.2,"width":2.8,"height":1.0,"fill_color":"4472C4","font_color":"FFFFFF","font_size":12}
]
```
**注意**: images は使わない（3要素共存の回避）

---

### パターンD: 全幅3カード（body なし・images なし）
3つの等価な要素を全幅で並べる。`width = (12.8 - 0.5 - 0.2*2) / 3 ≈ 4.0`
```json
"objects": [
  {"type":"box","text":"項目1\n説明","left":0.5, "top":3.5,"width":3.9,"height":1.5,"fill_color":"4472C4","font_color":"FFFFFF","font_size":12},
  {"type":"box","text":"項目2\n説明","left":4.6, "top":3.5,"width":3.9,"height":1.5,"fill_color":"4472C4","font_color":"FFFFFF","font_size":12},
  {"type":"box","text":"項目3\n説明","left":8.7, "top":3.5,"width":3.9,"height":1.5,"fill_color":"4472C4","font_color":"FFFFFF","font_size":12}
]
```
`left[1] = left[0] + width + gap = 0.5 + 3.9 + 0.2 = 4.6`
`left[2] = left[1] + width + gap = 4.6 + 3.9 + 0.2 = 8.7`

---

### パターンB: 3カード＋右画像（objects左側・image右側）
```json
"objects": [
  {"type":"box","text":"項目1\n説明","left":0.5,"top":3.5,"width":2.1,"height":1.5,"fill_color":"4472C4","font_color":"FFFFFF","font_size":11},
  {"type":"box","text":"項目2\n説明","left":2.8,"top":3.5,"width":2.1,"height":1.5,"fill_color":"4472C4","font_color":"FFFFFF","font_size":11},
  {"type":"box","text":"項目3\n説明","left":5.1,"top":3.5,"width":2.1,"height":1.5,"fill_color":"4472C4","font_color":"FFFFFF","font_size":11}
],
"images": [
  {"prompt":"...", "model":"gemini-3-pro-image-preview","left":7.6,"top":1.8,"width":5.3}
]
```
objects が `left: 0.5〜7.2` に収まり、image が `left: 7.6〜12.9` に収まる → 隙間なし

---

### パターンA: テキスト＋右画像（objects なし）
```json
"body": "・説明1（左側に収まる文字数）\n・説明2\n・説明3\n・説明4",
"images": [
  {"prompt":"...", "model":"gemini-3-pro-image-preview","left":7.5,"top":1.8,"width":5.3}
]
```
左側テキスト、右側画像の最もシンプルな構成。

---

### フェーズ図（3ステップ）: パターンC の変形
```json
"objects": [
  {"type":"box","text":"Phase 1\n調査","left":0.5,"top":4.3,"width":2.5,"height":1.0,"fill_color":"4472C4","font_color":"FFFFFF","font_size":12},
  {"type":"arrow","left":3.1,"top":4.55,"width":0.5,"height":0.5,"fill_color":"ED7D31"},
  {"type":"box","text":"Phase 2\n設計","left":3.7,"top":4.3,"width":2.5,"height":1.0,"fill_color":"4472C4","font_color":"FFFFFF","font_size":12},
  {"type":"arrow","left":6.3,"top":4.55,"width":0.5,"height":0.5,"fill_color":"ED7D31"},
  {"type":"box","text":"Phase 3\n実装","left":6.9,"top":4.3,"width":2.5,"height":1.0,"fill_color":"4472C4","font_color":"FFFFFF","font_size":12}
]
```

---

## 5. objects 座標計算テンプレート

### N個の等幅ボックスを均等配置する計算式
```
スライド幅: 13.3インチ
使用可能幅: 12.8インチ（左マージン 0.5）
ボックス幅 = (12.8 - 0.5*(N-1)) / N  ← ギャップ0.5インチの場合

N=2:  width = 6.15  left[0]=0.5  left[1]=7.15
N=3:  width = 3.93  left[0]=0.5  left[1]=4.93  left[2]=9.37 ※または width=4.0 gap=0.2で綺麗
N=4:  width = 2.95  left[0]=0.5  left[1]=3.95  left[2]=7.4  left[3]=10.85

# width=4.0, gap=0.2 の 3ボックス（推奨）
left[0]=0.5  left[1]=4.7  left[2]=8.9
```

### 画像エリアと objects の衝突回避
- objects の `left + width` の最大値 < images の `left` となるよう設計
- 例: objects最右端 = 5.1 + 2.1 = 7.2 → images left = 7.6（0.4インチのバッファ）

---

## 6. 画像配置ガイドライン

### contentスライドの画像エリア
- **右半分推奨**: `left: 7.5〜8.0`, `top: 1.5〜2.0`, `width: 5.0〜5.5`
- 本文（左側）と画像（右側）で視線を分離する
- 画像がある場合、本文の箇条書きは左側3〜4項目に絞る

### objects と画像が共存する場合（パターンB）
- objects の x 範囲: `left: 0.5 〜 7.2`（全幅の54%）
- images の x 範囲: `left: 7.6 〜 12.9`（全幅の40%）
- objects の高さは `height: 1.2〜2.0` に設定（本文エリアをフル活用）

### 画像プロンプト品質基準
- **英語で記述**（Geminiの品質向上）
- スライドの内容と直接関連させる
- スタイル指定を含める: `clean minimal business illustration`, `flat design`, `professional`
- NGワード: `photo`, `realistic` (ベクター系の方がスライドに馴染む)

---

## 7. スライド種別ごとの設計指針

| type | 目的 | 推奨パターン |
|---|---|---|
| `title` | 第一印象・権威付け | シンプルに。タイトルとサブタイトル（日付・宛先）のみ |
| `agenda` | 全体像の提示 | 章番号＋章名のみ。1行1章 |
| `chapter` | 章の区切り | 短く力強いタイトルのみ。写真なし（ミニマル） |
| `chapter_photo` | 章の区切り（写真あり） | 視覚インパクト重視の章扉 |
| `content` | 主張・証拠 | A/B/C/Dパターンから1つ選ぶ。3要素共存は禁止 |
| `end` | 締め・次のアクション | 「ご清聴ありがとうございました」系。シンプルに |

---

## 8. アンチパターン（やってはいけないこと）

- **body + objects + images を全部使う**: レイアウト崩壊の最大原因。必ずパターンA/B/C/Dから選ぶ
- **objects が左端に偏る**: 右半分に空白が残り間抜けに見える。全幅レイアウトに直す
- **3ボックスの left 計算が甘い**: `0.5, 3.2, 5.9` のように詰まると右端に大きな空白。計算式で確認
- **箇条書きを読むだけのスライド**: 聴衆は読めるが、話す意味がない
- **フォント色が白×白**: 背景と同化して見えない
- **図解なしの content**: 最低1つの objects か images を入れる
- **画像が左側にある**: 日本語は左から読むため、テキスト左・画像右が基本
- **タイトルが体言止めでない**: 「〜について」は弱い。「〜で○○を実現する」が強い

---

## 9. セルフチェックリスト（Tier 2 生成前に確認）

1. body/objects/images の3要素を同時に使っていないか？
2. objects の座標を計算し、右端の空白が 1インチ以下か？
3. N個のボックスを均等幅で配置しているか（計算式を使ったか）？
4. objects と images の x 座標が衝突していないか？
5. 1スライドのメッセージが1つに絞られているか？
