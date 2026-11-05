/**
 * Vietnam Real Estate AI - Client Application Logic
 * Đồ thị Tri thức Neo4j + Học máy Gradient Boosting
 */

// ==========================================
// 1. TOAST NOTIFICATION & FORM ERROR SYSTEM
// ==========================================
function showToast(message, type = 'warning') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'pointer-events-auto p-3.5 rounded-xl shadow-lg border flex items-start gap-2.5 text-xs font-semibold transform transition-all duration-300 translate-y-2 opacity-0';

    let iconName = 'alert-triangle';
    if (type === 'error') {
        toast.classList.add('bg-rose-50', 'border-rose-200', 'text-rose-900');
        iconName = 'alert-circle';
    } else if (type === 'success') {
        toast.classList.add('bg-emerald-50', 'border-emerald-200', 'text-emerald-900');
        iconName = 'check-circle';
    } else if (type === 'info') {
        toast.classList.add('bg-blue-50', 'border-blue-200', 'text-blue-900');
        iconName = 'info';
    } else {
        toast.classList.add('bg-amber-50', 'border-amber-200', 'text-amber-900');
        iconName = 'alert-triangle';
    }

    toast.innerHTML = `
        <i data-lucide="${iconName}" class="w-4 h-4 flex-shrink-0 mt-0.5"></i>
        <div class="flex-1 leading-snug">${message}</div>
        <button onclick="this.parentElement.remove()" class="text-slate-400 hover:text-slate-600 transition">
            <i data-lucide="x" class="w-3.5 h-3.5"></i>
        </button>
    `;

    container.appendChild(toast);
    if (window.lucide) lucide.createIcons();

    // Trigger animation
    requestAnimationFrame(() => {
        toast.classList.remove('translate-y-2', 'opacity-0');
        toast.classList.add('translate-y-0', 'opacity-100');
    });

    // Auto remove after 4 seconds
    setTimeout(() => {
        toast.classList.remove('translate-y-0', 'opacity-100');
        toast.classList.add('translate-y-2', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

function showFormError(msg) {
    const errorBox = document.getElementById('form-error-box');
    const errorMsg = document.getElementById('form-error-msg');
    if (errorBox && errorMsg) {
        errorMsg.innerText = msg;
        errorBox.classList.remove('hidden');
    }
}

function clearFormError() {
    const errorBox = document.getElementById('form-error-box');
    if (errorBox) errorBox.classList.add('hidden');
}

// ==========================================
// 2. REAL-TIME INPUT VALIDATORS & CLAMPING
// ==========================================
function validateAreaInput(elem) {
    let val = parseFloat(elem.value);
    if (isNaN(val)) return;
    if (val > 180) {
        showToast('Diện tích định giá tối đa hỗ trợ là 180m² (chuẩn nhà ở dân dụng). Đã tự động điều chỉnh về 180m².', 'warning');
        elem.value = 180;
    } else if (val < 20 && val > 0) {
        showToast('Diện tích định giá tối thiểu là 20m². Đã tự động điều chỉnh về 20m².', 'warning');
        elem.value = 20;
    }
    syncAreaFromNum(elem.value);
}

function validateFrontageInput(elem) {
    let val = parseFloat(elem.value);
    if (isNaN(val)) return;
    if (val > 12.0) {
        showToast('Mặt tiền tối đa là 12m (chuẩn nhà phố/liền kề). Đã tự động điều chỉnh về 12m.', 'warning');
        elem.value = 12.0;
    } else if (val < 2.0 && val > 0) {
        showToast('Mặt tiền tối thiểu là 2m. Đã tự động điều chỉnh về 2m.', 'warning');
        elem.value = 2.0;
    }
    syncFrontageFromNum(elem.value);
}

function validateRoadInput(elem) {
    let val = parseFloat(elem.value);
    if (isNaN(val)) return;
    if (val > 15.0) {
        showToast('Độ rộng đường vào tối đa là 15m. Đã tự động điều chỉnh về 15m.', 'warning');
        elem.value = 15.0;
    } else if (val < 1.5 && val > 0) {
        showToast('Độ rộng đường vào tối thiểu là 1.5m. Đã tự động điều chỉnh về 1.5m.', 'warning');
        elem.value = 1.5;
    }
    syncRoadFromNum(elem.value);
}

function validateFloorsInput(elem) {
    let val = parseFloat(elem.value);
    if (isNaN(val)) return;
    if (val > 7) {
        showToast('Số tầng tối đa là 7 tầng (nhà ở dân dụng). Đã tự động điều chỉnh về 7 tầng.', 'warning');
        elem.value = 7;
    } else if (val < 1 && val > 0) {
        elem.value = 1;
    }
}

function validateBedroomInput(elem) {
    let val = parseFloat(elem.value);
    if (isNaN(val)) return;
    if (val > 8) {
        showToast('Số phòng ngủ tối đa là 8 phòng. Đã tự động điều chỉnh về 8 phòng.', 'warning');
        elem.value = 8;
    } else if (val < 1 && val > 0) {
        elem.value = 1;
    }
}

function validateBathroomInput(elem) {
    let val = parseFloat(elem.value);
    if (isNaN(val)) return;
    if (val > 8) {
        showToast('Số phòng WC tối đa là 8 phòng. Đã tự động điều chỉnh về 8 phòng.', 'warning');
        elem.value = 8;
    } else if (val < 1 && val > 0) {
        elem.value = 1;
    }
}

// ĐỒNG BỘ 2 CHIỀU GIỮA Ô NHẬP SỐ VÀ THANH TRƯỢT (SLIDER)
function syncAreaFromSlider(val) {
    document.getElementById('input-area-num').value = val;
    clearFormError();
}
function syncAreaFromNum(val) {
    if (val && !isNaN(val)) {
        document.getElementById('input-area').value = Math.min(180, Math.max(20, parseFloat(val)));
    }
    clearFormError();
}

function syncFrontageFromSlider(val) {
    document.getElementById('input-frontage-num').value = val;
    clearFormError();
}
function syncFrontageFromNum(val) {
    if (val && !isNaN(val)) {
        document.getElementById('input-frontage').value = Math.min(12, Math.max(2, parseFloat(val)));
    }
    clearFormError();
}

function syncRoadFromSlider(val) {
    document.getElementById('input-road-num').value = val;
    clearFormError();
}
function syncRoadFromNum(val) {
    if (val && !isNaN(val)) {
        document.getElementById('input-road').value = Math.min(15, Math.max(1.5, parseFloat(val)));
    }
    clearFormError();
}

// ==========================================
// 3. TAB NAVIGATION (PRESERVE STATE)
// ==========================================
function switchTab(tab, updateHistory = true) {
    if (!['predict', 'chat', 'models'].includes(tab)) {
        tab = 'predict';
    }

    ['predict', 'chat', 'models'].forEach(t => {
        const content = document.getElementById('tab-content-' + t);
        const btn = document.getElementById('tab-btn-' + t);
        if (!content || !btn) return;
        if (t === tab) {
            content.classList.remove('hidden');
            btn.className = 'nav-tab-active flex-1 sm:flex-initial px-2.5 sm:px-3.5 py-1.5 text-[11px] sm:text-xs font-bold rounded-lg transition flex items-center justify-center gap-1 sm:gap-1.5 whitespace-nowrap';
        } else {
            content.classList.add('hidden');
            btn.className = 'nav-tab-inactive flex-1 sm:flex-initial px-2.5 sm:px-3.5 py-1.5 text-[11px] sm:text-xs font-bold rounded-lg transition flex items-center justify-center gap-1 sm:gap-1.5 whitespace-nowrap';
        }
    });

    try {
        localStorage.setItem('active_app_tab', tab);
        if (updateHistory && window.location.hash !== '#' + tab) {
            history.replaceState(null, null, '#' + tab);
        }
    } catch (e) {
        console.error('Lỗi lưu tab state:', e);
    }

    if (window.lucide) {
        lucide.createIcons();
    }
}

// ==========================================
// 4. DISTRICT OPTIONS DICTIONARY
// ==========================================
const DISTRICTS_MAP = {
    'Hà Nội': ['Cầu Giấy', 'Đống Đa', 'Ba Đình', 'Hai Bà Trưng', 'Thanh Xuân', 'Hoàng Mai', 'Hà Đông', 'Long Biên', 'Tây Hồ', 'Nam Từ Liêm', 'Bắc Từ Liêm', 'Hoài Đức', 'Thanh Trì', 'Gia Lâm', 'Đông Anh', 'Chương Mỹ', 'Quận huyện khác'],
    'TP. Hồ Chí Minh': ['Quận 1', 'Quận 2', 'Quận 3', 'Quận 4', 'Quận 6', 'Quận 7', 'Quận 8', 'Quận 9', 'Quận 10', 'Quận 11', 'Quận 12', 'Bình Thạnh', 'Tân Bình', 'Gò Vấp', 'Thủ Đức', 'Phú Nhuận', 'Tân Phú', 'Bình Tân', 'Nhà Bè', 'Hóc Môn', 'Bình Chánh', 'Quận huyện khác'],
    'Đà Nẵng': ['Hải Châu', 'Thanh Khê', 'Sơn Trà', 'Ngũ Hành Sơn', 'Liên Chiểu', 'Cẩm Lệ', 'Quận huyện khác'],
    'Hưng Yên': ['Văn Giang', 'Mỹ Hào', 'Khoái Châu', 'Yên Mỹ', 'Quận huyện khác'],
    'Bình Dương': ['Thủ Dầu Một', 'Thuận An', 'Dĩ An', 'Bến Cát', 'Tân Uyên', 'Quận huyện khác'],
    'Hải Phòng': ['Hồng Bàng', 'Ngô Quyền', 'Lê Chân', 'Hải An', 'An Dương', 'Quận huyện khác'],
    'Đồng Nai': ['Biên Hòa', 'Long Thành', 'Nhơn Trạch', 'Quận huyện khác'],
    'Tỉnh thành khác': ['Quận huyện khác']
};

function updateDistrictOptions() {
    const city = document.getElementById('input-city').value;
    const districtSelect = document.getElementById('input-district');
    districtSelect.innerHTML = '<option value="" disabled selected>-- Chọn Quận / Huyện --</option>';

    const districts = DISTRICTS_MAP[city] || ['Quận huyện khác'];
    districts.forEach(d => {
        const opt = document.createElement('option');
        opt.value = d;
        opt.innerText = d;
        districtSelect.appendChild(opt);
    });
    clearFormError();
}

function onSampleCityChange() {
    const city = document.getElementById('sample-city-filter').value;
    const districtSelect = document.getElementById('sample-district-filter');
    districtSelect.innerHTML = '<option value="">Tất cả quận huyện</option>';

    if (city && DISTRICTS_MAP[city]) {
        DISTRICTS_MAP[city].forEach(d => {
            const opt = document.createElement('option');
            opt.value = d;
            opt.innerText = d;
            districtSelect.appendChild(opt);
        });
    }
    fetchSampleData();
}

// ==========================================
// 5. FETCH & LOAD SAMPLE REAL PROPERTIES
// ==========================================
let currentSamples = [];

async function fetchSampleData() {
    const city = document.getElementById('sample-city-filter').value;
    const district = document.getElementById('sample-district-filter').value;
    const floors = document.getElementById('sample-floors-filter').value;
    const bedroom = document.getElementById('sample-bedroom-filter').value;

    let url = `/api/sample-data?limit=400`;
    if (city) url += `&city=${encodeURIComponent(city)}`;
    if (district) url += `&district=${encodeURIComponent(district)}`;
    if (floors) url += `&floors=${encodeURIComponent(floors)}`;
    if (bedroom) url += `&bedroom=${encodeURIComponent(bedroom)}`;

    try {
        const res = await fetch(url);
        const data = await res.json();
        currentSamples = data.samples || [];

        const countBadge = document.getElementById('sample-total-count');
        if (countBadge) {
            countBadge.innerText = `${data.total_matched.toLocaleString()} BĐS phù hợp`;
        }

        const select = document.getElementById('sample-select');
        select.innerHTML = `<option value="">-- Chọn 1 trong ${currentSamples.length} BĐS thực tế thị trường --</option>`;

        currentSamples.forEach((item, index) => {
            const opt = document.createElement('option');
            opt.value = index;
            opt.innerText = `[${item.city} - ${item.district}] ${item.area}m² | ${item.floors || 1}T | Giá rao: ${item.price_billion} Tỷ (~${item.unit_price_million_m2} Tr/m²)`;
            select.appendChild(opt);
        });

    } catch (err) {
        console.error('Lỗi lấy mẫu dữ liệu:', err);
    }
}

function loadSelectedSample() {
    const idx = document.getElementById('sample-select').value;
    if (idx === '') return;

    const sample = currentSamples[parseInt(idx)];
    if (!sample) return;

    clearFormError();

    // Điền vào form
    const citySelect = document.getElementById('input-city');
    citySelect.value = sample.city;
    updateDistrictOptions();

    document.getElementById('input-district').value = sample.district;
    
    // Diện tích
    const boundedArea = Math.min(180, Math.max(20, sample.area));
    document.getElementById('input-area').value = boundedArea;
    document.getElementById('input-area-num').value = boundedArea;

    // Mặt tiền & Đường
    const boundedFrontage = Math.min(12, Math.max(2, sample.frontage || 4.0));
    document.getElementById('input-frontage').value = boundedFrontage;
    document.getElementById('input-frontage-num').value = boundedFrontage;

    const boundedRoad = Math.min(15, Math.max(1.5, sample.access_road || 4.5));
    document.getElementById('input-road').value = boundedRoad;
    document.getElementById('input-road-num').value = boundedRoad;

    // Quy mô
    document.getElementById('input-floors').value = Math.min(7, Math.max(1, sample.floors || 3));
    document.getElementById('input-bedroom').value = Math.min(8, Math.max(1, sample.bedroom || 3));
    document.getElementById('input-bathroom').value = Math.min(8, Math.max(1, sample.bathroom || 2));
    document.getElementById('input-legal').value = sample.legal_status || 'Have certificate';
    document.getElementById('input-direction').value = sample.house_direction || 'Đông - Nam';

    predictPrice(sample.actual_price);
}

// ==========================================
// 6. VALIDATE & EXECUTE VALUATION
// ==========================================
function validateAndPredict() {
    clearFormError();

    const city = document.getElementById('input-city').value;
    const district = document.getElementById('input-district').value;
    const area = parseFloat(document.getElementById('input-area-num').value || document.getElementById('input-area').value);
    const frontage = parseFloat(document.getElementById('input-frontage-num').value || document.getElementById('input-frontage').value || 4.0);
    const road = parseFloat(document.getElementById('input-road-num').value || document.getElementById('input-road').value || 4.5);
    const floors = parseFloat(document.getElementById('input-floors').value || 3);
    const bedroom = parseFloat(document.getElementById('input-bedroom').value || 3);
    const bathroom = parseFloat(document.getElementById('input-bathroom').value || 2);

    if (!city || !district) {
        const msg = 'Vui lòng chọn Tỉnh / Thành phố và Quận / Huyện trước khi thực hiện định giá.';
        showToast(msg, 'warning');
        showFormError(msg);
        return;
    }
    if (!area || isNaN(area) || area < 20 || area > 180) {
        const msg = 'Diện tích sàn hợp lệ từ 20m² đến 180m² (phân khúc nhà ở dân dụng thực tế). Vui lòng nhập trong khoảng này.';
        showToast(msg, 'warning');
        showFormError(msg);
        document.getElementById('input-area-num').focus();
        return;
    }
    if (frontage < 2.0 || frontage > 12.0) {
        const msg = 'Mặt tiền nhà ở tiêu chuẩn dao động từ 2m đến 12m. Vui lòng kiểm tra lại thông số.';
        showToast(msg, 'warning');
        showFormError(msg);
        document.getElementById('input-frontage-num').focus();
        return;
    }
    if (road < 1.5 || road > 15.0) {
        const msg = 'Độ rộng đường vào nhà tiêu chuẩn từ 1.5m đến 15m. Vui lòng kiểm tra lại thông số.';
        showToast(msg, 'warning');
        showFormError(msg);
        document.getElementById('input-road-num').focus();
        return;
    }
    if (floors < 1 || floors > 7) {
        const msg = 'Số tầng nhà dân dụng tiêu chuẩn từ 1 đến 7 tầng. Vui lòng kiểm tra lại.';
        showToast(msg, 'warning');
        showFormError(msg);
        document.getElementById('input-floors').focus();
        return;
    }
    if (bedroom < 1 || bedroom > 8) {
        const msg = 'Số phòng ngủ tiêu chuẩn từ 1 đến 8 phòng. Vui lòng kiểm tra lại.';
        showToast(msg, 'warning');
        showFormError(msg);
        document.getElementById('input-bedroom').focus();
        return;
    }
    if (bathroom < 1 || bathroom > 8) {
        const msg = 'Số phòng WC tiêu chuẩn từ 1 đến 8 phòng. Vui lòng kiểm tra lại.';
        showToast(msg, 'warning');
        showFormError(msg);
        document.getElementById('input-bathroom').focus();
        return;
    }

    predictPrice();
}

async function predictPrice(actualPrice = null) {
    const btn = document.getElementById('btn-predict');
    if (btn) btn.innerHTML = '<span class="animate-pulse">Đang thẩm định giá...</span>';

    const city = document.getElementById('input-city').value || 'Hà Nội';
    const district = document.getElementById('input-district').value || 'Cầu Giấy';
    const area = parseFloat(document.getElementById('input-area-num').value || document.getElementById('input-area').value || 75);
    const frontage = parseFloat(document.getElementById('input-frontage-num').value || document.getElementById('input-frontage').value || 4.0);
    const road = parseFloat(document.getElementById('input-road-num').value || document.getElementById('input-road').value || 4.5);
    const floors = parseFloat(document.getElementById('input-floors').value || 3);
    const bedroom = parseFloat(document.getElementById('input-bedroom').value || 3);
    const bathroom = parseFloat(document.getElementById('input-bathroom').value || 2);
    const legal = document.getElementById('input-legal').value || 'Have certificate';
    const direction = document.getElementById('input-direction').value || 'Đông - Nam';

    const payload = {
        city: city,
        district: district,
        area: area,
        frontage: frontage,
        access_road: road,
        floors: floors,
        bedroom: bedroom,
        bathroom: bathroom,
        legal_status: legal,
        house_direction: direction,
        actual_price: actualPrice
    };

    try {
        const res = await fetch('/api/predict', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            const errorBody = await res.json().catch(() => ({}));
            let errorDetail = 'Lỗi xác thực dữ liệu từ máy chủ.';
            if (errorBody.detail) {
                if (Array.isArray(errorBody.detail)) {
                    errorDetail = errorBody.detail.map(d => `${d.loc ? d.loc.slice(-1)[0] : ''}: ${d.msg}`).join('; ');
                } else {
                    errorDetail = errorBody.detail;
                }
            }
            showToast(errorDetail, 'error');
            showFormError(errorDetail);
            return;
        }

        const data = await res.json();

        // Ẩn Standby State và hiện kết quả định giá
        const standbyState = document.getElementById('valuation-standby-state');
        const resultContainer = document.getElementById('valuation-result-container');
        if (standbyState) standbyState.classList.add('hidden');
        if (resultContainer) resultContainer.classList.remove('hidden');

        // Hiển thị Tổng giá định giá
        const priceElem = document.getElementById('res-price');
        if (priceElem) priceElem.innerText = data.predicted_price_billion.toFixed(2);
        
        // Hiển thị Đơn giá trung bình ước lượng (Triệu/m2)
        const unitPriceElem = document.getElementById('res-unit-price');
        if (unitPriceElem) {
            unitPriceElem.innerHTML = `Đơn giá ước lượng: <span class="text-emerald-700 font-extrabold text-xs sm:text-sm">~ ${data.unit_price_million_per_m2} Triệu VNĐ / m²</span>`;
        }

        // Huy hiệu so sánh giá thực tế
        const badge = document.getElementById('res-comparison-badge');
        if (badge) {
            if (data.actual_vs_predicted) {
                badge.classList.remove('hidden');
                document.getElementById('res-actual-price').innerText = data.actual_vs_predicted.actual_price_billion.toFixed(2) + ' TỶ';
                document.getElementById('res-error-badge').innerText = `Sai lệch: ${data.actual_vs_predicted.error_billion} Tỷ (${data.actual_vs_predicted.error_percentage}%)`;
            } else {
                badge.classList.add('hidden');
            }
        }

        // Cập nhật thẻ thông tin phân tích thị trường khu vực
        const locElem = document.getElementById('insight-location');
        if (locElem) locElem.innerText = `${payload.district}, ${payload.city}`;

        const tierElem = document.getElementById('insight-tier');
        if (tierElem) {
            if (data.predicted_price_billion < 5.0) tierElem.innerText = 'Phổ thông (< 5 Tỷ)';
            else if (data.predicted_price_billion <= 12.0) tierElem.innerText = 'Trung - Cao cấp (5 - 12 Tỷ)';
            else tierElem.innerText = 'Cao cấp / Biệt thự (> 12 Tỷ)';
        }

        // Bóc tách cấu phần giá trị (Dạng bảng chuyên nghiệp)
        const featureContainer = document.getElementById('feature-bars');
        if (featureContainer && data.feature_contributions) {
            featureContainer.innerHTML = '';
            
            data.feature_contributions.forEach(item => {
                let iconName = 'layers';
                let subDesc = '';
                const fLower = item.feature.toLowerCase();
                if (fLower.includes('diện tích')) {
                    iconName = 'maximize-2';
                    subDesc = 'Quy mô diện tích sàn sử dụng';
                } else if (fLower.includes('vị trí')) {
                    iconName = 'map-pin';
                    subDesc = 'Mặt bằng giá thị trường khu vực';
                } else if (fLower.includes('mặt tiền') || fLower.includes('đường')) {
                    iconName = 'navigation';
                    subDesc = 'Lợi thế tiếp cận & giao thông';
                } else if (fLower.includes('quy mô')) {
                    iconName = 'home';
                    subDesc = 'Kết cấu xây dựng thực tế';
                } else if (fLower.includes('pháp lý') || fLower.includes('hướng')) {
                    iconName = 'shield-check';
                    subDesc = 'Tính an toàn pháp lý & phong thủy';
                }

                const row = document.createElement('div');
                row.className = 'flex items-center justify-between p-2.5 rounded-xl bg-slate-50 border border-slate-100 hover:bg-slate-100/80 transition text-xs';
                row.innerHTML = `
                    <div class="flex items-center gap-2.5">
                        <div class="w-7 h-7 rounded-lg bg-white border border-slate-200 flex items-center justify-center text-blue-600 shadow-2xs">
                            <i data-lucide="${iconName}" class="w-3.5 h-3.5"></i>
                        </div>
                        <div>
                            <div class="font-bold text-slate-800">${item.feature}</div>
                            <div class="text-[10.5px] text-slate-400 font-medium">${subDesc}</div>
                        </div>
                    </div>
                    <div class="text-right">
                        <div class="font-extrabold text-slate-900 text-xs">${item.impact}</div>
                        <span class="inline-block mt-0.5 px-2 py-0.2 rounded-md bg-emerald-50 border border-emerald-200 text-emerald-800 font-bold text-[10.5px]">
                            ${item.weight}%
                        </span>
                    </div>
                `;
                featureContainer.appendChild(row);
            });
        }

        showToast(`Đã định giá thành công: ${data.predicted_price_billion.toFixed(2)} Tỷ VNĐ (~${data.unit_price_million_per_m2} Tr/m²)`, 'success');

    } catch (err) {
        console.error('Lỗi định giá:', err);
        showToast('Có lỗi xảy ra khi kết nối máy chủ thẩm định.', 'error');
    } finally {
        if (btn) {
            btn.innerHTML = `
                <i data-lucide="sparkles" class="w-4 h-4 text-white"></i>
                <span>Thực hiện Định giá BĐS</span>
            `;
        }
        if (window.lucide) lucide.createIcons();
    }
}

// HỎI TRỢ LÝ AI VỀ KHU VỰC ĐANG ĐỊNH GIÁ
function askAiAboutArea() {
    const city = document.getElementById('input-city').value || 'Hà Nội';
    const district = document.getElementById('input-district').value || 'Cầu Giấy';
    switchTab('chat');
    sendQuickPrompt(`Mặt bằng giá và thị trường bất động sản tại ${district}, ${city}`);
}

function resetForm() {
    clearFormError();
    document.getElementById('input-city').selectedIndex = 0;
    const districtSelect = document.getElementById('input-district');
    districtSelect.innerHTML = '<option value="" disabled selected>-- Chọn Quận / Huyện --</option>';

    document.getElementById('input-area').value = 75;
    document.getElementById('input-area-num').value = '';
    document.getElementById('input-frontage').value = 4.0;
    document.getElementById('input-frontage-num').value = '';
    document.getElementById('input-road').value = 4.5;
    document.getElementById('input-road-num').value = '';
    document.getElementById('input-floors').value = '';
    document.getElementById('input-bedroom').value = '';
    document.getElementById('input-bathroom').value = '';
    document.getElementById('input-legal').selectedIndex = 0;
    document.getElementById('input-direction').selectedIndex = 0;
    document.getElementById('sample-select').value = '';

    // Khôi phục về Standby state ban đầu
    const standbyState = document.getElementById('valuation-standby-state');
    const resultContainer = document.getElementById('valuation-result-container');
    if (standbyState) standbyState.classList.remove('hidden');
    if (resultContainer) resultContainer.classList.add('hidden');
}

// ==========================================
// 7. KNOWLEDGE GRAPH CHATBOT LOGIC
// ==========================================
function toggleApiKeySettings() {
    const panel = document.getElementById('api-key-panel');
    if (panel) {
        panel.classList.toggle('hidden');
    }
}

function saveApiKey() {
    const key = document.getElementById('api-key-input').value.trim();
    const provider = document.getElementById('api-provider').value;
    if (key) {
        localStorage.setItem('user_ai_api_key', key);
        localStorage.setItem('user_ai_provider', provider);
        const badge = document.getElementById('ai-mode-badge');
        if (badge) {
            badge.innerText = `AI: ${provider.toUpperCase()} Đã kích hoạt`;
            badge.className = 'text-[10px] sm:text-[11px] px-2.5 py-1 rounded-full bg-blue-50 text-blue-700 font-extrabold border border-blue-200';
        }
        showToast('Đã lưu khóa API an toàn trong trình duyệt.', 'success');
        toggleApiKeySettings();
    } else {
        localStorage.removeItem('user_ai_api_key');
        const badge = document.getElementById('ai-mode-badge');
        if (badge) {
            badge.innerText = 'Đồ thị Neo4j: Sẵn sàng';
            badge.className = 'text-[10px] sm:text-[11px] px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 font-extrabold border border-emerald-200';
        }
        showToast('Đã xóa cấu hình API key.', 'info');
    }
}

function sendQuickPrompt(promptText) {
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.value = promptText;
        sendChatMessage();
    }
}

async function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const msg = input.value.trim();
    if (!msg) return;

    const chatMessages = document.getElementById('chat-messages');

    // 1. Render User Message
    const userDiv = document.createElement('div');
    userDiv.className = 'flex justify-end';
    userDiv.innerHTML = `
        <div class="bg-blue-600 text-white p-3 rounded-2xl max-w-[85%] text-xs font-semibold shadow-sm leading-relaxed">
            ${escapeHtml(msg)}
        </div>
    `;
    chatMessages.appendChild(userDiv);
    input.value = '';
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // 2. Render Bot Loading Message
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'flex justify-start';
    loadingDiv.innerHTML = `
        <div class="card-surface p-3 max-w-[85%] text-xs text-slate-500 shadow-sm flex items-center gap-2">
            <i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin text-blue-600"></i>
            <span>Đang tra cứu Đồ thị Tri thức Neo4j và tổng hợp câu trả lời...</span>
        </div>
    `;
    chatMessages.appendChild(loadingDiv);
    if (window.lucide) lucide.createIcons();
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // 3. Gọi API Chat
    const apiKey = localStorage.getItem('user_ai_api_key') || null;
    const provider = localStorage.getItem('user_ai_provider') || 'openai';

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                message: msg,
                api_key: apiKey,
                provider: provider
            })
        });
        const data = await res.json();
        loadingDiv.remove();

        // 4. Render Bot Reply
        const botDiv = document.createElement('div');
        botDiv.className = 'flex justify-start';

        let propertyCardsHtml = '';
        if (data.matched_properties && data.matched_properties.length > 0) {
            propertyCardsHtml = `
                <div class="mt-2.5 pt-2 border-t border-slate-100 space-y-2">
                    <div class="text-[11px] font-extrabold text-blue-900 flex items-center gap-1">
                        <i data-lucide="home" class="w-3 h-3 text-blue-600"></i>
                        <span>Bất động sản phù hợp từ Đồ thị Tri thức (${data.matched_properties.length} căn):</span>
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                        ${data.matched_properties.slice(0, 4).map(p => `
                            <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200/80 text-[11px] hover:border-blue-300 transition shadow-2xs">
                                <div class="font-bold text-slate-900">${p.district}, ${p.city}</div>
                                <div class="text-slate-600 mt-0.5">${p.area}m² • ${p.floors || 1} tầng • ${p.bedroom || 1} PN</div>
                                <div class="mt-1 flex justify-between items-center">
                                    <span class="font-extrabold text-emerald-700 text-xs">${p.price_billion} Tỷ</span>
                                    <span class="text-[10px] text-slate-500 font-semibold">~${p.unit_price_million_m2} Tr/m²</span>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }

        botDiv.innerHTML = `
            <div class="card-surface p-3.5 max-w-[90%] text-xs leading-relaxed shadow-sm space-y-2">
                <div class="text-slate-800">${formatMarkdown(data.reply)}</div>
                ${propertyCardsHtml}
            </div>
        `;
        chatMessages.appendChild(botDiv);

    } catch (err) {
        loadingDiv.remove();
        const errDiv = document.createElement('div');
        errDiv.className = 'flex justify-start';
        errDiv.innerHTML = `
            <div class="card-surface p-3 text-xs text-rose-600 border border-rose-200 bg-rose-50 rounded-xl">
                Không thể kết nối đến Trợ lý Đồ thị Neo4j. Vui lòng thử lại sau.
            </div>
        `;
        chatMessages.appendChild(errDiv);
    } finally {
        if (window.lucide) lucide.createIcons();
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.innerText = text;
    return div.innerHTML;
}

