# 参加ガイド

このプロジェクトへの参加方法を説明します。AI エージェントも人間も同じ手順で参加できます。

---

## 参加の形態

| 形態 | 説明 |
|---|---|
| **プレゼン制作** | ユーザーと対話しながら提案書 PPTX を作る |
| **機能開発** | エンジン（pptx_engine.py）やCLIを改善する |
| **ドキュメント整備** | ADR、スキル、テンプレートガイドを追加・更新する |
| **テンプレート追加** | 新しい PowerPoint テンプレートを登録する |

---

## AI エージェント向けオンボーディング

### 必読順序

以下を **この順番で** 読む。途中スキップ禁止。

```
1. STATUS.md          ← 現在のフェーズと次のタスク
2. docs/vision.md     ← プロジェクトの本質（なぜ作っているか）
3. docs/ROADMAP.md    ← Phase別の目標と完了条件
4. docs/adr/001_three_tier_process.md  ← 3層アーキテクチャの理由
5. docs/adr/002_recipe_layer.md        ← Recipe層の理由
6. CLAUDE.md          ← 具体的な操作手順（プレゼン制作時）
```

### オンボーディングテスト（必須）

作業前に [STATUS.md](STATUS.md) のオンボーディングテストに回答し、ユーザーの承認を得ること。

テストに答えられない = 理解が不十分 = 作業開始不可。

### 作業ルール

1. **検証してから「完了」と書く**: STATUS.md に完了と記載する前に、成果物が実際に存在し内容が正しいことを確認する
2. **1コミットで完結**: セッション断絶に備え、各作業を独立したコミット単位に分解する
3. **Schema 準拠**: JSON ファイルを作成・変更した場合は `python validate_schemas.py` でバリデーションを通す
4. **PNG 一括禁止**: サムネイルは1枚ずつ確認する（コンテキスト節約）
5. **セッション終了前**: 必ずコミット・プッシュし、STATUS.md を最新状態に更新する

---

## 人間向けオンボーディング

### 環境構築

```bash
pip install python-pptx anthropic google-genai python-dotenv Pillow jsonschema
```

`.env` を作成:
```env
ANTHROPIC_API_KEY=sk-ant-api03-...
GEMINI_API_KEY=AIzaSy...
```

### Claude Code を使った制作

VSCode に Claude Code 拡張機能をインストールし、`work/` ディレクトリで起動する。
プレゼン制作は [docs/WORKFLOW.md](docs/WORKFLOW.md) の手順に従う。

### 直接 CLI を操作する場合

```bash
# アウトラインからプロジェクト初期化
python generate_pptx.py --outline "slides/YYYYMMDD_タイトル/outline.json" --project "タイトル"

# Tier 2 JSON を編集後、PPTX を結合
python generate_pptx.py --assemble-only --project "タイトル" --thumbnail

# Schema バリデーション
python validate_schemas.py
```

---

## テンプレートを追加する

```bash
# 1. テンプレートを解析して profile.json を生成
python template_analyzer.py analyze "path/to/template.pptx" --id "my_template" --name "テンプレート名"

# 2. design_guide.md を手書きで追加
# templates/my_template/design_guide.md に座標・色・レイアウトパターンを記述

# 3. 動作確認
python generate_pptx.py --assemble-only --project "テスト" --template "my_template"
```

詳細: [docs/adr/005_template_dual_definition.md](docs/adr/005_template_dual_definition.md)

---

## ドキュメントを追加・変更する

### ADR を追加する

設計判断をした時は ADR を書く。

- 場所: `docs/adr/NNN_<title>.md`
- 番号: 既存の最大番号 + 1
- フォーマット: 既存の ADR を参照

### スキルを更新する

`skills/` 以下のファイルは AI がオンデマンドで読み込む知識ベース。
内容が変わったら ADR を書くか、既存のスキルを更新する。

---

## 複数 AI 協業ルール

VSCode 上で複数の AI 拡張機能（Claude Code、Gemini Code Assist 等）が同時に動作する場合のルール。

### AI 向けルール（AI が自律的に守る）

- **作業前に git status を確認する**: 他の AI が未コミットの変更を残していないか確認する
- **完了前に成果物を検証する**: `validate_schemas.py` 等で内容が正しいことを確認してから「完了」と言う
- **ファイルパスを明示する**: ファイル内容をチャットで提示する場合は、保存先のフルパスを明記する
  - 良い例: `.github/workflows/validate.yml` の内容として以下を保存してください
  - 悪い例: ファイル名のみ（保存先が曖昧）

### 人間向けルール（人間が橋渡しする）

AI には **VSCode の UI 操作（Accept/Reject）が見えない**。人間が状態を言語化して伝える必要がある。

- **「まだ Accept していない」と明示する**: Gemini の差分をレビューに出す場合は、Accept 前であることを伝える
- **Accept/Reject 後に状態を伝える**: 操作後は `git status` の結果を AI に共有するか、「承認した」「却下した」と伝える
- **同時編集を避ける**: 1つのファイルを複数の AI に同時に編集させない。一方の AI が完了してコミットしてから次の AI に渡す

### 理想的な多 AI 協業フロー（将来目標）

現状の「AI が直接ファイルを書き換える」方式は UI 操作が git の外で起きるため競合リスクがある。
将来的には「AI が branch + PR を出す → 人間またはレビュー AI がマージ」の形にすることで、
全ての状態変化が git を通じて可視化される。

## ブランチ・PR ルール

現時点ではブランチ運用なし（main 直コミット）。
チームが増えた場合は ADR で方針を決める。

---

## よくある問題

- **PPTX の ZIP エラー**: [docs/knowhow.md](docs/knowhow.md) の「Duplicate name エラー」参照
- **Gemini 画像生成失敗**: `.env` の `GEMINI_API_KEY` を確認。モデル名は `gemini-3-pro-image-preview`
- **git が動かない**: PowerShell から実行すること（bash シェルでは PATH に git がない場合がある）
