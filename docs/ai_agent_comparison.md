# AI エージェント比較：設定と動作モデルの考察

> 作成: 2026-02-14 | 担当: Claude Code (Sonnet 4.5)
> 更新: このファイルは実験結果が蓄積されたら随時更新する

---

## 概要

このプロジェクトでは複数の AI エージェントが協業している。
各エージェントの動作モデルと能力を正確に理解することで、
「何を誰に頼むか」の判断精度を上げることが目的。

---

## 動作モデルの基本分類

AI コーディングアシスタントには根本的に異なる2つのモデルがある。

```
【提案型】  ユーザー → AI → diff 提案 → Accept/Reject → ファイル変更
【実行型】  ユーザー → AI → コマンド実行・ファイル操作（即座に反映）
```

| 特性 | 提案型 | 実行型 |
|---|---|---|
| ファイル変更のタイミング | Accept 後 | 即座 |
| git への反映 | UI 操作経由 | 直接 |
| 競合リスク | 低（人間がゲート） | 高（即座に反映） |
| 作業速度 | 遅い（確認コスト） | 速い |
| 自己検証（実行→確認） | 不可 | 可能 |

---

## 各エージェントの現状（2026-02-14 時点）

### Claude Code（Anthropic）

**モデル**: ネイティブ実行型

- ターミナルから直接起動、ファイルシステムに直接アクセス
- `python validate_schemas.py` を実行して結果を自己検証できる
- `git status` / `git log` をリアルタイムで確認できる
- **CLAUDE.md を自動的に読み込んでプロジェクト固有のルールに従う**
- 破壊的操作（`git push` 等）は確認を求めるが、それ以外は自律実行

**このプロジェクトでの位置づけ**: メインの実装担当

---

### Gemini Code Assist（Google、VSCode拡張）

**モデル**: デフォルトは提案型。Agent Mode で実行型に切り替え可能。

#### 通常モード（提案型）
- GitHub リポジトリ全体を参照できる
- ファイル変更は diff 提案 → Accept/Reject 経由
- ターミナルコマンドは実行できない（提案のみ）

#### Agent Mode（実行型）
- Gemini CLI が内部エンジンとして動作
- ファイル読み書き（絶対パスで直接）
- ターミナルコマンド実行（python, git 等）
- 破壊的操作は確認プロンプトが出る
- **既知の問題（2026-01）**: VSCode 上の Agent Mode でシェルコマンドがブロックされるケースがある

#### Gemini CLI（ターミナル版）
- オープンソース（https://github.com/google-gemini/gemini-cli）
- Claude Code と同等のアーキテクチャ（ターミナル直接実行）
- ファイルシステム直接アクセス、git, python 等を自律実行
- `.geminiignore` でコンテキストから除外するファイルを制御可能

**このプロジェクトでの観察結果（2セッション）**:
- 通常モードでは「確認せずに推測で回答する」傾向がある
- Q4（ファイル検証）でファイル名を省略・推測した
- パス指定に誤りがある yml を提案した（`work/slides/` が余分）
- **根本原因は動作モデルではなく「確認習慣の欠如」**

---

### GitHub Copilot（Microsoft、VSCode拡張）

**モデル**: デフォルトは提案型。Agent Mode（VSCode 1.99以降）で実行型に近づく。

#### 通常モード（提案型）
- コード補完・インラインサジェスト中心
- チャットで質問・ファイル生成提案

#### Agent Mode（VSCode 1.99以降）
- ターミナルコマンドを実行できる
- ただし**毎回 Allow/Deny の確認が必要**
- 「このセッション中は常に Allow」「このワークスペースでは常に Allow」の設定で自動化可能
- `Allow` 設定を使えば Claude Code に近い自律動作が可能

**未実験**: このプロジェクトでは未使用。Agent Mode での動作は未検証。

---

### OpenAI Codex CLI（OpenAI）

**モデル**: ネイティブ実行型（Claude Code / Gemini CLI と同等設計）

- ターミナルエージェント（`npx codex` で起動）
- ファイル読み書き・コマンド実行がデフォルト
- Agent モードで自律的なマルチステップ実行
- `o4-mini` / `o3` ベースのモデル
- MCP サーバー統合対応

**未実験**: このプロジェクトでは未使用。

---

## 2026年の新動向：Agent Skills の標準化

Codex CLI、Gemini CLI、Claude Code で「Agent Skills」という共通フォーマットが収束しつつある。

```
.agent/skills/     ← ワークスペーススコープのスキル
~/.gemini/skills/  ← グローバルスコープのスキル
```

このプロジェクトの `skills/` ディレクトリは、
将来この標準フォーマットに移行できる設計になっている（エージェント非依存）。

---

## 動作モデルと「確認習慣」の関係

### 重要な発見

Gemini の失敗は「提案型だから」ではなかった。

