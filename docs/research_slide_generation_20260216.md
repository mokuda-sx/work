# スライド生成に関する調査メモ

> 調査日: 2026-02-16 | 調査者: Claude Code (Opus 4.6)

## 調査の動機

Phase 3（参照ライブラリ）の設計にあたり、以下を調査:
1. 参照ベースのスライド生成に関する最新研究
2. 画像生成モデル（Nano Banana Pro / NANOBANAPRO）による資料作成ノウハウ

---

## 1. PPTAgent（EMNLP 2025）

**論文**: Hao Zheng et al., "PPTAgent: Generating and Evaluating Presentations Beyond Text-to-Slides"
**URL**: https://arxiv.org/abs/2501.03936
**GitHub**: https://github.com/icip-cas/PPTAgent

### 概要

参照プレゼンテーションを分析し、編集ベースで新しいスライドを生成する2段階フレームワーク。

### Stage I: Presentation Analysis

- スライドを **structural**（表紙・目次・締め）と **content** に分類
- content スライドは **画像類似度による階層的クラスタリング**（閾値0.65）でグループ化
- 各クラスタから **content schema** を抽出（要素のcategory, modality, content）
- テキスト・画像をプレースホルダーに置換して干渉を最小化

### Stage II: Presentation Generation

- LLMがアウトラインを生成（参照スライド選択 + ドキュメント関連セクション + タイトル + 説明）
- PPTXのXMLをHTMLに変換してLLMに渡す（XMLより解釈しやすい）
- 5つの編集API: テキスト削除/置換、画像削除/置換、段落複製
- **自己修正メカニズム**: REPL環境でエラー検出 → 最大2回の反復修正

### PPTEval（評価フレームワーク）

3軸で1-5評価:
- **Content**: 情報品質、テキスト明瞭性、視覚サポート
- **Design**: 配色、視覚要素、デザイン原則への準拠
- **Coherence**: 論理構造、文脈的流れ

MLLMがスライド画像を直接評価。人間評価者との平均Pearson相関0.71。

### 我々のプロジェクトとの関連

| PPTAgentの要素 | 我々の対応物 | 差異・改善点 |
|---|---|---|
| Stage I クラスタリング | `analyze_ref.py` | 我々は形状レベルの詳細のみ。抽象的スキーマ抽出がない |
| アウトライン計画 | Tier 1 生成 | 参照のセマンティック情報を前提ルールとして注入する仕組みがまだない |
| 編集ベース生成 | Recipe → Tier 2 変換 | 我々はJSON中間層経由。直接XML編集より安全だが柔軟性は劣る |
| 自己修正 | Phase 4 構想 | まだ未実装 |
| PPTEval 3軸 | `critique_rubric.md` | 統合・拡充の余地あり |

---

## 2. AutoPresent（UC Berkeley, 2025年1月）

**論文**: Ge, Wang, Zhou et al., "AutoPresent"
**URL**: https://nlp.cs.berkeley.edu/pubs/Ge-Wang-Zhou-Peng-Subramanian-Tan-Sap-Suhr-Fried-Neubig-Darrell_2025_AutoPresent_paper.pdf

### 核心的知見

- **コード生成アプローチが画像生成を大幅に上回る**
  - Stable Diffusion, DALL-Eによるend-to-end画像生成は品質が低い
  - LLMによるコード生成（→構造的スライド）の方が実用的
- LLAMA 8Bベースのモデルでもfine-tuningでGPT-4oに迫る性能
- SLIDESBENCHベンチマーク提供

### 我々への示唆

我々のJSON→PPTX変換パイプラインはAutoPresentの結論と一致する方向性。
画像生成モデルは「スライド全体を画像として生成」には不向きだが、
スライド内の挿絵・図解要素としては有効（現在のGemini画像生成の使い方）。

---

## 3. Nano Banana Pro（NANOBANAPRO）のスライド/インフォグラフィック生成