function formatMarkdown(text) {
    if (!text) return '';
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n\n/g, '<br><br>')
        .replace(/\n/g, '<br>');
}

// ==========================================
// 8. INITIALIZE APPLICATION ON LOAD
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    // 1. Phục hồi API Key đã lưu
    const savedKey = localStorage.getItem('user_ai_api_key');
    const savedProvider = localStorage.getItem('user_ai_provider') || 'openai';
    if (savedKey) {
        const badge = document.getElementById('ai-mode-badge');
        if (badge) {
            badge.innerText = `AI: ${savedProvider.toUpperCase()} Đã kích hoạt`;
            badge.className = 'text-[10px] sm:text-[11px] px-2.5 py-1 rounded-full bg-blue-50 text-blue-700 font-extrabold border border-blue-200';
        }
        const keyInput = document.getElementById('api-key-input');
        if (keyInput) keyInput.value = savedKey;
        const provSelect = document.getElementById('api-provider');
        if (provSelect) provSelect.value = savedProvider;
    }

    // 2. Phục hồi Tab từ Hash hoặc LocalStorage
    let initialTab = 'predict';
    if (window.location.hash) {
        const hashTab = window.location.hash.replace('#', '');
        if (['predict', 'chat', 'models'].includes(hashTab)) {
            initialTab = hashTab;
        }
    } else {
        const savedTab = localStorage.getItem('active_app_tab');
        if (savedTab && ['predict', 'chat', 'models'].includes(savedTab)) {
            initialTab = savedTab;
        }
    }
    switchTab(initialTab, false);

    window.addEventListener('hashchange', () => {
        const hashTab = window.location.hash.replace('#', '');
        if (['predict', 'chat', 'models'].includes(hashTab)) {
            switchTab(hashTab, false);
        }
    });

    // 3. Tải danh sách BĐS mẫu
    fetchSampleData();

    // 4. Bắt phím Enter trong ô Chat
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendChatMessage();
            }
        });
    }

    // 5. Khởi tạo biểu tượng Lucide
    renderIcons();
    setTimeout(renderIcons, 100);
    setTimeout(renderIcons, 500);
});

function renderIcons() {
    if (window.lucide && typeof lucide.createIcons === 'function') {
        try {
            lucide.createIcons();
        } catch (e) {
            console.warn('Lỗi render icon:', e);
        }
    }
}

window.addEventListener('load', renderIcons);
