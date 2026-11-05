/**
 * TAB 2: VIS.JS KNOWLEDGE GRAPH VISUALIZER & INSPECTOR
 */

async function initKnowledgeGraph() {
  const container = document.getElementById('visNetworkContainer');
  const loading = document.getElementById('graphLoading');
  if (!container) return;
  if (loading) loading.style.display = 'block';

  try {
    const res = await fetch('/api/graph');
    const data = await res.json();
    
    appState.allNodes = data.nodes || [];
    appState.allEdges = data.edges || [];

    const nodesDataSet = new vis.DataSet(appState.allNodes);
    const edgesDataSet = new vis.DataSet(appState.allEdges);
    appState.networkData = { nodes: nodesDataSet, edges: edgesDataSet };

    const options = {
      nodes: {
        shadow: true,
        borderWidth: 2
      },
      edges: {
        width: 1.5,
        smooth: {
          type: 'continuous'
        },
        shadow: false
      },
      physics: {
        stabilization: { iterations: 150 },
        barnesHut: {
          gravitationalConstant: -3500,
          springConstant: 0.04,
          springLength: 95
        }
      },
      interaction: {
        hover: true,
        tooltipDelay: 150,
        navigationButtons: false,
        keyboard: true
      }
    };

    appState.visNetwork = new vis.Network(container, appState.networkData, options);

    // Event on Node Click
    appState.visNetwork.on('click', function (params) {
      if (params.nodes.length > 0) {
        const nodeId = params.nodes[0];
        fetchAndShowNodeDetails(nodeId);
      }
    });

    // Toolbar Event Listeners
    setupGraphToolbar();
    if (loading) loading.style.display = 'none';
  } catch (err) {
    if (loading) loading.innerHTML = `<p class="text-danger">Lỗi tải đồ thị: ${err.message}</p>`;
  }
}

function setupGraphToolbar() {
  // Fit Button
  const btnFit = document.getElementById('btnFitGraph');
  if (btnFit) {
    btnFit.addEventListener('click', () => {
      if (appState.visNetwork) appState.visNetwork.fit({ animation: true });
    });
  }

  // Toggle Physics
  const btnPhys = document.getElementById('btnTogglePhysics');
  if (btnPhys) {
    btnPhys.addEventListener('click', () => {
      appState.physicsEnabled = !appState.physicsEnabled;
      appState.visNetwork.setOptions({ physics: { enabled: appState.physicsEnabled } });
      btnPhys.classList.toggle('btn-primary', appState.physicsEnabled);
    });
  }

  // Filter Select
  const filterSelect = document.getElementById('graphFilterSelect');
  if (filterSelect) {
    filterSelect.addEventListener('change', (e) => {
      const selectedGroup = e.target.value;
      if (selectedGroup === 'ALL') {
        appState.networkData.nodes.clear();
        appState.networkData.nodes.add(appState.allNodes);
      } else {
        const filtered = appState.allNodes.filter(n => n.group === selectedGroup);
        appState.networkData.nodes.clear();
        appState.networkData.nodes.add(filtered);
      }
    });
  }

  // Search
  const searchInput = document.getElementById('graphSearchInput');
  const doSearch = () => {
    if (!searchInput) return;
    const query = searchInput.value.toLowerCase().trim();
    if (!query) return;
    const found = appState.allNodes.find(n => n.label.toLowerCase().includes(query));
    if (found && appState.visNetwork) {
      appState.visNetwork.focus(found.id, { scale: 1.4, animation: true });
      appState.visNetwork.selectNodes([found.id]);
      fetchAndShowNodeDetails(found.id);
    } else {
      alert(`Không tìm thấy thực thể phù hợp với "${query}"`);
    }
  };

  const btnSearch = document.getElementById('btnGraphSearch');
  if (btnSearch) btnSearch.addEventListener('click', doSearch);
  if (searchInput) searchInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') doSearch(); });

  // Sync Neo4j Button
  const btnSync = document.getElementById('btnSyncNeo4j');
  if (btnSync) {
    btnSync.addEventListener('click', async () => {
      btnSync.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Syncing...';
      try {
        const res = await fetch('/api/neo4j/sync', { method: 'POST' });
        const data = await res.json();
        alert(data.message || 'Đồng bộ hoàn tất!');
        if (typeof checkNeo4jStatus === 'function') checkNeo4jStatus();
      } catch (e) {
        alert('Lỗi sync Neo4j: ' + e.message);
      } finally {
        btnSync.innerHTML = '<i class="fa-solid fa-arrows-rotate"></i> Sync Neo4j';
      }
    });
  }
}

async function fetchAndShowNodeDetails(nodeId) {
  const body = document.getElementById('inspectorBody');
  const sub = document.getElementById('inspectorSub');
  if (!body) return;

  try {
    const res = await fetch(`/api/graph/node/${nodeId}`);
    const data = await res.json();
    const node = data.node;

    if (sub) sub.innerText = `ID: ${node.id} | Nhóm: ${node.type}`;

    let html = `
      <div class="node-detail-card">
        <span class="node-type-badge" style="background:${node.type==='Medicine'?'#d1fae5':(node.type==='Disease'?'#e0f2fe':'#fef3c7')}; color:${node.type==='Medicine'?'#059669':(node.type==='Disease'?'#0284c7':'#d97706')}">${node.type}</span>
        <h3 class="node-label-title">${node.label}</h3>
        <p class="node-summary">${node.summary || 'Không có mô tả chi tiết.'}</p>
    `;

    if (node.active_ingredient) {
      html += `
        <div class="node-info-section">
          <div class="node-info-label"><i class="fa-solid fa-flask"></i> Hoạt chất chính:</div>
          <div class="node-info-val">${node.active_ingredient}</div>
        </div>
      `;
    }

    if (node.dosage) {
      html += `
        <div class="node-info-section">
          <div class="node-info-label"><i class="fa-solid fa-pills"></i> Liều lượng tham khảo:</div>
          <div class="node-info-val">${node.dosage}</div>
        </div>
      `;
    }

    if (node.price_ref) {
      html += `
        <div class="node-info-section">
          <div class="node-info-label"><i class="fa-solid fa-tag"></i> Giá tại Nhà thuốc Long Châu:</div>
          <div class="node-info-val text-primary" style="font-weight:700;">${node.price_ref}</div>
        </div>
      `;
    }

    if (data.outgoing && data.outgoing.length > 0) {
      html += `
        <div class="node-info-section" style="margin-top:1rem;">
          <div class="node-info-label"><i class="fa-solid fa-arrow-right-from-bracket"></i> Quan hệ liên kết (${data.outgoing.length}):</div>
          <ul class="rel-list">
      `;
      data.outgoing.forEach(rel => {
        html += `
          <li class="rel-item">
            <span class="rel-tag">${rel.relation}</span>
            <span>${rel.target_label}</span>
          </li>
        `;
      });
      html += `</ul></div>`;
    }

    if (node.longchau_url) {
      html += `
        <a href="${node.longchau_url}" target="_blank" class="longchau_link-btn longchau-link-btn">
          <i class="fa-solid fa-arrow-up-right-from-square"></i> Xem trên Nhà thuốc Long Châu
        </a>
      `;
    }

    html += `</div>`;
    body.innerHTML = html;
  } catch (err) {
    body.innerHTML = `<p class="text-danger">Không thể tải thông tin node: ${err.message}</p>`;
  }
}
