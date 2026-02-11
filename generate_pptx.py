"""
generate_pptx.py
Claude Code（VSCode）から直接呼び出すPPTX生成CLIツール

使い方:
  python generate_pptx.py "DX推進の提案書、製造業向け、5スライド"
  python generate_pptx.py --recipe recipes/dx_manufacturing.json
  python generate_pptx.py --recipe recipes/dx_manufacturing.json --no-image
  python generate_pptx.py --outline outline.json   # 既存JSONから生成

生成されたPPTXは output/ に保存され、git commitされる。
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

RECIPES_DIR = Path(__file__).parent / "recipes"
SLIDES_DIR  = Path(__file__).parent / "slides"
RECIPES_DIR.mkdir(exist_ok=True)
SLIDES_DIR.mkdir(exist_ok=True)

# ─── Claude API でアウトライン生成 ────────────────────
OUTLINE_SYSTEM_PROMPT = """あなたはプロのコンサルタントです。
ユーザーの要望を聞いて、提案書の中間言語JSONを生成してください。

出力形式（JSON配列のみ。マークダウン記法不要）:
[
  {"type": "title", "title": "提案書タイトル（20〜35文字）", "subtitle": "2026年X月　クライアント名御中"},
  {"type": "agenda", "title": "目次", "body": "1. 背景と課題\n2. 提案内容\n3. 期待効果\n4. スケジュール"},
  {"type": "chapter", "title": "1. 背景と課題"},
  {
    "type": "content",
    "title": "スライドタイトル（20〜35文字）",
    "subtitle": "キーメッセージ（40〜70文字）",
    "body": "・箇条書き1（30〜50文字）\n・箇条書き2（30〜50文字）\n・箇条書き3（30〜50文字）\n・箇条書き4（30〜50文字）",
    "objects": [
      {"type": "box", "text": "現状", "left": 0.5, "top": 4.5, "width": 2.5, "height": 0.9,
       "fill_color": "C00000", "font_color": "FFFFFF", "font_size": 13},
      {"type": "arrow", "left": 3.1, "top": 4.7, "width": 0.6, "height": 0.5, "fill_color": "ED7D31"},
      {"type": "box", "text": "目標", "left": 3.8, "top": 4.5, "width": 2.5, "height": 0.9,
       "fill_color": "4472C4", "font_color": "FFFFFF", "font_size": 13}
    ],
    "images": [
      {"prompt": "Professional business illustration related to the slide topic, clean minimal style",
       "model": "gemini-3-pro-image-preview",
       "left": 7.5, "top": 1.5, "width": 5.3}
    ]
  },
  {"type": "end"}
]

