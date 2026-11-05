/**
 * DIABETES CLINICAL AI & KNOWLEDGE GRAPH - APPLICATION ENTRYPOINT
 * Modular Clean Architecture
 */

document.addEventListener('DOMContentLoaded', () => {
  initTabNavigation();
  initFormInputs();
  if (typeof initChatEventListeners === 'function') {
    initChatEventListeners();
  }
  initNeo4jModal();
  initApiKeyModal();
  checkNeo4jStatus();
  loadBenchmarkData();
});
