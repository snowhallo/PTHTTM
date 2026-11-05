$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $docxPath = "D:\learning\phat_trien_he_thong_thong_minh\A06_06_taint.731.docx"
    $pdfPath = "D:\learning\phat_trien_he_thong_thong_minh\A06_06_taint.731.pdf"
    $pdfBackup = "D:\learning\phat_trien_he_thong_thong_minh\ass6\A06_06_taint.731.pdf"
    
    Write-Host "[*] Opening Word document: $docxPath"
    $doc = $word.Documents.Open($docxPath)
    Write-Host "[*] Exporting PDF: $pdfPath"
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close()
    
    Copy-Item $pdfPath $pdfBackup -Force
    Write-Host "[+] Successfully exported PDF to $pdfPath and $pdfBackup"
} catch {
    Write-Host "[!] Error exporting PDF: $_"
} finally {
    $word.Quit()
}
