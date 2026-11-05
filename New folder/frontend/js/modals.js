/**
 * MODAL DIALOG CONTROLLERS - NEO4J & GEMINI API KEY CONFIGURATION
 */

async function checkNeo4jStatus() {
  const badgeBtn = document.getElementById('btnOpenNeo4jModal');
  const text = document.getElementById('neo4jStatusText');
  const dot = document.getElementById('neo4jStatusDot');
  try {
    const res = await fetch('/api/neo4j/status');
    const data = await res.json();
    if (data.connected) {
      if (text) text.innerText = `Neo4j DB Online (${data.node_count} Nodes)`;
      if (dot) {
        dot.style.background = '#10b981';
        dot.style.boxShadow = '0 0 0 3px rgba(16, 185, 129, 0.2)';
      }
      if (badgeBtn) {
        badgeBtn.style.background = '#ecfdf5';
        badgeBtn.style.borderColor = '#a7f3d0';
        badgeBtn.style.color = '#047857';
      }
    } else {
      if (text) text.innerText = `Local Graph (${data.node_count} Nodes)`;
      if (dot) {
        dot.style.background = '#0284c7';
        dot.style.boxShadow = '0 0 0 3px rgba(2, 132, 199, 0.2)';
      }
      if (badgeBtn) {
        badgeBtn.style.background = '#ffffff';
        badgeBtn.style.borderColor = '#cbd5e1';
        badgeBtn.style.color = '#334155';
      }
    }
  } catch (e) {
    if (text) text.innerText = 'Graph Engine Active';
  }
}

// Neo4j Configuration Modal Handlers
function initNeo4jModal() {
  const modal = document.getElementById('neo4jModal');
  const btnOpen = document.getElementById('btnOpenNeo4jModal');
  const btnClose = document.getElementById('btnCloseNeo4jModal');
  const form = document.getElementById('neo4jConfigForm');
  const feedback = document.getElementById('neo4jModalFeedback');
  const btnSubmit = document.getElementById('btnSaveNeo4jConfig');

  if (!modal) return;

  const openModal = () => {
    modal.classList.remove('hidden');
    if (feedback) {
      feedback.className = 'modal-feedback hidden';
      feedback.innerText = '';
    }
  };

  const closeModal = () => {
    modal.classList.add('hidden');
  };

  if (btnOpen) btnOpen.addEventListener('click', openModal);
  if (btnClose) btnClose.addEventListener('click', closeModal);

  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const uri = document.getElementById('neo4jUri').value.trim();
      const user = document.getElementById('neo4jUser').value.trim();
      const password = document.getElementById('neo4jPassword').value.trim();

      if (btnSubmit) {
        btnSubmit.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Đang kết nối...';
        btnSubmit.disabled = true;
      }

      try {
        const res = await fetch('/api/neo4j/config', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ uri, user, password })
        });
        const data = await res.json();

        if (feedback) {
          feedback.classList.remove('hidden');
          if (data.connected) {
            feedback.className = 'modal-feedback success';
            feedback.innerHTML = `<i class="fa-solid fa-circle-check"></i> ${data.message}`;
            checkNeo4jStatus();
            // Refresh graph if initialized
            if (appState.visNetwork && typeof initKnowledgeGraph === 'function') {
              initKnowledgeGraph();
            }
            setTimeout(() => { closeModal(); }, 1800);
          } else {
            feedback.className = 'modal-feedback error';
            feedback.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${data.message}`;
          }
        }
      } catch (err) {
        if (feedback) {
          feedback.className = 'modal-feedback error';
          feedback.innerText = 'Lỗi gửi yêu cầu: ' + err.message;
        }
      } finally {
        if (btnSubmit) {
          btnSubmit.innerHTML = '<i class="fa-solid fa-link"></i> <span>Kết Nối & Đồng Bộ Dữ Liệu</span>';
          btnSubmit.disabled = false;
        }
      }
    });
  }
}

// API Key Modal Handlers
function initApiKeyModal() {
  const modal = document.getElementById('apiKeyModal');
  const btnOpen = document.getElementById('btnOpenApiKeyModal');
  const btnClose = document.getElementById('btnCloseApiKeyModal');
  const form = document.getElementById('apiKeyConfigForm');
  const feedback = document.getElementById('apiKeyModalFeedback');
  const btnSubmit = document.getElementById('btnSaveApiKey');

  if (!modal) return;

  const openModal = () => {
    modal.classList.remove('hidden');
    if (feedback) {
      feedback.className = 'modal-feedback hidden';
      feedback.innerText = '';
    }
  };

  const closeModal = () => {
    modal.classList.add('hidden');
  };

  if (btnOpen) btnOpen.addEventListener('click', openModal);
  if (btnClose) btnClose.addEventListener('click', closeModal);

  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const geminiApiKey = document.getElementById('geminiApiKey').value.trim();

      if (btnSubmit) {
        btnSubmit.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Đang lưu...';
        btnSubmit.disabled = true;
      }

      try {
        const res = await fetch('/api/chat/config', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ gemini_api_key: geminiApiKey })
        });
        
        if (!res.ok) {
          throw new Error(`Server chưa nạp endpoint mới (mã lỗi ${res.status}). Hãy tắt và chạy lại 'python app.py' trên Terminal.`);
        }
        
        const data = await res.json();

        if (feedback) {
          feedback.classList.remove('hidden');
          if (data.success) {
            feedback.className = 'modal-feedback success';
            feedback.innerHTML = `<i class="fa-solid fa-circle-check"></i> ${data.message}`;
            setTimeout(() => { closeModal(); }, 1500);
          } else {
            feedback.className = 'modal-feedback error';
            feedback.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${data.message || 'Lỗi cập nhật'}`;
          }
        }
      } catch (err) {
        if (feedback) {
          feedback.className = 'modal-feedback error';
          feedback.innerText = 'Lỗi gửi yêu cầu: ' + err.message;
        }
      } finally {
        if (btnSubmit) {
          btnSubmit.innerHTML = '<i class="fa-solid fa-floppy-disk"></i> <span>Lưu & Kích Hoạt Generative AI</span>';
          btnSubmit.disabled = false;
        }
      }
    });
  }
}
