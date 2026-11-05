/**
 * TAB 3: GRAPHRAG MEDICAL CHATBOT & MARKDOWN PARSING
 */

function handleChatKeyDown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendChatMessage();
  }
}

function autoResizeChatInput(el) {
  if (!el) return;
  el.style.height = 'auto';
  const newHeight = Math.min(Math.max(el.scrollHeight, 42), 120);
  el.style.height = newHeight + 'px';
}

function sendSuggestedQuery(text) {
  const input = document.getElementById('chatInput');
  if (input) {
    input.value = text;
    autoResizeChatInput(input);
    sendChatMessage();
  }
}

async function sendChatMessage() {
  const input = document.getElementById('chatInput');
  if (!input) return;
  const text = input.value.trim();
  if (!text) return;

  // Append user message
  appendMessage('user', text);
  input.value = '';
  input.style.height = '42px';

  // Append typing indicator
  const typingId = appendTypingIndicator();

  const payload = {
    message: text,
    ml_context: appState.lastPrediction
  };

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    removeTypingIndicator(typingId);
    appendMessage('bot', data.answer || 'Xin lỗi, tôi không thể xử lý câu hỏi này lúc này.', data.engine_mode);
  } catch (err) {
    removeTypingIndicator(typingId);
    appendMessage('bot', `Lỗi kết nối tới dịch vụ Chatbot: ${err.message}`);
  }
}

function appendMessage(sender, text, engineMode = null) {
  const container = document.getElementById('chatMessages');
  if (!container) return;
  const msgDiv = document.createElement('div');
  msgDiv.className = `msg ${sender === 'user' ? 'user-msg' : 'bot-msg'}`;

  const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  const formattedText = parseSimpleMarkdown(text);

  let badgeHtml = '';
  if (engineMode) {
    const isLLM = engineMode.includes('Generative') || engineMode.includes('Gemini') || engineMode.includes('OpenAI');
    const badgeColor = isLLM ? '#0d9488' : '#64748b';
    const badgeBg = isLLM ? '#f0fdfa' : '#f1f5f9';
    const badgeIcon = isLLM ? 'fa-wand-magic-sparkles' : 'fa-database';
    badgeHtml = `<span style="display:inline-block; font-size:0.7rem; font-weight:600; padding:0.15rem 0.5rem; border-radius:9999px; background:${badgeBg}; color:${badgeColor}; border:1px solid ${badgeColor}33; margin-bottom:0.4rem;"><i class="fa-solid ${badgeIcon}"></i> ${engineMode}</span>`;
  }

  msgDiv.innerHTML = `
    <div class="msg-avatar"><i class="fa-solid ${sender === 'user' ? 'fa-user' : 'fa-notes-medical'}"></i></div>
    <div class="msg-bubble">
      ${badgeHtml}
      <div class="msg-text">${formattedText}</div>
      <span class="msg-time">${timeStr}</span>
    </div>
  `;

  container.appendChild(msgDiv);
  container.scrollTop = container.scrollHeight;
}

function appendTypingIndicator() {
  const container = document.getElementById('chatMessages');
  if (!container) return null;
  const typingDiv = document.createElement('div');
  const id = 'typing-' + Date.now();
  typingDiv.id = id;
  typingDiv.className = 'msg bot-msg';
  typingDiv.innerHTML = `
    <div class="msg-avatar"><i class="fa-solid fa-notes-medical"></i></div>
    <div class="msg-bubble">
      <div class="msg-text"><i class="fa-solid fa-spinner fa-spin"></i> Đang suy nghĩ và đối chiếu Knowledge Graph...</div>
    </div>
  `;
  container.appendChild(typingDiv);
  container.scrollTop = container.scrollHeight;
  return id;
}

function removeTypingIndicator(id) {
  if (!id) return;
  const el = document.getElementById(id);
  if (el) el.remove();
}

function initChatEventListeners() {
  const clearBtn = document.getElementById('btnClearChat');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      const container = document.getElementById('chatMessages');
      if (container) {
        container.innerHTML = `
          <div class="msg bot-msg">
            <div class="msg-avatar"><i class="fa-solid fa-notes-medical"></i></div>
            <div class="msg-bubble">
              <div class="msg-text">
                <p>Lịch sử hội thoại đã được làm mới. Bạn có thể nhập câu hỏi để tiếp tục tra cứu thông tin.</p>
              </div>
              <span class="msg-time">Hệ thống</span>
            </div>
          </div>
        `;
      }
    });
  }
}

function parseSimpleMarkdown(text) {
  if (!text) return '';
  return text
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^#### (.*$)/gim, '<h4>$1</h4>')
    .replace(/^> (.*$)/gim, '<blockquote>$1</blockquote>')
    .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/gim, '<em>$1</em>')
    .replace(/\[(.*?)\]\((.*?)\)/gim, '<a href="$2" target="_blank" style="color:#0284c7;text-decoration:underline;">$1</a>')
    .replace(/\n\n/gim, '<br><br>')
    .replace(/\n/gim, '<br>');
}
