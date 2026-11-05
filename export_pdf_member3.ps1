$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $docxPath = "D:\learning\phat_trien_he_thong_thong_minh\task_thanh_vien_3_du_doan_tieu_duong_gnn.docx"
    $pdfPath = "D:\learning\phat_trien_he_thong_thong_minh\task_thanh_vien_3_du_doan_tieu_duong_gnn.pdf"
    
    Write-Host "[*] Opening Word document: $docxPath"
    $doc = $word.Documents.Open($docxPath)
    Write-Host "[*] Exporting PDF: $pdfPath"
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close()
    
    Write-Host "[+] Successfully exported PDF to: $pdfPath"
} catch {
    Write-Host "[!] Error exporting PDF: $_"
} finally {
    $word.Quit()
}

