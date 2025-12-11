// =========================
//  FORMATAÇÕES
// =========================
function formatarMoeda(v) {
  if (isNaN(v)) v = 0;
  return v.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });
}

// =========================
//  LÓGICA DO WEBSOCKET
// =========================
document.addEventListener("DOMContentLoaded", () => {
  const grid = document.getElementById("metas-grid");
  const resumoTotal = document.getElementById("resumo-total");
  const resumoMensal = document.getElementById("resumo-mensal");
  const resumoProj = document.getElementById("resumo-total-proj");

  const wsDot = document.getElementById("ws-dot");
  const wsText = document.getElementById("ws-text");

  // -----------------------
  // Status do WebSocket
  // -----------------------
  function setStatus(online) {
    if (!wsDot || !wsText) return;

    if (online) {
      wsDot.classList.add("online");
      wsText.textContent = "Conectado em tempo real";
    } else {
      wsDot.classList.remove("online");
      wsText.textContent = "Offline";
    }
  }

  // -----------------------
  // Renderizar cards
  // -----------------------
  function renderCards(metas) {
    if (!grid) return;

    grid.innerHTML = "";

    metas.forEach((meta) => {
      const div = document.createElement("div");
      div.className = "card glass";
      div.setAttribute("data-id", meta.id);

      const categoria =
        meta.categoria === "curto"
          ? "CURTO PRAZO"
          : meta.categoria === "medio"
          ? "MÉDIO PRAZO"
          : "LONGO PRAZO";

      div.innerHTML = `
        <span class="tag ${meta.categoria}">${categoria}</span>

        <div class="card-title">${meta.nome}</div>

        <div class="info">🪙 Valor mensal: <b>${formatarMoeda(meta.valor_mensal)}</b></div>
        <div class="info">📆 Duração: <b>${meta.qt_meses} meses</b></div>
        <div class="info">📈 Juros anual: <b>${meta.taxa_juros.toFixed(2)}%</b></div>

        <div class="acoes">
          <a href="/metas/${meta.id}/editar" class="btn-editar">Editar</a>

          <form method="POST" action="/metas/${meta.id}/excluir" style="display:inline;">
            <button class="btn-excluir">Excluir</button>
          </form>
        </div>
      `;

      // animação suave de entrada
      div.style.opacity = 0;
      div.style.transition = "opacity 0.3s";
      grid.appendChild(div);
      requestAnimationFrame(() => (div.style.opacity = 1));
    });
  }

  // -----------------------
  // Atualizar resumo
  // -----------------------
  function atualizarResumo(metas) {
    if (!Array.isArray(metas)) metas = [];

    const total = metas.length;
    const somaMensal = metas.reduce(
      (acc, m) => acc + Number(m.valor_mensal || 0),
      0
    );

    const somaProjetado = metas.reduce(
      (acc, m) => acc + Number(m.valor_mensal || 0) * Number(m.qt_meses || 0),
      0
    );

    if (resumoTotal) resumoTotal.textContent = total;
    if (resumoMensal) resumoMensal.textContent = somaMensal.toLocaleString("pt-BR", { minimumFractionDigits: 2 });
    if (resumoProj) resumoProj.textContent = somaProjetado.toLocaleString("pt-BR", { minimumFractionDigits: 2 });
  }

  // -----------------------
  // Conectar WebSocket
  // -----------------------
  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
  const wsUrl = `${protocol}://${window.location.host}/ws/metas`;
  const socket = new WebSocket(wsUrl);

  socket.onopen = () => setStatus(true);
  socket.onerror = () => setStatus(false);
  socket.onclose = () => setStatus(false);

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);

      if (data.type === "metas_update") {
        const metas = data.metas || [];

        renderCards(metas);
        atualizarResumo(metas);
      }
    } catch (err) {
      console.error("Erro ao receber dados do WebSocket:", err);
    }
  };
});
