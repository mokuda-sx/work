
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
