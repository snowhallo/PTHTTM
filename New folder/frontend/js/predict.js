/**
 * TAB 1: FORM INPUTS, PRESETS & CLINICAL PREDICTION (ML)
 * Compact 2-Column Grid Architecture (Quick Top 3 & Full 8 Parameters)
 */

appState.predictionMode = 'quick';

function setPredictionMode(mode) {
  appState.predictionMode = mode;
  const btnQuick = document.getElementById('btnModeQuick');
  const btnFull = document.getElementById('btnModeFull');
  const advFields = document.querySelectorAll('.adv-field');
  const btnText = document.getElementById('predictBtnText');
  const presetsRow = document.getElementById('presetsRow');

  if (mode === 'full') {
    if (btnQuick) btnQuick.classList.remove('active');
    if (btnFull) btnFull.classList.add('active');
    advFields.forEach(el => el.classList.remove('hidden'));
    if (btnText) {
      btnText.innerHTML = '<span class="mode-text-full">Thực Hiện Dự Đoán Chuyên Sâu (Đủ 8 Chỉ Số)</span><span class="mode-text-short">Dự Đoán (8 Chỉ Số)</span>';
    }
    
    if (presetsRow) {
      presetsRow.innerHTML = `
        <span class="presets-label"><i class="fa-solid fa-wand-magic-sparkles"></i> Mẫu (8 chỉ số):</span>
        <button type="button" class="preset-btn" onclick="applyPreset(95, 22.5, 26, 0, 70, 20, 75, 0.25)">Khỏe mạnh</button>
        <button type="button" class="preset-btn warning" onclick="applyPreset(120, 28.5, 45, 1, 85, 28, 140, 0.55)">Tiền ĐTĐ & Huyết áp</button>
        <button type="button" class="preset-btn danger" onclick="applyPreset(168, 36.5, 50, 3, 94, 35, 220, 0.88)">Nguy cơ cao (Type 2)</button>
      `;
    }
  } else {
    if (btnQuick) btnQuick.classList.add('active');
    if (btnFull) btnFull.classList.remove('active');
    advFields.forEach(el => el.classList.add('hidden'));
    if (btnText) {
      btnText.innerHTML = '<span class="mode-text-full">Thực Hiện Dự Đoán Học Máy (Top 3)</span><span class="mode-text-short">Dự Đoán (Top 3)</span>';
    }
    
    if (presetsRow) {
      presetsRow.innerHTML = `
        <span class="presets-label"><i class="fa-solid fa-wand-magic-sparkles"></i> Mẫu:</span>
        <button type="button" class="preset-btn" onclick="applyPreset(100, 28.5, 29, 0, 70, 20, 75, 0.25)">Bình thường</button>
        <button type="button" class="preset-btn warning" onclick="applyPreset(118, 29.5, 42, 1, 80, 26, 125, 0.45)">Tiền ĐTĐ</button>
        <button type="button" class="preset-btn danger" onclick="applyPreset(165, 38.0, 52, 3, 94, 35, 210, 0.85)">Nguy cơ cao</button>
      `;
    }
  }
}

function initFormInputs() {
  const pairs = [
    { range: 'rangeGlucose', input: 'inputGlucose' },
    { range: 'rangeBMI', input: 'inputBMI' },
    { range: 'rangeAge', input: 'inputAge' },
    { range: 'rangeBP', input: 'inputBP' },
    { range: 'rangeInsulin', input: 'inputInsulin' },
    { range: 'rangeDPF', input: 'inputDPF' },
    { range: 'rangePregnancies', input: 'inputPregnancies' },
    { range: 'rangeSkin', input: 'inputSkin' }
  ];

  pairs.forEach(p => {
    const rangeEl = document.getElementById(p.range);
    const inputEl = document.getElementById(p.input);

    if (rangeEl && inputEl) {
      rangeEl.addEventListener('input', () => {
        inputEl.value = rangeEl.value;
      });

      inputEl.addEventListener('input', () => {
        rangeEl.value = inputEl.value;
      });
    }
  });

  // Handle Form Submit
  const form = document.getElementById('predictionForm');
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      await performPrediction();
    });
  }

  // Ask bot button with context
  const btnAskBot = document.getElementById('btnAskBotWithContext');
  if (btnAskBot) {
    btnAskBot.addEventListener('click', () => {
      if (!appState.lastPrediction) return;
      switchTab('tab-chat');
      
      const pred = appState.lastPrediction;
      const inp = pred.inputs || {};
      
      let promptMsg = '';
      if (pred.mode === 'full') {
        promptMsg = `Tôi vừa thực hiện chẩn đoán chuyên sâu (8 chỉ số lâm sàng): Đường huyết = ${inp.Glucose} mg/dL, BMI = ${inp.BMI}, Tuổi = ${inp.Age}, Huyết áp = ${inp.BloodPressure} mmHg, Insulin = ${inp.Insulin} μU/ml, Phả hệ di truyền = ${inp.DiabetesPedigreeFunction}, Mang thai = ${inp.Pregnancies} lần. Mô hình phân loại tôi thuộc nhóm "${pred.label}" (${pred.risk_level}). Xin tư vấn phác đồ điều trị và các sản phẩm Long Châu phù hợp.`;
      } else {
        promptMsg = `Tôi vừa đo chỉ số: Glucose = ${inp.Glucose} mg/dL, BMI = ${inp.BMI}, Tuổi = ${inp.Age}. Mô hình chẩn đoán tôi thuộc nhóm "${pred.label}" (${pred.risk_level}). Xin tư vấn phác đồ và thuốc Long Châu phù hợp.`;
      }
      
      const chatInput = document.getElementById('chatInput');
      if (chatInput) {
        chatInput.value = promptMsg;
        if (typeof sendChatMessage === 'function') {
          sendChatMessage();
        }
      }
    });
  }
}

