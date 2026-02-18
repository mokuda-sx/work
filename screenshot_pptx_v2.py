"""
screenshot_pptx_v2.py
Python + pywin32 で PowerPoint を操作してスクリーンショット取得
"""
import sys
from pathlib import Path
import time

try:
    from win32com.client import Dispatch
    import win32com.client
    from win32com.client import constants
except ImportError:
    print("pywin32 をインストールしてください: pip install pywin32")
    sys.exit(1)

def capture_pptx(pptx_path, output_dir):
    """PPTX から各スライドを画像でキャプチャ"""
    pptx_path = Path(pptx_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nPowerPoint を起動中...\n")
    
    try:
        # PowerPoint を起動
        ppt = Dispatch("PowerPoint.Application")
        ppt.Visible = True
        
        # PPTX を開く
        print(f"開く: {pptx_path}")
        pres = ppt.Presentations.Open(str(pptx_path), True, True, 1)
        time.sleep(2)
        
        # 各スライドをエクスポート
        slide_count = pres.Slides.Count
        print(f"スライド数: {slide_count}\n")
        
        for i in range(1, slide_count + 1):
            slide = pres.Slides(i)
            output_path = str(output_dir / f"slide_{i-1}.jpg")
            
            print(f"  スライド {i-1}: ".ljust(15), end="", flush=True)
            
            # shapes の情報をログ
            shape_count = slide.Shapes.Count
            print(f"({shape_count} オブジェクト) → ", end="", flush=True)
            
            # JPEG でエクスポート (1920x1080)
            slide.Export(output_path, "JPG", 1920, 1080)
            print(f"保存: {Path(output_path).name}")
            time.sleep(1)
        
        print(f"\n✓ キャプチャ完了: {output_dir}")
        
        # PowerPoint を閉じる
        pres.Close()
        ppt.Quit()
        
        return output_dir
    
    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python screenshot_pptx_v2.py <pptx_path> [output_dir]")
        sys.exit(1)
    
    pptx_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else Path(pptx_path).parent / "screenshots"
    
    capture_pptx(pptx_path, output_dir)
