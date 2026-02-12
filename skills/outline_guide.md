# スキル: アウトライン設計ガイド

> **使い方**: 新しいプレゼンのアウトラインを設計する際に読む。通常の編集作業では不要。

---

## 標準的なスライド構成パターン

### 提案書（5〜8スライド）
```
title         → 提案書タイトル + 日付・宛先（実写風写真）
agenda        → アジェンダ（3〜5章、階層構造可。表紙と同じ写真を再利用）
chapter       → 1章タイトル
content       → 1-1: 現状・課題
content       → 1-2: 課題の深堀
chapter       → 2章タイトル
content       → 2-1: 提案内容
content       → 2-2: 期待効果
end           → エンドスライド
```

### 報告書（3〜5スライド）
```
title         → 報告書タイトル
content       → エグゼクティブサマリー
content × N   → 詳細（各テーマ）
end           → 次のアクション
```

---

## アウトライン品質チェック

アウトラインを生成したら以下を確認:

1. **title**: タイトルが提案の価値を表しているか
   - NG: 「DX推進について」
   - OK: 「製造ラインのDX化で生産効率30%向上を実現する提案」

2. **agenda**: 章立てが論理的か
   - 「現状→課題→提案→効果→進め方」が基本ストーリー

3. **content**: 各スライドに図解/画像の指示があるか
   - 最低30%のcontentスライドにobjectsかimagesを入れる

4. **end**: エンドスライドに次のアクションがあるか

---

## 業種・用途別タイトル例

### 製造業DX
- 「生産ラインの見える化でコスト20%削減を実現するDXロードマップ」
- 「品質管理AIの導入による不良率1/10への挑戦」

### IT・クラウド移行
- 「オンプレからクラウドへの移行で運用コストを年間○千万円削減する提案」
- 「レガシーシステム刷新による開発速度3倍化計画」

### コンサル提案一般
- 「〇〇課題を解決する3ステップ改革の提案」
- 「〇〇分野における競争優位確立のための戦略提案」

---

## JSONサンプル（最小構成・contentスライド）

```json
{
  "type": "content",
  "title": "AIデータ分析による予防保全の実現（25文字）",
  "subtitle": "設備の故障を事前に予測し、ダウンタイムを80%削減する（28文字）",
  "body": "・センサーデータをリアルタイムで収集・AIで異常検知\n・月次定期点検から「必要な時だけ点検」へシフト\n・過去5年の故障データから99%精度のモデル構築済み\n・パイロット3拠点で平均ダウンタイム82%削減を達成",
  "objects": [
    {"type":"box","text":"現状\n定期点検","left":0.5,"top":4.5,"width":2.5,"height":1.0,"fill_color":"C00000","font_color":"FFFFFF","font_size":12},
    {"type":"arrow","left":3.1,"top":4.75,"width":0.5,"height":0.5,"fill_color":"ED7D31"},
    {"type":"box","text":"提案\n予防保全","left":3.7,"top":4.5,"width":2.5,"height":1.0,"fill_color":"4472C4","font_color":"FFFFFF","font_size":12}
  ],
  "images": [
    {"prompt":"Industrial IoT sensor monitoring dashboard with AI anomaly detection, clean flat design, blue tones",
     "model":"gemini-3-pro-image-preview","left":7.3,"top":1.5,"width":5.5}
  ]
}
```
