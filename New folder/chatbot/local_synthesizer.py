import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("LocalSynthesizer")

class LocalMedicalSynthesizer:
    """
    Synthesizes grounded clinical responses for local Knowledge Graph offline mode.
    """
    def synthesize_response(self, query: str, context: Dict[str, Any], ml_pred: Optional[Dict[str, Any]], extracted: Dict[str, Any]) -> str:
        """Dynamic response generator based on question intent and knowledge graph."""
        intents = set(extracted.get("intents", []))
        clinical_data = extracted.get("clinical_data", {})
        parts = []

        # Optional ML Context banner if provided and relevant
        if ml_pred and "DIAGNOSTIC_CRITERIA" not in intents and "TYPE_COMPARISON" not in intents:
            label = ml_pred.get("label", "Chưa rõ")
            conf = ml_pred.get("confidence", "75")
            parts.append(f"> **Ngữ cảnh chẩn đoán lâm sàng ghi nhận:** Mô hình học máy phân loại **{label}** (Độ tin cậy: {conf}%)\n")

        # =========================================================================
        # 1. SPECIAL CASE: DIAGNOSTIC CRITERIA & BLOOD SUGAR THRESHOLDS
        # =========================================================================
        if "DIAGNOSTIC_CRITERIA" in intents or ("chỉ số" in query.lower() and "mắc" in query.lower()):
            parts.append("### Tiêu chuẩn chẩn đoán bệnh Đái tháo đường (Bộ Y tế & ADA)\n")
            parts.append("Theo hướng dẫn chẩn đoán của **Bộ Y tế Việt Nam** và **Hiệp hội Đái tháo đường Hoa Kỳ (ADA)**, một người được chẩn đoán mắc đái tháo đường khi thỏa mãn **ít nhất một trong 4 tiêu chuẩn** sau:\n")
            
            parts.append("| Xét nghiệm / Chỉ số | Người bình thường | Tiền đái tháo đường | Chẩn đoán Đái tháo đường |")
            parts.append("| :--- | :--- | :--- | :--- |")
            parts.append("| **1. Đường huyết tương lúc đói (FPG)**<br>*(Nhịn ăn ít nhất 8 giờ)* | **< 100 mg/dL**<br>(< 5.6 mmol/L) | **100 – 125 mg/dL**<br>(5.6 – 6.9 mmol/L) | **≥ 126 mg/dL**<br>(≥ 7.0 mmol/L) *(Làm 2 lần khác ngày)* |")
            parts.append("| **2. Chỉ số HbA1c**<br>*(Đường huyết trung bình 3 tháng)* | **< 5.7%** | **5.7% – 6.4%** | **≥ 6.5%** *(Thực hiện tại lab chuẩn hóa)* |")
            parts.append("| **3. Nghiệm pháp dung nạp Glucose (OGTT)**<br>*(Sau uống 75g glucose 2 giờ)* | **< 140 mg/dL**<br>(< 7.8 mmol/L) | **140 – 199 mg/dL**<br>(7.8 – 11.0 mmol/L) | **≥ 200 mg/dL**<br>(≥ 11.1 mmol/L) |")
            parts.append("| **4. Đường huyết ngẫu nhiên / Bất kỳ** | — | — | **≥ 200 mg/dL**<br>(≥ 11.1 mmol/L) *kèm triệu chứng 4 nhiều* |")
            parts.append("")
            
            parts.append("#### Các chỉ số yếu tố nguy cơ phối hợp (Theo mô hình Chapter 12):")
            parts.append("- **Chỉ số khối cơ thể (BMI):** BMI ≥ 23 kg/m² (ngưỡng thừa cân người châu Á) làm tăng rõ rệt mức độ đề kháng insulin ở mô cơ và mô mỡ.")
            parts.append("- **Độ tuổi:** Người từ 45 tuổi trở lên có tốc độ suy giảm chức năng tế bào beta tụy tự nhiên theo tuổi tác.")
            parts.append("- **Huyết áp:** Huyết áp ≥ 140/90 mmHg thường đi kèm trong hội chứng chuyển hóa.")
            parts.append("")
            
            parts.append("#### Thiết bị kiểm tra đường huyết tại nhà (Nhà thuốc Long Châu):")
            parts.append("- **Máy đo đường huyết OneTouch Verio Vue / Accu-Chek Instant:** Giúp theo dõi biến động đường huyết mao mạch lúc đói và sau ăn 2 giờ (Giá tham khảo tại Long Châu: ~750.000đ - 1.250.000đ).")
            parts.append("")
            parts.append("> **Lưu ý chuyên môn:** Để có kết luận chính xác, người bệnh cần đến bệnh viện làm xét nghiệm máu tĩnh mạch, không dùng que thử mao mạch tại nhà để tự chẩn đoán bệnh.")
            return "\n".join(parts)

        # =========================================================================
        # 2. SPECIAL CASE: SYMPTOMS & WARNING SIGNS
        # =========================================================================
        if "SYMPTOMS" in intents and "MEDICATION" not in intents and "COMPLICATIONS" not in intents:
            parts.append("### Dấu hiệu & Triệu chứng nhận biết Bệnh Đái tháo đường\n")
            parts.append("#### 1. Bộ 4 triệu chứng kinh điển (\"4 nhiều\"):")
            parts.append("- **1. Tiểu nhiều & Tiểu đêm (Polyuria):** Thận tăng đào thải lượng đường dư thừa qua nước tiểu kéo theo nước, khiến người bệnh đi tiểu liên tục, đặc biệt vào ban đêm.")
            parts.append("- **2. Khát nước liên tục (Polydipsia):** Do mất nhiều nước qua đường tiểu, trung tâm khát ở não bị kích thích, người bệnh uống bao nhiêu nước vẫn cảm thấy khô miệng, khát họng.")
            parts.append("- **3. Sụt cân nhanh không rõ nguyên nhân:** Do thiếu hụt insulin hoặc đề kháng insulin, glucose không vào được tế bào, cơ thể phải phân hủy mô cơ và mô mỡ để lấy năng lượng.")
            parts.append("- **4. Ăn nhiều nhưng mau đói (Polyphagia):** Tế bào bị bỏ đói phát tín hiệu thèm ăn liên tục.")
            parts.append("")
            
            parts.append("#### 2. Các triệu chứng cảnh báo tổn thương sớm:")
            parts.append("- **Thị lực giảm / Nhìn mờ:** Nồng độ đường trong máu cao làm thay đổi thể tích dịch và độ cong của thủy tinh thể.")
            parts.append("- **Tê bì, châm chích đầu chi:** Cảm giác như kiến bò ở lòng bàn chân và đầu ngón tay do tổn thương dây thần kinh cảm giác ngoại biên.")
            parts.append("- **Vết thương lâu lành:** Đường huyết cao làm tổn thương mạch máu vi tuần hoàn và suy giảm hoạt tính bạch cầu, khiến các vết trầy xước nhỏ dễ nhiễm trùng.")
            parts.append("")
            parts.append("> **Khuyến nghị:** Khi xuất hiện từ 2 triệu chứng trên, bạn nên làm xét nghiệm đường huyết đói và HbA1c tại cơ sở y tế.")
            return "\n".join(parts)

        # =========================================================================
        # 3. SPECIAL CASE: COMPLICATIONS
        # =========================================================================
        if "COMPLICATIONS" in intents and "MEDICATION" not in intents:
            parts.append("### Các biến chứng nguy hiểm của Bệnh Đái tháo đường\n")
            parts.append("Đái tháo đường không kiểm soát tốt đường huyết kéo dài sẽ gây tổn thương mạch máu toàn thân:")
            parts.append("")
            parts.append("#### 1. Biến chứng mạch máu nhỏ (Microvascular):")
            parts.append("- **Tổn thương thận (Diabetic Nephropathy):** Đường huyết cao phá hủy màng lọc cầu thận, gây rò rỉ đạm niệu (Microalbuminuria) và tiến triển thành suy thận mạn giai đoạn cuối.")
            parts.append("- **Bệnh võng mạc (Diabetic Retinopathy):** Phù hoàng điểm, xuất huyết võng mạc, là nguyên nhân hàng đầu gây suy giảm thị lực và mù lòa.")
            parts.append("- **Bệnh thần kinh (Diabetic Neuropathy):** Mất cảm giác đau ở bàn chân, khiến người bệnh không nhận biết được các vết thương nhỏ.")
            parts.append("")
            parts.append("#### 2. Biến chứng mạch máu lớn (Macrovascular):")
            parts.append("- **Bệnh mạch vành & Nhồi máu cơ tim:** Tăng nguy cơ xơ vữa động mạch gấp 2 – 4 lần người bình thường.")
            parts.append("- **Đột quỵ não:** Tắc hẹp mạch máu não do mảng xơ vữa.")
            parts.append("- **Bàn chân đái tháo đường:** Vết loét nhiễm trùng kết hợp thiếu máu nuôi dưỡng dễ dẫn đến hoại tử và nguy cơ phải đoạn chi.")
            parts.append("")
            parts.append("> **Lưu ý chuyên môn:** Kiểm soát tốt chỉ số HbA1c < 7.0% và huyết áp < 130/80 mmHg giúp giảm tới 40% nguy cơ mắc các biến chứng trên.")
            return "\n".join(parts)

        # =========================================================================
        # 4. SPECIAL CASE: DIET & NUTRITION
        # =========================================================================
        if "DIET_NUTRITION" in intents and "MEDICATION" not in intents:
            parts.append("### Hướng dẫn Chế độ Dinh dưỡng cho Người Đái tháo đường\n")
            parts.append("#### 1. Nguyên tắc đĩa thức ăn chuẩn:")
            parts.append("- **1/2 đĩa:** Các loại rau củ không chứa tinh bột (rau cải, súp lơ, dưa chuột, mướp đắng).")
            parts.append("- **1/4 đĩa:** Protein chất lượng cao (cá thu, cá hồi, ức gà, đậu phụ, trứng).")
            parts.append("- **1/4 đĩa:** Tinh bột hấp thu chậm (gạo lứt, yến mạch, khoai lang luộc, các loại đậu hạt).")
            parts.append("")
            parts.append("#### 2. Nhóm thực phẩm nên và không nên:")
            parts.append("- **Nên dùng:** Thực phẩm có chỉ số đường huyết thấp (GI < 55), bổ sung chất xơ hòa tan ≥ 25g/ngày để làm chậm quá trình hấp thu đường vào máu sau ăn.")
            parts.append("- **Cần hạn chế:** Nước ngọt có ga, bánh kẹo, đường tinh luyện, tinh bột tinh chế (bánh mì trắng, xôi nếp), trái cây có độ ngọt đậm (sầu riêng, xoài chín, mít, nhãn).")
            parts.append("")
            parts.append("#### 3. Sản phẩm dinh dưỡng chuyên biệt tại Nhà thuốc Long Châu:")
            parts.append("- **Sữa Glucerna 850g:** Công thức dinh dưỡng giải phóng chậm Triple Care giúp bình ổn đường huyết (Giá tham khảo: ~850.000đ/hộp).")
            parts.append("- **Trà Dây thìa canh / Viên uống Dây thìa canh:** Hỗ trợ ức chế hấp thu glucose ở ruột non (Giá tham khảo: ~110.000đ/hộp).")
            return "\n".join(parts)

        # =========================================================================
        # 5. SPECIAL CASE: TYPE 1 VS TYPE 2 COMPARISON
        # =========================================================================
        if "TYPE_COMPARISON" in intents:
            parts.append("### Phân biệt Đái tháo đường Type 1 và Type 2\n")
            parts.append("| Đặc điểm | Đái tháo đường Type 1 | Đái tháo đường Type 2 |")
            parts.append("| :--- | :--- | :--- |")
            parts.append("| **Cơ chế bệnh sinh** | Tự miễn phá hủy hoàn toàn tế bào beta tụy $\\rightarrow$ **Thiếu insulin tuyệt đối** | **Đề kháng insulin** kết hợp suy giảm tiết insulin tương đối |")
            parts.append("| **Độ tuổi khởi phát** | Thường gặp ở trẻ em, thanh thiếu niên (< 30 tuổi) | Thường gặp ở người trưởng thành, trung niên (≥ 40 tuổi) |")
            parts.append("| **Thể trạng** | Thường gầy sút cân nhanh | Thường thừa cân, béo phì (BMI ≥ 23) |")
            parts.append("| **Triệu chứng khởi phát** | Đột ngột, rầm rộ (dễ nhiễm toan ceton) | Âm thầm kéo dài, thường phát hiện tình cờ khi khám định kỳ |")
            parts.append("| **Phác đồ điều trị** | **Bắt buộc tiêm Insulin suốt đời** (Lantus, Mixtard...) | Thay đổi lối sống + Thuốc uống (Metformin, SGLT2...) $\\rightarrow$ Insulin khi cần |")
            return "\n".join(parts)

        # =========================================================================
        # 6. SPECIAL CASE: MEDICATIONS & LONG CHAU PHARMACY CATALOG
        # =========================================================================
        if "MEDICATION" in intents or len(context.get("medicines", [])) > 0:
            parts.append("### Thông tin Dược phẩm Điều trị Đái tháo đường (Nhà thuốc Long Châu)\n")
            parts.append("> **Lưu ý chuyên môn:** Thuốc điều trị đái tháo đường là thuốc kê đơn. Người bệnh tuyệt đối không tự ý mua dùng hoặc thay đổi liều mà không có chỉ định của bác sĩ.\n")
            
            meds = context.get("medicines", [])
            if meds:
                for med in meds:
                    parts.append(f"#### {med.get('label')}")
                    parts.append(f"- **Hoạt chất chính:** {med.get('active_ingredient', 'N/A')}")
                    parts.append(f"- **Phân loại nhóm:** {med.get('group', 'Thuốc điều trị đái tháo đường')}")
                    parts.append(f"- **Tác dụng dược lý:** {med.get('summary', '')}")
                    parts.append(f"- **Liều dùng & Cách uống tham khảo:** {med.get('dosage', 'Theo đơn bác sĩ')}")
                    parts.append(f"- **Giá niêm yết tham khảo tại Long Châu:** **{med.get('price_ref', 'Liên hệ nhà thuốc')}**")
                    if med.get("longchau_url"):
                        parts.append(f"- **Tra cứu chi tiết:** [Xem sản phẩm trên Long Châu]({med.get('longchau_url')})")
                    parts.append("")
            else:
                parts.append("#### Các nhóm thuốc điều trị phổ biến tại Hệ thống Long Châu:")
                parts.append("- **1. Nhóm Biguanide (Glucophage / Metformin 500mg, 850mg, 1000mg):** Lựa chọn đầu tay điều trị Type 2. Giúp giảm sản xuất glucose tại gan và tăng nhạy cảm insulin (Giá: ~155.000đ/hộp).")
                parts.append("- **2. Nhóm ức chế SGLT-2 (Forxiga 10mg / Jardiance 10mg):** Đào thải glucose dư thừa qua nước tiểu, bảo vệ tim mạch và làm chậm suy thận (Giá: ~620.000đ - 700.000đ/hộp).")
                parts.append("- **3. Nhóm ức chế DPP-4 (Januvia 50mg, 100mg / Galvus 50mg):** Kích thích tụy tiết insulin phụ thuộc glucose sau ăn, không gây hạ đường huyết quá mức (Giá: ~480.000đ - 550.000đ/hộp).")
                parts.append("- **4. Insulin sinh học (Lantus Solostar / Mixtard 30 Penfill):** Bổ sung nồng độ insulin chuẩn cho Type 1 và Type 2 kiểm soát kém (Giá: ~280.000đ - 350.000đ/bút).")
                parts.append("")
                
            return "\n".join(parts)

        # =========================================================================
        # 7. CLINICAL PARAMETERS EVALUATION (UP TO 8 FEATURES)
        # =========================================================================
        if clinical_data:
            parts.append("### Đánh giá các chỉ số sức khỏe của bạn:\n")
            if "Glucose" in clinical_data:
                g = clinical_data["Glucose"]
                if g < 100:
                    status = "Bình thường (lúc đói)"
                elif g <= 125:
                    status = "Nguy cơ Tiền đái tháo đường"
                else:
                    status = "Vượt ngưỡng chẩn đoán Đái tháo đường (≥ 126 mg/dL)"
                parts.append(f"- **Đường huyết ({g} mg/dL):** {status}")
                
            if "BMI" in clinical_data:
                bmi = clinical_data["BMI"]
                if bmi < 18.5:
                    b_status = "Thiếu cân"
                elif bmi < 23:
                    b_status = "Bình thường"
                elif bmi < 25:
                    b_status = "Thừa cân (tiền béo phì theo chuẩn WPRO châu Á)"
                else:
                    b_status = "Béo phì, làm tăng mạnh nguy cơ đề kháng insulin"
                parts.append(f"- **Chỉ số BMI ({bmi} kg/m²):** {b_status}")
                
            if "Age" in clinical_data:
                age = clinical_data["Age"]
                a_status = "Nhóm tuổi có tỷ lệ mắc đái tháo đường Type 2 cao" if age >= 45 else "Nhóm tuổi trẻ, cần chú ý chế độ lối sống"
                parts.append(f"- **Độ tuổi ({int(age)} tuổi):** {a_status}")

            if "BloodPressure" in clinical_data:
                bp = clinical_data["BloodPressure"]
                bp_status = "Huyết áp tâm trương cao (≥ 90 mmHg), cần phòng ngừa biến chứng tim mạch/thận" if bp >= 90 else "Huyết áp ở ngưỡng an toàn"
                parts.append(f"- **Huyết áp ({bp} mmHg):** {bp_status}")

            if "Insulin" in clinical_data:
                ins = clinical_data["Insulin"]
                ins_status = "Nồng độ tăng cao (≥ 160 μU/ml), biểu hiện đề kháng insulin mô ngoại vi" if ins >= 160 else "Nồng độ insulin trong giới hạn tham chiếu"
                parts.append(f"- **Insulin huyết thanh ({ins} μU/ml):** {ins_status}")

            if "DiabetesPedigreeFunction" in clinical_data:
                dpf = clinical_data["DiabetesPedigreeFunction"]
                dpf_status = "Yếu tố di truyền gia đình cao (≥ 0.70)" if dpf >= 0.7 else "Yếu tố di truyền ở mức trung bình"
                parts.append(f"- **Hệ số phả hệ di truyền ({dpf}):** {dpf_status}")

            if "Pregnancies" in clinical_data:
                preg = clinical_data["Pregnancies"]
                if preg >= 3:
                    parts.append(f"- **Tiền sử thai kỳ ({int(preg)} lần):** Cần lưu ý theo dõi đái tháo đường thai kỳ và rối loạn đường huyết sau sinh.")
                
            parts.append("\n> **Khuyến nghị:** Bạn nên đến cơ sở y tế để được thực hiện xét nghiệm định lượng Glucose tĩnh mạch và đo chỉ số HbA1c chính thức.")
            return "\n".join(parts)

        # =========================================================================
        # 8. GENERAL FALLBACK
        # =========================================================================
        parts.append("### Tư vấn Thông tin Bệnh Đái tháo đường\n")
        parts.append("Hệ thống có thể hỗ trợ bạn tra cứu các nội dung sau:")
        parts.append("- **1. Tiêu chuẩn chẩn đoán:** Các ngưỡng đường huyết lúc đói, đường huyết sau ăn và chỉ số HbA1c.")
        parts.append("- **2. Dấu hiệu nhận biết:** Triệu chứng 4 nhiều (khát, tiểu nhiều, sụt cân, ăn nhiều), mờ mắt, tê bì chân tay.")
        parts.append("- **3. Danh mục thuốc Long Châu:** Hoạt chất, liều dùng và giá tham khảo (Glucophage, Januvia, Forxiga, Jardiance, Insulin...).")
        parts.append("- **4. Chế độ dinh dưỡng & Vận động:** Thực đơn chỉ số GI thấp, cách lựa chọn thực phẩm và bài tập phù hợp.\n")
        parts.append("*Hãy nhập câu hỏi cụ thể hoặc chọn một trong các câu hỏi mẫu bên dưới để nhận thông tin chi tiết.*")
        return "\n".join(parts)

local_synthesizer = LocalMedicalSynthesizer()
