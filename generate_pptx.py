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
OUTPUT_DIR  = Path(__file__).parent / "output"
RECIPES_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

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
    parser.add_argument("--no-image",  action="store_true", help="画像生成をスキップ")
    parser.add_argument("--thumbnail", action="store_true", help="生成後にPNGサムネイルを書き出す（要pywin32）")
    parser.add_argument("--save-recipe", help="生成したアウトラインをレシピとして保存するファイル名")
    parser.add_argument("--git",       action="store_true", help="生成後にgit commit & push")
    args = parser.parse_args()

    # ─ アウトライン取得 ─
    if args.recipe:
        recipe_path = RECIPES_DIR / args.recipe if not Path(args.recipe).is_absolute() else Path(args.recipe)
        print(f"レシピを読み込み: {recipe_path}")
        outline = json.loads(recipe_path.read_text(encoding="utf-8"))
    elif args.outline:
        print(f"アウトラインを読み込み: {args.outline}")
        outline = json.loads(Path(args.outline).read_text(encoding="utf-8"))
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
    if args.output:
        output_name = args.output if args.output.endswith(".pptx") else args.output + ".pptx"
    else:
        title = outline[0].get("title", "提案書")[:20] if outline else "提案書"
        output_name = f"{timestamp}_{title}.pptx"
    output_path = OUTPUT_DIR / output_name

    # ─ PPTX生成 ─
    print(f"\nPPTX生成中...")
    from pptx_engine import build_pptx, export_thumbnails
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
