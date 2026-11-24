let categoriasCache = [];
let chartInstance = null;
let historicoSimulacoes = JSON.parse(localStorage.getItem('historico_tributos')) || [];

const formatarMoeda = (valor) => {
  return Number(valor).toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  });
};

// Carrega categorias do backend FastAPI
async function carregarCategorias() {
  const select = document.getElementById('categoria');
  const totalText = document.getElementById('total-categorias');

  try {
    const response = await fetch('/api/categorias');
    if (!response.ok) throw new Error('Falha ao buscar categorias');

    categoriasCache = await response.json();
    select.innerHTML = '<option value="">Selecione uma categoria...</option>';

    categoriasCache.forEach(cat => {
      const option = document.createElement('option');
      option.value = cat.id;
      option.textContent = cat.nome;
      select.appendChild(option);
    });

    totalText.textContent = `Total de categorias disponíveis: ${categoriasCache.length}`;

    // Seleciona a primeira categoria automaticamente para facilitar o teste
    if (categoriasCache.length > 0) {
      select.value = categoriasCache[0].id;
      atualizarDetalhesCategoria(categoriasCache[0].id);
    }
  } catch (error) {
    console.error(error);
    select.innerHTML = '<option value="">Erro ao carregar categorias</option>';
  }
}

function atualizarDetalhesCategoria(categoriaId) {
  const box = document.getElementById('categoria-info');
  const cat = categoriasCache.find(c => String(c.id) === String(categoriaId));

  if (cat) {
    document.getElementById('cat-nome').textContent = cat.nome;
    document.getElementById('cat-descricao').textContent = cat.descricao || 'Alíquotas conforme tabela oficial.';
    box.style.display = 'block';
  } else {
    box.style.display = 'none';
  }
}

// Renderiza o gráfico de rosca (Chart.js)
function atualizarGrafico(valorLiquido, detalhamento) {
  const ctx = document.getElementById('graficoComposicao').getContext('2d');

  if (chartInstance) {
    chartInstance.destroy();
  }

  const labels = ['Valor Líquido', ...detalhamento.map(d => d.tributo)];
  const dataValues = [valorLiquido, ...detalhamento.map(d => d.valor_embutido)];
  const cores = ['#3b82f6', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4'];

  chartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: dataValues,
        backgroundColor: cores.slice(0, labels.length),
        borderWidth: 2,
        borderColor: '#ffffff'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: {
            boxWidth: 12,
            font: { family: 'Inter', size: 12 }
          }
        },
        tooltip: {
          callbacks: {
            label: (context) => ` ${context.label}: ${formatarMoeda(context.raw)}`
          }
        }
      },
      cutout: '62%'
    }
  });
}

// Renderiza o histórico na tabela
function renderizarHistorico() {
  const tbody = document.getElementById('historico-body');
  if (historicoSimulacoes.length === 0) {
    tbody.innerHTML = '<tr><td colspan="3" class="empty-msg">Nenhuma simulação realizada ainda.</td></tr>';
    return;
  }

  tbody.innerHTML = historicoSimulacoes.map(item => `
    <tr>
      <td><strong>${item.categoria}</strong><br><small style="color:#64748b">${item.data}</small></td>
      <td>${formatarMoeda(item.preco)}</td>
      <td class="text-green"><strong>${formatarMoeda(item.impostos)}</strong> (${item.percentual})</td>
    </tr>
  `).join('');
}

// Envia o cálculo para o FastAPI
async function realizarCalculo(event) {
  event.preventDefault();

  const categoriaId = document.getElementById('categoria').value;
  const precoInput = document.getElementById('preco').value;

  if (!categoriaId || !precoInput) {
    alert('Por favor, selecione uma categoria e informe o preço.');
    return;
  }

  try {
    const response = await fetch('/api/calcular', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        categoria_id: categoriaId,
        preco_final: precoInput
      })
    });

    const dados = await response.json();

    if (!response.ok) {
      alert(dados.detail || 'Erro ao calcular tributos.');
      return;
    }

    // Atualiza Resumo
    document.getElementById('res-impostos-valor').textContent = formatarMoeda(dados.total_tributos_valor);
    document.getElementById('res-impostos-perc').textContent = `(${dados.total_tributos_percentual})`;
    document.getElementById('res-liquido-valor').textContent = formatarMoeda(dados.valor_liquido_estimado);

    // Atualiza Barra de Proporção
    const percNum = parseFloat(dados.total_tributos_percentual.replace('%', '')) || 0;
    const percLiquido = Math.max(0, 100 - percNum);
    document.getElementById('bar-impostos').style.width = `${Math.min(100, percNum)}%`;
    document.getElementById('bar-liquido').style.width = `${percLiquido}%`;

    // Atualiza Detalhamento de Tributos
    const listaDiv = document.getElementById('detalhamento-lista');
    listaDiv.innerHTML = dados.detalhamento_por_tributo.map(item => {
      const p = parseFloat(item.percentual.replace('%', '')) || 0;
      const larguraBarra = Math.min(100, (p / 35) * 100); // Escala visual proporcional
      return `
        <div class="tax-item">
          <div>
            <div class="tax-name">${item.tributo}</div>
            <div class="tax-perc-sub">${item.percentual}</div>
          </div>
          <div class="progress-track">
            <div class="progress-fill" style="width: ${larguraBarra}%"></div>
          </div>
          <div class="tax-amount">${formatarMoeda(item.valor_embutido)}</div>
        </div>
      `;
    }).join('');

    // Atualiza Gráfico
    atualizarGrafico(dados.valor_liquido_estimado, dados.detalhamento_por_tributo);

    // Salva no Histórico
    const agora = new Date();
    const dataFormatada = agora.toLocaleDateString('pt-BR') + ' ' + agora.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
    
    historicoSimulacoes.unshift({
      categoria: dados.categoria,
      preco: dados.preco_final_informado,
      impostos: dados.total_tributos_valor,
      percentual: dados.total_tributos_percentual,
      data: dataFormatada
    });

    historicoSimulacoes = historicoSimulacoes.slice(0, 5); // Mantém os últimos 5
    localStorage.setItem('historico_tributos', JSON.stringify(historicoSimulacoes));
    renderizarHistorico();

  } catch (error) {
    console.error('Erro na requisição:', error);
    alert('Não foi possível conectar ao servidor FastAPI.');
  }
}

// Eventos
document.addEventListener('DOMContentLoaded', () => {
  carregarCategorias();
  renderizarHistorico();

  document.getElementById('categoria').addEventListener('change', (e) => {
    atualizarDetalhesCategoria(e.target.value);
  });

  document.getElementById('simulador-form').addEventListener('submit', realizarCalculo);

  document.getElementById('btn-limpar-historico').addEventListener('click', () => {
    historicoSimulacoes = [];
    localStorage.removeItem('historico_tributos');
    renderizarHistorico();
  });
});