| フェーズ | Gemini の失敗 | 動作モデルの関係 |
|---|---|---|
| Phase 1 | 空ファイルを作成して「完了」と申告 | 提案型でも実行型でも起きる |
| Phase 2（第1バッチ） | 空ファイルをコミット | 提案型だから人間が防げた |
| Phase 2（第2バッチ） | パスを推測で記述 | 実行型なら誤ったパスに書き込む危険 |

**実行型に切り替えると「確認習慣の欠如」がより危険になる**。

Agent Mode に切り替える前に、以下を検証すること：

```
Q4 強化版テスト（Agent Mode 用）:
  「docs/adr/ にあるADRファイルの件数と、
   001_*.md ファイルの最初の1行を実際に読んで引用せよ」

→ 実際にコマンドを実行して引用できれば「確認習慣あり」
→ 記憶や推測で答えれば「確認習慣なし」
```

---

## このプロジェクトでの役割分担（推奨）

| 作業種別 | 推奨エージェント | 理由 |
|---|---|---|
| 実装・ファイル操作・git | Claude Code | ネイティブ実行型、CLAUDE.md を自動読み込み |
| 設計相談・ドキュメント読解 | Gemini（通常モード） | GitHub コンテキスト、提案型で安全 |
| 大規模リファクタリング（実験的） | Gemini Agent Mode / Copilot Agent Mode | Agent Mode の安定性が確認できれば |
| 他 CLI エージェントとの比較実験 | Gemini CLI / Codex CLI | 実験場として活用可能 |

---

## 多 AI 協業のリスクと対策

### 競合パターン（実際に発生）

```
Claude Code が STATUS.md を編集・コミット
      ↑
Gemini が STATUS.md の diff を提案（まだ未Accept）
      ↓
ユーザーが Accept → Claude の変更と競合
```

**対策**: CONTRIBUTING.md の「複数 AI 協業ルール」参照
- 人間側ルール：「まだ Accept していない」と明示する
- AI 側ルール：作業前に `git status` を確認する

### 将来の理想形

```
Gemini → branch を作成 → PR を出す → Claude or 人間がレビュー → merge
```

全ての状態変化が git を通じて可視化される。
現状の「Accept/Reject が git の外で起きる」問題が解消される。

---

## 将来の統合候補

### OpenClaw（ローカル AI ゲートウェイ）

> 状態: **インストール済み（2026-02-14）、未統合**
> リポジトリ: https://github.com/openclaw/openclaw

#### 概要

ローカルで動く AI アシスタントのゲートウェイ。WhatsApp / Slack / Discord / Teams / LINE 等のメッセージングチャネルから Claude や OpenAI を呼び出せる。

```
[WhatsApp / Slack / Teams / Discord 等]
        ↓
    OpenClaw Gateway (ws://127.0.0.1:18789)
        ↓
    Claude / OpenAI（モデル選択可）
        ↓
    ツール実行（ブラウザ、スクリーン録画、スキル等）
```

#### このプロジェクトとの接続可能性

| 側面 | 評価 |
|---|---|
| スキルアーキテクチャ（ClawHub） | このプロジェクトの `skills/` と構造が近い。将来の互換性がある |
| メッセージング経由のトリガー | 「Slack で `スライド作って` → PPTX 生成」が実現できる可能性 |
| チームアクセス | VSCode を持たないメンバーも提案書生成プロセスにアクセスできる |
| ファイルシステム操作 | Claude Code のような直接操作はしない（ゲートウェイが主な役割）|

#### 今でない理由

1. **Phase 3 はコンテンツ作業** — 参照ライブラリの構築に OpenClaw は不要
2. **インターフェース拡張より先に品質** — ゲートウェイを増やす前に生成品質が安定していることが前提
3. **役割の明確化が先** — Claude Code / Gemini / Copilot の役割分担が確立してから外部チャネルを接続する

#### 統合を検討すべきタイミング

以下のいずれかに当たったとき：
- Phase 3 完了後、チームでの共同制作ユースケースが出てきたとき
- 「VSCode を開かずにスライドを依頼したい」という具体的なニーズが生まれたとき
- OpenClaw のスキル仕様が Agent Skills 標準に収束したとき（他エージェントとの共通化）

---

## 参考リンク

- [Gemini CLI (GitHub)](https://github.com/google-gemini/gemini-cli)
- [Gemini Code Assist Agent Mode](https://developers.google.com/gemini-code-assist/docs/agent-mode)
- [GitHub Copilot Agent Mode (VSCode)](https://code.visualstudio.com/blogs/2025/02/24/introducing-copilot-agent-mode)
- [OpenAI Codex CLI (GitHub)](https://github.com/openai/codex)
- [OpenClaw (GitHub)](https://github.com/openclaw/openclaw)
- このプロジェクトの協業ルール: [CONTRIBUTING.md](../CONTRIBUTING.md)
- Phase 2 回顧録（実験記録）: [retrospective_phase2_20260214.md](retrospective_phase2_20260214.md)
