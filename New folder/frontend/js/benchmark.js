/**
 * TAB 4: CHAPTER 12 EXPERIMENTAL BENCHMARK DATA LOADER
 */

async function loadBenchmarkData() {
  try {
    const res = await fetch('/api/benchmark');
    const data = await res.json();
    const rows = data.benchmark || [];
    const tbody = document.getElementById('benchmarkTableBody');
    if (!tbody || rows.length === 0) return;

    tbody.innerHTML = '';
    rows.forEach(r => {
      const tr = document.createElement('tr');
      if (r.is_best) tr.className = 'highlight-row';

      tr.innerHTML = `
        <td><strong>${r.subset}</strong> ${r.is_best ? '⭐' : ''}</td>
        <td><code>${r.features.join(', ')}</code></td>
        <td>${r.logistic_regression}</td>
        <td>${r.is_best ? `<span class="badge-best">${r.knn}</span>` : r.knn}</td>
        <td>${r.svm_linear}</td>
        <td>${r.svm_rbf}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    console.warn('Could not load dynamic benchmark table, using fallback data.', e);
  }
}
