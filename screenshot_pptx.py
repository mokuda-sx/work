"""
screenshot_pptx.py
PowerPoint を COM オブジェクトで操作してスクリーンショットを取得
"""
import subprocess
import time
from pathlib import Path

# PowerPoint VBScript で JPEG スクリーンショット取出
vbscript = r"""
Dim objPPT, objPres, objSlide, strOutputPath, i
Dim fso, pptPath, outputDir

' コマンドライン引数から PPTX パスと出力ディレクトリを取得
Set fso = CreateObject("Scripting.FileSystemObject")
pptPath = WScript.Arguments(0)
outputDir = WScript.Arguments(1)

' PowerPoint を起動
Set objPPT = CreateObject("PowerPoint.Application")
objPPT.Visible = True

' PPTX を開く
Set objPres = objPPT.Presentations.Open(pptPath, , , 2)
WScript.Sleep 2000

' 各スライドを JPEG でエクスポート
For i = 1 To objPres.Slides.Count
    strOutputPath = outputDir & "\slide_" & (i - 1) & ".jpg"
    objPres.Slides(i).Export strOutputPath, "JPG", 1920, 1080
    WScript.Echo "Exported: " & strOutputPath
    WScript.Sleep 500
Next

' PowerPoint を閉じる
objPres.Close
objPPT.Quit

WScript.Echo "Done"
"""

def capture_pptx(pptx_path, output_dir):
    """PPTX の各スライドを JPEG でキャプチャ"""
    pptx_path = Path(pptx_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    vbs_path = output_dir / "capture.vbs"
    vbs_path.write_text(vbscript, encoding="utf-8-sig")
    
    print(f"VBScript で PowerPoint を操作中...\n")
    result = subprocess.run(
        ["cscript.exe", str(vbs_path), str(pptx_path), str(output_dir)],
        capture_output=True,
        text=True,
        timeout=60
    )
    
    print(result.stdout)
    if result.stderr:
        print("Error:", result.stderr)
    
    return output_dir

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("使用方法: python screenshot_pptx.py <pptx_path> [output_dir]")
        sys.exit(1)
    
    pptx_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else Path(pptx_path).parent / "screenshots"
    
    capture_pptx(pptx_path, output_dir)