**モデル**: Gemini 3 Pro Image (通称 Nano Banana Pro)
**リリース**: 2025年11月 by Google DeepMind

### 特徴

- 高精度テキストレンダリング（日中韓対応）
- "Thinking" プロセス: プロンプトを推論してから生成
- Search Grounding: Google検索と連携して事実に基づく図表を生成
- Few-shot: 最大14枚の参照画像でブランド一貫性を維持

### ICSフレームワーク（プロンプト構造）

| 要素 | 説明 | 我々の対応 |
|---|---|---|
| **I**mage type | blueprint, infographic, diagram等 | Recipe の `pattern` |
| **C**ontent | 情報・データ | Recipe の `body_points` |
| **S**tyle | McKinsey風、comic風等 | Recipe の `tone` + テンプレートの色 |

### ベストプラクティス

1. **レイアウト明示**: "single-column", "two-column" → 我々の `pattern` と同じ発想
2. **セクション上限 3-5**: 認知負荷の観点 → `design_principles.md` の情報密度と一致
3. **Chain-of-Thought**: 複雑な構図は段階的にレイアウトロジックを記述 → Recipe層がこの役割
4. **ネガティブ指示**: "no busy textures, no photo backgrounds" → objects/images排他ルールと同じ考え方
5. **テキスト囲み**: ダブルクォートでリテラル指定 → prompt設計の参考

### Google Workspace統合

- Google Slides に "Help me visualize" 機能として統合（2025年12月〜）
- インフォグラフィック・スライド生成に特化した訓練がなされている
- Workspace Enterprise / Gemini Advanced で利用可能

---

## 4. 総合的な示唆

### 現アーキテクチャの妥当性

- **構造的JSON → PPTX変換**はAutoPresentの結論（コード生成 > 画像生成）と整合
- **Recipe層**はICSフレームワークと同じ構造化を独立に発見していた
- **3層分離**（意図→設計→実装）は研究でも有効性が確認されている方向

### Phase 3（参照ライブラリ）への具体的示唆

1. **analysis.jsonにサマリー層を追加**: PPTAgentのスキーマ抽出に相当。スライドタイプ分布、構成パターン、トーンを抽象化
2. **参照マッチング**: 口語指示からタグ抽出 → 参照の `purpose` / `tags` でマッチ → 構成パターンを前提ルールとして注入
3. **PPTEvalの3軸を `critique_rubric.md` に統合**: Content / Design / Coherence

### Phase 4（自己改善）への示唆

1. **PPTAgentの自己修正メカニズム**: REPL + 最大2回反復。我々も停止条件を「3回以内」に設定済み
2. **PPTEvalの定量評価**: MLLMによるスライド画像直接評価。サムネイルベースの評価フローに接続可能

---

## 参考リンク

- [PPTAgent (EMNLP 2025)](https://arxiv.org/abs/2501.03936)
- [PPTAgent GitHub](https://github.com/icip-cas/PPTAgent)
- [AutoPresent (Berkeley, 2025)](https://nlp.cs.berkeley.edu/pubs/Ge-Wang-Zhou-Peng-Subramanian-Tan-Sap-Suhr-Fried-Neubig-Darrell_2025_AutoPresent_paper.pdf)
- [Nano Banana Pro Prompting Guide (Atlabs)](https://www.atlabs.ai/blog/the-ultimate-nano-banana-pro-prompting-guide-mastering-gemini-3-pro-image)
- [Nano Banana Pro Infographic Prompts (Mew Design)](https://docs.mew.design/blog/gemini-nano-banana-pro-ai-infographic-prompts/)
- [Google Workspace - Nano Banana Pro統合](https://workspaceupdates.googleblog.com/2025/11/workspace-nano-banana-pro.html)
- [Sider.ai - Best Prompts for Infographics](https://sider.ai/blog/ai-image/best-prompts-for-nano-banana-pro-infographics-a-practical-guide)
