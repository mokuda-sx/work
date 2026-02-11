"""
pptx_engine.py
PPTX生成エンジン（中間言語JSONからPPTXを生成するコアモジュール）

中間言語スキーマ:
[
  {
    "type": "title" | "agenda" | "chapter" | "content" | "end",
    "title": "スライドタイトル",
    "subtitle": "キーメッセージ",
    "body": "本文\n複数行\n箇条書き",
    "objects": [
      {"type": "box",   "text": "ラベル", "left": 0.5, "top": 3.0, "width": 2.5, "height": 0.9,
       "fill_color": "4472C4", "font_color": "FFFFFF", "font_size": 14, "bold": true},
      {"type": "arrow", "left": 3.1, "top": 3.2, "width": 0.5, "height": 0.5, "fill_color": "ED7D31"},
      {"type": "text",  "text": "補足", "left": 1.0, "top": 4.0, "width": 4.0, "height": 0.5,
       "font_color": "404040", "font_size": 11}
    ],
    "images": [
      {"prompt": "English image prompt",
       "model": "gemini-3-pro-image-preview",
       "left": 7.0, "top": 1.5, "width": 5.5}
    ]
  }
]

座標系: 幅13.3 × 高さ7.5インチ（16:9）
"""

import os
import io
import json
import ast
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE

TEMPLATE_PATH = Path(__file__).parent / "SX_提案書_3.0_16x9.pptx"
OUTPUT_DIR    = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

LAYOUT = {
    "title":   0,
    "chapter": 4,
    "agenda":  2,
    "content": 6,
    "end":    14,
}

# ─── テンプレート操作 ─────────────────────────────────
def load_template() -> Presentation:
    return Presentation(str(TEMPLATE_PATH))

def remove_all_slides(prs: Presentation):
    r_ns = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    slide_id_list = prs.slides._sldIdLst
    for sld_id in list(slide_id_list):
        rId = sld_id.get(f'{{{r_ns}}}id')
        if rId:
            prs.part.rels.pop(rId)
        slide_id_list.remove(sld_id)

# ─── テキスト設定 ─────────────────────────────────────
def fill_text_frame(tf, text: str):
    tf.clear()
    lines = [l for l in text.split('\n') if l.strip()]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line

def set_placeholder_text(slide, ph_idx: int, text: str) -> bool:
    for shape in slide.shapes:
        if shape.is_placeholder and shape.placeholder_format.idx == ph_idx:
            fill_text_frame(shape.text_frame, text)
            return True
    return False

def set_body_text(slide, text: str):
    for idx in [10, 14, 1, 2]:
        if set_placeholder_text(slide, idx, text):
            return

# ─── オブジェクト設定 ─────────────────────────────────
def parse_objects(objects) -> list[dict]:
    if not objects:
        return []
    if isinstance(objects, list):
        return [o for o in objects if isinstance(o, dict)]
    if isinstance(objects, str):
        try:
            result = ast.literal_eval(objects.strip())
            return result if isinstance(result, list) else []
        except Exception:
            try:
                return json.loads(objects.strip())
            except Exception:
                return []
    return []

