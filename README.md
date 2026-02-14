# AI PowerPoint Generator

AI との対話で、企業の PowerPoint テンプレートから提案書を生成する実験プロジェクト。

単なるテキスト流し込みではなく、**人間の制作プロセスを分解・明示化**し、AI が各段階に参加できる構造を実現している。

## 何ができるか

- テンプレートに基づいた提案書 PPTX の生成
- 複数テンプレート対応（自社・他社テンプレートの切り替え）
- AI 画像生成（Gemini API）によるスライド内画像の自動挿入
- 対話ベースの段階的制作（1枚ずつレビューしながら作る）

## アーキテクチャ

```
Tier 1（アウトライン）→ Recipe（設計意図）→ Tier 2（テンプレート固有JSON）→ PPTX結合
     構成・流れ         何をどう見せるか      座標・色・フォントサイズ       最終出力
```

- **Tier 1**: 全体の構成とストーリーライン（JSON）
- **Recipe**: スライドごとの設計意図。テンプレート非依存（JSON）
- **Tier 2**: テンプレート固有の座標・色・フォント設定（JSON）
- **Assembly**: Tier 2 ファイル群 → PPTX 結合

詳細: [docs/vision.md](docs/vision.md) | 設計判断の理由: [docs/adr/](docs/adr/)

## セットアップ

### 必要要件

- Python 3.10 以上
- Anthropic API Key（テキスト生成用）
- Google Gemini API Key（画像生成用）

### インストール

```bash
pip install python-pptx anthropic google-genai python-dotenv Pillow
```

### 環境変数

プロジェクトルートに `.env` ファイルを作成:

```env
ANTHROPIC_API_KEY=sk-ant-api03-...
GEMINI_API_KEY=AIzaSy...
```

## 使い方

### Claude Code との対話（推奨）

VSCode + Claude Code 拡張機能を使い、対話形式でスライドを制作する。
ワークフローの詳細は [CLAUDE.md](CLAUDE.md) を参照。

### CLI コマンド

```bash
# アウトラインからプロジェクト構造を作成
python generate_pptx.py --outline "outline.json" --project "提案書タイトル"

# Tier 2 ファイルから PPTX を結合
python generate_pptx.py --assemble-only --project "提案書タイトル"

# サムネイル付きで結合
python generate_pptx.py --assemble-only --project "提案書タイトル" --thumbnail

# 画像生成なし（高速）
python generate_pptx.py --assemble-only --project "提案書タイトル" --no-image

# テンプレート登録
python template_analyzer.py analyze "path/to/template.pptx" --id "my_template" --name "Template Name"
```

## プロジェクト構成

```
work/
├── pptx_engine.py          # PPTX 生成エンジン
├── generate_pptx.py        # CLI エントリーポイント
├── template_analyzer.py    # テンプレート登録ツール
├── CLAUDE.md               # AI ワークフロー定義
├── STATUS.md               # 現在の開発状態（セッション引き継ぎ用）
├── templates/              # テンプレート定義
│   ├── sx_proposal/        #   SX提案書 3.0（デフォルト）
│   └── jr_east/            #   JR East テンプレート
├── skills/                 # AI スキルファイル（共通）
├── slides/                 # 生成プロジェクト（プロジェクト別）
└── docs/                   # ドキュメント
    ├── vision.md           #   プロジェクトビジョン
    ├── ROADMAP.md          #   開発ロードマップ
    ├── knowhow.md          #   技術ノウハウ
    └── adr/                #   Architecture Decision Records
```

## ドキュメント

| ファイル | 内容 |
|---|---|
| [CLAUDE.md](CLAUDE.md) | AI ワークフロー定義・JSON スキーマ |
| [STATUS.md](STATUS.md) | 現在の開発状態・次のアクション |
| [docs/vision.md](docs/vision.md) | プロジェクトビジョン・5つの原則 |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Phase 0-4 開発ロードマップ |
| [docs/knowhow.md](docs/knowhow.md) | 技術的注意点・既知の問題 |
| [docs/adr/](docs/adr/) | 設計判断の記録 |

## 開発状況

現在のフェーズと進捗は [STATUS.md](STATUS.md) を参照。
