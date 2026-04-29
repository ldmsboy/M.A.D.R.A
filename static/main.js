let network = null;
let allNodes = null;
let allEdges = null;
let nodeIds = [];

async function loadData() {
  const resultDiv = document.getElementById('result');
  try {
    const res = await fetch('/data');
    if (!res.ok) throw new Error('No se pudo cargar data');
    var data = await res.json();
  } catch (err) {
    resultDiv.innerText = 'Error cargando datos: ' + err.message;
    console.error(err);
    return;
  }
  // Normalize nodes
  const nodes = (data.nodes || []).map(n => ({ id: n.id, label: n.label }));
  // Normalize edges which may be objects {from,to,weight} or arrays [from,to,weight]
  const edges = (data.edges || []).map(e => {
    if (Array.isArray(e)) {
      return { from: e[0], to: e[1], label: String(e[2]), weight: e[2], width: 2 };
    }
    // assume object
    return { from: e.from, to: e.to, label: String(e.weight), weight: e.weight, width: 2 };
  });

  allNodes = new vis.DataSet(nodes);
  allEdges = new vis.DataSet(edges);

  // populate node-list and edge-list UI
  const nodeList = document.getElementById('node-list');
  const edgeList = document.getElementById('edge-list');
  nodeList.innerHTML = '';
  edgeList.innerHTML = '';
  for (const n of nodes) {
    const li = document.createElement('li');
    li.textContent = `${n.id} — ${n.label}`;
    // add quick buttons
    const setS = document.createElement('button'); setS.textContent = 'Start'; setS.className = 'tiny';
    const setE = document.createElement('button'); setE.textContent = 'End'; setE.className = 'tiny';
    setS.addEventListener('click', () => { document.getElementById('start').value = n.id; });
    setE.addEventListener('click', () => { document.getElementById('end').value = n.id; });
    li.appendChild(document.createTextNode(' '));
    li.appendChild(setS); li.appendChild(setE);
    nodeList.appendChild(li);
  }
  for (const ed of edges) {
    const li = document.createElement('li');
    li.textContent = `${ed.from} → ${ed.to} (peso: ${ed.weight})`;
    edgeList.appendChild(li);
  }

  // populate datalist for autocompletion
  nodeIds = nodes.map(n => n.id);
  const datalist = document.getElementById('nodes-list');
  datalist.innerHTML = '';
  for (const id of nodeIds) {
    const opt = document.createElement('option');
    opt.value = id;
    datalist.appendChild(opt);
  }

  const container = document.getElementById('network');
  const visData = { nodes: allNodes, edges: allEdges };
  const options = {
    edges: { arrows: { to: false }, smooth: { type: 'dynamic' }, color: { inherit: false } },
    nodes: { shape: 'dot', size: 16, font: { color: '#e6eef8' } },
    physics: { stabilization: true },
    interaction: { hover: true, tooltipDelay: 100 }
  };
  if (typeof vis === 'undefined' || !vis.Network) {
    resultDiv.innerText = 'La librería de visualización no se cargó. Revisa la conexión a internet.';
    console.error('vis not available');
  } else {
    network = new vis.Network(container, visData, options);
  }

  // enable analyze button now that data is loaded
  document.getElementById('analyze').disabled = false;
}

async function analyze() {
  const start = document.getElementById('start').value.trim();
  const end = document.getElementById('end').value.trim();
  const resultDiv = document.getElementById('result');
  if (!start || !end) {
    resultDiv.innerText = 'Escribe Origen y Destino (usa la lista desplegable si necesitas).';
    return;
  }
  // quick validation that nodes exist
  if (nodeIds.length && (!nodeIds.includes(start) || !nodeIds.includes(end))) {
    resultDiv.innerText = 'Uno o ambos nodos no existen. Revisa los ids en la lista.';
    return;
  }

  resultDiv.innerText = 'Analizando...';
  // disable button and show spinner
  const btn = document.getElementById('analyze');
  btn.disabled = true;
  btn.textContent = 'Analizando...';
  const spinner = document.createElement('span'); spinner.className = 'spinner';
  btn.appendChild(spinner);

  const res = await fetch('/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ start, end })
  });

  // abort after timeout if no response
  // (fetch doesn't support timeout natively; we rely on server to respond quickly)

  if (!res.ok) {
    const err = await res.json();
    resultDiv.innerText = 'Error: ' + (err.error || res.statusText);
    btn.disabled = false; btn.textContent = 'Analizar Ruta';
    return;
  }

  const data = await res.json();
  console.log('analyze response:', data);
  // show basic results immediately so UI isn't blocked by visualization steps
  if (data.path && data.path.length) {
    resultDiv.innerText = `Ruta: ${data.path.join(' -> ')} | Costo total: ${data.cost}`;
  }
  if (!data.path || data.path.length === 0) {
    resultDiv.innerText = 'No se encontró ruta.';
    return;
  }
  // Do visualization updates in a try/catch so failures don't hide the cost
  try {
    // Reset styles
    if (allNodes && allEdges) {
      allNodes.forEach(n => allNodes.update({ id: n.id, color: undefined }));
      allEdges.forEach(e => allEdges.update({ id: e.id, color: undefined, width: 2 }));

      // Highlight path nodes
      for (const nodeId of data.path) {
        // guard: only update if node exists
        if (nodeIds.includes(nodeId)) {
          allNodes.update({ id: nodeId, color: { background: '#ffcc00' } });
        }
      }

      // Highlight edges in path
      for (let i = 0; i < data.path.length - 1; i++) {
        const from = data.path[i];
        const to = data.path[i + 1];
        const matches = allEdges.get({ filter: e => e.from === from && e.to === to });
        for (const m of matches) {
          allEdges.update({ id: m.id, color: { color: '#ff0000' }, width: 4 });
        }
      }

      // Mark critical edges differently
      if (data.critical_edges && data.critical_edges.length) {
        for (const item of data.critical_edges) {
          const [u, v, w] = item;
          const matches = allEdges.get({ filter: e => e.from === u && e.to === v });
          for (const m of matches) {
            allEdges.update({ id: m.id, color: { color: '#00ff00' }, width: 6 });
          }
        }
      }
    }
  } catch (visErr) {
    console.error('Visualización falló:', visErr);
  }
  // restore button state
  btn.disabled = false; btn.textContent = 'Analizar Ruta';
}

document.getElementById('analyze').addEventListener('click', analyze);
window.addEventListener('load', loadData);
