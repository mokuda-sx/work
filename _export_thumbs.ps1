param(
    [string]$PptxPath,
    [string]$OutDir
)
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = [Microsoft.Office.Core.MsoTriState]::msoTrue
try {
    $pres = $ppt.Presentations.Open($PptxPath, $true, $false, $false)
    $pres.Export($OutDir, 'PNG', 1920, 1080)
    $pres.Close()
    Write-Output "OK"
} finally {
    $ppt.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
}
