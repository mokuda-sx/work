"""
dev_tools.py - 開発・デバッグ用ユーティリティ

使い方:
  python dev_tools.py env                              # API キー確認
  python dev_tools.py template <path.pptx>             # テンプレートのシェイプ・構造確認
  python dev_tools.py layouts <path.pptx>              # レイアウト別プレースホルダー一覧
  python dev_tools.py layouts                          # デフォルトテンプレートのレイアウト
"""

import sys
from pathlib import Path


def cmd_env():
    """環境変数（APIキー）の設定確認"""
    from dotenv import load_dotenv
    import os
    load_dotenv()
    ak = os.getenv("ANTHROPIC_API_KEY", "")
    gk = os.getenv("GEMINI_API_KEY", "")
    print("ANTHROPIC_API_KEY:", ak[:20] + "..." if len(ak) > 20 else ak or "(not set)")
    print("GEMINI_API_KEY   :", gk[:20] + "..." if len(gk) > 20 else gk or "(not set)")


def cmd_template(pptx_path: str):
    """テンプレートのスライド・シェイプ構造を表示"""
    from pptx import Presentation
    prs = Presentation(pptx_path)
    print(f"File: {pptx_path}")
    print(f"Slides: {len(prs.slides)}")
    print(f"Size: {prs.slide_width.inches:.3f} x {prs.slide_height.inches:.3f} inches")
    print()
    print("=== Layouts ===")
    for i, layout in enumerate(prs.slide_layouts):
        print(f"  [{i}] {layout.name}")
    print()
    print("=== Slides ===")
    for i, slide in enumerate(prs.slides):
        layout_name = slide.slide_layout.name
        print(f"\nSlide {i+1} [{layout_name}]: {len(slide.shapes)} shapes")
        for s in slide.shapes:
            text = ""
            if s.has_text_frame:
                text = s.text_frame.text[:40].replace("\n", " ")
            try:
                ph_idx = s.placeholder_format.idx if s.is_placeholder else None
            except Exception:
                ph_idx = None
            print(f'  type={s.shape_type} name="{s.name}" ph_idx={ph_idx} text="{text}"')


def cmd_layouts(pptx_path: str):
    """レイアウト別のプレースホルダー一覧を表示"""
    from pptx import Presentation
    prs = Presentation(pptx_path)
    print(f"File: {pptx_path}")
    print()
    print("=== Layout Placeholders ===")
    for i, layout in enumerate(prs.slide_layouts):
        print(f"\n[{i}] {layout.name}")
        for ph in layout.placeholders:
            print(f"  ph_idx={ph.placeholder_format.idx} name=\"{ph.name}\" type={ph.placeholder_format.type}")

    print("\n\n=== Slide Placeholders (actual) ===")
    for i, slide in enumerate(prs.slides):
        print(f"\nSlide {i+1} [{slide.slide_layout.name}]")
        for ph in slide.placeholders:
            text = ph.text_frame.text[:40].replace("\n", " ") if ph.has_text_frame else ""
            print(f'  ph_idx={ph.placeholder_format.idx} name="{ph.name}" text="{text}"')


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    default_template = str(Path(__file__).parent / "templates" / "sx_proposal" / "template.pptx")

    if cmd == "env":
        cmd_env()
    elif cmd == "template":
        path = sys.argv[2] if len(sys.argv) > 2 else default_template
        cmd_template(path)
    elif cmd == "layouts":
        path = sys.argv[2] if len(sys.argv) > 2 else default_template
        cmd_layouts(path)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
