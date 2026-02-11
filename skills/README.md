# スキルライブラリ

Claude Code がオンデマンドで読み込むモジュール型ナレッジ集。
必要な時だけ Read ツールで読み込むことでトークンを節約する。

## スキル一覧

| ファイル | 読み込むタイミング | 内容 |
|---|---|---|
| [design_principles.md](design_principles.md) | デザイン設計・評価時 | カラー・レイアウト・図解の原則 |
| [critique_rubric.md](critique_rubric.md) | サムネイル診断時 | スライド評価チェックリスト |
| [outline_guide.md](outline_guide.md) | アウトライン設計時 | 構成パターン・JSONサンプル |

## 使い方（Claude Code 向け）

```
# 通常の生成作業: スキルは読まない（トークン節約）

# アウトライン設計が難しい場合:
Read skills/outline_guide.md

# 視覚チェック（--thumbnail 後）:
Read skills/critique_rubric.md
# 問題があれば:
Read skills/design_principles.md

# 新しいノウハウを発見したら:
# 該当スキルファイルを Edit ツールで更新して蓄積する
```

## スキル追加のガイドライン

- **分割基準**: 1スキル = 1つのユースケース（読み込み粒度）
- **ファイルサイズ**: 1スキル 100〜300行 を目安（大きすぎるとトークン無駄）
- **形式**: マークダウン + コード例（AIが読みやすい形式）
- **更新方法**: 新発見時に Edit ツールで即追記（忘れる前に）
