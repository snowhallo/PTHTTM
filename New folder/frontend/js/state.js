/**
 * APPLICATION GLOBAL STATE & TAB NAVIGATION (WITH PERSISTENCE)
 */

const appState = {
  currentTab: 'tab-predict',
  lastPrediction: null,
  visNetwork: null,
  allNodes: [],
  allEdges: [],
  networkData: { nodes: null, edges: null },
  chatHistory: [],
  physicsEnabled: true
};

function initTabNavigation() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTab = btn.getAttribute('data-tab');
      switchTab(targetTab);
    });
  });

  // Restore active tab on page refresh via hash or localStorage
  const validTabs = ['tab-predict', 'tab-graph', 'tab-chat', 'tab-benchmark'];
  const hash = window.location.hash ? window.location.hash.replace('#', '') : '';
  const savedTab = (validTabs.includes(hash) ? hash : null) || localStorage.getItem('activeDiabetesTab') || 'tab-predict';

  if (validTabs.includes(savedTab)) {
    switchTab(savedTab);
  }
}

function switchTab(tabId) {
  appState.currentTab = tabId;
  
  // Persist to localStorage and URL Hash for seamless page refreshes
  try {
    localStorage.setItem('activeDiabetesTab', tabId);
    if (window.location.hash !== `#${tabId}`) {
      window.history.replaceState(null, null, `#${tabId}`);
    }
  } catch (e) {
    // Ignore storage errors if private mode
  }
  
  // Update Buttons
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-tab') === tabId);
  });
  
  // Update Panels
  document.querySelectorAll('.tab-content').forEach(content => {
    content.classList.toggle('active', content.id === tabId);
  });

  // Graph tab handling: init or redraw + fit
  if (tabId === 'tab-graph') {
    if (!appState.visNetwork) {
      if (typeof initKnowledgeGraph === 'function') {
        initKnowledgeGraph();
      }
    } else {
      setTimeout(() => {
        if (appState.visNetwork) {
          appState.visNetwork.redraw();
          appState.visNetwork.fit({ animation: false });
        }
      }, 150);
    }
  }
}
