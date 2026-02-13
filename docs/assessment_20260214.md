# システム評価レポート — 2026-02-14

## 概要

AI PowerPoint Generator の現状を「AIコンテンツ作成システム」として評価する。

## リポジトリ構成（評価時点）

```
work/
├── pptx_engine.py          # PPTX 生成エンジン
├── generate_pptx.py        # CLI エントリーポイント
├── template_analyzer.py    # テンプレート登録ツール
├── dev_tools.py            # 開発・診断ツール
├── CLAUDE.md               # AI ワークフロー定義
├── README.md               # リポジトリ説明（未整備）
├── templates/              # テンプレート定義
│   ├── sx_proposal/        #   SX提案書 3.0
│   └── jr_east/            #   JR East
├── skills/                 # AI スキルファイル（共通）
│   ├── slide_recipe.md     #   レシピ生成・変換
│   ├── design_principles.md#   デザイン共通原則
│   ├── critique_rubric.md  #   診断手法
│   ├── outline_guide.md    #   構成パターン
│   └── project_rules.md    #   プロジェクト管理ルール
├── slides/                 # 生成プロジェクト
│   ├── 20260213_jr_east_AI提案書自動生成v3/
│   └── 20260213_sx_proposal_AI提案書自動生成v3/
└── docs/                   # ドキュメント
    ├── vision.md
    └── knowhow.md
```

## 評価

### 強み

1. **3 Tier アーキテクチャ**: Outline → Recipe → Tier 2 の分離設計が優れている。設計意図（Recipe）とテンプレート固有の実装詳細（Tier 2）が分離されており、同じ内容を別テンプレートで再利用できる。

2. **Skills アーキテクチャ**: AI の知識をオンデマンドで読み込む外部 Markdown ファイルとして管理。コンテキストウィンドウの制約下で合理的。共通スキル（skills/）とテンプレート固有スキル（templates/*/design_guide.md）の2層構造。

3. **テンプレート二重定義**: profile.json（機械可読）と design_guide.md（AI可読）の併用。コードと AI が同じテンプレート定義を異なる形式で参照できる。

4. **対話ベースのワークフロー**: レシピ段階でユーザーとディスカッションする設計。「一括生成」ではなく「1枚ずつ丁寧に作る」思想がシステムに組み込まれている。

5. **全ファイル git 管理**: PPTX・サムネイル・Tier 2 JSON を含め全て git で追跡。バイナリ成果物のバージョン管理を git 履歴に統一。

### 課題

1. **システムとデータの混在**: コード（pptx_engine.py 等）と生成物（slides/）が同一リポジトリ。プロジェクト数の増加でリポジトリが肥大化するリスク。

2. **オーケストレーターが暗黙的**: 3 Tier フローの制御ロジックは CLAUDE.md に自然言語で記述。Claude Code が不在だと Recipe 生成や Tier 2 変換を実行できない。再現性・自動化に制約。

3. **CLAUDE.md の肥大化**: ワークフロー定義、JSON スキーマ、CLI リファレンス、スキル読み込みルールが1ファイルに集約。メンテナンス性低下のリスク。

4. **形式的な品質管理の不在**:
   - `requirements.txt` / `pyproject.toml` がない
   - JSON スキーマバリデーションがない
   - 自動テストがない

5. **README.md が未整備**: プロジェクト概要、セットアップ手順、使い方が記載されていない。

### 総合評価

プロトタイプ・個人ツールとしては高い完成度。3 Tier + Recipe + Skills の設計思想はプロダクト化にも耐えるポテンシャルがある。次の段階に進むには、依存関係管理、README 整備、CLAUDE.md 分離が優先。

### 次回評価時の確認事項

- [ ] リポジトリサイズの推移（git 管理方針の影響）
- [ ] CLAUDE.md のサイズと分割の必要性
- [ ] テンプレート数の増加に伴うスケーラビリティ
- [ ] 新規ユーザーが参加できる状態か（README・セットアップ手順）
