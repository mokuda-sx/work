import sys
import json
from pathlib import Path

# Add grandparent directory (work root) to path
work_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(work_root))

from pptx_engine import build_from_slides_dir

# Get the slides subdirectory
slides_subdir = Path(__file__).parent / "slides"
current_dir = Path(__file__).parent

#　結合用 outline.json を生成
slides_files = sorted(slides_subdir.glob("*.json"))
outline = []
for f in slides_files:
    data = json.loads(f.read_text(encoding="utf-8"))
    outline.append(data)

# outline.json をプロジェクトルートに保存
outline_path = current_dir / "outline.json"
outline_path.write_text(json.dumps(outline, ensure_ascii=False, indent=2))
print(f"Generated: {outline_path}")

# Now build PPTX
output_path = current_dir / "20260217_1802_fontsize_fix.pptx"

print(f"Generating PPTX from outline...")
result = build_from_slides_dir(slides_subdir, output_path, template_id="sx_proposal")
print(f"Done: {result}")