function applyPreset(glucose, bmi, age, pregnancies = 0, bp = 72, skin = 23, insulin = 80, dpf = 0.47) {
  const setVal = (rangeId, inputId, val) => {
    const r = document.getElementById(rangeId);
    const i = document.getElementById(inputId);
    if (r && i) {
      r.value = val;
      i.value = val;
    }
  };

  setVal('rangeGlucose', 'inputGlucose', glucose);
  setVal('rangeBMI', 'inputBMI', bmi);
  setVal('rangeAge', 'inputAge', age);
  setVal('rangeBP', 'inputBP', bp);
  setVal('rangeInsulin', 'inputInsulin', insulin);
  setVal('rangeDPF', 'inputDPF', dpf);
  setVal('rangePregnancies', 'inputPregnancies', pregnancies);
  setVal('rangeSkin', 'inputSkin', skin);

  performPrediction();
}

async function performPrediction() {
  const btn = document.getElementById('btnPredict');
  if (!btn) return;
  const originalHtml = btn.innerHTML;
  btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> <span>Đang xử lý mô hình...</span>';
  btn.disabled = true;

  const mode = appState.predictionMode || 'quick';
  const payload = {
    mode: mode,
    Glucose: parseFloat(document.getElementById('inputGlucose')?.value || 100),
    BMI: parseFloat(document.getElementById('inputBMI')?.value || 30),
    Age: parseFloat(document.getElementById('inputAge')?.value || 29)
  };

  if (mode === 'full') {
    payload.Pregnancies = parseFloat(document.getElementById('inputPregnancies')?.value || 1);
    payload.BloodPressure = parseFloat(document.getElementById('inputBP')?.value || 72);
    payload.SkinThickness = parseFloat(document.getElementById('inputSkin')?.value || 23);
    payload.Insulin = parseFloat(document.getElementById('inputInsulin')?.value || 80);
    payload.DiabetesPedigreeFunction = parseFloat(document.getElementById('inputDPF')?.value || 0.47);
  }

  try {
    const res = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    appState.lastPrediction = data;
    renderPredictionResult(data);
  } catch (err) {
    alert('Lỗi kết nối tới Server API: ' + err.message);
  } finally {
    btn.innerHTML = originalHtml;
    btn.disabled = false;
  }
}

function renderPredictionResult(data) {
  const placeholder = document.getElementById('resPlaceholder');
  const compEl = document.getElementById('resComputed');
  if (placeholder) placeholder.classList.add('hidden');
  if (compEl) compEl.classList.remove('hidden');

  const banner = document.getElementById('diagBanner');
  const icon = document.getElementById('diagIcon');
  const title = document.getElementById('diagTitle');
  const tag = document.getElementById('diagTag');

  if (data.prediction === 1) {
    if (banner) banner.className = 'diagnosis-banner danger';
    if (icon) icon.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i>';
    if (title) title.innerText = 'Diabetic (Nguy Cơ Mắc Bệnh Cao)';
    if (tag) {
      tag.innerText = `Mức độ nguy cơ: ${data.risk_level}`;
      tag.style.color = '#dc2626';
    }
  } else {
    if (banner) banner.className = 'diagnosis-banner';
    if (icon) icon.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
    if (title) title.innerText = 'Not Diabetic (Chỉ Số Bình Thường)';
    if (tag) {
      tag.innerText = `Mức độ nguy cơ: ${data.risk_level}`;
      tag.style.color = '#059669';
    }
  }

  // Metrics
  const confVal = document.getElementById('valConfidence');
  const confFill = document.getElementById('fillConfidence');
  if (confVal) confVal.innerText = data.confidence + '%';
  if (confFill) confFill.style.width = data.confidence + '%';

  const probVal = document.getElementById('valProbDiabetic');
  const probFill = document.getElementById('fillProbDiabetic');
  if (probVal) probVal.innerText = data.diabetic_probability + '%';
  if (probFill) probFill.style.width = data.diabetic_probability + '%';

  // Recommendations
  const recsList = document.getElementById('recsList');
  if (recsList) {
    recsList.innerHTML = '';
    (data.recommendations || []).forEach(r => {
      const li = document.createElement('li');
      li.innerText = r;
      recsList.appendChild(li);
    });
  }
}