ルール:
- contentスライドには適宜 objects（図解）と images（AI生成画像）を追加する
- objectsは「現状→提案」「フェーズ図」「比較表」など図解が有効な場合に使う
- imagesは各contentスライドに1枚程度、スライド右半分（left:7.0以上）に配置する
- imageのpromptは英語で具体的に記述する（スライドの内容に合わせる）
- 座標系: 幅13.3 × 高さ7.5インチ。コンテンツエリアtop:1.5〜7.0
- JSON配列のみ返すこと
"""

def generate_outline_with_claude(description: str) -> list[dict]:
    import anthropic
    key = os.getenv("ANTHROPIC_API_KEY", "")
    if not key:
        raise ValueError("ANTHROPIC_API_KEY が設定されていません")
    client = anthropic.Anthropic(api_key=key)
    print(f"Claude にアウトライン生成を依頼中...")
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=8192,
        system=OUTLINE_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": description}],
    )
    raw = response.content[0].text.strip()
    # マークダウンブロック対応
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
    return json.loads(raw)

# ─── git commit helper ───────────────────────────────
def git_commit(filepath: Path, message: str):
    try:
        subprocess.run(["git", "add", str(filepath)], cwd=filepath.parent, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", message], cwd=filepath.parent, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=filepath.parent, check=True, capture_output=True)
        print(f"  [git] commit & push 完了: {filepath.name}")
    except subprocess.CalledProcessError as e:
        print(f"  [git] 失敗（手動でpushしてください）: {e}")

# ─── メイン ──────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="AI PowerPoint Generator CLI")
    parser.add_argument("description", nargs="?", help="提案書の説明（例: 'DX推進の提案書、製造業向け'）")
    parser.add_argument("--recipe",   help="レシピJSONファイルのパス（recipes/xxx.json）")
    parser.add_argument("--outline",  help="既存のアウトラインJSONファイル")
    parser.add_argument("--output",   help="出力ファイル名（省略時は自動命名）")
    parser.add_argument("--project",  help="プロジェクト名（slides/YYYYMMDD_<project>/ に保存）")
    parser.add_argument("--no-image",  action="store_true", help="画像生成をスキップ")
    parser.add_argument("--thumbnail", action="store_true", help="生成後にPNGサムネイルを書き出す（PowerPoint必要、管理者権限不要）")
    parser.add_argument("--save-recipe", help="生成したアウトラインをレシピとして保存するファイル名")
    parser.add_argument("--git",          action="store_true", help="生成後にgit commit & push")
    parser.add_argument("--assemble-only", action="store_true",
                        help="project_dir/slides/ の既存Tier 2ファイルを結合するだけ（--project 必須）")
    args = parser.parse_args()

    # ─ --assemble-only: 既存 Tier 2 ファイルを結合 ─
    if args.assemble_only:
        if not args.project:
            print("エラー: --assemble-only には --project が必要です")
            sys.exit(1)
        safe_project = "".join(c for c in args.project if c not in r'\/:*?"<>|')
        matching = sorted(SLIDES_DIR.glob(f"*_{safe_project}"), reverse=True)
        if not matching:
            print(f"エラー: プロジェクトフォルダーが見つかりません: *_{safe_project}")
            sys.exit(1)
        project_dir   = matching[0]
        slides_subdir = project_dir / "slides"
        if not slides_subdir.exists():
            print(f"エラー: slides/ サブフォルダーがありません: {slides_subdir}")
            sys.exit(1)
        timestamp   = datetime.now().strftime("%Y%m%d_%H%M")
        output_path = project_dir / (args.output if args.output else f"{timestamp}_{safe_project}.pptx")
        print(f"\nTier 2 結合中: {slides_subdir}")
        from pptx_engine import build_from_slides_dir
        result_path = build_from_slides_dir(slides_subdir, output_path, export_png=args.thumbnail)
        print(f"\n完了: {result_path}")
        subprocess.Popen(["powershell", "-Command", f"Start-Process '{result_path}'"])
        if args.git:
            git_commit(result_path, f"Assemble: {args.project}")
        return

    # ─ アウトライン取得 ─
    if args.recipe:
        recipe_path = RECIPES_DIR / args.recipe if not Path(args.recipe).is_absolute() else Path(args.recipe)
        print(f"レシピを読み込み: {recipe_path}")
        outline = json.loads(recipe_path.read_text(encoding="utf-8"))
    elif args.outline:
        print(f"アウトラインを読み込み: {args.outline}")
        raw = json.loads(Path(args.outline).read_text(encoding="utf-8"))
        # Tier 1 形式（{title, description, slides: [{index, type, title, note}]}）の検出
        if isinstance(raw, dict) and "slides" in raw:
            print(f"  [Tier 1] インデックス形式を検出: {len(raw['slides'])}スライド")
            outline = raw["slides"]  # Tier 1 エントリ（各スライドの最小情報）を使用
            # プロジェクト名が未指定なら title から取得
            if not args.project:
                args.project = raw.get("title", "提案書")[:30]
        else:
            outline = raw
    elif args.description:
        outline = generate_outline_with_claude(args.description)
        print(f"  → {len(outline)}スライドのアウトライン生成完了")
    else:
        parser.print_help()
        sys.exit(1)

    # ─ 画像生成スキップ設定 ─
    if args.no_image:
        for slide in outline:
            slide.pop("images", None)

    # ─ レシピ保存 ─
    if args.save_recipe:
        recipe_path = RECIPES_DIR / args.save_recipe
        recipe_path.write_text(json.dumps(outline, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  [recipe] 保存: {recipe_path}")

    # ─ 出力パス決定 ─
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    title_raw = outline[0].get("title", "提案書")[:20] if outline else "提案書"

    # プロジェクトフォルダー: slides/YYYYMMDD_<project名>/
    date_str = datetime.now().strftime("%Y%m%d")
    project_name = args.project if args.project else title_raw
    # ファイル名に使えない文字を除去
    safe_project = "".join(c for c in project_name if c not in r'\/:*?"<>|')
    project_dir = SLIDES_DIR / f"{date_str}_{safe_project}"
    project_dir.mkdir(exist_ok=True)

    if args.output:
        output_name = args.output if args.output.endswith(".pptx") else args.output + ".pptx"
    else:
        output_name = f"{timestamp}_{safe_project}.pptx"
    output_path = project_dir / output_name

    # outline.json もプロジェクトフォルダーにコピー保存（読み込んだ内容そのまま）
    raw_outline = json.loads(Path(args.outline).read_text(encoding="utf-8")) if args.outline else outline
    (project_dir / "outline.json").write_text(
        json.dumps(raw_outline, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # ─ Tier 2 スタブファイル生成（Tier 1 形式の場合のみ） ─
    # Tier 1 形式の検出: outline が list で各要素に "index" キーがあり body/objects/images がない
    is_tier1_entries = (
        isinstance(outline, list) and outline
        and all("index" in s and "body" not in s and "objects" not in s for s in outline)
    )
    slides_subdir = project_dir / "slides"
    if is_tier1_entries:
        slides_subdir.mkdir(exist_ok=True)
        for s in outline:
            idx  = s.get("index", 0)
            stype = s.get("type", "content")
            fname = f"{idx:02d}_{stype}.json"
            fpath = slides_subdir / fname
            if not fpath.exists():  # 既存の展開済みファイルは上書きしない
                fpath.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  [Tier 2] スタブ作成: {slides_subdir} ({len(outline)}枚)")
        print(f"  ↑ 各 .json を展開後、--assemble-only --project \"{args.project}\" で結合してください")

    # ─ PPTX生成 ─
    print(f"\nPPTX生成中...")
    if is_tier1_entries and slides_subdir.exists():
        from pptx_engine import build_from_slides_dir
        result_path = build_from_slides_dir(slides_subdir, output_path, export_png=args.thumbnail)
    else:
        from pptx_engine import build_pptx
        result_path = build_pptx(outline, output_path, export_png=args.thumbnail)
    print(f"\n完了: {result_path}")

    # ─ 自動オープン ─
    subprocess.Popen(["powershell", "-Command", f"Start-Process '{result_path}'"])

    # ─ git commit ─
    if args.git:
        title = outline[0].get("title", "提案書") if outline else "提案書"
        git_commit(result_path, f"Add slide: {title}")

    # アウトラインのJSONも表示（Claude Codeが確認しやすいように）
    print(f"\n--- 生成されたアウトライン ---")
    print(json.dumps(outline, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
