# スライド生成の厳格プロセス

> **目的**: AIエージェントがスキルを正しく読み、参照作品を活用し、検証可能な形でスライドを生成する

---

## プロセスフロー（全6ステップ）

```
Step 1: パターン認識
  ↓
Step 2: 参照作品の構造解析（ツール使用）
  ↓
Step 3: スキル参照の明示
  ↓
Step 4: 実装
  ↓
Step 5: デザイン検証（ツール使用）
  ↓
Step 6: ユーザー承認
```

---

## Step 1: パターン認識

### 実行内容
- `recipes/XX_content.recipe.json` の `pattern` フィールドを読む
- `skills/slide_recipe.md` で該当パターンの説明を探す
- 参照作品の記載を確認

### 成果物
```
パターン: swimlane_process
参照作品: sx_ai_callcenter slide 3
```

---

## Step 2: 参照作品の構造解析

### 必須コマンド
```bash
python analyze_ref.py extract-pattern refs/<family>/<id>/analysis.json --slide <N>
```

### 実行例
```bash
python analyze_ref.py extract-pattern refs/sx/sx_ai_callcenter/analysis.json --slide 3
```

### 確認事項
- **座標**：left/top/width/height の正確な値
- **色**：fill_color の実際の値
- **テキスト**：どのような文言が使われているか
- **フォントサイズ**：font_sizes の値

### 重要原則
⚠️ **抽出した座標を勝手に変更しない**
⚠️ **「だいたいこのくらい」で決めない**

---

## Step 3: スキル参照の明示

### 実装ファイルにコメント記録

```json
{
  "index": 1,
  "type": "content",
  "title": "...",
  "_skill_refs": {
    "pattern": "swimlane_process (slide_recipe.md L280-320)",
    "reference_work": "sx_ai_callcenter slide 3",
    "reference_analysis": "python analyze_ref.py extract-pattern refs/sx/sx_ai_callcenter/analysis.json --slide 3",
    "colors": {
      "404040": "design_guide.md L48 (neutral/補足)",
      "4472C4": "design_guide.md L48 (solution/提案)",
      "ED7D31": "design_guide.md L48 (accent/矢印)"
    },
    "coordinate_basis": "参照作品 slide 3 の座標を基準（left: 0.354-0.748, 幅: 0.394）"
  },
  "objects": [...]
}
```

### 記録すべき情報
1. **パターン名**と記載場所（ファイル名 + 行番号）
2. **参照作品**の特定（family/id/slide番号）
3. **色の根拠**（design_guide.md の該当行 + セマンティック名）
4. **座標の根拠**（参照作品の実測値、または計算式）

---

## Step 4: 実装

### 実装原則

#### 4.1 座標
- **extract-pattern の座標を基準**に使う
- 必要に応じてスケール調整するが、**根拠を記録**
- 勝手な調整は禁止

#### 4.2 色
- **design_guide.md で定義された色のみ使用**
- 参照作品で使われている色でも、design_guide にない場合は使用前に確認
- セマンティック名（primary/secondary/accent/neutral）を理解して選択

#### 4.3 テキスト
- 参照作品の**構造**を参考に（縦書き/横書き、改行位置など）
- 具体的な文言は recipe.json の内容に合わせる

#### 4.4 フォントサイズ
- 推奨範囲：9-20pt
- 参照作品の値を基準に選択

---

## Step 5: デザイン検証

### 必須コマンド
```bash
python dev_tools.py validate-design slides/<project>/slides/XX_content.json
```

### 実行例
```bash
python dev_tools.py validate-design "slides/20260217_AI PPT生成の仕組み説明/slides/01_content.json"
```

### 検証項目
- ✓ 色が design_guide.md で定義されているか
- ✓ 座標が content area（0.5-12.8, 1.5-7.0）内か
- ✓ フォントサイズが推奨範囲（9-20pt）か

### エラー対応
- **エラーがある場合**：必ず修正してから次へ
- **警告がある場合**：確認後、必要に応じて修正

---

## Step 6: ユーザー承認

### 提示内容
1. **設計意図**の説明
   - どのパターンを使ったか
   - なぜその参照作品を選んだか
   - どの座標・色を使ったか

2. **`_skill_refs` の提示**
   - どのスキルを参照したか
   - どの行番号のルールを適用したか

3. **検証結果の提示**
   - validate-design の結果
   - エラー・警告の有無

### 承認待ち
⚠️ **ユーザーの承認を得るまで PPTX 生成しない**

---

## 禁止事項

### ❌ 絶対にしてはいけないこと

1. **スキルを読まずに実装**
   - 「だいたいこんな感じ」で座標を決める
   - 色を推測で選ぶ

2. **参照作品を確認せずに実装**
   - extract-pattern を実行せず、記憶で作る
   - 座標を「適当に調整」する

3. **検証をスキップ**
   - validate-design を実行しない
   - エラーがあるのに無視する

4. **ユーザー承認前に PPTX 生成**
   - 設計を提示せず、いきなり生成する
   - エラーがあるのに生成を強行する

---

## チェックリスト（AI用）

各ステップ完了時に自己確認：

### Step 1（パターン認識）
- [ ] recipe.json の pattern を読んだ
- [ ] slide_recipe.md でパターン説明を確認した
- [ ] 参照作品を特定した

### Step 2（参照作品解析）
- [ ] `python analyze_ref.py extract-pattern ...` を実行した
- [ ] 座標・色・テキスト・フォントサイズを記録した

### Step 3（スキル参照明示）
- [ ] `_skill_refs` セクションを作成した
- [ ] 色の根拠を design_guide.md の行番号で記録した
- [ ] 座標の根拠を記録した

### Step 4（実装）
- [ ] 参照作品の座標を基準に使った
- [ ] design_guide.md で定義された色のみ使った
- [ ] 勝手な調整をしていない

### Step 5（検証）
- [ ] `python dev_tools.py validate-design ...` を実行した
- [ ] エラーがあれば修正した
- [ ] 警告を確認した

### Step 6（承認）
- [ ] 設計意図を説明した
- [ ] `_skill_refs` を提示した
- [ ] ユーザーの承認を待っている

---

## まとめ

このプロセスにより、以下が保証される：

1. **トレーサビリティ**：どのスキルを根拠に実装したか記録
2. **再現性**：同じパターンを再利用可能
3. **品質保証**：ツールによる自動検証
4. **説明責任**：ユーザーに根拠を提示可能

**重要**: このプロセスは「AIが従うべきルール」であり、**すべてのスライド生成で必須**。