def add_objects_to_slide(slide, objects: list[dict]):
    for obj in parse_objects(objects):
        obj_type = obj.get("type", "box")
        left   = Inches(obj.get("left",   1.0))
        top    = Inches(obj.get("top",    2.0))
        width  = Inches(obj.get("width",  2.0))
        height = Inches(obj.get("height", 0.8))

        if obj_type in ("box", "rect"):
            shape = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RECTANGLE, left, top, width, height)
            shape.fill.solid()
            shape.fill.fore_color.rgb = RGBColor.from_string(obj.get("fill_color", "4472C4"))
            shape.line.fill.background()
            text = obj.get("text", "")
            if text:
                tf = shape.text_frame
                tf.word_wrap = True
                tf.clear()
                p = tf.paragraphs[0]
                p.text = text
                p.alignment = PP_ALIGN.CENTER
                run = p.runs[0] if p.runs else p.add_run()
                run.font.size  = Pt(obj.get("font_size", 12))
                run.font.color.rgb = RGBColor.from_string(obj.get("font_color", "FFFFFF"))
                run.font.bold  = obj.get("bold", True)

        elif obj_type == "arrow":
            shape = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RIGHT_ARROW, left, top, width, height)
            shape.fill.solid()
            shape.fill.fore_color.rgb = RGBColor.from_string(obj.get("fill_color", "ED7D31"))
            shape.line.fill.background()

        elif obj_type == "text":
            txBox = slide.shapes.add_textbox(left, top, width, height)
            tf = txBox.text_frame
            tf.word_wrap = True
            tf.clear()
            p = tf.paragraphs[0]
            p.text = obj.get("text", "")
            p.alignment = PP_ALIGN.LEFT
            if p.runs:
                run = p.runs[0]
                run.font.size  = Pt(obj.get("font_size", 11))
                run.font.color.rgb = RGBColor.from_string(obj.get("font_color", "404040"))

# ─── 画像生成 (Gemini) ───────────────────────────────
def generate_image_gemini(prompt: str, model: str = "gemini-3-pro-image-preview") -> bytes | None:
    from google import genai
    from google.genai import types as genai_types
    key = os.getenv("GEMINI_API_KEY", "")
    if not key:
        print(f"  [skip] GEMINI_API_KEY 未設定")
        return None
    print(f"  [image] 生成中: {prompt[:50]}...")
    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=genai_types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"]),
    )
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            print(f"  [image] 生成完了")
            return part.inline_data.data
    return None

def add_images_to_slide(slide, images: list[dict]):
    for img_spec in images:
        prompt = img_spec.get("prompt", "")
        if not prompt:
            continue
        model     = img_spec.get("model", "gemini-3-pro-image-preview")
        left_inch = img_spec.get("left",  7.0)
        top_inch  = img_spec.get("top",   1.5)
        width_inch= img_spec.get("width", 5.5)
        img_bytes = generate_image_gemini(prompt, model=model)
        if img_bytes:
            slide.shapes.add_picture(
                io.BytesIO(img_bytes),
                Inches(left_inch), Inches(top_inch), Inches(width_inch)
            )

# ─── スライド追加 ─────────────────────────────────────
def add_slide(prs: Presentation, slide_data: dict):
    layout_key = slide_data.get("type", "content")
    title      = slide_data.get("title",    "")
    subtitle   = slide_data.get("subtitle", "")
    body       = slide_data.get("body",     "")
    objects    = parse_objects(slide_data.get("objects", []))
    images     = slide_data.get("images",   [])

    layout = prs.slide_layouts[LAYOUT.get(layout_key, LAYOUT["content"])]
    slide  = prs.slides.add_slide(layout)

    if title:    set_placeholder_text(slide, 0, title)
    if subtitle: set_placeholder_text(slide, 13, subtitle)
    if body:     set_body_text(slide, body)
    if objects:  add_objects_to_slide(slide, objects)
    if images:   add_images_to_slide(slide, images)

    return slide

# ─── メイン生成関数 ───────────────────────────────────
def build_pptx(outline: list[dict], output_path: str | Path) -> Path:
    """
    outline: 中間言語JSONリスト
    output_path: 出力先パス
    Returns: 保存したファイルのPath
    """
    prs = load_template()
    remove_all_slides(prs)
    for i, slide_data in enumerate(outline):
        if not isinstance(slide_data, dict):
            continue
        slide_type = slide_data.get("type", "content")
        print(f"  [{i+1}/{len(outline)}] {slide_type}: {slide_data.get('title', '')[:30]}")
        add_slide(prs, slide_data)
    output_path = Path(output_path)
    prs.save(str(output_path))
    return output_path
