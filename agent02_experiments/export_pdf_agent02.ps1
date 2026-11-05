$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $docxPath = "D:\learning\phat_trien_he_thong_thong_minh\agent02_06_15_taint.docx"
    $pdfPath = "D:\learning\phat_trien_he_thong_thong_minh\agent02_06_15_taint.pdf"
    $pdfBackup = "D:\learning\phat_trien_he_thong_thong_minh\agent02_experiments\agent02_06_15_taint.pdf"
    $pdfWithId = "D:\learning\phat_trien_he_thong_thong_minh\agent02_06_15_taint.731.pdf"
    
    Write-Host "[*] Opening Word document: $docxPath"
    $doc = $word.Documents.Open($docxPath)
    Write-Host "[*] Exporting PDF: $pdfPath"
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close()
    
    Copy-Item $pdfPath $pdfBackup -Force
    Copy-Item $pdfPath $pdfWithId -Force
    Write-Host "[+] Successfully exported PDF to:"
    Write-Host "    - $pdfPath"
    Write-Host "    - $pdfBackup"
    Write-Host "    - $pdfWithId"
} catch {
    Write-Host "[!] Error exporting PDF: $_"
} finally {
    $word.Quit()
}

